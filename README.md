# g_man
A Discord bot for editing videos, useful for simple edits or making memes. It can apply filters, modify bitrate, and create glitch art. <br>
Filters are applied using FFMPEG, with some corruption commands using tomato.py (https://github.com/itsKaspar/tomato) or AviGlitch (https://github.com/ucnv/aviglitch).

## Features
* Change video and audio bitrate.
* Easily apply various filters such as contrast, blur, volume, etc.
  * For advanced users, there is a !filter command that can apply almost any filter available in FFMPEG.
* Apply premade sequences of filters, such as !tutorial to convert a video into an old-school YouTube tutorial.
* Corrupt videos in various ways, such as datamoshing and modifying random chunks of bytes in the video file.

## Usage
* Send a video to a channel. This can either be a youtube/twitter/cdn.discordapp link, or an uploaded video file.
* Run a command and the bot will reply back with the edited video.

## Commands
https://github.com/nkrasn/g_man/blob/master/COMMANDS.md<br>
You can get this link from within Discord by sending "!help" in a channel

## Requirements
* discord.py with voice support (tested on version 1.5)
* Static build of ffmpeg (version 4.2 or above)
* ffmpeg-python
* youtube_dl
* AviGlitch, see https://github.com/ucnv/aviglitch for installation instructions.

You can install the python packages easily, preferably in a virtual environment, by running
```
pip install -r requirements.txt
```

*Tip:* If you using Mac or Linux, you may have Python 2/Pip 2 preinstalled. You should run:
```
pip3 install -r requirements.txt
```

All other requirements should be install manually.

At the moment, it is required to have a folder called ffmpeg4-2-2 in the root of the bot's directory containing a static build of ffmpeg. Despite the name, any version of ffmpeg at or above 4.2 can be used (folder name will be changed in a future update). <br>

## Installation
* Install all requirements.
* Create the following folders in the bot's root directory, if they don't exist:
  * ffmpeg4-2-2
    * This should contain a static build of ffmpeg.
  * vids
    * This is the output directory for ffmpeg.
  * fonts
    * Drag an Arial .ttf file in here, and any other fontfile you want.
  * tutorial
    * Drag any .mp3 background music you want for the !tutorial command (such as "Trance - 009 Sound System Dreamscape" or "Evanescence - Bring Me to Life")
  * clips
    * Contains any files used by other commands.
* Create a cache.json file in the root directory containing `{}`
* Create a bot_info.json file in the root directory containing the following content:
```
     {
      "owners":             ["your discord user ID"],
      "login":              "Your Discord app token goes here"
     }
```
* Run `python3 gman.py`
