#!/usr/bin/env bash
set -euo pipefail

# Install the typewriter CLI into a user bin directory.

SCRIPT_DIR="$(cd -- "$(dirname "$0")" && pwd)"
SOURCE="$SCRIPT_DIR/main.py"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required but not found in PATH." >&2
  exit 1
fi

BIN_DIR="${BIN_DIR:-"$HOME/.local/bin"}"
if [ ! -d "$BIN_DIR" ]; then
  BIN_DIR="$HOME/bin"
fi

mkdir -p "$BIN_DIR"
TARGET="$BIN_DIR/typewriter"

install -m 755 "$SOURCE" "$TARGET"

# Verify runtime dependencies so the command works after installation.
if ! python3 - <<'PY' >/dev/null 2>&1; then
import importlib
for mod in ("pyautogui", "pyperclip"):
    importlib.import_module(mod)
PY
  echo "Missing dependencies detected. Install with: pip install pyautogui pyperclip" >&2
  exit 1
fi

echo "Installed to $TARGET"

case ":$PATH:" in
  *":$BIN_DIR:"*) ;;
  *)
    echo "Note: $BIN_DIR is not on PATH. Add it or run with the full path." >&2
    ;;
esac
