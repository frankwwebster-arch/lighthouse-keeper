#!/bin/zsh

PROJECT_DIR="${0:A:h}"
exec python3 "$PROJECT_DIR/scripts/keeper_review_offline.py" "$@"
