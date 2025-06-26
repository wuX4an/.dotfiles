#!/bin/sh

DIR="$HOME/Pictures/Screenshots/$(date '+%Y-%m-%d_%H:%M:%S').png"

maim -u /dev/stdout | satty --copy-command "xclip -selection clipboard -t image/png" --filename - --output-filename "$DIR" &

while :; do
  WIN_ID=$(xdotool search --class satty 2>/dev/null | head -n1)
  if [ -n "$WIN_ID" ]; then
    WIDTH=960
    HEIGHT=600

    # Obtener resolución de pantalla actual
    SCREEN_WIDTH=$(xdpyinfo | grep dimensions | awk '{print $2}' | cut -d'x' -f1)
    SCREEN_HEIGHT=$(xdpyinfo | grep dimensions | awk '{print $2}' | cut -d'x' -f2)

    # Calcular posición para centrar ventana
    POS_X=$(((SCREEN_WIDTH - WIDTH) / 2))
    POS_Y=$(((SCREEN_HEIGHT - HEIGHT + (SCREEN_HEIGHT / 19)) / 2))

    # Redimensionar y mover la ventana
    xdotool windowsize "$WIN_ID" $WIDTH $HEIGHT
    xdotool windowmove "$WIN_ID" $POS_X $POS_Y
    break
  fi
  sleep 0.05
done
