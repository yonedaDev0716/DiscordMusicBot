import discord
from discord.ext import commands
import asyncio
import os
import sys
import davey
import nacl
import nacl.secret
import nacl.utils
import nacl.bindings
import cffi
import _cffi_backend

print("DAVEY OK")
print("PyNaCl OK")
print("CFFI OK")

VC_CHANNEL_ID = 722817070739357770

TOKEN = "MTA2Njg5OTM2NjU0NTE5OTExNA.GEFCwZ.-_Cjc5_NkskdCZPpS_aGyDKJOUbeI6_pa0upMQ"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

COMMAND_FILE = os.path.join(
    BASE_DIR,
    "command.txt"
)

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
        "audio=仮想デバイス (Yamaha SYNCROOM Driver (WDM))",
        executable=r"C:\ffmpeg\bin\ffmpeg.exe",
        before_options='-f dshow',
        options='-ac 2 -ar 48000 -f s16le'
    )

    ctx.voice_client.play(source)

    await ctx.send("配信開始")

@bot.command()
async def test(ctx):

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

    print("channel =", channel)

    if channel is None:
        print("VCチャンネル取得失敗")
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

    try:

        if not bot.voice_clients:
            return

        vc = bot.voice_clients[0]

        if vc.is_playing():
            vc.stop()

        print("PLAY START")

        source = discord.FFmpegPCMAudio(
            "audio=仮想デバイス (Yamaha SYNCROOM Driver (WDM))",
            executable=r"C:\ffmpeg\bin\ffmpeg.exe",
            before_options="-f dshow",
            options="-ac 2 -ar 48000 -f s16le"
        )

        vc.play(source)

        print("PLAY OK")

    except Exception as e:

        print("PLAY ERROR")
        print(repr(e))

async def command_watcher():

    while True:
        print(os.path.abspath("command.txt"))
        print("watching...")
        try:

            if os.path.exists(COMMAND_FILE):

                with open(
                    COMMAND_FILE,
                    "r",
                    encoding="utf-8"
                ) as f:

                    cmd = f.read().strip()

                os.remove(COMMAND_FILE)

                print("GUI COMMAND:", cmd)

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



