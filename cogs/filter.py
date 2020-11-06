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

class TimeoutError(Exception):
    pass

def interrupt(a, b):
    raise TimeoutError()

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
    
    def get_randomized_catalog(self):
        random_catalog = {
            'v lagfun': 'decay={}'.format(random.uniform(0.7, 1.0)),
            'v median': 'radius={}'.format(random.randint(1, 10)),
            'v eq': [ 
                'contrast={}'.format(random.uniform(0.5, 3)),
                'saturation={}'.format(random.uniform(0, 3)),
                'gamma={}'.format(random.uniform(0.6, 1.5)),
                'brightness={}'.format(random.uniform(-0.15, 0.15)),
            ],
            'v hue': 'h={}'.format(random.uniform(0, 360)),
            'v fps': 'fps={}'.format(random.randint(3, 30)),
            'v amplify': 'radius={}'.format(random.randint(2, 25)),

            'a volume': 'volume={} precision=fixed'.format(random.uniform(1, 1000)),
            'a chorus': 'delays={}ms decays=1 speeds={} depths=4'.format(random.randint(30, 80), random.randint(6, 30)),
            'a superequalizer': '1b={} 2b={} 3b={} 4b={} 5b={} 6b={} 7b={} 8b={} 9b={} 10b={} 11b={} 12b={} 13b={} 14b={} 15b={} 16b={} 17b={} 18b={}'.format(
                random.uniform(0.5, 20),random.uniform(0.5, 20),random.uniform(0.5, 20),random.uniform(0.5, 20),random.uniform(0.5, 20),
                random.uniform(0.5, 20),random.uniform(0.5, 20),random.uniform(0.5, 20),random.uniform(0.5, 20),random.uniform(0.5, 20),
                random.uniform(0.5, 20),random.uniform(0.5, 20),random.uniform(0.5, 20),random.uniform(0.5, 20),random.uniform(0.5, 20),
                random.uniform(0.5, 20),random.uniform(0.5, 20),random.uniform(0.5, 20),
            ),
        }
        return random_catalog
    
    @commands.command(description='Increase video volume. If you get a filesize of 0, lower the volume!', pass_context=True)
    async def volume(self, ctx, volume_db : float):
        await self.execute_filter(ctx, [['a', 'volume', 'volume={} precision=fixed'.format(volume_db)]])
    
    @commands.command(description='Make lighter pixels leak into next frames more i think not sure. Use a value between 0 and 1. Value of 1 makes nothing ever fade away.')
    async def lagfun(self, ctx, decay : float):
        decay = max(0, min(decay, 1.0))
        await self.execute_filter(ctx, [['v', 'lagfun', 'decay={}'.format(decay)]])

    @commands.command(description='Blur the video. Value is radius of the blur', pass_context=True)
    async def blur(self, ctx, radius : float): # supposed to be int lmao
        await self.execute_filter(ctx, [['v', 'median', 'radius={}'.format(radius)]])
    
    @commands.command(description='Increase/decrease contrast', pass_context=True)
    async def contrast(self, ctx, contrast : float):
        await self.execute_filter(ctx, [['v', 'eq', 'contrast={}'.format(contrast)]])

    @commands.command(description='Increase/decrease saturation', pass_context=True)
    async def saturation(self, ctx, saturation : float):
        await self.execute_filter(ctx, [['v', 'eq', 'saturation={}'.format(saturation)]])

    @commands.command(description='Increase/decrease gamma', pass_context=True)
    async def gamma(self, ctx, gamma : float):
        await self.execute_filter(ctx, [['v', 'eq', 'gamma={}'.format(gamma)]])
    
    @commands.command(description='Increase/decrease brightness', pass_context=True)
    async def brightness(self, ctx, brightness : float):
        await self.execute_filter(ctx, [['v', 'eq', 'brightness={}'.format(brightness)]])

    @commands.command(description='Adjust hue', pass_context=True)
    async def hue(self, ctx, degrees : float):
        await self.execute_filter(ctx, [['v', 'hue', 'h={}'.format(degrees)]])
    
    @commands.command(description='Wobbly sound. Default speed is 20', pass_context=True)
    async def wobble(self, ctx, speed=20.0):
        await self.execute_filter(ctx, [['a', 'chorus', 'delays=80ms decays=1 speeds={} depths=4'.format(speed)]])

    @commands.command(description='Resize the video. Default is 480x360', pass_context=True)
    async def scale(self, ctx, w=480, h=360):
        await self.execute_filter(ctx, [['v', 'scale', 'w={} h={}'.format(w, h)], ['v', 'setsar', 'r=1:1']])
    
    @commands.command(description='Change the FPS. default is 15fps', pass_context=True)
    async def fps(self, ctx, framerate=15):
        await self.execute_filter(ctx, [['v', 'fps', 'fps={}'.format(framerate)]])

    @commands.command(description='Make stuff colorful and sorta deepfried. Value between 4 and 16 is fun', pass_context=True)
    async def amplify(self, ctx, radius : float):
        await self.execute_filter(ctx, [['v', 'amplify', 'radius={}'.format(radius)]])
    
    @commands.command(description='Make stuff look kinda cartoony', pass_context=True)
    async def cartoony(self, ctx):
        await self.execute_filter(ctx, [['v', 'edgedetect', 'low=0.1 high=0.3 mode=colormix']])
    
    @commands.command(description='Invert the colors', pass_context=True)
    async def invert(self, ctx):
        await self.execute_filter(ctx, [['v', 'negate', 'negate_alpha=0']])
    
    @commands.command(description='18-band equalizer. you can pass how high or low you want each band to be, or set to -1 to make it random.', pass_context=True)
    async def equalizer(self, ctx, b1=-1, b2=-1, b3=-1, b4=-1, b5=-1, b6=-1, b7=-1, b8=-1, b9=-1, b10=-1, b11=-1, b12=-1, b13=-1, b14=-1, b15=-1, b16=-1, b17=-1, b18=-1):
        b = [b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15, b16, b17, b18]
        for i in range(len(b)):
            if(b[i] == -1):
                b[i] = random.uniform(0, 20)

        await self.execute_filter(ctx, [['a', 'superequalizer', '1b={} 2b={} 3b={} 4b={} 5b={} 6b={} 7b={} 8b={} 9b={} 10b={} 11b={} 12b={} 13b={} 14b={} 15b={} 16b={} 17b={} 18b={}'.format(
            b[0], b[1], b[2], b[3], b[4], b[5], b[6], b[7], b[8], b[9], b[10], b[11], b[12], b[13], b[14], b[15], b[16], b[17]
        )]])
    
    @commands.command(description='No description needed.', pass_context=True)
    async def demonize(self, ctx):
        effects = []
        #effects.append(['a', 'asetrate', 'r=44100*0.5'])
        #effects.append(['a', 'atempo', 'tempo=2'])
        effects.append(['a', 'chorus', 'delays=80ms decays=1 speeds=20 depths=4'])
        effects.append(['v', 'amplify', 'radius=4'])
        effects.append(['v', 'lagfun', 'decay=0.95'])
        effects.append(['v', 'amplify', 'radius=2'])
        effects.append(['v', 'amplify', 'radius=6'])
        await self.execute_filter(ctx, effects)
    
    @commands.command(description="Apply a bunch of random effects. Provide a number if you want a specific amount of effects, otherwise it's random. Say 'unique' after the number if you don't want to repeat effects.")
    async def randomize(self, ctx, effect_amount: int = -1, is_unique: str = ""):
        if(effect_amount == -1):
            effect_amount = random.randint(3, 10)
        effect_amount = min(40, max(1, effect_amount))
        effects = []

        is_unique = True if is_unique == 'unique' else random.choice([True, False])
        used = set()

        for i in range(effect_amount):
            random_catalog = self.get_randomized_catalog()

            effect_and_category = None
            if(is_unique):
                while(effect_and_category is None or effect_and_category in used):
                    if(len(used) == len(random_catalog)):
                        used = set()
                    effect_and_category = random.choice(list(random_catalog))
                used.add(effect_and_category)
            else:
                effect_and_category = random.choice(list(random_catalog))

            effect_category, effect = effect_and_category.split(' ')
            effect_params = random_catalog[effect_category + ' ' + effect]

            if(type(effect_params) == list):
                effect_params = random.choice(effect_params)
            
            effects.append([effect_category, effect, effect_params])

        print("is unique? " + str(is_unique))
        for eff in effects:
            print(eff)
        await self.execute_filter(ctx, effects)


    @commands.command(description="Reverse the video.")
    async def backwards(self, ctx):
        input_vid, is_yt, result = await image_cache.download_last_video(ctx)
        if(not result):
            await ctx.send("Error downloading the video")
            return
        
        async with ctx.typing():
            try:
                input_stream = ffmpeg.input(input_vid)
                video_stream = input_stream.video
                audio_stream = input_stream.audio

                video_stream = ffmpeg.filter(video_stream, 'reverse')
                audio_stream = ffmpeg.filter(audio_stream, 'areverse')
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
    

    @commands.command(description="Speed the video.")
    async def speed(self, ctx, speed_change : float = 2.0):
        input_vid, is_yt, result = await image_cache.download_last_video(ctx)
        if(not result):
            await ctx.send("Error downloading the video")
            return
        
        speed_change = max(0.05, speed_change)

        async with ctx.typing():
            try:
                input_stream = ffmpeg.input(input_vid)
                video_stream = input_stream.video
                audio_stream = input_stream.audio

                # No issues if we need to change speed by 0.5
                if(speed_change >= 0.5):
                    video_stream = ffmpeg.filter(video_stream, 'setpts', str(1.0/speed_change)+'*PTS')
                    audio_stream = ffmpeg.filter(audio_stream, 'atempo', speed_change)
                # But decreasing by <0.5 doesn't work, so several speed changes are needed
                else:
                    current_speed = 1.0
                    while(current_speed >= speed_change):
                        if(current_speed * 0.5 <= speed_change):
                            video_stream = ffmpeg.filter(video_stream, 'setpts', str(1.0/(speed_change/current_speed))+'*PTS')
                            audio_stream = ffmpeg.filter(audio_stream, 'atempo', speed_change/current_speed)
                            break
                        video_stream = ffmpeg.filter(video_stream, 'setpts', str(2.0)+'*PTS')
                        audio_stream = ffmpeg.filter(audio_stream, 'atempo', 0.5)
                        current_speed *= 0.5

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

    

    @commands.command(description="loop the video.")
    async def loop(self, ctx, amount : int = 2):
        input_vid, is_yt, result = await image_cache.download_last_video(ctx)
        if(not result):
            await ctx.send("Error downloading the video")
            return
        
        amount = max(2, min(20, amount))

        async with ctx.typing():
            try:
                input_stream = ffmpeg.input(input_vid)
                joined_stream = [input_stream.video, input_stream.audio]

                for i in range(amount - 1):
                    #video_stream = ffmpeg.concat(video_stream, input_stream)
                    joined_stream = ffmpeg.concat(joined_stream[0], joined_stream[1], input_stream.video, input_stream.audio, v=1, a=1).node

                (
                    ffmpeg
                    .output(joined_stream[0], joined_stream[1], 'vids/out.mp4', fs='7M')
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

    

            


    @commands.command(description="Apply any video filter that's in ffmpeg 4.2.2. If you are doing a multi-input filter, replace v|a with the last n videos you need to use. Format: !filter v|a|last_n_vids last_n_vids filter_name arg1=0.5 arg2=1.1")
    async def filter(self, ctx, filter_type, filter_name, *, arg_list : str = None):
        if((arg_list is None and not (filter_name == 'reverse' or filter_name == 'areverse' or filter_name == 'earwax'))):
            return
        await self.execute_filter(ctx, [[filter_type, filter_name, arg_list]])
    







    # Run filters
    # effects: [[filter_type, filter_name, param_list], ...]
    async def execute_filter(self, ctx, effects):
        input_vids = []
        input_count = 1
        # not a good way to check if this is single-input
        if(effects[0][0] in 'va'):
            input_vids.append(image_cache.get_from_cache(str(ctx.message.channel.id))[-1])
        # multi-input
        else: 
            input_count = int(effects[0][0])
            for i in range(input_count):
                input_vids.append(image_cache.get_from_cache(str(ctx.message.channel.id))[-(i+1)])

        # Determine if the source should be an attachment or youtube video
        for i in range(len(input_vids)):
            input_vid = input_vids[i]
            #input_vid = image_cache.get_from_cache(str(ctx.message.channel.id))[-1]
            is_yt = False
            if(input_vid is None): # no video found in the channel
                await ctx.send("Didn't find any videos to modify...")
                return
            elif(re.match(image_cache.yt_regex, input_vid) or re.match(image_cache.twitter_regex, input_vid)): # yt video
                is_yt = True
                result, input_vids[i] = await image_cache.yt(ctx, input_vid, str(i))
                if(not result):
                    await ctx.send("Quitting :(")
                    return
        # Determine if the output is video or audio
        out_filename = 'vids/out.'
        only_audio = False
        if(input_vids[0].split('.')[-1] in image_cache.audio_filetypes): # this is broken, audio never worked
            out_filename += 'ogg'
            only_audio = True
        else:
            out_filename += 'mp4'

        #await ctx.send("I will get back to you...")
        #print('\nI will get back to you...\n')
        async with ctx.typing():
            try:
                input_vid = input_vids[0]
                print(input_vid)
                
                in_stream = ffmpeg.input(input_vid)
                out_stream = None

                if(only_audio):
                    a = in_stream
                else:
                    v = in_stream.video
                    a = in_stream.audio
                
                for effect in effects:
                    filter_type = effect[0]
                    filter_name = effect[1]
                    param_list = effect[2]

                    # Create params
                    param_dict = {}
                    param_list = param_list.split(' ')
                    for param in param_list:
                        param = param.split('=')
                        param_dict[param[0]] = param[1]

                    #if(filter_type in 'va'):
                    if(input_count == 1):
                        # Do audio stuff
                        if(filter_type == 'a'):
                            a = a.filter(filter_name, **param_dict)
                        
                        # Do video stuff
                        if(filter_type == 'v' and not only_audio):
                            v = v.filter(filter_name, **param_dict)
                        
                        out_stream = ffmpeg.output(v, a, out_filename, fs='7M')
                    else:
                        # Do multi-input video stuff
                        #input_count = int(filter_type)
                        #input_vids = []
                        #for i in range(input_count):
                        #    input_vids.append(image_cache.get_from_cache(str(ctx.message.channel.id))[-(i+1)])
                        '''
                        for i in range(len(input_vids)):
                            input_vids[i] = ffmpeg.input(input_vids[i])
                        out_stream = ffmpeg.filter(input_vids, filter_name, **param_dict)
                        out_stream = out_stream.output(out_filename)
                        '''
                        in_streams = []
                        in_streams_a = []
                        in_streams_v = []
                        for i in range(len(input_vids)):
                            in_streams.append(ffmpeg.input(input_vids[i]))
                            in_streams_a.append(in_streams[i].audio)
                            in_streams_v.append(in_streams[i].video)
                        mixed_a = ffmpeg.filter(in_streams_a, "amix", **{'inputs': len(in_streams_a)})
                        mixed_v = ffmpeg.filter(in_streams_v, filter_name, **param_dict)
                        out_stream = ffmpeg.output(mixed_v, mixed_a, out_filename, fs='7M')
                        

                out_stream = out_stream.global_args('-loglevel', 'error')
                out_stream = out_stream.global_args('-nostdin')
                ffmpeg.run(out_stream, cmd='ffmpeg4-2-2/ffmpeg', overwrite_output=True)

                await ctx.send(file=discord.File(out_filename))
            except TimeoutError as e:
                await ctx.send('Command took to long to execute.\n```\n' + str(e) + '```')
            except Exception as e:
                await ctx.send('Error:\n```\n' + str(e) + '```')
                print(traceback.format_exc())
            if(is_yt):
                os.remove(input_vid)
        

def setup(bot):
    bot.add_cog(Filter(bot))
