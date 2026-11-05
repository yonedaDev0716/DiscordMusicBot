import discord
from discord.ext import commands
import asyncio
import json
import os
import sys



if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(
    os.path.dirname(BASE_DIR),
    "config.json"
)

with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    config = json.load(f)

TOKEN = config["token"]
VC_CHANNEL_ID = config["vc_channel_id"]
FFMPEG_PATH = config["ffmpeg_path"]
AUDIO_DEVICE = config["audio_device"]

print("TOKEN LEN =", len(TOKEN))
print("TOKEN START =", TOKEN[:10])

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

COMMAND_FILE = os.path.join(BASE_DIR, "command.txt")
print(CONFIG_FILE)
if not os.path.exists(CONFIG_FILE):

    default_config = {
        "token": "SET_TOKEN_HERE",
        "vc_channel_id": 0,
        "ffmpeg_path": "C:\\ffmpeg\\bin\\ffmpeg.exe",
        "audio_device": "仮想デバイス (Yamaha SYNCROOM Driver (WDM))"
    }

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(
            default_config,
            f,
            ensure_ascii=False,
            indent=4
        )

    print("config.json を作成しました")
    sys.exit()

@bot.event
async def on_ready():
    print(f"Login: {bot.user}")
    bot.loop.create_task(command_watcher())


@bot.command()
async def join(ctx):
    if not ctx.author.voice:
        await ctx.send("VCに入ってません")
        return

    channel = ctx.author.voice.channel

    if ctx.voice_client:
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect()

    await ctx.send("参加しました")


@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("退出しました")


@bot.command()
async def play(ctx):

    if not ctx.voice_client:
        await ctx.send("先に !join")
        return

    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()

    source = discord.FFmpegPCMAudio(
        f"audio={AUDIO_DEVICE}",
        executable=FFMPEG_PATH,
        before_options="-f dshow"
    )

    ctx.voice_client.play(source)

    await ctx.send("配信開始")


@bot.command()
async def test(ctx):

    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()

    source = discord.FFmpegPCMAudio(
        r"C:\Users\rainb\Music\test.mp3",
        executable=r"C:\ffmpeg\bin\ffmpeg.exe"
    )

    ctx.voice_client.play(source)

    await ctx.send("test")


@bot.command()
async def stop(ctx):

    if ctx.voice_client:
        ctx.voice_client.stop()
        await ctx.send("停止")


async def gui_join():

    channel = bot.get_channel(VC_CHANNEL_ID)

    if channel is None:
        return

    if not bot.voice_clients:
        await channel.connect()


async def gui_leave():

    if bot.voice_clients:
        await bot.voice_clients[0].disconnect()


async def gui_stop():

    if bot.voice_clients:

        vc = bot.voice_clients[0]

        if vc.is_playing():
            vc.stop()


async def gui_play():

    if not bot.voice_clients:
        return

    vc = bot.voice_clients[0]

    if vc.is_playing():
        vc.stop()

    source = discord.FFmpegPCMAudio(
        f"audio={AUDIO_DEVICE}",
        executable=FFMPEG_PATH,
        before_options="-f dshow"
    )

    vc.play(source)


async def command_watcher():

    while True:

        try:

            if os.path.exists(COMMAND_FILE):

                with open(
                    COMMAND_FILE,
                    "r",
                    encoding="utf-8"
                ) as f:

                    cmd = f.read().strip()

                os.remove(COMMAND_FILE)

                if cmd == "join":
                    await gui_join()

                elif cmd == "play":
                    await gui_play()

                elif cmd == "stop":
                    await gui_stop()

                elif cmd == "leave":
                    await gui_leave()

                elif cmd == "shutdown":

                    await gui_stop()
                    await gui_leave()

                    await bot.close()

        except Exception as e:
            print(e)

        await asyncio.sleep(1)


bot.run(TOKEN)