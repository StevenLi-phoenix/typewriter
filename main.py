#!/usr/bin/env python3
import argparse
import random
import sys
import time
from typing import List, Optional

import pyautogui as pg
import pyperclip


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Type text automatically with optional noisy keystrokes."
    )
    parser.add_argument(
        "-t",
        "--text",
        help="Text to type. Defaults to clipboard contents if omitted.",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=5.0,
        help="Seconds to wait before typing begins.",
    )
    parser.add_argument(
        "--cps",
        type=float,
        default=10.0,
        help="Characters per second typing speed.",
    )
    parser.add_argument(
        "--noise-prob",
        type=float,
        default=0.2,
        help="Probability (0-1) to inject and erase a random snippet before each word.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="Seed for randomness to make behavior reproducible.",
    )
    args = parser.parse_args()

    if args.cps <= 0:
        parser.error("--cps must be greater than zero.")
    if args.delay < 0:
        parser.error("--delay must be zero or positive.")
    if not 0 <= args.noise_prob <= 1:
        parser.error("--noise-prob must be between 0 and 1.")

    return args


def load_text(explicit_text: Optional[str]) -> str:
    if explicit_text:
        return explicit_text

    clipboard_text = str(pyperclip.paste())
    if clipboard_text.strip():
        return clipboard_text

    raise SystemExit("No text provided and clipboard is empty.")


def maybe_type_noise(words: List[str], interval: float, noise_prob: float) -> None:
    if random.random() >= noise_prob or not words:
        return

    filler = random.choice(words)
    glitch_length = max(1, int(len(filler) * random.random()))
    glitch = filler[:glitch_length]

    # Type a short snippet, then erase it to mimic human typing noise.
    pg.typewrite(glitch, interval=interval)
    time.sleep(interval)
    for _ in glitch:
        pg.press("backspace")
        time.sleep(0.02)


def type_words(words: List[str], interval: float, noise_prob: float) -> None:
    for word in words:
        maybe_type_noise(words, interval, noise_prob)
        pg.typewrite(word, interval=interval)
        time.sleep(interval)
        pg.press("space")
        time.sleep(interval)


def main() -> None:
    args = parse_args()
    if args.seed is not None:
        random.seed(args.seed)

    text = load_text(args.text)
    if not text:
        raise ValueError("No text provided and clipboard is empty.")
    interval = 1 / args.cps
    print(
        f"Typing {len(text)} characters at ~{args.cps:.1f} chars/sec "
        f"after {args.delay:.1f}s delay. Noise prob: {args.noise_prob:.2f}."
    )
    time.sleep(args.delay)
    for paragraph in text.split("\n"):
        try:
            type_words(paragraph.split(), interval, args.noise_prob)
        except KeyboardInterrupt:
            sys.exit("Interrupted before completion.")
        pg.press("enter")


if __name__ == "__main__":
    main()
