#!/usr/bin/env bash
#
#  ███████╗ ██████╗██████╗ ███████╗███████╗███╗   ██╗    ██╗      ██████╗  ██████╗██╗  ██╗
#  ██╔════╝██╔════╝██╔══██╗██╔════╝██╔════╝████╗  ██║    ██║     ██╔═══██╗██╔════╝██║ ██╔╝
#  ███████╗██║     ██████╔╝█████╗  █████╗  ██╔██╗ ██║    ██║     ██║   ██║██║     █████╔╝
#  ╚════██║██║     ██╔══██╗██╔══╝  ██╔══╝  ██║╚██╗██║    ██║     ██║   ██║██║     ██╔═██╗
#  ███████║╚██████╗██║  ██║███████╗███████╗██║ ╚████║    ███████╗╚██████╔╝╚██████╗██║  ██╗
#  ╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝    ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝
#	gh0stzk - https://github.com/gh0stzk/dotfiles
#	15.10.2024 14:26:09
#	Dependencies - i3lock-color
#

TEMP_IMAGE="/tmp/i3lock.jpg"

# Colors
bg=1a1b26
fg=c0caf5
ring=15161e
wrong=f7768e
date=c0caf5
verify=9ece6a

default_lockscreen() {

  maim -d 0.3 -u ${TEMP_IMAGE}
  magick $TEMP_IMAGE -blur 5x5 $TEMP_IMAGE
  i3lock -n --force-clock -i $TEMP_IMAGE -e --indicator \
    --radius=30 --ring-width=60 --inside-color=$bg \
    --ring-color=$ring --insidever-color=$verify --ringver-color=$verify \
    --insidewrong-color=$wrong --ringwrong-color=$wrong --line-uses-inside \
    --keyhl-color=$verify --separator-color=$verify --bshl-color=$verify \
    --time-str="%H:%M" --time-size=140 --date-str="%a, %d %b" \
    --date-size=45 --verif-text="Verifying Password..." --wrong-text="Wrong Password!" \
    --noinput-text="" --ind-pos="300:610" \
    --time-font="Departure Mono:style=Bold" --date-font="Departure Mono" --verif-font="Departure Mono" \
    --greeter-font="Departure Mono" --wrong-font="Departure Mono" --verif-size=23 \
    --greeter-size=23 --wrong-size=23 --time-pos="300:390" \
    --date-pos="300:450" --greeter-pos="300:780" --wrong-pos="300:820" \
    --verif-pos="300:655" --date-color=$date --time-color=$date \
    --greeter-color=$fg --wrong-color=$wrong --verif-color=$verify \
    --verif-pos="300:820" --pointer=default --refresh-rate=60 \
    --pass-media-keys --pass-volume-keys

}

case $1 in
-r | --rice)
  rice_lockscreen
  ;;
-h | --help)
  echo -e "ScreenLocker [options]
Note: If an option is not specified, the screen locks with a screenshot with a blur effect.

Options:
	[-r] [--rice]	Set the screen locker with a random wallpaper of the current theme.\n"
  ;;
*)
  default_lockscreen
  ;;
esac
