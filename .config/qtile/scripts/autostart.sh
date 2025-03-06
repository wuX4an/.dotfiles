#!/bin/sh

CONFIG=$HOME/.config/qtile/config.d

picom --config $CONFIG/picom/other.conf &
dunst -conf $CONFIG/dunst/dunstrc &
mpd $CONFIG/mpd/mpd.conf &
flameshot &
