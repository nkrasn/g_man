import asyncio
import discord
from discord.ext import commands
import ffmpeg
import media_cache
import os
import random
import re
import subprocess
from subprocess import Popen
import textwrap
import video_creator
import youtube_dl

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.use_yt = False
        self.vc = None


    async def _replace_audio(self, ctx, vstream, astream, kwargs):
        audio_filename = kwargs['audio_filename']
        if(os.path.isfile(f'clips/{audio_filename}')):
            astream = ffmpeg.input(f'clips/{audio_filename}')
            return (vstream, astream, {'shortest':None, 'vcodec':'copy'})
        else:
            await ctx.send(f'Could not find `{audio_filename}` in my `clips` folder! Please report this error to the g_man Discord server.')
            return None, None, {'ignore':True}


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

    
    async def _deepfry(self, ctx, vstream, astream, kwargs):
        vstream = (
            vstream
            .filter('scale', w=240, h=-2)
            .filter('eq', contrast=2, saturation=2)
            .filter('unsharp', luma_msize_x=7, luma_msize_y=7, luma_amount=2.5)
            .filter('eq', contrast=4, saturation=3)
            .filter('scale', w=360, h=-2)
        )
        astream = (
            astream
            .filter('crystalizer', i=10)
            .filter('volume', volume=2, precision='fixed')
        )
        return vstream, astream, {}
    @commands.command()
    async def deepfry(self, ctx):
        await video_creator.apply_filters_and_send(ctx, self._deepfry, {})


    async def _demonize(self, ctx, vstream, astream, kwargs):
        astream = astream.filter('chorus', delays='80ms', decays=1, speeds=20, depths=4)
        vstream = (
            vstream
            .filter('amplify', radius=1, factor=3)
            .filter('eq', contrast=1.3)
            .filter('lagfun', decay=0.95)
            .filter('eq', saturation=1.3)
            .filter('amplify', radius=1, factor=5)
        )
        return vstream, astream, {'fs':'4M'}
    @commands.command(pass_context=True)
    async def demonize(self, ctx):
        await video_creator.apply_filters_and_send(ctx, self._demonize, {})

    
    def semitones_to_pitches(self, semitones):
        semitones = semitones.split(' ')
        semitones = list(filter(lambda x : x.replace('.', '', 1).lstrip('-').isdigit(), semitones))
        pitches = []

        if(len(semitones) == 0):
            semitones = random.choice((
                (7, 14, -12),
                (3, 7),
                (-12, 12),
                (6, 12),
                (3, 6, 12)
            ))
        
        a = 2**(1.0/12.0)
        for semitone in semitones:
            semitone = float(semitone)
            pitch = a**abs(semitone)
            if(semitone < 0):
                pitch = 1.0 / pitch
            pitches.append(pitch)

        return pitches

    async def _harmonize(self, ctx, vstream, astream, kwargs):
        pitches = kwargs['pitches']
        astreams = []
        for i in range(len(pitches)):
            pitch = pitches[i]
            astream = astream.asplit()
            astreams.append(astream[1].filter('rubberband', pitch=pitch))
            astream = astream[0]
        astreams.append(astream)

        astream = astreams[0]
        for i in range(1, len(astreams)):
            astream = ffmpeg.filter([astream, astreams[i]], 'amix').filter('volume', volume=2, precision='fixed')

        return vstream, astream, {}
    @commands.command()
    async def harmonize(self, ctx, *, semitones : str = ''):
        pitches = self.semitones_to_pitches(semitones)
        await video_creator.apply_filters_and_send(ctx, self._harmonize, {'pitches':pitches})

    async def _harmonizedeep(self, ctx, vstream, astream, kwargs):
        pitches = kwargs['pitches']
        for pitch in pitches:
            astream = astream.asplit()
            astream = (
                ffmpeg
                .filter(
                    [
                        astream[0].filter('rubberband', pitch=pitch),
                        astream[1]
                    ],
                    'amix'
                )
                .filter('volume', volume=2, precision='fixed')
            )
        return vstream, astream, {}
    @commands.command()
    async def harmonizedeep(self, ctx, *, semitones : str = ''):
        pitches = self.semitones_to_pitches(semitones)
        await video_creator.apply_filters_and_send(ctx, self._harmonizedeep, {'pitches':pitches})
    

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

    
    @commands.command()
    async def mahna(self, ctx):
        await video_creator.apply_filters_and_send(ctx, self._replace_audio, {'audio_filename':'mahna.mp3'})
    @commands.command()
    async def mahnamahna(self, ctx):
        await self.mahna(ctx)


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


    async def _sequencer(self, ctx, vstream, astream, kwargs):
        len_to_speed = (1, 2, 1, 0.5)

        # Make vstream/astream for rests
        vstream = vstream.split()
        vrest = vstream[1].filter('eq', brightness=-1)
        vstream = vstream[0]
        astream = astream.asplit()
        arest = astream[1].filter('volume', volume=-100, precision='fixed')
        astream = astream[0]

        # Make vstream/astream for final result
        vstream = vstream.split()
        vfinale = vstream[1]
        vstream = vstream[0]
        astream = astream.asplit()
        afinale = astream[1]
        astream = astream[0]

        # Making the song
        notes = kwargs['notes']
        for note in notes:
            note_tone, note_len = note[0], len_to_speed[note[1]]
            vnote = None
            anote = None

            if(note_tone == '.'):
                vrest = vrest.split()
                vnote = vrest[1]
                arest = arest.asplit()
                anote = arest[1]
            else:
                vstream = vstream.split()
                vnote = vstream[1]
                astream = astream.asplit()
                anote = astream[1].filter('rubberband', pitch=note_tone)

            if(note_len != 1):
                vnote = vnote.filter('setpts', f'{1.0/note_len}*PTS')
                anote = anote.filter('atempo', note_len)
            vfinale = ffmpeg.concat(vfinale, vnote, v=1, a=0)
            afinale = ffmpeg.concat(afinale, anote, v=0, a=1)
            
            if(note_tone == '.'):
                vrest = vrest[0]
                arest = arest[0]
            else:
                vstream = vstream[0]
                astream = astream[0]

        return vfinale, afinale, {}
    def semitone_to_pitch(self, semitone):
        pitch = (2**(1.0/12.0))**abs(semitone)
        if(semitone < 0):
            pitch = 1.0 / pitch
        return pitch
    @commands.command()
    async def sequencer(self, ctx, *, notes : str = '0 0 12x 7x ..'):
        # Unfortunately, does not work at the moment
        # Maybe one day...
        return
        # Tokenize
        notes = notes.split(' ')
        await ctx.send(notes)
        for i in range(len(notes)):
            raw_note = notes[i]

            if(re.match(r'(\-?[0-9]+x*$)|(\.+$)', raw_note)):
                # Rests
                if(raw_note[0] == '.'):
                    notes[i] = ('.', len(raw_note))
                # Notes
                else:
                    note = (None, None)
                    hold_pos = raw_note.find('x')
                    if(hold_pos == -1):
                        note = (self.semitone_to_pitch(int(raw_note)), 1)
                    else:
                        semitone = int(raw_note[:hold_pos])
                        hold = len(raw_note[hold_pos:]) + 1
                        note = (self.semitone_to_pitch(semitone), hold)
                    notes[i] = note
            else:
                notes[i] = None
                continue
        notes = list(filter(lambda x : x is not None, notes))
        await ctx.send(notes)
        await video_creator.apply_filters_and_send(ctx, self._sequencer, {'notes':notes})


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
        #img_stream = ffmpeg.input('clips/hypercam.jpg').filter("scale", w=300, h=-2)
        vstream = (
            ffmpeg
            .filter(vstream, "scale", w=640, h=480)
            .filter("setsar", r="1:1")
            #.overlay(img_stream)
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
    
    async def _vintage(self, ctx, vstream, astream, kwargs):
        vstream = (
            vstream
            .filter('scale', w=100, h=-2)
            .filter('noise', alls=50, allf='t+u')
            .filter('scale', w=480, h=-2)
            .filter('hue', s=0)
            .filter('vignette')
            .filter('vignette')
            .filter('fps', fps=60)
            .filter('scroll', v=1.0/100.0)
            .filter('fps', fps=29)
            .filter('scroll', v=-(60.0/29.0)/100.0)
            .filter('fps', 6)
        )

        eq_vals = [5]*4 + [4]*2 + [3] + [2]*2 + [1]*2 + [0]*7
        eq_dict = {}
        for i in range(18):
            eq_dict[f'{i+1}b'] = eq_vals[i]
        astream = astream.filter('superequalizer', **eq_dict)

        return vstream, astream, {}
    @commands.command()
    async def vintage(self, ctx):
        await video_creator.apply_filters_and_send(ctx, self._vintage, {})

        



def setup(bot):
    bot.add_cog(Fun(bot))
