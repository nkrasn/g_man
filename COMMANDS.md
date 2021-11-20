Run any of these commands, and the most recently posted video will be edited. Videos can be a link (youtube, twitter, and discord supported) or a direct upload.<br>

Command parameters surrounded by <> are required, [] are optional.

Some commands may be listed as having multiple names, this means they are the same command.<br>
Example: `!saturate 5` is the same as `!saturation 5`<br>

If you run `!help` with the bot, a link to this page will be sent.<br>
If you run `!help <command_name>`, the bot will display command details for `<command_name>` using the information here.<br><br>

# Bitrate
_Note_: You can use `k` for kilobits in your parameters. Examples: `4.3k` instead of `4300`, `25k` instead of `25000`.
| Command | Format | Min/Max Values | Description | Examples |
| --- | --- | --- | --- | --- |
| vb | `!vb <bitrate>` | `1000 to 200000` | Set the video bitrate. | `!vb 30k` |
| ab | `!ab <bitrate>` | `1000 to 200000` | Set the audio bitrate. | `!ab 50k` |
| b | `!b <video_bitrate> <audio_bitrate>` | video_bitrate: `1000 to 200000`<br>audio_bitrate: `1000 to 200000` | Set the video and audio bitrate. | `!b 30k 50k` |
<br>

# Filters
| Command | Format | Min/Max Values | Description | Examples |
| --- | --- | --- | --- | --- |
| amplify | `!amplify [amount] [radius]` | amount: `0 to 65535`<br><br>radius: `1 to 63` | Makes pixels more colorful the more they change. A higher `[amount]` makes the pixels more colorful, with a default value of 6.<br><br>`[radius]` determines how many adjacent frames each frame looks at to consider how much a pixel has changed by. By default the value is 1.<br><br>NOTE: a higher `[radius]` causes more frames to drop at the start and end of the video. | `!amplify 15`<br><br>`!amplify 15 30`
| audioblend<br>audiomerge | `!audioblend` | | Blends the audio in the second to most recent video with the audio from the most recent video. | `!audioblend` |
| audioswap | `!audioswap` | | Swaps the audio in the second to most recent video with the audio from the most recent video. | `!audioswap` |
| backwards<br>reverse | `!backwards` | | Reverses the video. | `!backwards` |
| bassboost | `!bassboost [treble_amount]` | `1 to 18` | Makes the audio bass boosted and loud. If you need more treble, increase `[treble_amount]` (by default it's 1). | `!bassboost`<br><br>`!bassboost 4` |
| bitcrush | `!bitcrush [samples] [bits]` | `1 to inf`<br>`1 to inf` | Bitcrushes the audio. By default, `[samples]` is 32 and `[bits]` is 2. Higher values make a more crushed sound. | `!bitcrush`<br><br>`!bitcrush 64`<br><br>`!bitcrush 8 8` |
| blur | `!blur <amount>` | `1 - 127` | Blurs the video. `[amount]` represents the radius of the blur around each pixel, with a default of 10. | `!blur`<br><br>`!blur 15` |
| brightness | `!brightness [amount]` | `-1 to 1` | Adjusts the brightness of a video, with a default `[amount]` of 1. | `!brightness`<br><br>`!brightness 0.5` |
| concat<br>merge | `!concat` | | Combines the two most recently sent videos. Most recent video will be played after the second to most recent. Video resolution will be the smallest width and height of both videos. | `!concat` |
| contrast | `!contrast [amount]` | `-1000 to 1000` | Changes the video's contrast, with a default `[amount]` of 10. | `!contrast`<br><br>`!contrast 2` |
| edges | `!edges` | | Shows only the edges in the video. | `!edges` |
| equalize<br>equalizer | `!equalize [b1] [b2] ... [b17] [b18]` | `0 to inf` | 18 band equalizer. More information here: https://ffmpeg.org/ffmpeg-filters.html#superequalizer<br>You can provide a number for each frequency band. If you don't provide a value, or set a value as -1, it is set to a random number between 0 and 20. | `!equalize`<br><br>`!equalize 10 10 -1 5 5 0 0` |
| extract | `!extract <start_time> <end_time>`<br><br>`!extract <duration>` | | Extracts the clip between `<start_time>` and `<end_time>`. Time can be specified in seconds (ex: `5` or `7.1`) or minutes:seconds (ex: `0:03` or `1:24.8`). You can also use `start` or `end` to specify the start or end of the video.<br><br>A shortcut for extracts starting at 0 is to provide just one number as a `<duration>`, meaning `!extract 0 1:15` is the same as `!extract 1:15`.<br><br>Secret trick: you can do `!extract 5 10 as really cool video` to extract between 5 and 10 seconds, save the extraction as "really cool video" to your bookmarks, and repost the original video. | `!extract 5`<br><br>`!extract 5 10`<br><br>`!extract 30 1:00`<br><br>`!extract 5 end` |
| fps | `!fps [framerate]` | `1 to 60` | Sets the framerate of the video, with a default of 15. | `!fps`<br><br>`!fps 24` |
| gamma | `!gamma [amount]` | `0.1 to 10` | Changes the video's gamma, with a default of 1.3. | `!gamma`<br><br>`!gamma 1.2` |
| greenscreen | `!greenscreen [color] [sensitivity]` | sensitivity: `0 to 0.99` | Uses the second to most recent video as a greenscreen and place it on top of the most recent video. Without any parameters, `#00FF00` is used as the greenscreen `[color]`, and 0.7 as the `[sensitivity]`.<br><br>`[color]` can be specified as a hexcode starting with #, or as the name of a color (see https://ffmpeg.org/ffmpeg-utils.html#Color).<br><br>`[sensitivity]` specifies how similar a pixel has to be to `[color]` to become transparent. | `!greenscreen`<br><br>`!greenscreen #0000ff`<br><br>`!greenscreen LightGreen 0.9` |
| hue | `!hue [degrees]` | `-inf to inf` | Changes the video's hue, with a default of 180. | `!hue`<br><br>`!hue 180` |
| interpolate | `!interpolate [fps]` | `1 to 30` | Sets the video's framerate to `[fps]`, then interpolate to a high framerate. Default `[fps]` is 5. | `!interpolate`<br><br>`!interpolate 10` |
| invert<br>inverse<br>negate<br>negative | `!invert` | | Inverts the video's colors. | `!invert` |
| lagfun | `!lagfun [amount]` | `0 to 1` | Makes darker pixels update slower. This can create an interesting smearing effect with lighter pixels. A higher `[amount]` makes the smearing last longer, with a value of 1 causing bright colors to never disappear. Values close to 0.96 create very noticable results. Default value is 0.96. | `!lagfun`<br><br>`!lagfun 0.99` |
| loop | `!loop [amount]` | `2 to 20` | Loops the video, default `[amount]` is 2 times. | `!loop`<br><br>`!loop 5` |
| nervous | `!nervous [radius]` | `2 to 512` | Randomizes frame positions. Each frame is shuffled with a frame that is at most `[radius]` frames away, with a default of 30. | `!nervous`<br><br>`!nervous 5` |
| pitch | `!pitch [amount]` | `More than 0` | Multiplies the pitch by `[amount]`, with a default of 2. There is also a `!semitone` command to offset the pitch by a number of semitones. | `!pitch`<br><br>`!pitch 0.5` |
| retro | `!retro [color_count]` | `1 to 255` | Reduces the number of colors in the video by making each RGB channel have `[color_count]` shades, with a default of 4.<br><br>Note that this doesn't reduce the total number of possible colors to `[color_count]`. Example: `[color_count]`=4 makes red have 4 shades, green have 4 shades, and blue have 4 shades, meaning there's actually 64 possible colors. | `!retro`<br><br>`!retro 2` |
| rotate | `!rotate [radians]` | `-inf to inf` | Rotates the video by `[radians]` radians. Default value is `t`.<br><br>You can use expressions supported by FFMPEG to create an animated rotation. See https://ffmpeg.org/ffmpeg-utils.html#Expression-Evaluation | `!rotate`<br><br>`!rotate PI/2`<br><br>`!rotate t`<br><br>`!rotate PI/8 * sin(t)` |
| rotatedeg | `!rotatedeg [degrees]` | `-inf to inf` | Rotates the video by `[degrees]` degrees. Default value is 45 degrees.<br>Expressions are not supported, see `!rotate` if you wish to use them. | `!rotatedeg`<br><br>`!rotatedeg 180` |
| saturate<br>saturation | `!saturate [amount]` | `-10 to 10` | Saturates the video, with a default `[amount]` of 10. | `!saturate 2` |
| scale<br>size | `!scale [width] [height]` | `50 to 1240` | Scales the video. You can preserve the aspect ratio by setting `[width]` or `[height]` to auto. By default, `[width]` is 480 and `<height>` is auto. | `!scale 640 480`<br><br>`!scale 240`<br><br>`!scale auto 720` |
| scroll | `!scroll [horizontal] [vertical]` | `-100 to 100` | Makes the video scroll with a default `[horizontal]` speed of 1 and `[vertical]` speed of 0. Speed describes how much of the video should scroll every frame (example: horizontal speed of 5 = video scrolls horizontally by 5% of its width every frame). | `!scroll`<br><br>`!scroll 5`<br><br>`!scroll 0 4` |
| semitone | `!semitone [semitone]` | `-inf to inf` | Same as `!pitch`, except pitch offset is specified in semitones. Default `[semitone]` value is 12. | `!semitone`<br><br>`!semitone 7` |
| shader | `!shader <x_equation> <y_equation>` | `Any valid equation works` | Advanced command that is a shortcut for the geq filter in FFMpeg. This command is equivalent to running `!filter geq r=r(x_equation,y_equation) g=g(x_equation,y_equation) b=b(x_equation,y_equation)` | `!shader mod(X+T*3,W) mod(Y+20*sin(T*5),H)`<br><br>`!shader X+20*sin(T*5+X*0.01) Y+20*cos(T*5+Y*0.01)` |
| speed | `!speed [amount]` | `0.05 to inf` | Changes the speed of the video, with a default of 2. | `!speed`<br><br>`!speed 0.5`<br><br>`!speed 1/2` |
| volume | `!volume [amount]` | `-inf to inf` | Increases/decreases the volume. A value of 1 has no change. Default value is 2. | `!volume`<br><br>`!volume 5` |
| wobble | `!wobble [frequency]` | `More than 0` | Makes the audio wobbly, with a default `[frequency]` of 8. | `!wobble`<br><br>`!wobble 15` |
| zoom | `!zoom [zoom_amount]` | `1 to 8` | Zooms in the video, with a default value of 2. | `!zoom`<br><br>`!zoom 1.5` |
<br>

# Corruption
| Command | Format | Min/Max Values | Description | Examples |
| --- | --- | --- | --- | --- |
| corrupt | `!corrupt [intensity]` | `0 to 1` | Sets random bytes in the video file to a random number, with a default `[intensity]` of 0.5. | `!corrupt`<br><br>`!corrupt 0.7` |
| faketime | `!faketime [type]` | | Corrupts the duration data. This can make videos look like they have an extremely long, negative, or perpetually increasing duration. A random one is chosen if `[type]` isn't specified.<br><br>Possible values for `[type]`:<br>- `long`: Duration appears as 357913994:07.<br>- `negative`: Duration appears as -16.<br>- `increasing`: Duration keeps increasing.<br>- `random`: Randomize the duration data. This is unstable and can actually shorten the video, it won't be chosen if you don't provide a `[type]`. | `!faketime`<br><br>`!faketime long`<br><br>`!faketime negative`<br><br>`!faketime increasing`<br><br>`!faketime random`
| mosh | `!mosh [max_iframe_interval]` | `2 to inf`<br> | Datamoshes the video. Maximum distance between iframes can be set with `[max_iframe_interval]`, by default it's 30. | `!mosh`<br><br>`!mosh 15` |
| rearrange | `!rearrange [intensity]` | `0 to 1` | Swaps random chunks of bytes in the video. A higher `[intensity]` does more swaps and makes the chunks longer, default is 0.5. | `!rearrange`<br><br>`!rearrange 0.4` |
| smear | `!smear` | | Makes a cool smearing effect, using `tomato.py`. | `!smear` |
| stutter | `!stutter` | | Repeats random chunks of bytes back-to-back in various places. A bit like `!smear`, but not as smooth. | `!stutter` |
<br>

# Fun effects
| Command | Format | Min/Max Values | Description | Examples |
| --- | --- | --- | --- | --- |
| americ | `!americ` | | Replaces the video's audio with "Never Meant" by American Football. | `!americ` |
| cartoony<br>cartoon | `!cartoony` | | Makes the video look more cartoony. | `!cartoony` |
| deepfry | `!deepfry` | | Deepfries the video. | `!deepfry` |
| demonize | `!demonize` | | Makes the video look and sound more scary. | `!demonize` |
| harmonize | `!harmonize [semitones]` | `-inf to inf` | Mixes pitched versions of the audio, pitches determined by how many `[semitones]` you want the original audio off by. If you don't provide a list of `[semitones]`, a random selection will be used.<br><br>For example, `!harmonize 4 7` mixes the original audio with versions that are 4 semitones higher and 7 semitones higher (AKA a major chord).  | `!harmonize`<br><br>`!harmonize -12`<br><br>`!harmonize 4 3 10` |
| harmonizedeep | `!harmonizedeep [semitones]` | `-inf to inf` | More chaotic version of !harmonize where the pitch of the last mix is adjusted rather than the original video. If you don't provide a list of `[semitones]`, a random selection will be used.<br><br>Difference between this and !harmonize becomes apparent when two pitches are provided, and gets more noticable as more `[semitones]` are added.<br><br>Example: `!harmonizedeep 3 7 -12` is the same as running these three commands in order: `!harmonize 3`, `!harmonize 7`, `!harmonize 12`. | `!harmonizedeep`<br><br>`!harmonizedeep -12 12`<br><br>`!harmonizedeep 3 7 10` |
| histogram | `!histogram` | | Converts the video into a histogram of the audio volume. | `!volume` |
| hypercam | `!hypercam` | | Adds an Unregistered Hypercam 2 watermark. | `!hypercam` |
| ifunny | `!ifunny` | | Adds an iFunny watermark. | `!ifunny` |
| mahna<br>mahnamahna | `!mahna` | | Replaces the video's audio with "Mah Na Mah Na" from the Muppets soundtrack. | `!mahna` |
| pingpong | `!pingpong` | | Plays the video, then plays it in reverse. | `!pingpong` |
| rainbow | `!rainbow [speed]` | `-inf to inf` | Makes the hue change over time, creating a rainbow effect. Default `[speed]` is 1. | `!rainbow`<br><br>`!rainbow 2` |
| tetris | `!tetris` | | Replaces the video's audio with the vocoded version of tetris beatbox. | `!tetris` |
| text | `!text [top_text]\|[bottom_text]` | | Adds captions to the top and bottom of the video. You separate `[top_text]` and `[bottom_text]` with a pipe symbol `\|`. | `!text this will be on top\|and this will be on the bottom`<br><br>`!text this will only be on top`<br><br>`!text \|this will only be on the bottom` |
| trippy | `!trippy [speed] [blend_mode]` | speed: `0.5 to 1` | Overlays and blends a slowed down version of the video on top of itself. You can control the `[speed]` of the overlay, by default it's 0.97.<br><br>`[blend_mode]` specifies how the videos blend together, by default it's set to `average`. A full list of blend modes can be found here: https://ffmpeg.org/ffmpeg-filters.html#blend-1 | `!trippy`<br><br>`!trippy 0.7`<br><br>`!trippy 0.8 xor` |
| tutorial | `!tutorial [top_text]\|[bottom_text]` | | Converts the video into an old-school YouTube tutorial made with Windows Movie Maker. You can customize the title screen's `[top_text]` and `[bottom_text]` the same way you would with the !text command. If no top text is provided, a randomized title is chosen. If no bottom text is provided, "By your_username" is chosen. | `!tutorial how to download google chrome\|working 2010` |
| vintage | `!vintage` | | Makes the video look like an old movie. | `!vintage` |
<br>

# Bookmarks
You can bookmark videos and load them in any server with g_man. Bookmark labels can only contain letters, numbers, and spaces.
| Command | Format | Min/Max Values | Description | Examples |
| --- | --- | --- | --- | --- |
| save<br>store | `!save [label]` | | Saves the most recent video to your bookmarks with the name `[label]`. You can also save a video with a blank `[label]`, which is useful as a temporary bookmark. | `!save really good video`<br><br>`!save` |
| load<br>use | `!load [label]` | | Loads a video from your bookmarks with the name `[label]`. | `!load really good video`<br><br>`!load` |
| delete<br>remove | `!delete <label>` | | Deletes a video from your bookmarks with the name `<label>`. | `!delete really good video` |
| bookmarks | `!bookmarks` | | Shows all your bookmarks. | `!bookmarks` |
<br>

# Utility
| Command | Format | Min/Max Values | Description | Examples |
| --- | --- | --- | --- | --- |
| download<br>fix | `!download` | | Downloads the last video sent and sends it as an MP4. Useful for downloading youtube/twitter videos and fixing videos Discord has trouble playing. | `!download` |
| gif | `!gif [fps]` | `1 to 24` | Converts the video to a GIF. Default `[fps]` is 24, consider lowering this number or scaling the video down if the GIF gets cut off. | `!gif`<br><br>`!gif 12`|
| mp3 | `!mp3` | | Converts the video to an mp3. | `!mp3`|
| swap | `!swap` | | Swaps the last two videos sent, simply by reposting the second to last video. | `!swap` |
| time<br>timestamp | `!time [speed]` | `0.05 to inf` | Draws a timestamp on the video to help you figure out when to `!extract`. You can set a lower `[speed]` for the video to help with precise timing.<br><br>NOTE: The video created by this command is ignored by g_man! This is so you don't have to run `!swap` or `!undo` afterwards in order to `!extract` from the original video. | `!time`<br><br>`!time 0.5` |
| undo | `!undo` | | Deletes the last video sent. | `!undo` |

# Advanced
## !filter command
EXPERIMENTAL: You can apply almost any filter from FFMPEG using the !filter command. At the moment, filters requiring two or more videos will not work.<br> You can get a link to all the filters in FFMPEG by typing `!filter help`.
* Format: `!filter <filter_name> <filter_args>`
* `<filter_args>` are formatted in this way: `arg1_name=arg1_value arg2_name=arg2_value ...`
* Examples:
    * `!filter aecho`
    * `!filter edgedetect low=0.1 mode=wires`
    * `!filter drawtext text="g_man was here" x="(main_w-tw)/2" y="(main_h-th)/2 + 100*sin(t*6)" fontsize=50`
* Multiple filters can be applied with one message by simply appending another `!filter <filter_name> <filter_args>`
* Examples:
    * `!filter reverse !filter areverse`
    * `!filter eq contrast=1.2 !filter hue h=60 enable=gte(t,3) !filter negate`
