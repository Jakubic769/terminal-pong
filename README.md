# 🏓 PyPong

**A tiny, dependency-free Pong game that runs right in your terminal.**

![size](https://img.shields.io/badge/size-~6%20KB-brightgreen)
![dependencies](https://img.shields.io/badge/dependencies-none-blue)
![python](https://img.shields.io/badge/python-3.x-yellow)
![platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey)

One file. No `pip`, no `curses` package to fetch — just the Python
standard library. Run the installer once and it adds `pong` to your
PATH automatically, on Linux, macOS, and Windows. No manual steps.

---

## Preview

```
 LEVEL: 2   SCORE  You: 3   CPU: 2
+------------------------------------------------------------+
|                                                              |
|  |                                                           |
|  |                          O                                |
|  |                                                         | |
|                                                             | |
|                                                             | |
+------------------------------------------------------------+
 W/S or Up/Down arrows = move    Q = quit
```

## Features

- 📦 **~6 KB, single file** — nothing to download, nothing to compile
- 🧩 **Zero dependencies** — no `pip install`, just Python's standard library
- 🖥️ **Cross-platform** — same file runs on Linux, macOS, and Windows
- 🔧 **Self-installing** — the installer adds `pong` to PATH for you
- 🏆 **Score & levels** — every 5 points, the ball speeds up a notch
- ⌨️ **Simple controls** — `W`/`S` or the arrow keys, `Q` to quit
- 🤖 **Built-in CPU opponent**

## Requirements

Just **Python 3**. Linux and macOS usually already have it. On Windows,
grab it from [python.org](https://www.python.org/downloads/) and make
sure **"Add python.exe to PATH"** is checked during install.

## Install the `pong` command

### Linux / macOS

```bash
chmod +x install_linux.sh
./install_linux.sh
```

This copies `pong.py` to `~/.local/bin/pong` and, if that folder isn't
already on your PATH, appends the needed line to your `~/.bashrc` /
`~/.zshrc` / `~/.profile` automatically. No `sudo` required.

Open a new terminal window and type:

```bash
pong
```

### Windows

```
install_windows.bat
```

Double-click it, or run it from `cmd`. It copies the game to
`%USERPROFILE%\PyPong`, creates `pong.bat` there, and adds that folder
to your **user PATH** automatically via PowerShell — no manual editing
of environment variables, no admin rights needed.

Open a **new** terminal window (cmd or PowerShell) and type:

```
pong
```

> Either way, Windows and your shell only pick up PATH changes in
> **newly opened** terminal windows — that's the one unavoidable step,
> everything else is automatic.

## Quick start (no install)

```bash
python3 pong.py      # Linux / macOS
python pong.py        # Windows
```

## Controls

| Key            | Action        |
|----------------|---------------|
| `W` / `↑`      | Move paddle up |
| `S` / `↓`      | Move paddle down |
| `Q`            | Quit the game |

## How it works

The whole game is one Python file that draws the board with plain ASCII
characters and repaints the terminal using ANSI escape codes — no
`curses`, no third-party libraries. Keyboard input is read
non-blockingly using `msvcrt` on Windows and `termios`/`select` on
Unix-like systems, both of which ship with Python itself. The
installers use only built-in tools too: shell rc files on Linux/macOS,
and PowerShell's `[Environment]` API on Windows (which, unlike `setx`,
has no risk of truncating a long PATH).

## License

Free to use, modify, and share.