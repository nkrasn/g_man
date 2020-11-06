import discord
import asyncio
from discord.ext import commands
import subprocess
import signal
from subprocess import Popen
import youtube_dl
import image_cache
import re
import os
import ffmpeg
import traceback
import random
import textwrap

class TimeoutError(Exception):
    pass

def interrupt(a, b):
    raise TimeoutError()

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.use_yt = False
        self.vc = None
    
    @commands.command(description='Datamoshing. Provide a number to change quality (lowest/default = 1.5). Provide another number to change screen width (default: 640)', pass_context=True)
    async def mosh(self, ctx, quality: float=1.5, width: int=640):
        quality = str(max(quality, 1.5))
        width = str(max(width, 20))

        input_vid, is_yt, result = await image_cache.download_last_video(ctx)
        if(not result):
            await ctx.send("Error downloading the video")
            return
        
        #out_filename = 'vids/out.mp4'

        await ctx.send("I will get back to you...")
        try:
            #await ctx.send(input_vid)
            p = Popen('./mosh.sh ' + input_vid + ' ' + quality + ' ' + width, bufsize=2048, shell=True, stdin=subprocess.PIPE)
            p.wait()
            # SUCCESS
            if(p.returncode == 0):
                await ctx.send(file=discord.File('vids/out.mp4'))
            else:
                await ctx.send("There was an error lol tell nikita")

        except TimeoutError as e:
            await ctx.send('Command took to long to execute.\n```\n' + str(e) + '```')
        except Exception as e:
            await ctx.send('Error:\n```\n' + str(e) + '```')
            print(traceback.format_exc())
        if(is_yt):
            os.remove(input_vid)




    @commands.command(description='for smoothie', pass_context=True)
    async def americ(self, ctx):
        input_vid, is_yt, result = await image_cache.download_last_video(ctx)
        if(not result):
            await ctx.send("Error downloading the video")
            return
        
        async with ctx.typing():
            try:
                victim = ffmpeg.input(input_vid)
                america_clip = ffmpeg.input('clips/americ.mp3')
                # put america in the vid
                (
                    ffmpeg
                    .output(america_clip.audio, victim.video, 'vids/out.mp4', fs='7M', shortest=None, vcodec='copy')
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
    


    @commands.command(description='for bundle', pass_context=True)
    async def metal(self, ctx):
        input_vid, is_yt, result = await image_cache.download_last_video(ctx)
        if(not result):
            await ctx.send("Error downloading the video")
            return
        
        async with ctx.typing():
            try:
                victim = ffmpeg.input(input_vid)
                america_clip = ffmpeg.input('clips/metal.mp3')
                # put america in the vid
                (
                    ffmpeg
                    .output(america_clip.audio, victim.video, 'vids/out.mp4', fs='7M', shortest=None, vcodec='copy')
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



    @commands.command(description='Replace the second to last video\'s audio with the last video\'s audio. Add "blend" if you want to blend their audio.', pass_context=True)
    async def audioswap(self, ctx, swap_type: str = "swap"):
        input_audio, is_yt, result = await image_cache.download_last_video(ctx)
        #await ctx.send("last video downloaded is: " + input_audio)
        if(not result):
            await ctx.send("Error downloading the first video")
            return
        input_video = image_cache.get_from_cache(str(ctx.message.channel.id))[-2]
        #await ctx.send("second to last video is: " + input_video)
        if(input_video is None):
            await ctx.send("Second input video is None, aborting")
        result, input_video = await image_cache.yt(ctx, input_video, 'audioswap')
        if(not result):
            await ctx.send("Error downloading the second video")
            return
        
        async with ctx.typing():
            try:
                video_stream = ffmpeg.input(input_video)
                audio_stream = ffmpeg.input(input_audio).audio
                if(swap_type == 'blend'):
                    audio_stream = ffmpeg.filter([video_stream.audio, audio_stream], 'amix')
                video_stream = video_stream.video
                
                (
                    ffmpeg
                    .output(audio_stream, video_stream, 'vids/out.mp4', fs='7M', shortest=None, vcodec='copy')
                    .run(cmd='ffmpeg4-2-2/ffmpeg', overwrite_output=True)
                )

                await ctx.send(file=discord.File('vids/out.mp4'))
            except TimeoutError as e:
                await ctx.send('Command took to long to execute.\n```\n' + str(e) + '```')
            except Exception as e:
                await ctx.send('Error:\n```\n' + str(e) + '```')
                print(traceback.format_exc())
            if(is_yt):
                os.remove(input_video)






    @commands.command(description="Unregistered Hypercam 2")
    async def hypercam(self, ctx):
        input_vid, is_yt, result = await image_cache.download_last_video(ctx)
        if(not result):
            await ctx.send("Error downloading the video")
            return
        
        async with ctx.typing():
            try:
                input_stream = ffmpeg.input(input_vid)
                video_stream = input_stream.video
                audio_stream = input_stream.audio
                image_stream = ffmpeg.input('clips/hypercam.jpg')

                video_stream = ffmpeg.filter(video_stream, 'scale', h=320, w=-2)
                video_stream = ffmpeg.overlay(video_stream, image_stream)
                #video_stream = ffmpeg.filter(video_stream, image_stream)
                (
                    ffmpeg
                    #.filter(video_stream, 'scale', h='480', w='-2')
                    #.overlay(image_stream)
                    #.output(audio_stream, 'vids/out.mp4', vcodec='copy')
                    .output(audio_stream, video_stream, 'vids/out.mp4', fs='7M')
                    #.output(input_stream, 'vids/out.mp4')
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
    



    @commands.command(description="ifunny")
    async def ifunny(self, ctx):
        input_vid, is_yt, result = await image_cache.download_last_video(ctx)
        if(not result):
            await ctx.send("Error downloading the video")
            return
        
        async with ctx.typing():
            try:
                input_stream = ffmpeg.input(input_vid)
                video_stream = input_stream.video
                audio_stream = input_stream.audio
                image_stream = ffmpeg.input('clips/ifunny.jpg')
                image_stream = ffmpeg.filter(image_stream, 'scale', h=16, w=-2)

                video_stream = ffmpeg.filter(video_stream, 'scale', h=320, w=-2)
                video_stream = ffmpeg.overlay(video_stream, image_stream, x="(main_w-overlay_w)", y="(main_h-overlay_h)")
                #video_stream = ffmpeg.filter(video_stream, image_stream)
                (
                    ffmpeg
                    #.filter(video_stream, 'scale', h='480', w='-2')
                    #.overlay(image_stream)
                    #.output(audio_stream, 'vids/out.mp4', vcodec='copy')
                    .output(audio_stream, video_stream, 'vids/out.mp4', fs='7M')
                    #.output(input_stream, 'vids/out.mp4')
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
            
    

    @commands.command(description="2011 memes (separate top and bottom text with the | symbol)")
    async def text(self, ctx, *, msg : str = None):
        input_vid, is_yt, result = await image_cache.download_last_video(ctx)
        if(not result):
            await ctx.send("Error downloading the video")
            return
        
        # Split up top and bottom
        top_msg = ''
        bot_msg = ''
        msg = msg.upper().split('|')
        for i in range(len(msg)):
            msg[i] = msg[i].strip()
        if(len(msg) == 1):
            top_msg = msg[0]
        else:
            top_msg = msg[0]
            bot_msg = msg[1]
        
        async with ctx.typing():
            try:
                input_stream = ffmpeg.input(input_vid)
                video_stream = input_stream.video
                audio_stream = input_stream.audio

                video_stream = ffmpeg.filter(video_stream, 'scale', h=380, w=-2)
                if(top_msg != ''):
                    video_stream = ffmpeg.filter(
                        video_stream, 'drawtext', 
                        text=top_msg, fontfile='fonts/impact.ttf', font='impact', fontsize='50',
                        x='(main_w-tw)/2', y='30',
                        fontcolor='white', borderw='3', bordercolor='black'
                    )
                if(bot_msg != ''):
                    video_stream = ffmpeg.filter(
                        video_stream, 'drawtext', 
                        text=bot_msg, fontfile='fonts/impact.ttf', font='impact', fontsize='50',
                        x='(main_w-tw)/2', y='(main_h-th-30)',
                        fontcolor='white', borderw='3', bordercolor='black'
                    )
                (
                    ffmpeg
                    .output(audio_stream, video_stream, 'vids/out.mp4', fs='7M')
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
    


    @commands.command(description="do the whip and the naynay")
    async def whip(self, ctx, amount: int = 1, delay: float = 0.8):
        try:
            if(self.vc is not None):
                await ctx.send("Please wait, child")
                return
            amount = min(100,max(0, amount))
            channel = ctx.author.voice.channel
            self.vc = await channel.connect()
            await asyncio.sleep(0.5)
            for i in range(amount):
                if(not self.vc.is_connected()):
                    break
                self.vc.play(discord.FFmpegPCMAudio('clips/johnny.mp3'))
                await asyncio.sleep(min(120, max(delay, 0.05)))
                self.vc.stop()
            await asyncio.sleep(1)
            await self.vc.disconnect()
            self.vc.cleanup()
            self.vc = None
        except Exception as e:
            await ctx.send(str(e))
    
    @commands.command(description="do the whip and the naynay")
    async def whatdidyousay(self, ctx, amount: int = 1, delay: float = 16):
        try:
            if(self.vc is not None):
                await ctx.send("Please wait, child")
                return
            amount = min(100,max(0, amount))
            channel = ctx.author.voice.channel
            self.vc = await channel.connect()
            await asyncio.sleep(0.5)
            for i in range(amount):
                if(not self.vc.is_connected()):
                    break
                self.vc.play(discord.FFmpegPCMAudio('clips/CLIKY_CLACKY.ogg'))
                await asyncio.sleep(min(120, max(delay, 0.1)))
                self.vc.stop()
            await asyncio.sleep(1)
            await self.vc.disconnect()
            self.vc.cleanup()
            self.vc = None
        except Exception as e:
            await ctx.send(str(e))
    
    @commands.command(description="xp")
    async def pinball(self, ctx, amount: int = 1, delay: float = 78.0):
        try:
            if(self.vc is not None):
                await ctx.send("Please wait, child")
                return
            amount = min(100,max(0, amount))
            channel = ctx.author.voice.channel
            self.vc = await channel.connect()
            await asyncio.sleep(0.5)
            for i in range(amount):
                if(not self.vc.is_connected()):
                    break
                self.vc.play(discord.FFmpegPCMAudio('clips/pinball.mp3'))
                await asyncio.sleep(min(120, max(delay, 0.1)))
                self.vc.stop()
            await asyncio.sleep(1)
            await self.vc.disconnect()
            self.vc.cleanup()
            self.vc = None
        except Exception as e:
            await ctx.send(str(e))
        
    @commands.command(description="xp")
    async def quack(self, ctx, amount: int = 1, delay: float = 0.8):
        try:
            if(self.vc is not None):
                await ctx.send("Please wait, child")
                return
            amount = min(100,max(0, amount))
            channel = ctx.author.voice.channel
            self.vc = await channel.connect()
            await asyncio.sleep(0.5)
            for i in range(amount):
                if(not self.vc.is_connected()):
                    break
                self.vc.play(discord.FFmpegPCMAudio('clips/quack.mp3'))
                await asyncio.sleep(min(120, max(delay, 0.1)))
                self.vc.stop()
            await asyncio.sleep(1)
            await self.vc.disconnect()
            self.vc.cleanup()
            self.vc = None
        except Exception as e:
            await ctx.send(str(e))

    @commands.command(description="undo the whip and naynay")
    async def whipdisconnect(self, ctx):
        try:
            if(self.vc is not None):
                self.vc.disconnect()
                self.vc.cleanup()
        except Exception as e:
            await ctx.send(e)
        self.vc = None








    @commands.command(description="Create an old-school tutorial.")
    async def tutorial(self, ctx, *, msg : str = ''):
        input_vid, is_yt, result = await image_cache.download_last_video(ctx)
        if(not result):
            await ctx.send("Error downloading the video")
            return
        
        # #104080 is blue background hex code
        # 3.47 seconds is how long title/credits is
        
        # Split up top and bottom
        title_top = ''
        title_bot = 'by ' + str(ctx.author.display_name)
        msg = msg.split('|')
        for i in range(len(msg)):
            msg[i] = msg[i].strip()
        if(len(msg) == 1):
            if(msg[0] == ''):
                title_top = random.choice([
                    'how to get free club penugin',
                    'My Movie',
                    'How To Download from Megaupload.com',
                    'How to Downalod off Megaupload.com',
                    'FREE robux tutorial WORKING 2009',
                    'Where to get Gta San Andreas Noob Mod V2',
                    'club penguin how to tip the iceberg the only way!!!!',
                    'club penguin proof of tipping iceberg!',
                    'Wizard 101 - How to get on 2 accounts!!!!',
                    'Emulator/Rom Tutorial',
                    'How to get on top of the night club in club penguin with out hacking',
                    'How to install cleo mods to GTA San Andreas',
                    'How to install weapon mods on GTA San Andreas (IMGTool)',
                    'Gta San Andreas goez crazy'
                ])
            else:
                title_top = msg[0]
        else:
            title_top = msg[0]
            title_bot = msg[1]
        
        # make it WRAP
        title_font_size = 60
        wrapped_title = textwrap.wrap(title_top, 16)
        if(len(wrapped_title) > 3):
            title_font_size = 50
            wrapped_title = textwrap.wrap(title_top, 19)
        sub_font_size = title_font_size * 0.7

        
        async with ctx.typing():
            try:
                # drawtext defaults
                drawtext_params = {
                    'fontcolor': '#f0f0f0', 
                    'fontfile': 'fonts/arial.ttf', 'font': 'Arial',
                    'shadowcolor': 'black', 'shadowx': 1, 'shadowy': 1
                }
                drawtext_noshadow_params = {
                    'fontcolor': '#f0f0f0', 
                    'fontfile': 'fonts/arial.ttf', 'font': 'Arial'
                }

                output_stream = ffmpeg.input('tutorial/bg.mp4')
                # Create scrolling text in the background
                output_stream = (
                    output_stream
                    .filter(
                        "drawtext", text=title_top, fontsize=180,
                        x="(main_w-tw)/2-th+t*70", y=100,
                        alpha='min(1,-abs(t-1.7)+1.7)*0.5', **drawtext_noshadow_params
                    )
                    .filter(
                        "drawtext", text=title_top, fontsize=385,
                        x="(main_w-tw)/2+th-t*40", y=200,
                        alpha='min(1,-abs(t-1.7)+1.7)*0.2', **drawtext_noshadow_params
                    )
                )
                # Create the title text
                for i in range(len(wrapped_title)):
                    if(i == 4):
                        break # only 4 lines at most
                    output_stream = ffmpeg.filter(
                        output_stream, "drawtext", text=wrapped_title[-i-1], fontsize=title_font_size, 
                        x="(main_w-tw)/2", y=f"main_h/2-({title_font_size*i})-{title_font_size/2}",
                        alpha="-abs(t-1.7)+1.7", **drawtext_params
                    )
                # Create the subtitle text
                output_stream = ffmpeg.filter(
                    output_stream, "drawtext", text=textwrap.wrap(title_bot, 19)[0], fontsize=sub_font_size, 
                        x="(main_w-tw)/2", y=f"main_h/2+({sub_font_size})",
                        alpha="-abs(t-1.7-0.25)+1.7-0.25", **drawtext_params
                )
                # Scale down then up for lower quality
                output_stream = (
                    ffmpeg
                    .filter(output_stream, "scale", w=500, h=375)
                    .filter("scale", w=640, h=480, flags="neighbor")
                )


                # Scaling the desired video + effects
                img_stream = ffmpeg.input('clips/hypercam.jpg').filter("scale", w=300, h=-2)
                vid_stream = ffmpeg.input(input_vid).video
                vid_stream = (
                    ffmpeg
                    .filter(vid_stream, "scale", w=640, h=480)
                    .filter("setsar", r="1:1")
                    .overlay(img_stream)
                )
                # Appending it to the title text
                output_stream = ffmpeg.concat(output_stream, vid_stream)


                # End credits
                end_stream = ffmpeg.input('tutorial/bg.mp4')
                end_stream = (
                    end_stream
                    .filter(
                        "drawtext", text="thank you", fontsize=60, 
                        x="(main_w-tw)/2", y=f"main_h/2-70",
                        alpha="-abs(t-1.7)+1.7", **drawtext_params
                    )
                    .filter(
                        "drawtext", text="for watching", fontsize=60, 
                        x="(main_w-tw)/2", y=f"main_h/2",
                        alpha="-abs(t-1.7)+1.7", **drawtext_params
                    )
                    .filter("scale", w=500, h=375)
                    .filter("scale", w=640, h=480, flags="neighbor")
                )
                # Appending credits to video
                output_stream = ffmpeg.concat(output_stream, end_stream)

                # Scale it down to 360p
                output_stream = (
                    output_stream
                    .filter("scale", w=360, h=270)
                    .filter("setsar", r="1:1")
                )


                # Adding music
                music_stream = ffmpeg.input("tutorial/" + random.choice(['evanescence', 'trance']) + '.mp3')

                (
                    ffmpeg
                    .output(output_stream, music_stream, 'vids/out.mp4', fs='7M', vsync=2, shortest=None)
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
    bot.add_cog(Fun(bot))
