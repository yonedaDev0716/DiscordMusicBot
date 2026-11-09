MusicForge
========================================

MusicForge is a tool that streams audio from a virtual audio device
to a Discord Voice Channel.

----------------------------------------
Requirements
----------------------------------------

1. Discord Bot

Go to Discord Developer Portal:

https://discord.com/developers/applications

Create:

- New Application
- Bot
- Obtain Bot TOKEN

After creating the bot, invite it to your Discord server.

Required Permissions:

- View Channels
- Connect
- Speak
- Send Messages

----------------------------------------

2. FFmpeg

Download FFmpeg:

https://ffmpeg.org/download.html

After installation, place it at:

C:\ffmpeg\bin\ffmpeg.exe

If FFmpeg is installed elsewhere,
change the FFmpeg Path in the settings screen.

FFmpeg installation guide:

https://qiita.com/Tadataka_Takahashi/items/9dcb0cf308db6f5dc31b

----------------------------------------

3. Virtual Audio Device

A virtual audio device is required for audio streaming.

Recommended:

Yamaha SYNCROOM

https://syncroom.yamaha.com/

After installation, the following device
should become available:

Virtual Device
(Yamaha SYNCROOM Driver (WDM))

----------------------------------------
Installation
----------------------------------------

Extract the distribution package.

MusicForge

├─ gui.exe
├─ config.json
└─ bot
    ├─ bot.exe
    └─ _internal

----------------------------------------
Initial Setup
----------------------------------------

1.

Launch:

gui.exe

2.

Enter your Discord Bot TOKEN into:

Bot Token

3.

Enter the target Voice Channel ID into:

VC Channel ID

4.

FFmpeg Path

Normally, the default value is:

C:\ffmpeg\bin\ffmpeg.exe

5.

Click:

Get Devices

to retrieve available audio devices.

6.

Select the device you want to use from:

Audio Device

Example:

Virtual Device
(Yamaha SYNCROOM Driver (WDM))

7.

Click:

Save Settings

----------------------------------------
Usage
----------------------------------------

Always save your settings before starting the bot.

----------------------------------------

1.

Click:

Start BOT

----------------------------------------

2.

Click:

Join VC

The bot will join the configured voice channel.

----------------------------------------

3.

Play the audio you want to stream.

Examples:

- SYNCROOM
- DAW software
- Media player

----------------------------------------

4.

Click:

Play

Audio from the selected device
will be streamed to the Discord Voice Channel.

----------------------------------------
Stopping Playback
----------------------------------------

Stop

Stops audio streaming.

----------------------------------------

Leave

Leaves the Voice Channel.

----------------------------------------

Stop BOT

Shuts down the bot.

----------------------------------------
Notes
----------------------------------------

- FFmpeg must be installed and accessible.
- A virtual audio device is required.
- Do not share your Discord Bot Token with others.
- The bot will not start if the token is invalid.
- Save your settings before first use.

----------------------------------------
Test Environment
----------------------------------------

Windows 11
Python 3.14
discord.py 2.7.1
FFmpeg
Yamaha SYNCROOM Driver (WDM)

----------------------------------------
About MusicForge
----------------------------------------

MusicForge was developed because many existing
Discord Audio Bots available online no longer worked
properly with current Discord.py versions and environments.

The application was written in Python and developed
using only the free version of Microsoft Copilot.

Its goal is to provide a simple and reliable way
to stream audio from a virtual audio device directly
into Discord Voice Channels.
