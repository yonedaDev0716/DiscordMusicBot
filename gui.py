import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import os

BOT_FILE = "bot.exe" if os.path.exists("bot.exe") else "bot.py"

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

COMMAND_FILE = os.path.join(
    BASE_DIR,
    "command.txt"
)


process = None

def start_bot():

    global process

    if process and process.poll() is None:
        return

    if BOT_FILE.endswith(".exe"):

        process = subprocess.Popen(
            [BOT_FILE]
        )

    else:

        process = subprocess.Popen(
            ["python", BOT_FILE]
        )

    status_var.set("BOT起動中")

    status_var.set("BOT起動中")
def send_command(cmd):
    print("GUI PATH")
    print("SEND:", cmd)
    with open(COMMAND_FILE, "w", encoding="utf-8") as f:
        f.write(cmd)


def stop_bot():

    global process

    if process and process.poll() is None:

        send_shutdown()

        root.after(
            3000,
            force_stop
        )

    else:

        status_var.set("BOT停止")

def force_stop():

    global process

    if process and process.poll() is None:

        process.kill()

    process = None

    status_var.set("BOT停止")

def on_close():

    stop_bot()

    root.after(
        3500,
        root.destroy
    )


root = tk.Tk()
root.title("MusicForge")
root.geometry("700x500")

status_var = tk.StringVar(value="BOT停止")

title = ttk.Label(
    root,
    text="Discord Music Bot",
    font=("Yu Gothic UI", 18, "bold")
)
title.pack(pady=10)

status_frame = ttk.LabelFrame(
    root,
    text="状態"
)
status_frame.pack(fill="x", padx=10)

ttk.Label(
    status_frame,
    textvariable=status_var
).pack(
    padx=10,
    pady=10
)

btn_frame = ttk.Frame(root)
btn_frame.pack(pady=10)
control_frame = ttk.LabelFrame(
    root,
    text="操作"
)
control_frame.pack(fill="x", padx=10, pady=10)


ttk.Button(
    control_frame,
    text="VC参加",
    command=lambda: send_command("join")
).grid(row=0, column=0, padx=5, pady=5)

ttk.Button(
    control_frame,
    text="再生",
    command=lambda: send_command("play")
).grid(row=0, column=1, padx=5, pady=5)

ttk.Button(
    control_frame,
    text="停止",
    command=lambda: send_command("stop")
).grid(row=0, column=2, padx=5, pady=5)

ttk.Button(
    control_frame,
    text="退出",
    command=lambda: send_command("leave")
).grid(row=0, column=3, padx=5, pady=5)

ttk.Button(
    btn_frame,
    text="BOT起動",
    command=start_bot
).grid(row=0, column=0, padx=5)

ttk.Button(
    btn_frame,
    text="BOT停止",
    command=stop_bot
).grid(row=0, column=1, padx=5)

settings = ttk.LabelFrame(
    root,
    text="設定"
)
settings.pack(fill="x", padx=10, pady=10)

ttk.Label(
    settings,
    text="FFmpeg"
).grid(row=0, column=0, sticky="w", padx=5)

ffmpeg_var = tk.StringVar(
    value=r"C:\ffmpeg\bin\ffmpeg.exe"
)

ttk.Entry(
    settings,
    textvariable=ffmpeg_var,
    width=60
).grid(row=0, column=1, padx=5)

ttk.Label(
    settings,
    text="音声デバイス"
).grid(row=1, column=0, sticky="w", padx=5)

device_var = tk.StringVar(
    value="仮想デバイス (Yamaha SYNCROOM Driver (WDM))"
)

ttk.Entry(
    settings,
    textvariable=device_var,
    width=60
).grid(row=1, column=1, padx=5)

log_frame = ttk.LabelFrame(
    root,
    text="ログ"
)
log_frame.pack(fill="both", expand=True, padx=10, pady=10)

log_text = tk.Text(log_frame)
log_text.pack(fill="both", expand=True)

def send_shutdown():

    with open(
        COMMAND_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        f.write("shutdown")
root.protocol(
    "WM_DELETE_WINDOW",
    on_close
)


root.mainloop()