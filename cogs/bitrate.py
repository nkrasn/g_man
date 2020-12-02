import discord
import asyncio
from discord.ext import commands
import subprocess
from subprocess import Popen
import youtube_dl
import media_cache
import json
import re
import os
import ffmpeg

class Bitrate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(pass_context=True)
    async def vb(self, ctx, bitrate : int):
        await self.execute_command(ctx, bitrate, None)
        
    @commands.command(pass_context=True)
    async def ab(self, ctx, bitrate : int):
        await self.execute_command(ctx, None, bitrate)
    
    @commands.command(pass_context=True)
    async def b(self, ctx, vbitrate : int, abitrate : int):
        await self.execute_command(ctx, vbitrate, abitrate)





    # Run bitrate commands
    async def execute_command(self, ctx, vbitrate, abitrate):
        if(vbitrate is None and abitrate is None):
            return

        # Determine if the source should be an attachment or youtube video
        input_vid = media_cache.get_from_cache(str(ctx.message.channel.id))[-1]
        is_yt = False
        if(input_vid is None): # no video found in the channel
            await ctx.send("Didn't find any videos to modify...")
            return
        elif(re.match(media_cache.yt_regex, input_vid)): # yt video
            is_yt = True
            result, input_vid = await media_cache.yt(ctx, input_vid, '0')
            if(not result):
                await ctx.send("Quitting :(")
                return

        bitrates_dict = {}
        if(vbitrate is not None):
            bitrates_dict['b:v'] = min(vbitrate, 10000000)
        if(abitrate is not None):
            bitrates_dict['b:a'] = min(abitrate, 10000000)
        #await ctx.send("I will get back to you...")
        async with ctx.typing():
            try:
                print(input_vid)
                stream = ffmpeg.input(input_vid)
                stream = ffmpeg.output(stream, 'vids/out.mp4', fs='7M', **bitrates_dict)
                ffmpeg.run(stream, cmd='ffmpeg4-2-2/ffmpeg', overwrite_output=True)
                '''
                (
                    ffmpeg
                    .input('vids/out.mp4')
                    .output('vids/out.mp4', bitrates_dict)
                    .run(cmd='ffmpeg4-2-2/ffmpeg')
                )'''
                await ctx.send(file=discord.File('vids/out.mp4'))
            except Exception as e:
                await ctx.send('Error:\n```\n' + str(e) + '```')
            if(is_yt):
                os.remove(input_vid)

def setup(bot):
    bot.add_cog(Bitrate(bot))
