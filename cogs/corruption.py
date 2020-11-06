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

class TimeoutError(Exception):
    pass

def interrupt(a, b):
    raise TimeoutError()

class Corruption(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.use_yt = False
    
    @commands.command(description='Corrupt the bytes in the video.\ncorrupt_ratio = how much of video to corrupt (0.95 is good, that means the 95 percent chunk in the middle).\ncorrupt_chance = chance of corrupting a byte (0.2 is good, means 20 percent chance).\nbyte_skip = how far apart every corrupted byte is (200 is good, means every 200th byte, asssuming corrupt_chance=1)', pass_context=True)
    async def corrupt(self, ctx, corrupt_ratio: float=-1, corrupt_chance: float=-1, byte_skip: int=-1):
        corrupt_ratio = random.uniform(0.94, 0.97) if corrupt_ratio == -1 else max(0, min(1, corrupt_ratio))
        corrupt_chance = random.random() if corrupt_chance == -1 else max(0, min(1, corrupt_chance))
        byte_skip = random.randint(10, 2500) if byte_skip == -1 else max(10, byte_skip)

        input_vid, is_yt, result = await image_cache.download_last_video(ctx)
        if(not result):
            await ctx.send("Error downloading the video")
            return
        
        #out_filename = 'vids/out.mp4'

        #await ctx.send("I will get back to you...")
        async with ctx.typing():
            try:
                # convert to avi
                avipath = 'vids/corrupt.avi'
                (
                    ffmpeg
                    .input(input_vid)
                    .output(avipath)
                    .run(cmd='ffmpeg4-2-2/ffmpeg', overwrite_output=True)
                )
                
                # screw it all up
                corrupt_start = int(os.path.getsize(avipath) * (1-corrupt_ratio))
                corrupt_end = int(os.path.getsize(avipath) * corrupt_ratio)
                corrupt_pos = int(corrupt_start)
                ogFile = open(avipath, 'r+b')
                while(corrupt_pos < corrupt_end):
                    ogFile.seek(corrupt_pos)
                    
                    corrupt_subpos = 0
                    iter_counter = 10
                    while(random.random() < corrupt_chance and iter_counter > 0):
                        ogFile.write(bytes([random.randint(0, 255)]))
                        corrupt_subpos += random.randint(1, 10)
                        iter_counter -= 1
                        ogFile.seek(corrupt_pos + corrupt_subpos)
                    
                    corrupt_pos += byte_skip
                ogFile.close()
                
                # back to mp4
                (
                    ffmpeg
                    .input(avipath)
                    .output('vids/out.mp4', fs='7M')
                    .run(cmd='ffmpeg4-2-2/ffmpeg', overwrite_output=True)
                )
                await ctx.send(file=discord.File('vids/out.mp4'))
                print("ratio: " + str(corrupt_ratio) + " | chance: " + str(corrupt_chance) + " | byte_skip: " + str(byte_skip))

            except TimeoutError as e:
                await ctx.send('Command took to long to execute.\n```\n' + str(e) + '```')
            except Exception as e:
                await ctx.send('Error:\n```\n' + str(e) + '```')
                print(traceback.format_exc())
            if(is_yt):
                os.remove(input_vid)
    




    @commands.command(description='Corrupt the video by repeating a chunk', pass_context=True)
    async def rearrange(self, ctx, corrupt_ratio: float=-1):
        corrupt_ratio = random.uniform(0.95, 0.97) if corrupt_ratio == -1 else max(0, min(1, corrupt_ratio))

        input_vid, is_yt, result = await image_cache.download_last_video(ctx)
        if(not result):
            await ctx.send("Error downloading the video")
            return
        
        #await ctx.send("I will get back to you...")
        async with ctx.typing():
            try:
                # convert to avi
                avipath = 'vids/corrupt.avi'
                (
                    ffmpeg
                    .input(input_vid)
                    .output(avipath)
                    .run(cmd='ffmpeg4-2-2/ffmpeg', overwrite_output=True)
                )
                
                # rearrange all the bytes
                #corrupt_start = int(os.path.getsize(avipath) * (1-loop_pos))
                #corrupt_end = int(os.path.getsize(avipath) * loop_pos)
                fh = open(avipath, 'r+b')

                for i in range(random.randint(10, 50)):
                    insertion_start = int(os.path.getsize(avipath) * random.uniform(0.05, 0.95))
                    extraction_start = int(os.path.getsize(avipath) * random.uniform(0.05, 0.85))
                    extraction_length = random.randint(1000, min(int(os.path.getsize(avipath) * 0.1), 50000))

                    # Start of video
                    fh.seek(0)
                    start_segment = fh.read(insertion_start)

                    # Middle of video
                    fh.seek(extraction_start)
                    mid_segment = fh.read(extraction_length)

                    # End of video
                    fh.seek(insertion_start)
                    end_segment = fh.read()

                    # Put it all together
                    fh.seek(0)
                    fh.write(start_segment + mid_segment + end_segment)

                fh.close()
                
                # back to mp4
                (
                    ffmpeg
                    .input(avipath)
                    .output('vids/out.mp4', fs='7M')
                    .run(cmd='ffmpeg4-2-2/ffmpeg', overwrite_output=True)
                )
                await ctx.send(file=discord.File('vids/out.mp4'))
            except TimeoutError as e:
                await ctx.send('Command took to long to execute.\n```\n' + str(e) + '```')
            except Exception as e:
                await ctx.send('Error:\n```\n' + str(e) + '```')
                print(traceback.format_exc())
            if(is_yt):
                os.remove(input_vid)





    @commands.command(description='Make the video stutter a lot', pass_context=True)
    async def stutter(self, ctx, corrupt_ratio: float=-1):
        corrupt_ratio = random.uniform(0.95, 0.96) if corrupt_ratio == -1 else max(0, min(1, corrupt_ratio))

        input_vid, is_yt, result = await image_cache.download_last_video(ctx)
        if(not result):
            await ctx.send("Error downloading the video")
            return
        
        #await ctx.send("I will get back to you...")
        async with ctx.typing():
            try:
                # convert to avi
                avipath = 'vids/corrupt.avi'
                tempavipath = 'vids/corrupttemp.avi'
                (
                    ffmpeg
                    .input(input_vid)
                    .output(tempavipath)
                    .run(cmd='ffmpeg4-2-2/ffmpeg', overwrite_output=True)
                )
                
                # repeat a bunch of bytes
                fi = open(tempavipath, 'rb')
                fo = open(avipath, 'wb')

                corrupt_start = int(os.path.getsize(tempavipath) * (1-corrupt_ratio))
                corrupt_end = int(os.path.getsize(tempavipath) * corrupt_ratio)
                seek_pos = corrupt_start + random.randint(0, 8000)

                fo.seek(0)
                fo.write(fi.read(corrupt_start)) # write the file header
                fi.seek(seek_pos)
                
                while(seek_pos < corrupt_end):
                    
                    for i in range(random.randint(1, 80)):
                        fo.write(fi.read(random.randint(300,1500)))
                        fi.seek(seek_pos)
                    
                    normal_seg_len = random.randint(1000, 10000)
                    fo.write(fi.read(normal_seg_len))
                    seek_pos += normal_seg_len
                    fi.seek(seek_pos)
                fo.write(fi.read())

                fi.close()
                fo.close()
                
                # back to mp4
                (
                    ffmpeg
                    .input(avipath)
                    .output('vids/out.mp4', fs='7M')
                    .run(cmd='ffmpeg4-2-2/ffmpeg', overwrite_output=True)
                )
                await ctx.send(file=discord.File('vids/out.mp4'))
            except TimeoutError as e:
                await ctx.send('Command took to long to execute.\n```\n' + str(e) + '```')
            except Exception as e:
                await ctx.send('Error:\n```\n' + str(e) + '```')
                print(traceback.format_exc())
            if(is_yt):
                os.remove(input_vid)
    
    


    @commands.command(description='Add 1 to a bunch of random bytes', pass_context=True)
    async def corruptadd(self, ctx, corrupt_ratio: float=-1):
        corrupt_ratio = random.uniform(0.95, 0.97) if corrupt_ratio == -1 else max(0, min(1, corrupt_ratio))

        input_vid, is_yt, result = await image_cache.download_last_video(ctx)
        if(not result):
            await ctx.send("Error downloading the video")
            return
        
        #await ctx.send("I will get back to you...")
        async with ctx.typing():
            try:
                # convert to avi
                avipath = 'vids/corrupt.avi'
                (
                    ffmpeg
                    .input(input_vid)
                    .output(avipath)
                    .run(cmd='ffmpeg4-2-2/ffmpeg', overwrite_output=True)
                )
                
                # rearrange all the bytes
                #corrupt_start = int(os.path.getsize(avipath) * (1-loop_pos))
                #corrupt_end = int(os.path.getsize(avipath) * loop_pos)
                filesize = os.path.getsize(avipath)
                fh = open(avipath, 'r+b')

                for i in range(random.randint(10, 10000)):
                    pos = int(filesize * random.uniform(0.05, 0.95))
                    fh.seek(pos)
                    for j in range(random.randint(2, 1000)):
                        curr = fh.read(1)
                        fh.seek(pos)
                        fh.write(bytes([min(255, int.from_bytes(curr, 'little') + 1)]))

                fh.close()
                
                # back to mp4
                (
                    ffmpeg
                    .input(avipath)
                    .output('vids/out.mp4', fs='7M')
                    .run(cmd='ffmpeg4-2-2/ffmpeg', overwrite_output=True)
                )
                await ctx.send(file=discord.File('vids/out.mp4'))
            except TimeoutError as e:
                await ctx.send('Command took to long to execute.\n```\n' + str(e) + '```')
            except Exception as e:
                await ctx.send('Error:\n```\n' + str(e) + '```')
                print(traceback.format_exc())
            if(is_yt):
                os.remove(input_vid)

    

    


        

        
    
    



        
        



def setup(bot):
    bot.add_cog(Corruption(bot))
