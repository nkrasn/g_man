# g_man
A Discord bot for editing videos, built primarily for creating memes. It can apply filters, modify bitrate, and create glitch art. <br>

## Features
* Change video and audio bitrate.
* Easily apply various filters such as contrast, blur, volume, etc.
  * For advanced users, there is a !filter command that can apply almost any filter available in ffmpeg.
* Apply various premade sequences of filters, such as making the video in the style of an old-school YouTube tutorial.
* Corrupt videos in various ways, such as removing iframes and modifying/repeating random byte chunks.

## Usage
* Send a video to a channel. This can be either a youtube/twitter/discordcdn link, or a video file directly uploaded.
* Run a command and the bot will reply back with the edited video.

## Commands
All commands start with !<br>
Command list coming soon. At the moment, you can run !help to see all commands, and !help command_name to get more details.

## Requirements
* discord.py with voice support (tested on version 1.5)
* Static build of ffmpeg (version 4.2 or above)
* ffmpeg-python
* youtube_dl
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
