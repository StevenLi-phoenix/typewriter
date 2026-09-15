#!/bin/zsh
SCRIPT_DIR="${0:A:h}"
"$SCRIPT_DIR/.venv/bin/python" "$SCRIPT_DIR/main.py" "$@"