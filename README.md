# g_man
A Discord bot for editing videos, useful for simple edits or making memes. It can apply a large variety of filters, modify bitrate, and create glitch art. <br>
Filters are applied using FFMPEG, with some corruption commands using tomato.py (https://github.com/itsKaspar/tomato) or AviGlitch (https://github.com/ucnv/aviglitch).

## Features
* Change video and audio bitrate.
* Easily apply various filters such as contrast, blur, volume, etc.
  * For advanced users, there is a !filter command that can apply almost any filter available in FFMPEG.
* Apply premade sequences of filters, such as !tutorial to convert a video into an old-school YouTube tutorial.
* Corrupt videos in various ways, such as datamoshing and modifying random chunks of bytes in the video file.
* Save your videos using a personal bookmark system, and load your bookmarks in any server g_man is in.

## Usage/Commands
https://github.com/nkrasn/g_man/blob/master/COMMANDS.md<br>
You can get this link from within Discord by sending "!help" in a channel

## Requirements
* discord.py with voice support (tested on version 1.5)
* Static build of ffmpeg (version 4.2 or above)
* A MongoDB database
  * The bot looks for a database called `gman`. It uses a collection called `inventory` for the bookmark system and `videos` for keeping track of videos sent.
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

At the moment, it is required to have a folder called ffmpeg-static in the root of the bot's directory containing a static build of ffmpeg. <br>

## Installation
* Install all requirements.
* Create the following folders in the bot's root directory, if they don't exist:
  * ffmpeg-static
    * This should contain a static build of ffmpeg.
  * vids
    * This is the output directory for ffmpeg.
  * fonts
    * Drag an Arial and Impact .ttf file in here, and any other fontfile you want. Arial is needed for the `!tutorial` command and Impact is needed for `!text`.
  * tutorial/songs
    * Drag any .mp3 background music you want for the !tutorial command (such as "Trance - 009 Sound System Dreamscape" or "Evanescence - Bring Me to Life")
  * clips
    * Contains any files used by other commands.
* Create a bot_info.json file in the root directory containing the following content:
```
     {
      "owners":             ["Your Discord user ID"],
      "login":              "Your Discord app token goes here",
      "mongo_url":          "Your MongoDB connection url goes here"
     }
```
* Run `python3 gman.py`
