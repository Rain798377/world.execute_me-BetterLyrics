import pygame
import time
from song_transcript import *
from utils import Style
from pathlib import Path


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
        # support optional 'append' flag in transcript entries
        # if 'append' is True, this lyric will be printed on the same line
        # as the previous lyric (useful for staggered delays)
        append_flag = lyric.get("append", False)
        lyrics_to_print.append(
            (lyric["start"], lyric["text"], styles[index], print_speed, append_flag))

    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    total_duration = (pygame.mixer.Sound(audio_file)).get_length()
    pygame.mixer.music.play()

    current_lyric_index = 0
    running = True

    while running:
        current_lyric = transcript[current_lyric_index]
        start_time = current_lyric["start"]
        current_time = pygame.mixer.music.get_pos() / 1000

        if current_time >= start_time:
            start_time, text, current_style, print_speed, append_flag = \
                lyrics_to_print[current_lyric_index]
            sep = " " if append_flag else "\n"
            slow_print(f"{sep}{text}", print_speed, current_style)
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