import discord
import asyncio
from discord.ext import commands
import subprocess
import signal
from subprocess import Popen
import youtube_dl
import random
import os
import shutil
import image_cache
import re
import os
import ffmpeg
import traceback
import video_creator

class Corruption(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.use_yt = False
    
    def get_corrupt_start_end(self, filesize):
        return (int(random.uniform(0.03, 0.05) * filesize), int(random.uniform(0.95, 0.97) * filesize))

    async def _tomato(self, filename, args, suffix):
        p = Popen(f'python3 ./tomato/tomato.py -i {filename} {args}', bufsize=2048, shell=True, stdin=subprocess.PIPE)
        p.wait()
        os.remove(filename)
        os.rename(f'{filename.split(".avi")[0]}{suffix}.avi', filename)
    

    async def _mosh(self, ctx, filename, kwargs):
        await self._tomato(filename, '', '-void')
    @commands.command(description='Datamoshing. Provide a number to change quality (lowest/default = 1.5). Provide another number to change output resolution width (default = 640)', pass_context=True)
    async def mosh(self, ctx):
        await video_creator.apply_corruption_and_send(ctx, self._mosh, {})
    

    async def _smear(self, ctx, filename, kwargs):
        await self._tomato(filename, '-m pulse -c 5', '-pulse-c5')
    @commands.command(description='Corrupt the video by smearing moving things around.')
    async def smear(self, ctx):
        await video_creator.apply_corruption_and_send(ctx, self._smear, {})


    async def _corrupt(self, ctx, filename, kwargs):
        fs = open(filename, 'r+b')
        filesize = os.path.getsize(filename)
        corrupt_start, corrupt_end = self.get_corrupt_start_end(filesize)
        intensity = kwargs['intensity']
        corrupt_pos = corrupt_start

        while(corrupt_pos < corrupt_end):
            fs.seek(corrupt_pos)
            # Corrupt a chunk of nearby bytes
            iters_intensity = int(intensity*200)
            max_iters = random.randint(int(iters_intensity * 0.1), iters_intensity)
            for i in range(max_iters):
                fs.write(bytes([random.randint(0, 255)]))
                corrupt_pos += random.randint(1, 10)
                fs.seek(corrupt_pos)
            # Find a new chunk to corrupt
            seek_intensity = int((1-intensity**2)*10000 + intensity * 4000)
            corrupt_pos += random.randint(int(seek_intensity*0.05), seek_intensity)
        fs.close()
    @commands.command(description='Corrupt the bytes in the video.)', pass_context=True)
    async def corrupt(self, ctx, intensity: float = 0.5):
        intensity = max(0, min(1, intensity))
        await video_creator.apply_corruption_and_send(ctx, self._corrupt, {'intensity':intensity})




    async def _rearrange(self, ctx, filename, kwargs):
        fs = open(filename, 'r+b')
        filesize = os.path.getsize(filename)
        corrupt_start, corrupt_end = self.get_corrupt_start_end(filesize)
        intensity = kwargs['intensity']
        max_chunk_length = int(filesize * 0.3 * intensity)

        for i in range(int(intensity*50)):
            chunk_length = random.randint(1000, max_chunk_length)
            chunk1_start = random.randint(corrupt_start, corrupt_end - chunk_length)
            chunk2_start = None
            # Keep looping if chunk2 is in a spot that would collide with chunk1
            max_iters = 25 # in case there's an infinite loop...
            while(chunk2_start is None or (chunk2_start > chunk1_start - chunk_length and chunk2_start < chunk1_start + chunk_length)):
                if(max_iters <= 0):
                    break
                chunk2_start = random.randint(corrupt_start, corrupt_end - chunk_length)
                max_iters -= 1
            if(max_iters <= 0):
                continue

            # Chunk 1
            fs.seek(chunk1_start)
            chunk1 = fs.read(chunk_length)
            # Chunk 2
            fs.seek(chunk2_start)
            chunk2 = fs.read(chunk_length)

            # Get the areas in between the chunks
            first_chunk_start = min(chunk1_start, chunk2_start)
            first_chunk_end = first_chunk_start + chunk_length
            second_chunk_start = max(chunk1_start, chunk2_start)
            second_chunk_end = second_chunk_start + chunk_length
            fs.seek(0)
            segment1 = fs.read(first_chunk_start)
            fs.seek(first_chunk_end)
            segment2 = fs.read(second_chunk_start - first_chunk_end)
            fs.seek(second_chunk_end)
            segment3 = fs.read()

            # Combine it all and write to file
            if(chunk1_start < chunk2_start):
                temp = chunk1
                chunk1 = chunk2
                chunk2 = temp
            fs.seek(0)
            fs.write(segment1 + chunk1 + segment2 + chunk2 + segment3)

        fs.close()
    @commands.command(description='Corrupt the video by swapping random chunks of its file.', pass_context=True)
    async def rearrange(self, ctx, intensity : float = 0.5):
        intensity = max(0, min(1, intensity))
        await video_creator.apply_corruption_and_send(ctx, self._rearrange, {'intensity':intensity})
    



    async def _stutter(self, ctx, filename, kwargs):
        temp_filename = f'{filename}2'
        fs = open(filename, 'r+b')
        filesize = os.path.getsize(filename)
        corrupt_start, corrupt_end = self.get_corrupt_start_end(filesize)
        corrupt_pos = corrupt_start + random.randint(0, 8000)

        # Duplicate the file
        fs_copy = open(temp_filename, 'wb')
        fs.seek(0)
        fs_copy.write(fs.read())
        fs_copy.close()
        fs_copy = open(temp_filename, 'rb')

        # Write the file header
        fs.seek(0)
        fs.write(fs_copy.read(corrupt_pos))
        fs_copy.seek(corrupt_pos)

        # Repeat bytes at the beginning of every chunk
        while(corrupt_pos < corrupt_end):
            # Repeating bytes
            for i in range(random.randint(1, 100)):
                fs.write(fs_copy.read(random.randint(300, 1500)))
                fs_copy.seek(corrupt_pos)
            # Seeking next chunk
            byte_skip = random.randint(1000, 10000)
            fs.write(fs_copy.read(byte_skip))
            corrupt_pos += byte_skip
            fs_copy.seek(byte_skip)
        fs.write(fs_copy.read())

        fs_copy.close()
        fs.close()

        os.remove(temp_filename)
    @commands.command(description='Make the video stutter a lot')
    async def stutter(self, ctx):
        await video_creator.apply_corruption_and_send(ctx, self._stutter, {})


        
        



def setup(bot):
    bot.add_cog(Corruption(bot))
