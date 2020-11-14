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
import shlex
import ffmpeg
import traceback
import random
import re
import video_creator

class Filter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.use_yt = False
        self.a_filters = (
            'acompressor',
            'acontrast',
            'acopy',
            'acrossfade',
            'acrossover',
            'acrusher',
            'acue',
            'adeclick',
            'adeclip',
            'adelay',
            'aintegral',
            'aecho',
            'aemphasis',
            'aeval',
            'afade',
            'afftdn',
            'afftfilt',
            'afir',
            'aformat',
            'afreqshift',
            'agate',
            'aiir',
            'alimiter',
            'allpass',
            'aloop',
            'amerge',
            'amix',
            'amultiply',
            'anequalizer',
            'anlmdn',
            'anlms',
            'anull',
            'apad',
            'aphaser',
            'aphaseshift',
            'apulsator',
            'aresample',
            'areverse',
            'arnndn',
            'asetnsamples',
            'asetpts',
            'asetrate',
            'ashowinfo',
            'asoftclip',
            'asr',
            'astats',
            'asubboost',
            'atempo',
            'atrim',
            'axcorrelate',
            'bandpass',
            'bandreject',
            'bass',
            'lowshelf',
            'biquad',
            'bs2b',
            'channelmap',
            'channelsplit',
            'chorus',
            'compand',
            'compensationdelay',
            'crossfeed',
            'crystalizer',
            'dcshift',
            'deesser',
            'drmeter',
            'dynaudnorm',
            'earwax',
            'equalizer',
            'extrastereo',
            'firequalizer',
            'flanger',
            'haas',
            'hdcd',
            'headphone',
            'highpass',
            'join',
            'ladspa',
            'loudnorm',
            'lowpass',
            'lv2',
            'mcompand',
            'pan',
            'replaygain',
            'resample',
            'rubberband',
            'sidechaincompress',
            'sidechaingate',
            'silencedetect',
            'silenceremove',
            'sofalizer',
            'stereotools',
            'stereowiden',
            'superequalizer',
            'surround',
            'highshelf',
            'tremolo',
            'vibrato',
            'volume',
            'volumedetect'
        )
        self.v_filters = (
            'addroi',
            'alphaextract',
            'alphamerge',
            'amplify',
            'ass',
            'atadenoise',
            'avgblur',
            'bbox',
            'bilateral',
            'bitplanenoise',
            'blackdetect',
            'blackframe',
            'blend',
            'bm3d',
            'boxblur',
            'bwdif',
            'cas',
            'chromahold',
            'chromakey',
            'chromanr',
            'chromashift',
            'ciescope',
            'codecview',
            'colorbalance',
            'colorchannelmixer',
            'colorkey',
            'colorhold',
            'colorlevels',
            'colormatrix',
            'colorspace',
            'convolution',
            'convolve',
            'copy',
            'coreimage',
            'cover_rect',
            'crop',
            'cropdetect',
            'cue',
            'curves',
            'datascope',
            'dblur',
            'dctdnoiz',
            'deband',
            'deblock',
            'decimate',
            'deconvolve',
            'dedot',
            'deflate',
            'deflicker',
            'dejudder',
            'delogo',
            'derain',
            'deshake',
            'despill',
            'detelecine',
            'dilation',
            'displace',
            'dnn_processing',
            'drawbox',
            'drawgraph',
            'drawgrid',
            'drawtext',
            'edgedetect',
            'elbg',
            'entropy',
            'eq',
            'erosion',
            'extractplanes',
            'fade',
            'fftdnoiz',
            'fftfilt',
            'field',
            'fieldhint',
            'fieldmatch',
            'fieldorder',
            'afifo',
            'fillborders',
            'find_rect',
            'floodfill',
            'format',
            'fps',
            'framepack',
            'framerate',
            'framestep',
            'freezedetect',
            'freezeframes',
            'frei0r',
            'fspp',
            'gblur',
            'geq',
            'gradfun',
            'graphmonitor',
            'greyedge',
            'haldclut',
            'hflip',
            'histeq',
            'histogram',
            'hqdn3d',
            'hwdownload',
            'hwmap',
            'hwupload',
            'hwupload_cuda',
            'hqx',
            'hstack',
            'hue',
            'hysteresis',
            'idet',
            'il',
            'inflate',
            'interlace',
            'kerndeint',
            'lagfun',
            'lenscorrection',
            'lensfun',
            'libvmaf',
            'limiter',
            'loop',
            'lut1d',
            'lut3d',
            'lumakey',
            'lutyuv',
            'tlut2',
            'maskedclamp',
            'maskedmax',
            'maskedmerge',
            'maskedmin',
            'maskedthreshold',
            'maskfun',
            'mcdeint',
            'median',
            'mergeplanes',
            'mestimate',
            'midequalizer',
            'minterpolate',
            'mix',
            'mpdecimate',
            'negate',
            'nlmeans',
            'nnedi',
            'noformat',
            'noise',
            'normalize',
            'null',
            'ocr',
            'ocv',
            'oscilloscope',
            'overlay',
            'overlay_cuda',
            'owdenoise',
            'pad',
            'palettegen',
            'paletteuse',
            'perspective',
            'phase',
            'photosensitivity',
            'pixdesctest',
            'pixscope',
            'pp',
            'pp7',
            'premultiply',
            'prewitt',
            'pseudocolor',
            'psnr',
            'pullup',
            'qp',
            'random',
            'readeia608',
            'readvitc',
            'remap',
            'removegrain',
            'removelogo',
            'repeatfields',
            'reverse',
            'rgbashift',
            'roberts',
            'rotate',
            'sab',
            'scale',
            'scale_npp',
            'scale2ref',
            'scroll',
            'scdet',
            'selectivecolor',
            'separatefields',
            'setpts',
            'setsar',
            'setfield',
            'setparams',
            'showinfo',
            'showpalette',
            'shuffleframes',
            'shuffleplanes',
            'signalstats',
            'signature',
            'smartblur',
            'sobel',
            'spp',
            'sr',
            'ssim',
            'stereo3d',
            'astreamselect',
            'subtitles',
            'super2xsai',
            'swaprect',
            'swapuv',
            'tblend',
            'telecine',
            'thistogram',
            'threshold',
            'thumbnail',
            'tile',
            'tinterlace',
            'tmedian',
            'tmix',
            'tonemap',
            'tpad',
            'transpose',
            'transpose_npp',
            'trim',
            'unpremultiply',
            'unsharp',
            'untile',
            'uspp',
            'v360',
            'vaguedenoiser',
            'vectorscope',
            'vidstabdetect',
            'vidstabtransform',
            'vflip',
            'vfrdet',
            'vibrance',
            'vignette',
            'vmafmotion',
            'vstack',
            'w3fdif',
            'waveform',
            'doubleweave',
            'xbr',
            'xfade',
            'xmedian',
            'xstack',
            'yadif',
            'yadif_cuda',
            'yaepblur',
            'zoompan',
            'zscale'
        )
    

    async def _amplify(self, ctx, vstream, astream, kwargs):
        vstream = vstream.filter('amplify', **kwargs)
        return vstream, astream, {}
    @commands.command(description='Make stuff colorful and sorta deepfried. Value between 4 and 16 is fun', pass_context=True)
    async def amplify(self, ctx, factor : float = 6, radius : float = 1):
        await video_creator.apply_filters_and_send(ctx, self._amplify, {'radius':radius, 'factor':factor})


    async def _backwards(self, ctx, vstream, astream, kwargs):
        vstream = ffmpeg.filter(vstream, 'reverse')
        astream = ffmpeg.filter(astream, 'areverse')
        return (vstream, astream, {})
    @commands.command(description="Reverse the video.")
    async def backwards(self, ctx):
        await video_creator.apply_filters_and_send(ctx, self._backwards, {})


    async def _volume(self, ctx, vstream, astream, kwargs):
        astream = astream.filter('volume', **kwargs)
        return vstream, astream, {}
    @commands.command(description='Increase video volume.', pass_context=True)
    async def volume(self, ctx, volume_db : float):
        await video_creator.apply_filters_and_send(ctx, self._volume, {'volume':volume_db, 'precision': 'fixed'})
    

    async def _lagfun(self, ctx, vstream, astream, kwargs):
        vstream = vstream.filter('lagfun', **kwargs)
        return vstream, astream, {}
    @commands.command(description='Make lighter pixels leak into next frames. Use a value between 0 and 1. Value of 1 makes nothing ever fade away.')
    async def lagfun(self, ctx, decay : float = 0.99):
        decay = max(0, min(decay, 1.0))
        await video_creator.apply_filters_and_send(ctx, self._lagfun, {'decay':decay})


    async def _blur(self, ctx, vstream, astream, kwargs):
        vstream = vstream.filter('median', **kwargs)
        return vstream, astream, {}
    @commands.command(description='Blur the video. Use a value between 1 and 127.', pass_context=True)
    async def blur(self, ctx, radius : float = 10): # supposed to be int lmao
        radius = max(1, min(radius, 127))
        await video_creator.apply_filters_and_send(ctx, self._blur, {'radius':radius})
    

    async def _contrast(self, ctx, vstream, astream, kwargs):
        vstream = vstream.filter('eq', **kwargs)
        return vstream, astream, {}
    @commands.command(description='Increase/decrease contrast', pass_context=True)
    async def contrast(self, ctx, contrast : float = 10):
        contrast = min(-1000, max(contrast, 1000))
        await video_creator.apply_filters_and_send(ctx, self._contrast, {'contrast':contrast})
    

    async def _edges(self, ctx, vstream, astream, kwargs):
        vstream = vstream.filter('edgedetect', low=0.1, mode='wires')
        return (vstream, astream, {})
    @commands.command(description="Show only the edges in the video.")
    async def edges(self, ctx):
        await video_creator.apply_filters_and_send(ctx, self._edges, {})


    async def _saturation(self, ctx, vstream, astream, kwargs):
        vstream = vstream.filter('hue', **kwargs)
        return vstream, astream, {}
    @commands.command(description='Increase/decrease saturation', pass_context=True)
    async def saturation(self, ctx, saturation : float = 10):
        saturation = min(-10, max(saturation, 10))
        await video_creator.apply_filters_and_send(ctx, self._saturation, {'s':saturation})
    @commands.command(description='Increase/decrease saturation', pass_context=True)
    async def saturate(self, ctx, saturation : float = 10):
        await self.saturation(ctx, saturation)


    async def _gamma(self, ctx, vstream, astream, kwargs):
        vstream = vstream.filter('eq', **kwargs)
        return vstream, astream, {}
    @commands.command(description='Increase/decrease gamma', pass_context=True)
    async def gamma(self, ctx, gamma : float = 1.3):
        gamma = min(0.1, max(gamma, 10))
        await video_creator.apply_filters_and_send(ctx, self._gamma, {'gamma':gamma})
    

    async def _brightness(self, ctx, vstream, astream, kwargs):
        vstream = vstream.filter('eq', **kwargs)
        return vstream, astream, {}
    @commands.command(description='Increase/decrease brightness', pass_context=True)
    async def brightness(self, ctx, brightness : str = '1'):
        try:
            brightness = int(brightness)
            brightness = max(-1, min(brightness, 1))
        except ValueError:
            pass
        await video_creator.apply_filters_and_send(ctx, self._brightness, {'brightness':brightness})


    async def _hue(self, ctx, vstream, astream, kwargs):
        vstream = vstream.filter('hue', **kwargs)
        return vstream, astream, {}
    @commands.command(description='Adjust hue', pass_context=True)
    async def hue(self, ctx, degrees : str):
        await video_creator.apply_filters_and_send(ctx, self._hue, {'h':degrees})
    @commands.command(description='Make a rainbow effect. You can provide a speed too!', pass_context=True)
    async def rainbow(self, ctx, speed : float = 1):
        await self.hue(ctx, f't*{speed*360}')


    async def _wobble(self, ctx, vstream, astream, kwargs):
        astream = astream.filter('chorus', delays='80ms', decays=1, depths=4, **kwargs)
        return vstream, astream, {}
    @commands.command(description='Wobbly sound. Default speed is 8', pass_context=True)
    async def wobble(self, ctx, speed : str = '8'):
        await video_creator.apply_filters_and_send(ctx, self._wobble, {'speeds':speed})


    async def _scale(self, ctx, vstream, astream, kwargs):
        vstream = (
            vstream
            .filter('scale', **kwargs)
            .filter('setsar', r='1:1')
        )
        return vstream, astream, {}
    @commands.command(description='Resize the video. Default is 360x270', pass_context=True)
    async def scale(self, ctx, w=360, h=270):
        if(w == 'auto' and h == 'auto'):
            return
        
        if(w != 'auto'):
            w = min(1240, max(w, 50))
        else:
            w = -2

        if(h != 'auto'):
            h = min(1240, max(h, 50))
        else:
            h = -2

        await video_creator.apply_filters_and_send(ctx, self._scale, {'w':w, 'h':h})
    

    async def _fps(self, ctx, vstream, astream, kwargs):
        vstream = vstream.filter('fps', **kwargs)
        return vstream, astream, {}
    @commands.command(description='Change the FPS. default is 15fps', pass_context=True)
    async def fps(self, ctx, framerate=15):
        await video_creator.apply_filters_and_send(ctx, self._fps, {'fps':framerate})
    

    async def _cartoony(self, ctx, vstream, astream, kwargs):
        vstream = vstream.filter('edgedetect', low=0.1, high=0.3, mode='colormix')
        return vstream, astream, {}
    @commands.command(description='Make stuff look kinda cartoony', pass_context=True)
    async def cartoony(self, ctx):
        await video_creator.apply_filters_and_send(ctx, self._cartoony, {})
    @commands.command(description='Make stuff look kinda cartoony', pass_context=True)
    async def cartoon(self, ctx):
        await self.cartoony(ctx)

    
    async def _negate(self, ctx, vstream, astream, kwargs):
        vstream = vstream.filter('negate')
        return vstream, astream, {}
    @commands.command(description='Invert the colors', pass_context=True)
    async def negate(self, ctx):
        await video_creator.apply_filters_and_send(ctx, self._negate, {})
    @commands.command(description='Invert the colors', pass_context=True)
    async def invert(self, ctx):
        await self.negate(ctx)
    @commands.command(description='Invert the colors', pass_context=True)
    async def negative(self, ctx):
        await self.negate(ctx)
    @commands.command(description='Invert the colors', pass_context=True)
    async def inverse(self, ctx):
        await self.negate(ctx)
    

    async def _equalizer(self, ctx, vstream, astream, kwargs):
        astream = astream.filter('superequalizer', **kwargs)
        return vstream, astream, {}
    @commands.command(description='18-band equalizer. You can provide 18 numbers for each frequency band. Not setting a number, or setting a number to -1, randomizes it.', pass_context=True)
    async def equalizer(self, ctx, b1=-1, b2=-1, b3=-1, b4=-1, b5=-1, b6=-1, b7=-1, b8=-1, b9=-1, b10=-1, b11=-1, b12=-1, b13=-1, b14=-1, b15=-1, b16=-1, b17=-1, b18=-1):
        b = [b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15, b16, b17, b18]
        b_dict = {}
        for i in range(len(b)):
            arg_name = f'{i+1}b'
            if(b[i] == -1):
                b_dict[arg_name] = random.uniform(0, 20)
            else:
                b_dict[arg_name] = b[i]

        await video_creator.apply_filters_and_send(ctx, self._equalizer, b_dict)
    @commands.command(description='18-band equalizer. You can provide 18 numbers for each frequency band. Not setting a number, or setting a number to -1, randomizes it.', pass_context=True)
    async def equalize(self, ctx, b1=-1, b2=-1, b3=-1, b4=-1, b5=-1, b6=-1, b7=-1, b8=-1, b9=-1, b10=-1, b11=-1, b12=-1, b13=-1, b14=-1, b15=-1, b16=-1, b17=-1, b18=-1):
        await self.equalizer(ctx, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15, b16, b17, b18)
    

    async def _trim(self, ctx, vstream, astream, kwargs):
        start = kwargs['start']
        end = kwargs['end']

        trim_kwargs = {}
        if(start is not None):
            trim_kwargs['start'] = start
        if(end is not None):
            trim_kwargs['end'] = end
            
        vstream = vstream.filter('trim', **trim_kwargs).filter('setpts', expr='PTS-STARTPTS')
        astream = astream.filter('atrim', **trim_kwargs).filter('asetpts', expr='PTS-STARTPTS')
        return (vstream, astream, {})
    @commands.command(description='Trim the start/end of a video. Example: !trim 0:13 1:27.3 to trim off anything before 13 seconds and after 1 minute and 27.3 seconds. You can also use start and end (examples: !trim start 1:27.3 and !trim 0:13 end)')
    async def trim(self, ctx, start : str = 'start', end : str = 'end'):
        if(re.match(r'(start|[0-9]\:[0-9][0-9](\.[0-9]+)?)', start) is None and re.match(r'(end|[0-9]\:[0-9][0-9](\.[0-9]+)?)', end) is None):
            return
        if(start == 'start' and end == 'end'):
            return

        # Create timestamps (None for start/end of video)
        if(start == 'start'):
            start = None
        else:
            start = '00:0' + start

        if(end == 'end'):
            end = None
        else:
            end = '00:0' + end

        await video_creator.apply_filters_and_send(ctx, self._trim, {'start':start, 'end':end})
    @commands.command(description='Trim the start/end of a video. Example: !trim 0:13 1:27.3 to trim off anything before 13 seconds and after 1 minute and 27.3 seconds. You can also use start and end (examples: !trim start 1:27.3 and !trim 0:13 end)')
    async def extract(self, ctx, start : str = 'start', end : str = 'end'):
        await self.trim(ctx, start, end)
    

    async def _concat(self, ctx, vstream, astream, kwargs):
        first_stream = ffmpeg.input(kwargs['first_vid_filepath'])
        vfirst = (
            first_stream.video
            .filter('scale', w=640, h=480)
            .filter('setsar', r='1:1')
        )
        afirst = first_stream.audio
        
        vstream = (
            vstream
            .filter('scale', w=640, h=480)
            .filter('setsar', r='1:1')
        )

        joined = ffmpeg.concat(vfirst, afirst, vstream, astream, v=1, a=1).node
        return (joined[0], joined[1], {'vsync':0})
    @commands.command(description='Play the last two videos side by side. The most recent video will be played after the second to most recent.')
    async def concat(self, ctx):
        first_vid_filepath, is_yt, result = await image_cache.download_nth_video(ctx, 1)
        if(not result):
            return
        await video_creator.apply_filters_and_send(ctx, self._concat, {'first_vid_filepath':first_vid_filepath})
        if(os.path.isfile(first_vid_filepath)):
            os.remove(first_vid_filepath)
    @commands.command(description='Play the last two videos side by side. The most recent video will be played after the second to most recent.')
    async def merge(self, ctx):
        await self.concat(ctx)


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
    @commands.command(description='No description needed.', pass_context=True)
    async def demonize(self, ctx):
        await video_creator.apply_filters_and_send(ctx, self._demonize, {})
    

    async def _speed(self, ctx, vstream, astream, kwargs):
        speed_change = kwargs['speed_change']
        if(speed_change >= 0.5):
            vstream = vstream.filter('setpts', f'{1.0/speed_change}*PTS')
            astream = astream.filter('atempo', speed_change)
        else:
            current_speed = 1.0
            while(current_speed >= speed_change):
                if(current_speed * 0.5 <= speed_change):
                    vstream = vstream.filter('setpts', f'{current_speed/speed_change}*PTS')
                    astream = astream.filter('atempo', speed_change/current_speed)
                    break
                vstream = vstream.filter('setpts', '2*PTS')
                astream = astream.filter('atempo', 0.5)
                current_speed *= 0.5
        return (vstream, astream, {})
    @commands.command(description="Make the video faster or slower.")
    async def speed(self, ctx, speed_change : float = 2.0):
        speed_change = max(0.05, speed_change)
        await video_creator.apply_filters_and_send(ctx, self._speed, {'speed_change': speed_change})
    

    async def _loop(self, ctx, vstream, astream, kwargs):
        amount = kwargs['amount']
        loop_streams = [vstream, astream]
        for i in range(amount - 1):
            loop_streams = ffmpeg.concat(loop_streams[0], loop_streams[1], vstream, astream, v=1, a=1).node
        return (loop_streams[0], loop_streams[1], {})
    @commands.command(description="Loop the video.")
    async def loop(self, ctx, amount : int = 2):
        amount = max(2, min(20, amount))
        await video_creator.apply_filters_and_send(ctx, self._loop, {'amount': amount})
    

    async def _pingpong(self, ctx, vstream, astream, kwargs):
        pingpong_stream = ffmpeg.concat(vstream, astream, vstream.filter('reverse'), astream.filter('areverse'), v=1, a=1).split()
        return (pingpong_stream[0], pingpong_stream[1], {})
    @commands.command(description="Plays the video, then plays it in reverse.")
    async def pingpong(self, ctx):
        await video_creator.apply_filters_and_send(ctx, self._pingpong, {})


    



    async def _filter(self, ctx, vstream, astream, kwargs):
        commands = kwargs['commands']
        for command in commands:
            filter_name = command[0]
            filter_args = command[1:]
            filter_args_kwargs = {}
            for arg in filter_args:
                arg_name, arg_val = arg.split('=',1)
                filter_args_kwargs[arg_name] = arg_val

            if(filter_name in self.v_filters):
                vstream = vstream.filter(filter_name, **filter_args_kwargs)
            elif(filter_name in self.a_filters):
                astream = astream.filter(filter_name, **filter_args_kwargs)

        return (vstream, astream, {'vsync':0})
    @commands.command(description="Apply most filters available in in ffmpeg 4.2.2")
    async def filter(self, ctx, *, commands : str = ''):
        commands = commands.split('!filter')
        for k,v in enumerate(commands):
            commands[k] = shlex.split(v)
        
        # Remove invalid commands
        commands_copy = commands
        commands = []
        invalid_commands_msg = ''
        for command in commands_copy:
            if(command[0] not in self.a_filters and command[0] not in self.v_filters):
                invalid_commands_msg += f'{command[0]} is not supported... yet?\n'
            else:
                commands.append(command)
        if(invalid_commands_msg != ''):
            if(len(commands) == 0):
                await ctx.send('None of those filters are supported... yet?')
                return
            else:
                await ctx.send(f'{invalid_commands_msg}Remaining filters will still be applied.')

        await video_creator.apply_filters_and_send(ctx, self._filter, {'commands':commands})





    async def _oldfilter(self, ctx, vstream, astream, kwargs):
        commands = kwargs['command']
        filter_name = commands[0]
        filter_args = commands[1:]
        filter_args_kwargs = {}
        for arg in filter_args:
            arg_name, arg_val = arg.split('=',1)
            filter_args_kwargs[arg_name] = arg_val

        if(filter_name in self.v_filters):
            vstream = vstream.filter(filter_name, **filter_args_kwargs)
        elif(filter_name in self.a_filters):
            astream = astream.filter(filter_name, **filter_args_kwargs)

        return (vstream, astream, {'vsync':0})
    @commands.command(description="Apply most filters available in in ffmpeg 4.2.2")
    async def oldfilter(self, ctx, *, command : str = ''):
        command = shlex.split(command)
        if(command[0] not in self.a_filters and command[0] not in self.v_filters):
            await ctx.send("That filter is not supported... yet?")
            return
        await video_creator.apply_filters_and_send(ctx, self._filter, {'command':command})
        
    





    
        

def setup(bot):
    bot.add_cog(Filter(bot))
