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
            'aderivative',
            'aintegral',
            'aecho',
            'aemphasis',
            'aeval',
            'afade',
            'afftdn',
            'afftfilt',
            'afir',
            'afifo',
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
            'treble',
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
            'fifo',
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
            'lut',
            'lutrgb',
            'lutyuv',
            'lut2',
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
            'setdar',
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


    async def _audioswap(self, ctx, vstream, astream, kwargs):
        vstream = ffmpeg.input(kwargs['target_filepath']).video
        return (vstream, astream, {'shortest':None, 'vcodec':'copy'})
    @commands.command(description="Swap the audio of the two most recent videos. The audio from the most recent video will be used.")
    async def audioswap(self, ctx):
        target_filepath, is_yt, result = await image_cache.download_nth_video(ctx, 1)
        if(not result):
            return
        await video_creator.apply_filters_and_send(ctx, self._audioswap, {'target_filepath':target_filepath})
        if(os.path.isfile(target_filepath)):
            os.remove(target_filepath)


    async def _backwards(self, ctx, vstream, astream, kwargs):
        vstream = ffmpeg.filter(vstream, 'reverse')
        astream = ffmpeg.filter(astream, 'areverse')
        return (vstream, astream, {})
    @commands.command(description="Reverse the video.")
    async def backwards(self, ctx):
        await video_creator.apply_filters_and_send(ctx, self._backwards, {})


    async def _blur(self, ctx, vstream, astream, kwargs):
        vstream = vstream.filter('median', **kwargs)
        return vstream, astream, {}
    @commands.command(description='Blur the video. Use a value between 1 and 127.', pass_context=True)
    async def blur(self, ctx, radius : float = 10): # supposed to be int lmao
        radius = max(1, min(radius, 127))
        await video_creator.apply_filters_and_send(ctx, self._blur, {'radius':radius})
    

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


    async def _contrast(self, ctx, vstream, astream, kwargs):
        vstream = vstream.filter('eq', **kwargs)
        return vstream, astream, {}
    @commands.command(description='Increase/decrease contrast', pass_context=True)
    async def contrast(self, ctx, contrast : float = 10):
        contrast = max(-1000, min(contrast, 1000))
        await video_creator.apply_filters_and_send(ctx, self._contrast, {'contrast':contrast})
    

    async def _edges(self, ctx, vstream, astream, kwargs):
        vstream = vstream.filter('edgedetect', low=0.1, mode='wires')
        return (vstream, astream, {})
    @commands.command(description="Show only the edges in the video.")
    async def edges(self, ctx):
        await video_creator.apply_filters_and_send(ctx, self._edges, {})


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
    

    async def _extract(self, ctx, vstream, astream, kwargs):
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
    @commands.command(description='Extract a portion of the video. Example: !extract 0:13 1:27.3 to get the clip between 13 seconds and 1 minute 27.3 seconds. You can also use start and end (examples: !extract start 1:27.3 and !extract 0:13 end)')
    async def extract(self, ctx, start : str = 'default', end : str = 'default'):
        sec_regex = r'[0-9]+(\.[0-9]+)?'
        min_regex = r'[0-9][0-9]?\:[0-9][0-9](\.[0-9]+)?'
        start_regex = '|'.join((r'start', sec_regex, min_regex))
        end_regex = '|'.join((r'end', sec_regex, min_regex))
        if(start == 'default'): # No arguments provided...
            return
        if(start == 'start' and (end == 'default' or end == 'end')): # Abort if extracting start to end
            return
        # Abort if arguments aren't the valid
        if(re.match(start_regex, start) is None or re.match(end_regex + r'|default', end) is None):
            return
        
        # None = start/end of video
        if(end == 'default'): # If only one argument provided, make it extract starting from the beginning
            end = start
            start = None
        else:
            if(start == 'start'):
                start = None
            if(end == 'end'):
                end = None

        await video_creator.apply_filters_and_send(ctx, self._extract, {'start':start, 'end':end})
    

    async def _fps(self, ctx, vstream, astream, kwargs):
        vstream = vstream.filter('fps', **kwargs)
        return vstream, astream, {}
    @commands.command(description='Change the FPS. default is 15fps', pass_context=True)
    async def fps(self, ctx, framerate=15):
        await video_creator.apply_filters_and_send(ctx, self._fps, {'fps':framerate})
    

    async def _gamma(self, ctx, vstream, astream, kwargs):
        vstream = vstream.filter('eq', **kwargs)
        return vstream, astream, {}
    @commands.command(description='Increase/decrease gamma', pass_context=True)
    async def gamma(self, ctx, gamma : float = 1.3):
        gamma = max(0.1, min(gamma, 10))
        await video_creator.apply_filters_and_send(ctx, self._gamma, {'gamma':gamma})

        
    async def _hue(self, ctx, vstream, astream, kwargs):
        vstream = vstream.filter('hue', **kwargs)
        return vstream, astream, {}
    @commands.command(description='Adjust hue', pass_context=True)
    async def hue(self, ctx, degrees : str):
        await video_creator.apply_filters_and_send(ctx, self._hue, {'h':degrees})


    async def _invert(self, ctx, vstream, astream, kwargs):
        vstream = vstream.filter('negate')
        return vstream, astream, {}
    @commands.command(description='Invert the colors', pass_context=True)
    async def invert(self, ctx):
        await video_creator.apply_filters_and_send(ctx, self._invert, {})
    @commands.command(description='Invert the colors', pass_context=True)
    async def negate(self, ctx):
        await self.invert(ctx)
    @commands.command(description='Invert the colors', pass_context=True)
    async def negative(self, ctx):
        await self.invert(ctx)
    @commands.command(description='Invert the colors', pass_context=True)
    async def inverse(self, ctx):
        await self.invert(ctx)


    async def _lagfun(self, ctx, vstream, astream, kwargs):
        vstream = vstream.filter('lagfun', **kwargs)
        return vstream, astream, {}
    @commands.command(description='Make lighter pixels leak into next frames. Use a value between 0 and 1. Value of 1 makes nothing ever fade away.')
    async def lagfun(self, ctx, decay : float = 0.99):
        decay = max(0, min(decay, 1.0))
        await video_creator.apply_filters_and_send(ctx, self._lagfun, {'decay':decay})
    

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


    async def _saturation(self, ctx, vstream, astream, kwargs):
        vstream = vstream.filter('hue', **kwargs)
        return vstream, astream, {}
    @commands.command(description='Increase/decrease saturation', pass_context=True)
    async def saturation(self, ctx, saturation : float = 10):
        saturation = max(-10, min(saturation, 10))
        await video_creator.apply_filters_and_send(ctx, self._saturation, {'s':saturation})
    @commands.command(description='Increase/decrease saturation', pass_context=True)
    async def saturate(self, ctx, saturation : float = 10):
        await self.saturation(ctx, saturation)
    

    async def _scale(self, ctx, vstream, astream, kwargs):
        vstream = (
            vstream
            .filter('scale', **kwargs)
            .filter('setsar', r='1:1')
        )
        return vstream, astream, {}
    @commands.command(description='Resize the video. Default is 360x270', pass_context=True)
    async def scale(self, ctx, w : str = '360', h : str = '270'):
        if(w == 'auto' and h == 'auto'):
            return
        
        if(w != 'auto'):
            w = min(1240, max(int(w), 50))
        else:
            w = -2

        if(h != 'auto'):
            h = min(1240, max(int(h), 50))
        else:
            h = -2

        await video_creator.apply_filters_and_send(ctx, self._scale, {'w':w, 'h':h})
    

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
    

    async def _volume(self, ctx, vstream, astream, kwargs):
        astream = astream.filter('volume', **kwargs)
        return vstream, astream, {}
    @commands.command(description='Increase video volume.', pass_context=True)
    async def volume(self, ctx, volume_db : float):
        await video_creator.apply_filters_and_send(ctx, self._volume, {'volume':volume_db, 'precision': 'fixed'})    


    async def _wobble(self, ctx, vstream, astream, kwargs):
        astream = astream.filter('chorus', delays='80ms', decays=1, depths=4, **kwargs)
        return vstream, astream, {}
    @commands.command(description='Wobbly sound. Default speed is 8', pass_context=True)
    async def wobble(self, ctx, speed : str = '8'):
        await video_creator.apply_filters_and_send(ctx, self._wobble, {'speeds':speed})




    async def _filter(self, ctx, vstream, astream, kwargs):
        commands = kwargs['commands']
        output_kwargs = {'vsync':0}
        output_arg_names = {
            'output_fs':'fs'
        }

        for command in commands:
            filter_name = command[0]
            filter_args = command[1:]
            filter_args_kwargs = {}
            for arg in filter_args:
                arg_name, arg_val = arg.split('=',1)
                if(arg_name in output_arg_names):
                    output_kwargs[output_arg_names[arg_name]] = arg_val
                else:
                    filter_args_kwargs[arg_name] = arg_val

            if(filter_name in self.v_filters):
                vstream = vstream.filter(filter_name, **filter_args_kwargs)
            elif(filter_name in self.a_filters):
                astream = astream.filter(filter_name, **filter_args_kwargs)

        return (vstream, astream, output_kwargs)
    @commands.command(description="Apply most filters available in in ffmpeg 4.2.2. https://ffmpeg.org/ffmpeg-filters.html")
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








    
        

def setup(bot):
    bot.add_cog(Filter(bot))
