import tkinter as tk
from tkinter import ttk
import subprocess
import os
import sys
import json
import re

# PyInstaller対応
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 構成:
# gui/
#   gui.exe
#   bot/
#      bot.exe
#      command.txt

CONFIG_FILE = os.path.join(
    BASE_DIR,
    "config.json"
)

if not os.path.exists(CONFIG_FILE):

    default_config = {
        "token": "",
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

def load_config():

    if not os.path.exists(CONFIG_FILE):
        return {
            "token": "",
            "vc_channel_id": 0,
            "ffmpeg_path": r"C:\ffmpeg\bin\ffmpeg.exe",
            "audio_device": "仮想デバイス (Yamaha SYNCROOM Driver (WDM))"
        }

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

    
def save_config():

    config = {
        "token": token_var.get(),
        "vc_channel_id": int(channel_var.get() or 0),
        "ffmpeg_path": ffmpeg_var.get(),
        "audio_device": device_var.get()
    }

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(
            config,
            f,
            ensure_ascii=False,
            indent=4
        )

    status_var.set("設定保存完了")

BOT_EXE = os.path.join(
    BASE_DIR,
    "bot",
    "bot.exe"
)

COMMAND_FILE = os.path.join(
    BASE_DIR,
    "bot",
    "command.txt"
)

process = None

def get_audio_devices():

    devices = []

    try:

        result = subprocess.run(
            [
                ffmpeg_var.get(),
                "-list_devices",
                "true",
                "-f",
                "dshow",
                "-i",
                "dummy"
            ],
            capture_output=True,
            text=True
        )

        lines = result.stderr.splitlines()

        for line in lines:

            if "DirectShow audio devices" in line:
                continue

            for line in lines:

                if "(audio)" in line.lower():

                    m = re.search(r'"(.+)"', line)

                    if m:
                        devices.append(m.group(1))


    except Exception as e:
        print(e)

    return devices


def start_bot():
    global process

    if process and process.poll() is None:
        return

    try:
        process = subprocess.Popen(
            [BOT_EXE],
            cwd=os.path.dirname(BOT_EXE),
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        status_var.set("BOT起動中")

    except Exception as e:
        print(e)
        status_var.set("起動失敗")


def send_command(cmd):
    try:
        with open(COMMAND_FILE, "w", encoding="utf-8") as f:
            f.write(cmd)



    except Exception as e:
        print(e)


def send_shutdown():
    with open(COMMAND_FILE, "w", encoding="utf-8") as f:
        f.write("shutdown")


def stop_bot():
    global process

    if process and process.poll() is None:
        send_shutdown()
        root.after(3000, force_stop)

def refresh_devices():

    devices = get_audio_devices()

    device_combo["values"] = devices

    if devices:

        current = device_var.get()

        if current in devices:
            device_combo.set(current)
        else:
            device_combo.current(0)

def force_stop():
    global process

    if process and process.poll() is None:
        process.kill()

    process = None
    status_var.set("BOT停止")


def on_close():
    stop_bot()
    root.after(3500, root.destroy)
root = tk.Tk()




root.title("MusicForge")
root.geometry("900x650")
config = load_config()

token_var = tk.StringVar(
    value=config.get("token", "")
)

channel_var = tk.StringVar(
    value=str(config.get("vc_channel_id", ""))
)
ffmpeg_var = tk.StringVar(
    value=config.get(
        "ffmpeg_path",
        r"C:\ffmpeg\bin\ffmpeg.exe"
    )
)

device_var = tk.StringVar(
    value=config.get(
        "audio_device",
        "仮想デバイス (Yamaha SYNCROOM Driver (WDM))"
    )
)

status_var = tk.StringVar(value="BOT停止")
settings_frame = ttk.LabelFrame(
    root,
    text="設定"
)
settings_frame.pack(
    fill="x",
    padx=10,
    pady=10
)

ttk.Label(
    settings_frame,
    text="Bot Token"
).grid(
    row=0,
    column=0,
    padx=5,
    pady=5,
    sticky="w"
)

ttk.Entry(
    settings_frame,
    textvariable=token_var,
    width=80
).grid(
    row=0,
    column=1,
    padx=5,
    pady=5
)

ttk.Label(
    settings_frame,
    text="VC Channel ID"
).grid(
    row=1,
    column=0,
    padx=5,
    pady=5,
    sticky="w"
)

ttk.Entry(
    settings_frame,
    textvariable=channel_var,
    width=30
).grid(
    row=1,
    column=1,
    padx=5,
    pady=5,
    sticky="w"
)
ttk.Label(
    settings_frame,
    text="FFmpeg Path"
).grid(
    row=2,
    column=0,
    padx=5,
    pady=5,
    sticky="w"
)

ttk.Entry(
    settings_frame,
    textvariable=ffmpeg_var,
    width=80
).grid(
    row=2,
    column=1,
    padx=5,
    pady=5
)

ttk.Label(
    settings_frame,
    text="Audio Device"
).grid(
    row=3,
    column=0,
    padx=5,
    pady=5,
    sticky="w"
)


ttk.Button(
    settings_frame,
    text="設定保存",
    command=save_config
).grid(
    row=4,
    column=1,
    sticky="w",
    pady=5
)
ttk.Label(
    root,
    text="Discord Music Bot",
    font=("Yu Gothic UI", 18, "bold")
).pack(pady=10)

ttk.Label(
    root,
    textvariable=status_var
).pack(pady=5)

ttk.Button(
    root,
    text="BOT起動",
    command=start_bot
).pack()

ttk.Button(
    root,
    text="BOT停止",
    command=stop_bot
).pack()

frame = ttk.LabelFrame(root, text="操作")
frame.pack(fill="x", padx=10, pady=10)
device_combo = ttk.Combobox(
    settings_frame,
    textvariable=device_var,
    width=60,
    state="readonly"
)

device_combo.grid(
    row=3,
    column=1,
    padx=5,
    pady=5
)

ttk.Button(
    settings_frame,
    text="デバイス取得",
    command=refresh_devices
).grid(
    row=3,
    column=2,
    padx=5,
    pady=5
)
ttk.Button(
    frame,
    text="VC参加",
    command=lambda: send_command("join")
).grid(row=0, column=0, padx=5, pady=5)

ttk.Button(
    frame,
    text="再生",
    command=lambda: send_command("play")
).grid(row=0, column=1, padx=5, pady=5)

ttk.Button(
    frame,
    text="停止",
    command=lambda: send_command("stop")
).grid(row=0, column=2, padx=5, pady=5)

ttk.Button(
    frame,
    text="退出",
    command=lambda: send_command("leave")
).grid(row=0, column=3, padx=5, pady=5)

root.protocol("WM_DELETE_WINDOW", on_close)
root.after(100, refresh_devices)
root.mainloop()