import pygame
import time
import random
import string
import os
from song_transcript import *
from utils import Style
from pathlib import Path


os.system('cls' if os.name == 'nt' else 'clear')


def calculate_print_speed(text: str, duration: float) -> float:
    total_length = len(text)
    speed = duration / (total_length * 5)

    if "," in text:
        speed *= 1.2
    if "." in text or "!" in text or "?" in text:
        speed *= 1.5

    return max(0.01, speed)


def slow_print(text: str, speed: float, colour: str) -> None:
    for character in text:
        print(colour + character + Style.RESET, end="", flush=True)
        time.sleep(speed)


def print_lyrics(audio_file: str, styles: list) -> None:
    lyrics_to_print = []
    for index, lyric in enumerate(transcript):
        print_speed = calculate_print_speed(lyric["text"], lyric["duration"])
        # support optional 'append' and 'overwrite' flags in transcript entries
        append_flag = lyric.get("append", False)
        overwrite_flag = lyric.get("overwrite", False)
        # optional prefix to display before the lyric text (e.g. '[Console]')
        # default to '[Console]' when not specified
        prefix = lyric.get("prefix", "[Console]")
        # optional scramble effect: prints scrambled ascii then the real lyric
        scramble_flag = lyric.get("scramble", False)
        # scramble_time can be provided per-entry, default to 0.15s
        scramble_time = lyric.get("scramble_time", 0.15)
        lyrics_to_print.append(
            (lyric["start"], prefix, lyric["text"], styles[index], print_speed, append_flag, overwrite_flag, scramble_flag, scramble_time))

    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    total_duration = (pygame.mixer.Sound(audio_file)).get_length()
    pygame.mixer.music.play()

    current_lyric_index = 0
    running = True

    last_print_len = 0
    while running:
        current_lyric = transcript[current_lyric_index]
        start_time = current_lyric["start"]
        current_time = pygame.mixer.music.get_pos() / 1000

        if current_time >= start_time:
            start_time, prefix, text, current_style, print_speed, append_flag, overwrite_flag, scramble_flag, scramble_time = \
                lyrics_to_print[current_lyric_index]
            if overwrite_flag:
                sep = "\r"
            else:
                sep = " " if append_flag else "\n"
            # include optional prefix only for non-appended lyrics
            prefix_to_use = prefix if not append_flag else ""
            # separate prefix and text so prefix doesn't mix with appended lines or timestamps
            text_part = text
            # display_text should be the lyric text only; prefix is printed separately
            display_text = text_part

            # compute printed length accounting for a leading space when appending
            printed_len = len(display_text) if not append_flag else (1 + len(display_text))

            # prepare prefix display (only for non-appended lyrics)
            prefix_display = f"{prefix_to_use} " if prefix_to_use else ""

            # handle cursor position for overwrite/newline cases
            if overwrite_flag:
                print("\r", end="", flush=True)
            elif sep == "\n" and last_print_len != 0:
                # start a new line before the next lyric when separator is newline
                print()

            # optional scramble effect: progressively settle random chars into the lyric
            if scramble_flag and not append_flag:
                chars = string.ascii_letters + string.digits + string.punctuation
                duration = scramble_time
                frame_delay = 0.02
                frames = max(1, int(duration / frame_delay))
                # scramble displays prefix inline with the text so they share a line
                for frame in range(frames):
                    progress = (frame + 1) / frames
                    settled = int(progress * len(text_part))
                    scrambled_part = ''.join(
                        text_part[i] if i < settled else random.choice(chars)
                        for i in range(len(text_part))
                    )
                    current_line = f"{prefix_display}{scrambled_part}"
                    pad = (last_print_len - len(current_line)) if last_print_len > len(current_line) else 0
                    print(f"\r{current_style}{current_line}{Style.RESET}{' ' * pad}", end="", flush=True)
                    time.sleep(frame_delay)
                # small pause after settle
                time.sleep(0.02)
                # clear any leftover characters if we overwrote a longer line
                if overwrite_flag and last_print_len > printed_len:
                    print(" " * (last_print_len - printed_len), end="", flush=True)
            else:
                # normal printing path
                # print prefix inline (no newline) if present
                if prefix_display:
                    print(f"{current_style}{prefix_display}{Style.RESET}", end="", flush=True)

                # determine text to print with slow_print
                if append_flag:
                    slow_print(" " + text_part, print_speed, current_style)
                else:
                    slow_print(text_part, print_speed, current_style)

                # If we overwrote a previous (longer) line, clear remaining chars
                if overwrite_flag and last_print_len > printed_len:
                    print(" " * (last_print_len - printed_len), end="", flush=True)

            # Update last printed length depending on separator
            # Track the length of the most-recently-displayed lyric text so overwrite can clear it.
            if sep == "\n":
                last_print_len = len(display_text)
            elif sep == " ":
                last_print_len += printed_len
            else:  # sep == '\r'
                last_print_len = printed_len
            current_lyric_index += 1
        handle_visuals(current_time)

        if current_lyric_index >= len(transcript):
            time.sleep((total_duration + 1) - current_time)
            running = False

    pygame.quit()


def handle_visuals(current_time: float) -> None:
    if print_statements:
        entry = print_statements[0]
        # timestamp is expected to be the last element in the entry
        ts = entry[-1] if isinstance(entry, (list, tuple)) and len(entry) >= 2 else None
        if isinstance(ts, (int, float)) and ts <= current_time:
            entry = print_statements.popleft()
            # If the first element is callable, treat this as a function call
            if callable(entry[0]):
                func = entry[0]
                args = entry[1] if len(entry) > 2 else ()
                if not isinstance(args, (list, tuple)):
                    args = (args,)
                try:
                    func(*args)
                except TypeError:
                    func()
            else:
                message = entry[0]
                print(f"\n{message}", end="", flush=True)

    if functions_to_execute and functions_to_execute[0][1] <= current_time:
        func, _ = functions_to_execute.popleft()
        func()


def main():
    current_dir = Path(__file__).parent
    audio_file = current_dir / "world-execute-me.mp3"
    styles = [Style.RED] * len(transcript)

    for index, colour in indices_styles.items():
        styles[index] = colour

    print_lyrics(audio_file, styles)


if __name__ == '__main__':
    main()