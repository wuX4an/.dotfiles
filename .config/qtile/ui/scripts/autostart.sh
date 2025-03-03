#!/bin/sh

picom --config ~/.config/qtile/config/picom/picom.conf &
dunst -conf ~/.config/qtile/config/dunst/dunstrc &
mpd ~/.config/qtile/config/mpd/mpd.conf &
