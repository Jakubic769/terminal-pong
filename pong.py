#!/usr/bin/env python3
"""
PyPong - an ultra-lightweight terminal Pong game.
Zero external dependencies (Python standard library only).
Works on Linux, macOS and Windows.
"""

import os
import sys
import time
import random

WIDTH = 60
HEIGHT = 20
PADDLE_H = 4
POINTS_PER_LEVEL = 5  # every N points scored, the game speeds up (level up)

# ---------------------------------------------------------------------------
# Non-blocking keyboard input - separate implementation for Windows and Unix
# ---------------------------------------------------------------------------
if os.name == "nt":
    import msvcrt

    def key_pressed():
        return msvcrt.kbhit()

    def get_key():
        ch = msvcrt.getch()
        if ch in (b"\x00", b"\xe0"):  # prefix for special keys (arrows)
            ch2 = msvcrt.getch()
            arrow_map = {b"H": "UP", b"P": "DOWN"}
            return arrow_map.get(ch2)
        try:
            return ch.decode("utf-8").lower()
        except UnicodeDecodeError:
            return None

    def init_terminal():
        pass

    def restore_terminal():
        pass

else:
    import termios
    import tty
    import select

    _fd = sys.stdin.fileno()
    _old_settings = None

    def init_terminal():
        global _old_settings
        _old_settings = termios.tcgetattr(_fd)
        tty.setcbreak(_fd)

    def restore_terminal():
        if _old_settings is not None:
            termios.tcsetattr(_fd, termios.TCSADRAIN, _old_settings)

    def key_pressed():
        dr, _, _ = select.select([sys.stdin], [], [], 0)
        return dr != []

    def get_key():
        ch = sys.stdin.read(1)
        if ch == "\x1b":  # ESC sequence - arrow keys
            ch2 = sys.stdin.read(1)
            ch3 = sys.stdin.read(1)
            if ch2 == "[":
                if ch3 == "A":
                    return "UP"
                if ch3 == "B":
                    return "DOWN"
            return None
        return ch.lower()


def clear_screen():
    sys.stdout.write("\033[H\033[J")


def hide_cursor():
    sys.stdout.write("\033[?25l")


def show_cursor():
    sys.stdout.write("\033[?25h")


class Pong:
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.score_left = 0
        self.score_right = 0
        self.level = 1
        self.speed = 0.06
        self.running = True
        self.reset_positions()

    def reset_positions(self):
        self.left_y = self.height // 2 - PADDLE_H // 2
        self.right_y = self.height // 2 - PADDLE_H // 2
        self.ball_x = self.width // 2
        self.ball_y = self.height // 2
        self.ball_dx = random.choice([-1, 1])
        self.ball_dy = random.choice([-1, 1])

    def level_up(self):
        self.level += 1
        self.speed = max(0.02, self.speed - 0.008)

    def move_ai(self):
        center = self.right_y + PADDLE_H // 2
        if center < self.ball_y - 1 and self.right_y + PADDLE_H < self.height - 1:
            self.right_y += 1
        elif center > self.ball_y + 1 and self.right_y > 1:
            self.right_y -= 1

    def update(self):
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        if self.ball_y <= 1 or self.ball_y >= self.height - 2:
            self.ball_dy *= -1

        if self.ball_x == 2:
            if self.left_y <= self.ball_y < self.left_y + PADDLE_H:
                self.ball_dx *= -1
            else:
                self.score_right += 1
                self.reset_positions()
                return

        if self.ball_x == self.width - 3:
            if self.right_y <= self.ball_y < self.right_y + PADDLE_H:
                self.ball_dx *= -1
            else:
                self.score_left += 1
                if self.score_left % POINTS_PER_LEVEL == 0:
                    self.level_up()
                self.reset_positions()
                return

        self.move_ai()

    def render(self):
        buf = []
        border = "+" + "-" * self.width + "+"
        buf.append(
            f" LEVEL: {self.level}   SCORE  You: {self.score_left}   CPU: {self.score_right}"
        )
        buf.append(border)
        grid = [[" " for _ in range(self.width)] for _ in range(self.height)]

        for i in range(PADDLE_H):
            if 0 <= self.left_y + i < self.height:
                grid[self.left_y + i][1] = "|"
            if 0 <= self.right_y + i < self.height:
                grid[self.right_y + i][self.width - 2] = "|"

        if 0 <= self.ball_y < self.height and 0 <= self.ball_x < self.width:
            grid[self.ball_y][self.ball_x] = "O"

        for row in grid:
            buf.append("|" + "".join(row) + "|")
        buf.append(border)
        buf.append(" W/S or Up/Down arrows = move    Q = quit")
        clear_screen()
        sys.stdout.write("\n".join(buf) + "\n")
        sys.stdout.flush()

    def handle_input(self):
        while key_pressed():
            k = get_key()
            if k in ("w", "UP"):
                if self.left_y > 1:
                    self.left_y -= 1
            elif k in ("s", "DOWN"):
                if self.left_y + PADDLE_H < self.height - 1:
                    self.left_y += 1
            elif k == "q":
                self.running = False

    def run(self):
        init_terminal()
        hide_cursor()
        try:
            while self.running:
                self.handle_input()
                self.update()
                self.render()
                time.sleep(self.speed)
        except KeyboardInterrupt:
            pass
        finally:
            restore_terminal()
            show_cursor()
            clear_screen()
            print(
                f"Game over! Final score - You: {self.score_left}  "
                f"CPU: {self.score_right}  (level reached: {self.level})"
            )


def main():
    Pong().run()


if __name__ == "__main__":
    main()