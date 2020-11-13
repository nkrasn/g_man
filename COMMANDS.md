Some commands may be listed as having multiple names, this means you can call the command in multiple ways.<br>
Example: `!saturate 5` can also be sent as `!saturation 5`<br><br>
# Bitrate
| Command | Format | Min/Max Values | Description | Examples |
| --- | --- | --- | --- | --- |
| vb | `!vb <bitrate>` | `8000 to 200000` | Set the video bitrate. | `!vb 30000` |
| ab | `!ab <bitrate>` | `8000 to 200000` | Set the audio bitrate. | `!ab 50000` |
| b | `!b <video_bitrate> <audio_bitrate>` | video_bitrate: `8000 to 200000`<br>audio_bitrate: `8000 to 200000` | Set the video and audio bitrate. | `!b 30000 50000` |
<br>

# Filters
| Command | Format | Min/Max Values | Description | Examples |
| --- | --- | --- | --- | --- |
| amplify | `!amplify <amount> <radius>` | amount: `0 to 65535`<br>radius: `1 to 63` | Makes pixels more colorful the more they change. A higher \<factor\> makes the pixels more colorful, with a default value of 6.<br><br>OPTIONAL: \<radius\> determines how many adjacent frames each frame looks at to consider how much a pixel has changed by. By default the value is 1.<br><br>NOTE: a higher \<radius\> causes more frames to drop at the start and end of the video. | `!amplify 15`<br><br>`!amplify 15 30`
| audioswap | `!audioswap` | | Swap the audio in the second to most recent video with the audio from the most recent video. | `!audioswap` |
| backwards | `!backwards` | | Reverse the video. | `!backwards` |
| blur | `!blur <amount>` | `1 - 127` | Blur the video. \<amount\> represents the radius of the blur around each pixel. | `!blur 10` |
| brightness | `!brightness <amount>` | `-1 to 1` | Adjust the brightness of a video. | `!brightness 2` |
| concat<br>merge | `!concat` | | Combine the two most recently sent videos. Most recent video will be played after the second to most recent. | `!concat` |
| contrast | `!contrast <amount>` | `-1000 to 1000` | Change the video's contrast. | `!contrast 2` |
| equalize<br>equalizer | `!equalize <b1> <b2> ... <b17> <b18>` | `0 to inf` | 18 band equalizer. More information here: https://ffmpeg.org/ffmpeg-filters.html#superequalizer<br>You can provide a number for each frequency band. If you don't provide a value, or set a value as -1, it is set to a random number between 0 and 20. | `!equalize 10 10 -1 5 5 0 0` |
| extract<br>trim | `!extract <start_time> <end_time>` | | Extract a clip between \<start_time\> and \<end_time\>. An example of a \<start_time\> or \<end_time\> value is 1:27.3 (1 minute and 27.3 seconds) or 0:02 (2 seconds). You can also use `start` and `end` as a value to represent 0:00 and the end of the video. | `!extract start 0:03.4`
| fps | `!fps <framerate>` | `1 to 60` | Set the framerate of the video. | `!fps 15` |
| gamma | `!gamma <amount>` | `0.1 to 10` | Change the video's gamma. | `!gamma 1.2` |
| hue | `!hue <degrees>` | `-inf to inf` | Change the video's hue. | `!hue 180` |
| invert<br>inverse<br>negate<br>negative | `!invert` | | Invert the video's colors. | `!invert` |
| lagfun | `!lagfun <amount>` | `0 to 1` | Makes darker pixels update slower. This can create an interesting smearing effect with lighter pixels. A higher \<amount\> makes the smearing last longer, with a value of 1 causing bright colors to never disappear. Values close to 0.96 very noticable results. | `!lagfun 0.99` |
| loop | `!loop <amount>` | `2 to 20` | Loop the video. | `!loop 5` |
| saturate<br>saturation | `!saturate <amount>` | `-10 to 10` | Saturate the video. | `!saturate 2` |
| scale | `!scale <width> <height>` | `50 to 1240` | Scale the video. You can maintain aspect ratio by setting \<width\> or \<height\> to auto. By default, \<width\>=360 and \<height\>=270. | `!scale 640 auto` |
| speed | `!speed <amount>` | `0.05 to inf` | Change the speed of the video. | `!speed 2` |
| volume | `!volume <amount>` | `-inf to inf` | Increase/decrease volume. A value of 1 does no change. | `!volume 5` |
| wobble | `!wobble <frequency>` | `More than 0` | Make the audio wobbly. | `!wobble 15` |
<br>

# Fun effects
| Command | Format | Min/Max Values | Description | Examples |
| --- | --- | --- | --- | --- |
| americ | `!americ` | | Replaces the video's audio with "Never Meant" by American Football. | `!americ` |
| cartoony<br>cartoon | `!cartoony` | | Makes the video look more cartoony. | `!cartoony` |
| demonize | `!demonize` | | Makes the video look and sound more scary. | `!demonize` |
| hypercam | `!hypercam` | | Add an Unregistered Hypercam 2 watermark. | `!hypercam` |
| ifunny | `!ifunny` | | Add an iFunny watermark. | `!ifunny` |
| pingpong | `!pingpong` | | Plays the video, then plays it in reverse. | `!pingpong` |
| rainbow | `!rainbow <speed>` | `-inf to inf` | Makes the hue change over time, creating a rainbow effect. By default it's 360 degrees per second, you can multiply this speed by \<speed\>. | `!rainbow 2` |
| text | `!text <top_text>|<bottom_text>` | | Adds captions to the top and bottom of the video. You separate \<top_text\> and \<bottom_text\> with a pipe symbol `|`. | `!text this will be on top|and this will be on the bottom`<br><br>`!text this will only be on top`<br><br>`!text |this will only be on the bottom` |
| tutorial | `!tutorial <top_text>|<bottom_text>` | | Converts the video into an old-school YouTube tutorial made with Windows Movie Maker. You can customize the title screen's \<top_text\> and \<bottom_text\> the same way you would with the !text command. If no top text is provided, a randomized title is chosen. If no bottom text is provided, "By your_username" is chosen. | `!tutorial how to download google chrome|working 2010` |
<br>

# Advanced
Some of these advanced features can be a little buggy at the moment.
* Some commands can use expressions/timeline editing variables from FFMPEG. More information here: https://ffmpeg.org/ffmpeg-filters.html#Timeline-editing<br>
This means you can recreate the rainbow effect with the command `!hue t*360`
* You can use most FFMPEG filters with the `!filter` command.
    * Format: `!filter <type> <filter_name> <filter_args>`
        * `<type>`: `v` for video filter, `a` for audio filter
        * `<filter_name>`: the name of the filter 
        * `<filter_args>`: a list of arguments for the filter. Each argument is separated by a space, and arguments are formatted as `arg_name=value`
    * Examples:
        * `!filter v edgedetect low=0.1 mode=wires`
        * `!filter a volume volume=10 enable=gte(t,4)`
