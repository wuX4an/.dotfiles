#!/bin/sh

# Variables
SESSION_NAME="yazelix"
LAYOUT="yazelix"
CONFIG_DIR="$HOME/.config/yazelix/zellij"

# Session exited
SESSION_EXITED=$(zellij ls | grep "$SESSION_NAME" | grep "EXITED")

if [ -n "$SESSION_EXITED" ]; then
  # Attempts to join the session; if it fails, it is dead → deletes it
  zellij delete-session yazelix --force
  zellij --config-dir "$CONFIG_DIR" \
    attach --create "$SESSION_NAME" \
    options --default-layout "$LAYOUT"
else
  zellij --config-dir "$CONFIG_DIR" \
    attach --create "$SESSION_NAME" \
    options --default-layout "$LAYOUT"
fi
