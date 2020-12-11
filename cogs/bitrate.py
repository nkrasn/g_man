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
import video_creator

class Bitrate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def clamp_bitrate(self, br):
        if(br is None):
            return None
        br = br.lower()
        if(re.match(r'[0-9]+(\.[0-9]+)?k?$', br) is None):
            return None

        br_num = float(br.replace('k',''))
        if('k' in br):
            br_num *= 1000
        br_num = int(br_num)

        return max(1000, min(br_num, 200000))

    async def _b(self, ctx, vstream, astream, kwargs):
        # All that's needed is to pass the bitrate output params stored in kwargs
        return vstream, astream, kwargs
    @commands.command()
    async def b(self, ctx, vid_bitrate, audio_bitrate):
        vid_bitrate = self.clamp_bitrate(vid_bitrate)
        audio_bitrate = self.clamp_bitrate(audio_bitrate)
        
        if(vid_bitrate is None and audio_bitrate is None):
            await ctx.send('Invalid bitrate. Try a value such as 4.3k (or 4300) or 25k (or 25000)')
            return
        bitrate_kwargs = {}
        if(vid_bitrate is not None):
            bitrate_kwargs['b:v'] = vid_bitrate
        if(audio_bitrate is not None):
            bitrate_kwargs['b:a'] = audio_bitrate

        await video_creator.apply_filters_and_send(ctx, self._b, bitrate_kwargs)

    @commands.command()
    async def vb(self, ctx, vid_bitrate):
        await self.b(ctx, vid_bitrate, None)

    @commands.command()
    async def ab(self, ctx, audio_bitrate):
        await self.b(ctx, None, audio_bitrate)







def setup(bot):
    bot.add_cog(Bitrate(bot))
