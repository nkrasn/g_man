import discord
import asyncio
from discord.ext import commands
import subprocess
import signal
from subprocess import Popen
import youtube_dl
import media_cache
import re
import os
import ffmpeg
import traceback
import random
import textwrap
import video_creator

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.use_yt = False
        self.vc = None


    async def _replace_audio(self, ctx, vstream, astream, kwargs):
        audio_filename = kwargs['audio_filename']
        astream = ffmpeg.input(f'clips/{audio_filename}')
        return (vstream, astream, {'shortest':None, 'vcodec':'copy'})


    @commands.command(pass_context=True)
    async def americ(self, ctx):
        await video_creator.apply_filters_and_send(ctx, self._replace_audio, {'audio_filename':'americ.mp3'})
    

    async def _cartoony(self, ctx, vstream, astream, kwargs):
        vstream = vstream.filter('edgedetect', low=0.1, high=0.3, mode='colormix')
        return vstream, astream, {}
    @commands.command(pass_context=True)
    async def cartoony(self, ctx):
        await video_creator.apply_filters_and_send(ctx, self._cartoony, {})
    @commands.command(pass_context=True)
    async def cartoon(self, ctx):
        await self.cartoony(ctx)


    async def _demonize(self, ctx, vstream, astream, kwargs):
        astream = astream.filter('chorus', delays='80ms', decays=1, speeds=20, depths=4)
        vstream = (
            vstream
            .filter('amplify', radius=1, factor=5)
            .filter('eq', contrast=1.3)
            .filter('lagfun', decay=0.95)
            .filter('eq', saturation=1.3)
            .filter('amplify', radius=1, factor=15)
        )
        return vstream, astream, {'fs':'4M'}
    @commands.command(pass_context=True)
    async def demonize(self, ctx):
        await video_creator.apply_filters_and_send(ctx, self._demonize, {})


    async def _gif(self, ctx, vstream, astream, kwargs):
        return (vstream, astream, {})
    @commands.command()
    async def gif(self, ctx):
        await video_creator.apply_filters_and_send(ctx, self._gif, {'is_gif':True})
    

    async def _histogram(self, ctx, vstream, astream, kwargs):
        vstream = astream.filter('ahistogram')
        return (vstream, astream, {})
    @commands.command()
    async def histogram(self, ctx):
        await video_creator.apply_filters_and_send(ctx, self._histogram, {})
    

    async def _watermark(self, ctx, vstream, astream, kwargs):
        x = kwargs['x']
        y = kwargs['y']
        w = kwargs['w']
        h = kwargs['h']
        watermark_stream = ffmpeg.input(kwargs['watermark_filepath'])
        if(w is not None and h is not None):
            watermark_stream = watermark_stream.filter('scale', w=w, h=h)
        vstream = vstream.filter('scale', h=320, w=-2).filter('setsar', r='1:1')
        vstream = ffmpeg.overlay(vstream, watermark_stream, x=x, y=y)
        return (vstream, astream, {})
    @commands.command()
    async def hypercam(self, ctx):
        await video_creator.apply_filters_and_send(ctx, self._watermark, {'watermark_filepath':'clips/hypercam.jpg', 'x':0, 'y':0, 'w':None, 'h':None})    
    @commands.command()
    async def ifunny(self, ctx):
        await video_creator.apply_filters_and_send(ctx, self._watermark, {'watermark_filepath':'clips/ifunny.jpg', 'x':'main_w-overlay_w', 'y':'main_h-overlay_h', 'w':-2, 'h':16})
        
    
    async def _mp3(self, ctx, vstream, astream, kwargs):
        return (vstream, astream, {})
    @commands.command()
    async def mp3(self, ctx):
        await video_creator.apply_filters_and_send(ctx, self._mp3, {'is_mp3':True})


    async def _pingpong(self, ctx, vstream, astream, kwargs):
        pingpong_stream = ffmpeg.concat(vstream, astream, vstream.filter('reverse'), astream.filter('areverse'), v=1, a=1).split()
        return (pingpong_stream[0], pingpong_stream[1], {})
    @commands.command()
    async def pingpong(self, ctx):
        await video_creator.apply_filters_and_send(ctx, self._pingpong, {})
    

    async def _rainbow(self, ctx, vstream, astream, kwargs):
        vstream = vstream.filter('hue', h=kwargs['h'])
        return vstream, astream, {}
    @commands.command(pass_context=True)
    async def rainbow(self, ctx, speed : float = 1):
        await video_creator.apply_filters_and_send(ctx, self._rainbow, {'h':f't*{speed*360}'})


    @commands.command(pass_context=True)
    async def tetris(self, ctx):
        await video_creator.apply_filters_and_send(ctx, self._replace_audio, {'audio_filename':'tetris.mp3'})

    
    async def _text(self, ctx, vstream, astream, kwargs):
        top_msg = kwargs['top_msg']
        bot_msg = kwargs['bot_msg']
        default_text_kwargs = {
            'fontfile':'fonts/impact.ttf',
            'font':'impact',
            'fontsize':50,
            'x':'(main_w-tw)/2',
            'fontcolor':'white',
            'borderw':3,
            'bordercolor':'black'
        }
        if(top_msg != ''):
            vstream = vstream.filter('drawtext', text=top_msg, y=30, **default_text_kwargs)
        if(bot_msg != ''):
            vstream = vstream.filter('drawtext', text=bot_msg, y='(main_h-th-30)', **default_text_kwargs)
        return (vstream, astream, {})
    @commands.command()
    async def text(self, ctx, *, msg : str = 'top text|bottom text'):
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
        await video_creator.apply_filters_and_send(ctx, self._text, {'top_msg':top_msg, 'bot_msg':bot_msg})
    

    async def _trippy(self, ctx, vstream, astream, kwargs):
        input_filename = kwargs['input_filename']
        speed = kwargs['speed']
        blend_mode = kwargs['blend_mode']

        slowed_down_video = (
            ffmpeg
            .input(input_filename).video
            .filter('setpts', f'{1.0/speed}*PTS')
        )
        vstream = ffmpeg.filter([slowed_down_video, vstream], 'blend', all_mode=blend_mode)
        return vstream, astream, {'shortest':None}
    @commands.command()
    async def trippy(self, ctx, speed : float = 0.97, blend_mode : str = 'average'):
        speed = min(1.0, max(0.5, speed))
        await video_creator.apply_filters_and_send(ctx, self._trippy, {'speed':speed, 'blend_mode':blend_mode})


    async def _tutorial(self, ctx, vstream, astream, kwargs):
        title_top = kwargs['title_top']
        title_bot = kwargs['title_bot']
        wrapped_title = kwargs['wrapped_title']
        title_font_size = kwargs['title_font_size']
        sub_font_size = kwargs['sub_font_size']

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
            output_stream, "drawtext", text=title_bot[:19], fontsize=sub_font_size, 
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
        vstream = (
            ffmpeg
            .filter(vstream, "scale", w=640, h=480)
            .filter("setsar", r="1:1")
            .overlay(img_stream)
        )
        # Appending it to the title text
        output_stream = ffmpeg.concat(output_stream, vstream)

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
        song = random.choice(os.listdir('tutorial/songs/'))
        astream = ffmpeg.input(f"tutorial/songs/{song}")

        return (output_stream, astream, {'vsync':2, 'shortest':None})
    @commands.command()
    async def tutorial(self, ctx, *, msg : str = ''):
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
                    'Gta San Andreas goez crazy',
                    'Austin Powers watch online free (link in description)'
                ])
            else:
                title_top = msg[0]
        else:
            title_top = msg[0]
            title_bot = msg[1]
        
        # Make the text wrap
        title_font_size = 60
        wrapped_title = textwrap.wrap(title_top, 16)
        if(len(wrapped_title) > 3):
            title_font_size = 50
            wrapped_title = textwrap.wrap(title_top, 19)
        sub_font_size = title_font_size * 0.7

        await video_creator.apply_filters_and_send(ctx, self._tutorial, {
            'title_top':title_top, 'title_bot':title_bot, 
            'wrapped_title':wrapped_title, 
            'title_font_size':title_font_size, 'sub_font_size':sub_font_size
        })
        



def setup(bot):
    bot.add_cog(Fun(bot))
