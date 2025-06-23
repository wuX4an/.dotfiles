CONFIG=$HOME/.config/qtile/config.d

qtile cmd-obj -f reload_config
picom --config $CONFIG/picom/other.conf &
dunst -conf $CONFIG/dunst/dunstrc &
mpd $CONFIG/mpd/mpd.conf &
