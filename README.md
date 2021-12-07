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
* Static build of ffmpeg (version 4.2 or above)
* A MongoDB database
  * The bot looks for a database called `gman`. It uses a collection called `inventory` for the bookmark system and `videos` for keeping track of videos sent.
* AviGlitch, see https://github.com/ucnv/aviglitch for installation instructions. This is needed for the !mosh command.
* All the Python packages in requirements.txt

You can install the Python packages, preferably in a virtual environment, by running
```
pip install -r requirements.txt
```

*Tip:* If you using Mac or Linux, you may have Python 2/Pip 2 preinstalled. You should run:
```
pip3 install -r requirements.txt
```
<br>

## Installation
* Download/install all requirements.
* Set up these folders with the following contents (if a folder doesn't exist, create it):
  * ffmpeg-static
    * Add the static build of ffmpeg to this folder (the executable ffmpeg file should be in this folder).
  * vids
    * Keep this folder empty as its contents are often deleted. It's used by g_man for processing videos.
  * fonts
    * Add .ttf files for the Arial and Impact fonts (called `arial.ttf` and `impact.ttf`) to this folder. Arial is required for the `!tutorial` command and Impact for `!text`.
    * (Optional) Upload any additional .ttf you want to use (useful if you use the `!filter` command).
  * tutorial/songs
    * Add any .mp3 background music you want for the !tutorial command. Some fitting songs are:
      * Trance - 009 Sound System Dreamscape
      * Evanescence - Bring Me to Life
      * Papa Roach - Last Resort
      * Any other songs used in YouTube tutorial videos during the late 2000's.
  * clips
    * Add the following .mp3 files if you wish to use the commands associated with them:
      * `americ.mp3` (The song "Never Meant" by American Football, used with the `!americ` command).
      * `mahna.mp3` (The song "Mah Na Mah Na" from the Muppets soundtrack, used with the `!mahna` command).
      * `tetris.mp3` (The Tetris beatbox song by Verbalase, used with the `!tetris` command).
* Create a copy of `bot_info_template.json` and rename it to `bot_info.json`. Fill it in with the appropriate information (keep the quotes).
* Run `python3 gman.py`
