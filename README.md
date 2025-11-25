# Typewriter

A tiny Python CLI that types text into the active window with adjustable speed, delay, and optional noisy keystrokes to mimic human typing.

## Requirements
- Python 3
- [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/) (keyboard control)
- [pyperclip](https://pyperclip.readthedocs.io/en/latest/) (clipboard access)

## Installation
1. Install the runtime dependencies:
   ```bash
   python3 -m pip install --user pyautogui pyperclip
   ```
2. Install the CLI into your user bin directory:
   ```bash
   ./install.sh
   ```
   The script installs `typewriter` into `$HOME/.local/bin` (or `$HOME/bin`). Add that directory to `PATH` if needed.

## Usage
The command waits the configured delay before typing. Focus the target window and place your cursor where the text should go.

- Type provided text at 8 characters/second after a 3s delay:
  ```bash
  typewriter --text "Hello from Typewriter" --delay 3 --cps 8
  ```
- Use clipboard contents (default) at 10 characters/second:
  ```bash
  typewriter --delay 5 --cps 10
  ```
- Add noisy keystrokes to mimic human corrections:
  ```bash
  typewriter --text "Example with noise" --noise-prob 0.35
  ```
- Make the noisy behavior reproducible:
  ```bash
  typewriter --text "Deterministic run" --noise-prob 0.3 --seed 123
  ```

CLI options:
- `--text / -t`: Text to type. Falls back to clipboard contents when omitted.
- `--delay`: Seconds to wait before typing begins (default 5).
- `--cps`: Characters per second typing speed (default 10).
- `--noise-prob`: Probability (0–1) to inject and erase a random snippet before each word (default 0.2).
- `--seed`: Seed the RNG for repeatable noisy runs.

## Notes
- On macOS, grant accessibility permissions to `python3` so PyAutoGUI can control the keyboard.
- The tool will type wherever your caret is active—keep it pointed at a safe target.

## Development
Run the script directly without installing:
```bash
python3 main.py --help
python3 main.py --text "Hello there" --delay 1 --cps 12 --noise-prob 0.1
```

## Uninstall
Remove the installed binary and its directory entry if desired:
```bash
rm -f ~/.local/bin/typewriter ~/.local/bin/typewriter.exe
```

