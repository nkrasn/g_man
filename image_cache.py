import json
import re
import youtube_dl
import os
import discord
import subprocess
import ffmpeg

MAX_MEM_PER_CHANNEL = 3
yt_regex = (r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
discord_cdn_regex = (r'https://cdn\.discordapp\.com/attachments/.+\.(mp4|webm|mov)')
twitter_regex = (r'(https?://)?(www\.)?(mobile\.)?twitter\.com/.+/status/[0-9]+(\?.+)?')

audio_filetypes = ['mp3', 'ogg', 'wav']
approved_filetypes = ['mp4', 'mov', 'avi', 'webm', 'flv', 'wmv'] + audio_filetypes

def add_to_cache(channel, img_url):
    channel = str(channel)
    data = None
    with open('cache.json', 'r') as json_file:
        data = json.load(json_file)
        # append to cache
        if(channel in data.keys()):
            data[channel].append(img_url)
            if(len(data[channel]) > MAX_MEM_PER_CHANNEL):
                data[channel].pop(0)
        # initialize entry in cache
        else:
            data[channel] = [img_url]
    with open('cache.json', 'w') as json_file:
        if(data is not None):
            json.dump(data, json_file)


def get_from_cache(channel):
    data = None
    with open('cache.json') as json_file:
        data = json.load(json_file)
        if(channel in data):
            return data[channel]
    return None



# Download youtube video
async def yt(ctx, url, suffix):
    #await ctx.send("Downloading the video...")
    async with ctx.typing():
        ydl_opts = {
            'noplaylist': True,
            'outtmpl': 'vids/target' + str(suffix) + '.mp4'
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            filesize = None
            if(re.match(yt_regex, url)):
                filesize = info['formats'][0]['filesize']
                print("filesize is " + str(filesize))
            if(filesize is not None and filesize > 25600000):
                if(filesize is None):
                    await ctx.send("video size is none??? wtf")
                else:
                    await ctx.send("Video is {}mb, which exceeds the maximum size (256mb)".format(filesize / 100000.0))
                return False
            else:
                #if(filesize is None and not re.match(twitter_regex, url)):
                    #await ctx.send("this video has a filesize of None for some reason altho im still gonna try and download")
                ydl.download([url])
                # get the file that was saved
                resulting_file = None
                for f in os.listdir('vids'):
                    if(f.startswith('target' + str(suffix) + '.')):
                        resulting_file = 'vids/' + f
                        break
                return True, resulting_file
    return False, None


async def download_last_video(ctx):
    # Determine if the source should be an attachment or youtube video
    input_vid = get_from_cache(str(ctx.message.channel.id))[-1]
    #await ctx.send(f'working on `{input_vid}`')
    is_yt = False
    if(input_vid is None): # no video found in the channel
        await ctx.send("Couldn't find a video to send, try sending a video before using a command.")
        return None, None, False
    elif(re.match(yt_regex, input_vid) or re.match(twitter_regex, input_vid)): # yt video
        is_yt = True
        result, input_vid = await yt(ctx, input_vid, 0)
        if(not result):
            await ctx.send("Could not download the video!")
            return None, None, False
    return input_vid, is_yt, True

async def download_nth_video(ctx, n):
    n = -(n + 1) # most recent videos are at the end
    input_vid = get_from_cache(str(ctx.message.channel.id))[n]
    #await ctx.send(f'working on `{input_vid}`')
    is_yt = False
    if(input_vid is None): # no video found in the channel
        await ctx.send("Couldn't find a video to send, try sending a video before using a command.")
        return None, None, False
    elif(re.match(yt_regex, input_vid) or re.match(twitter_regex, input_vid)): # yt video
        is_yt = True
        result, input_vid = await yt(ctx, input_vid, n)
        if(not result):
            await ctx.send("Could not download the video!")
            return None, None, False
    return input_vid, is_yt, True
