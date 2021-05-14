import discord
import asyncio
from discord.ext import commands
import subprocess
from subprocess import Popen
import youtube_dl
import random
import os
import media_cache
import re
import os
import ffmpeg
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
    

    async def _faketime(self, ctx, output_filename, fake_type):
        fs = open(output_filename, 'r+b')
        filesize = os.path.getsize(output_filename)
        
        try:
            if(fake_type == 'increasing'): # webm
                duration_data = fs.read(16*32).find(b'\x2a\xd7\xb1')
                fs.seek(duration_data)
                duration_data += fs.read(16*32).find(b'\x44\x89') + 4
                fs.seek(duration_data)
                fs.write(b'\x00')
            else: # mp4
                # find mvhd and modify the duration data from there
                #fs.seek(filesize-40000)
                fs.seek(0)
                duration_data_idx = fs.read().find(b'\x6d\x76\x68\x64') + 18
                #fs.seek(filesize-40000+duration_data_idx)
                fs.seek(duration_data_idx)

                if(fake_type == 'negative'):
                    fs.write(b'\x00\x01\xff\xff\xff\xf0')
                elif(fake_type == 'random'):
                    random_bytes = []
                    for i in range(6):
                        random_bytes.append(random.randint(0, 255))
                    fs.write(bytes(random_bytes))
                else: # default to 'long'
                    fs.write(b'\x00\x01\x7f\xff\xff\xff')
        except Exception as e:
            print(e)
            await ctx.send("Couldn't modify duration data :(\nSomething that might work: try running a random filter through the video (such as `!volume 1` or `!scale 480`) and try again.")
            fs.close()
            return False


        fs.close()
        return True
    @commands.command()
    async def faketime(self, ctx, fake_type : str = ''):
        # doesn't seem like i can use apply_corruption_and_send here... or apply_filters_and_send
        # so, will have to repeat code a bit

        # determine type of fake time...
        fake_types = ['long', 'negative', 'increasing']
        if(fake_type == ''):
            fake_type = random.choice(fake_types)
        fake_types.append('random')
        if(fake_type not in fake_types):
            fake_types_str = '`' + ', '.join(fake_types) + '`'
            await ctx.send(f"I'm not sure what you mean. Here are the types of fake time I understand:\n{fake_types_str}")
            return

        # download the video...
        await video_creator.set_progress_bar(ctx.message, 0)
        async with ctx.typing():
            input_vid, is_yt, result = await media_cache.download_last_video(ctx)
            if(not result):
                await ctx.send("Error downloading the video")
                return

            output_filename = f'./vids/{ctx.message.id}.'
            output_params = {}
            if(fake_type == 'increasing'):
                output_filename += 'webm'
                # because libvpx-vp9 is slow
                output_params['threads'] = 8
                output_params['cpu-used'] = 8
            else:
                output_filename += 'mp4'

            (
                ffmpeg
                .input(input_vid)
                .output(output_filename, fs='7M', **output_params)
                .run(cmd='ffmpeg-static/ffmpeg', overwrite_output=True)
            )
        await video_creator.set_progress_bar(ctx.message, 1)

        # apply corrupted timestamp...
        was_successful = True
        async with ctx.typing():
            was_successful = await self._faketime(ctx, output_filename, fake_type)
        await video_creator.set_progress_bar(ctx.message, 2)

        # send vid...
        if(was_successful):
            await video_creator.set_progress_bar(ctx.message, 3)
            await ctx.send(file=discord.File(output_filename))

        # Remove files
        try:
            if(os.path.isfile(output_filename)):
                os.remove(output_filename)
        except Exception as e:
            print(e)
        try:
            if(is_yt):
                os.remove(input_vid)
        except Exception as e:
            print(e)
        await ctx.message.clear_reactions()
    

    async def _mosh(self, ctx, filename, kwargs):
        #k = kwargs['k']
        #await self._tomato(filename, f'-m void -k {k}', '-void')
        temp_filename = filename.split('/')
        temp_filename[1] = 'x' + temp_filename[1]
        temp_filename = '/'.join(temp_filename)

        p = Popen(f'datamosh {filename} -o {temp_filename}', bufsize=2048, shell=True, stdin=subprocess.PIPE)
        p.wait()
        os.remove(filename)
        os.rename(temp_filename, filename)
    @commands.command(pass_context=True)
    async def mosh(self, ctx, g : int = 30):
        g = max(2, g)
        #qmin = min(99, max(5, qmin))
        #avi_kwargs = {'vcodec':'mpeg4', 'vtag':'xvid', 'bf':0, 'g':g, 'qmin':qmin, 'qmax':100}
        #avi_kwargs = {'vcodec':'mpeg4', 'vtag':'xvid', 'bf':0, 'g':g, 'qmin':q, 'qmax':q*4, 'keyint_min':g, 'mbd':'rd', 'ssim_acc':4, 'force_key_frames':f'expr:gte(t,n_forced*{g})', 'me_method':'log'}
        avi_kwargs = {'vcodec':'mpeg4', 'vtag':'xvid', 'bf':0, 'g':g, 'keyint_min':g, 'mbd':'rd', 'ssim_acc':4, 'force_key_frames':f'expr:gte(t,n_forced*{g})', 'me_method':'log'}
        mp4_kwargs = {}
        await video_creator.apply_corruption_and_send(ctx, self._mosh, {}, avi_kwargs, mp4_kwargs)
    

    async def _smear(self, ctx, filename, kwargs):
        await self._tomato(filename, '-m pulse -c 5', '-pulse-c5')
    @commands.command()
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
    @commands.command(pass_context=True)
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
    @commands.command(pass_context=True)
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
    @commands.command()
    async def stutter(self, ctx):
        await video_creator.apply_corruption_and_send(ctx, self._stutter, {})


        
        



def setup(bot):
    bot.add_cog(Corruption(bot))
