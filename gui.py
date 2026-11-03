import tkinter as tk
from tkinter import ttk
import subprocess
import os
import sys

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


def start_bot():
    global process

    if process and process.poll() is None:
        return

    try:
        process = subprocess.Popen(
            [BOT_EXE],
            cwd=os.path.dirname(BOT_EXE)
        )

        status_var.set("BOT起動中")

    except Exception as e:
        print(e)
        status_var.set("起動失敗")


def send_command(cmd):
    try:
        with open(COMMAND_FILE, "w", encoding="utf-8") as f:
            f.write(cmd)

        print("SEND:", cmd)

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
root.geometry("700x500")

status_var = tk.StringVar(value="BOT停止")

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

root.mainloop()