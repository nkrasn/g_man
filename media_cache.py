import database as db
import discord
import ffmpeg
import os
import re
import requests
import subprocess
from yt_dlp import YoutubeDL

MAX_MEM_PER_CHANNEL = 8
yt_regex = (r'(https?://)?(www\.)?(m\.youtube|youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
discord_cdn_regex = (r'https://(cdn|media)\.discordapp\.(com|net)/attachments/.+\.(mp4|MP4|webm|WEBM|mov|MOV|mkv|MKV|gif|GIF)')
twitter_regex = (r'(https?://)?(www\.)?(mobile\.)?(fx)?twitter\.com/.+/status/[0-9]+(\?.+)?')
tumblr_regex = (r'(https?://)?(www\.)?((va\.media\.tumblr\.com/tumblr_.+\.(mp4|MP4|webm|WEBM|mov|MOV|mkv|MKV|gif|GIF))|(.+\.tumblr\.com/(post|video/.+)/[0-9]+(/[0-9]+/)?))')
hosted_file_regex = (r'(https?://)?(www\.)?.+\.(com|org|net|us|co|edu|ca|cn|fr|ch|au|in|de|jp|nl|uk|mx|no|ru|br|se|es)/.+\.(png|PNG|jpg|JPG|jpeg|JPEG|mp4|MP4|webm|WEBM|mov|MOV|mkv|MKV|gif|GIF)')

audio_filetypes = ['mp3', 'ogg', 'wav']
video_filetypes = ['mp4', 'mov', 'avi', 'webm', 'flv', 'wmv', 'mkv']
image_filetypes = ['gif', 'png', 'jpg', 'jpeg']
approved_filetypes = audio_filetypes + video_filetypes + image_filetypes

def add_to_cache(message, img_url):
    msg_id = str(message.id)
    channel = str(message.channel.id)
    
    inserted_vid = db.vids.insert_one({'channel':channel, 'message_id':msg_id, 'url':img_url})
    
    channel_vids = db.vids.find({'channel':channel}).sort('_id', 1)
    channel_vids_count = channel_vids.count()
    # Removing old videos
    if(channel_vids_count > MAX_MEM_PER_CHANNEL):
        to_delete = list(channel_vids.limit(channel_vids_count - MAX_MEM_PER_CHANNEL))
        to_delete = list(map(lambda x : x['_id'], to_delete))
        db.vids.delete_many({'_id' : {'$in': to_delete}})


def get_from_cache(channel):
    vids = list(db.vids.find({'channel':channel}).sort('_id', 1))
    if(len(vids) == 0):
        return None
    vids = list(map(lambda x : x['url'], vids))
    return vids



# Download youtube video
async def yt(ctx, url, suffix):
    #await ctx.send("Downloading the video...")
    async with ctx.typing():
        ydl_opts = {
            'noplaylist': True,
            'outtmpl': 'vids/target' + str(suffix) + '.mp4'
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            resulting_file = None
            for f in os.listdir('vids'):
                if(f.startswith('target' + str(suffix) + '.')):
                    resulting_file = 'vids/' + f
                    break
            return True, resulting_file
    return False, None


async def download_last_video(ctx):
    return await download_nth_video(ctx, 0)

async def download_nth_video(ctx, n):
    n = -(n + 1) # most recent videos are at the end
    input_vid = get_from_cache(str(ctx.message.channel.id))
    if(input_vid is None): # no video found in the channel
        await ctx.send("Couldn't find a video to send, try sending a video before using a command.")
        return None, None, False
    input_vid = input_vid[n]
    #await ctx.send(f'working on `{input_vid}`')
    is_yt = True # TODO: remove this flag, all videos will be downloaded now instead of passing URL to ffmpeg
    if(re.match(yt_regex, input_vid) or re.match(twitter_regex, input_vid) or re.match(tumblr_regex, input_vid)): # yt video
        is_yt = True
        result, input_vid = await yt(ctx, input_vid, ctx.message.id)#n)
        if(not result):
            #await ctx.send("Could not download the video!")
            return None, None, False
    else: # discord video
        file_extension = input_vid.split('.')[-1]
        input_vid_filepath = f'vids/target{ctx.message.id}{n}.{file_extension}'
        with open(input_vid_filepath, 'wb') as f:
            r = requests.get(input_vid)
            f.write(r.content)
        input_vid = input_vid_filepath


    return input_vid, is_yt, True
