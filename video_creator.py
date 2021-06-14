import asyncio
import discord
import ffmpeg
from ffprobe import FFProbe
import media_cache
import os
import traceback

loading_emotes = [
    '\U0001F1EC',
    '\U0001F1F2',
    '\U0001F1E6',
    '\U0001F1F3'
]
async def set_progress_bar(message, idx):
    await message.add_reaction(loading_emotes[idx])

async def print_ffmpeg_error(ctx, e):
    err_full = str(e.stderr.decode('utf8'))
    err = err_full.split('\n')
    friendlier_err = ''
    for line in err:
        if(line.startswith('[') and 'Copyleft' not in line):
            friendlier_err += '* ' + line[line.rfind(']')+2:] + '\n'
    if(len(friendlier_err) > 1800):
        friendlier_err = friendlier_err[:1800]
    await ctx.send(f"An error occurred :( ```{friendlier_err}```\nIf the error doesn't make sense, try scaling the video(s) down using `!scale 480` and try again.")
    print(err_full)

# Download the video, then wrap the filter code in a try catch statement
async def apply_filters_and_send(ctx, code, kwargs):
    await set_progress_bar(ctx.message, 0)
    input_vid, is_yt, result = await media_cache.download_last_video(ctx)
    if(not result):
        await ctx.send("There was an error downloading the video, try uploading the video again.")
        return
    await set_progress_bar(ctx.message, 1)

    is_mp3 = False
    is_gif = False
    is_ignored_mp4 = False
    if('is_mp3' in kwargs):
        is_mp3 = kwargs['is_mp3']
    if('is_gif' in kwargs):
        is_gif = kwargs['is_gif']
    if('is_ignored_mp4' in kwargs):
        is_ignored_mp4 = kwargs['is_ignored_mp4']
    kwargs['input_filename'] = input_vid
                
    output_filename = f'vids/{ctx.message.id}.'
    if(is_mp3):
        output_filename += 'mp3'
    elif(is_gif):
        output_filename += 'gif'
    elif(is_ignored_mp4): # Regular mp4, but not recorded in the database
        output_filename += '_ignore.mp4'
    else:
        output_filename += 'mp4'
    
    async with ctx.typing():
        try:
            input_stream = ffmpeg.input(input_vid)
            vstream = input_stream.video
            astream = input_stream.audio
            vstream, astream, output_params = await code(ctx, vstream, astream, kwargs)
            if('fs' in output_params):
                del output_params['fs']
            if('movflags' not in output_params):
                output_params['movflags'] = 'faststart'
            await set_progress_bar(ctx.message, 2)

            ffmpeg_output = None
            if(is_mp3):
                ffmpeg_output = ffmpeg.output(astream, output_filename, **output_params)
            elif(is_gif):
                ffmpeg_output = ffmpeg.output(vstream, output_filename, **output_params)
            else:
                ffmpeg_output = ffmpeg.output(astream, vstream, output_filename, **output_params)

            # Pass 1
            try:
                ffmpeg_output.run(cmd='ffmpeg-static/ffmpeg', overwrite_output=True, capture_stderr=True)
            except ffmpeg._run.Error as e:
                # Error will most likely happen due to the video having no audio
                ffmpeg_output = ffmpeg.output(vstream, output_filename, **output_params)
                ffmpeg_output.run(cmd='ffmpeg-static/ffmpeg', overwrite_output=True, capture_stderr=True)

            # Pass 2 (if the file is too big)
            resulting_filesize = os.path.getsize(output_filename) / 1000000
            if(resulting_filesize > 7.9):
                # Calculate bitrate needed
                longest_duration = 0
                metadata = FFProbe(output_filename)
                for stream in metadata.streams:
                    if(stream.is_video() or stream.is_audio()):
                        duration = stream.duration_seconds()
                        longest_duration = max(longest_duration, duration)
                output_params['b:v'] = 7500000 / longest_duration

                # Create the new video
                input_filename_pass2 = 'vids/pass2' + output_filename.split('/')[1]
                os.rename(output_filename, input_filename_pass2)
                input_stream = ffmpeg.input(input_filename_pass2)
                ffmpeg.output(input_stream, output_filename, **output_params).run(cmd='ffmpeg-static/ffmpeg', overwrite_output=True, capture_stderr=True)
                os.remove(input_filename_pass2)


            await set_progress_bar(ctx.message, 3)
            try:
                await ctx.send(file=discord.File(output_filename))
            except Exception as e:
                resulting_filesize = os.path.getsize(output_filename) / 1000000
                gman_msg = await ctx.send(f"File too big to send ({resulting_filesize} mb)")

        except asyncio.TimeoutError as e:
            await ctx.send(f'Command took to long to execute.\n```\n{str(e)}```')
        # Making errors a little easier to understand
        except ffmpeg.Error as e:
            await print_ffmpeg_error(ctx, e)
        except Exception as e:
            await ctx.send(f'Error:\n```\n{str(e)}```')
            print(traceback.format_exc())

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


# Convert corrupted video to mp4
# Very repetitive, maybe there's a way to combine the two wrappers
async def apply_corruption_and_send(ctx, code, code_kwargs, avi_kwargs = {}, mp4_kwargs = {}):
    await set_progress_bar(ctx.message, 0)
    input_vid, is_yt, result = await media_cache.download_last_video(ctx)
    if(not result):
        await ctx.send("Error downloading the video")
        return
    await set_progress_bar(ctx.message, 1)

    avi_filename = f'vids/{ctx.message.id}.avi'
    output_filename = f'vids/{ctx.message.id}.mp4'
    
    async with ctx.typing():
        try:
            #x264_params = {'x264-params':'keyint=25:min-keyint=25:scenecut=0'}
            (
                ffmpeg
                .input(input_vid)
                .output(avi_filename, fs='7M', **avi_kwargs)#qmin=30, qmax=30, g=2500, keyint_min=2500)#**x264_params)
                .run(cmd='ffmpeg-static/ffmpeg', overwrite_output=True)
            )

            successful_corrupt = True
            try:
                await code(ctx, avi_filename, code_kwargs)
                await set_progress_bar(ctx.message, 2)
            except Exception as e:
                await ctx.send(f'Error while corrupting the video: {e}')
                print(e)
                successful_corrupt = False

            if(successful_corrupt):
                (
                    ffmpeg
                    .input(avi_filename)
                    .output(output_filename, fs='7M', **mp4_kwargs)
                    .run(cmd='ffmpeg-static/ffmpeg', overwrite_output=True, capture_stderr=True)
                )
                await set_progress_bar(ctx.message, 3)
                await ctx.send(file=discord.File(output_filename))
        except asyncio.TimeoutError as e:
            await ctx.send(f'Command took to long to execute.\n```\n{str(e)}```')
        # Making errors a little easier to understand
        except ffmpeg.Error as e:
            await print_ffmpeg_error(ctx, e)
        except Exception as e:
            await ctx.send(f'Error:\n```\n{str(e)}```')
            print(traceback.format_exc())

        # Remove files
        try:
            if(os.path.isfile(avi_filename)):
                os.remove(avi_filename)
        except Exception as e:
            print(e)
        try:
            if(os.path.isfile(output_filename)):
                os.remove(output_filename)
        except Exception as e:
            print(e)
        try:
            os.remove(input_vid)
        except Exception as e:
            print(e)
        await ctx.message.clear_reactions()

    