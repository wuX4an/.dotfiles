from libqtile import bar, widget
from libqtile.config import Screen
from libqtile import qtile

### Modules ###

from .modules.widgets.wifi import wifi
from .modules.widgets.bluetooth import bluetooth
import os
from settings import settings
home = os.path.expanduser('~')

settings = settings()
images = settings["dirs"]["IMAGES"]
open_in_term = settings["terminal"]["FLOATING"]

#### Custom Functions ####


#### MOUSE CALLBACKS ####
def open_pulsemixer():
    qtile.cmd_spawn(f"{open_in_term} pulsemixer")

def open_bluetui():
    qtile.cmd_spawn(f"{open_in_term} bluetui")

def open_rmpc():
    qtile.cmd_spawn(f"{open_in_term} rmpc -c {settings["dirs"]["CONFIG"]}/rmpc/config.ron")

def open_nmpy():
    qtile.cmd_spawn(f"{open_in_term} python3 {settings["dirs"]["SETTINGS"]}/modules/network/fzf.py")

#### BAR ####
screens = [
    Screen(
        wallpaper = "~/.config/qtile/wallpapers/wallpaper_6.jpg",
        wallpaper_mode = 'fill',
        top=bar.Bar(
            [
                widget.Spacer(
                    length=10,
                    background='#232A2E',

                ),
                widget.Image( # Kirby
                    filename=f'{images}/kirby.png',
                    margin=-3,
                    background='#232A2E',
                ),
                widget.Image(
                    filename=f'{images}/6.png',
                ),
                widget.GroupBox(
                    disable_drag=True,
                    borderwidth=2,
                    highlight_method='block',
                    active='#86918A',
                    block_highlight_text_color="#D3C6AA",
                    highlight_color='#4B427E',
                    inactive='#232A2E',
                    foreground='#4B427E',
                    background='#343F44',
                    this_current_screen_border='#343F44',
                    this_screen_border='#343F44',
                    other_current_screen_border='#343F44',
                    other_screen_border='#343F44',
                    urgent_border='#343F44',
                    font="Departure Mono",
                    fontsize=18,
                    # padding=0
                ),
                widget.Image(
                    filename=f'{images}/1.png',

                ),
                widget.CurrentLayoutIcon(
                    custom_icon_paths=[f"{images}/layout"],
                    scale=0.75,
                ),
                widget.Spacer(
                    length=8,
                ),
                widget.CurrentLayout(),
                widget.Image(
                    filename=f'{images}/1.png',

                ),
                widget.Mpd2(
                    status_format="{play_status}",
                    idle_format='{play_status}',
                    play_states={'pause': ' ', 'play': ' ', 'stop': ' '},
                    no_connection=" ",
                    mouse_callbacks={'Button3': open_rmpc},
                    mouse_buttons={1: 'toggle', 3: None, 4: 'previous', 5: 'next'},
                    font="Symbols Nerd Font",
                ),
                widget.Image(
                    filename=f'{images}/1.png',
                ),
                widget.Prompt(prompt="{prompt}: "),
                # widget.WindowName(),
                widget.Spacer(),
                # widget.Wttr(
                #     format='%t',
                #     foreground="#f6c177",
                #     fmt="<u>{}</u>",
                # ),

                # widget.Spacer(background=(0, 0, 0, 0)),
                widget.Spacer(),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Image(
                    filename=f'{images}/3.png',
                ),
                widget.Systray(
                    background='#232A2E',
                    fontsize=2,
                    padding=6,
                ),
                widget.Image(
                    filename=f'{images}/6.png',
                ),
                widget.GenPollText(
                    func=wifi,
                    mouse_callbacks={"Button1": open_nmpy},
                    update_interval=5,
                    font="Symbols Nerd Font",
                    fontsize=18,
                    fmt="{}",
                ),
                widget.Image(
                    filename=f'{images}/2.png',
                ),
                widget.GenPollText(
                    func=bluetooth,
                    mouse_callbacks={"Button1": open_bluetui},
                    update_interval=5,
                    font="Symbols Nerd Font",
                    fontsize=18,
                    fmt="{}",
                ),
                widget.Image(
                    filename=f'{images}/2.png',
                ),
                widget.PulseVolume(
                    unmute_format='ESCUCHO {volume}%',
                    mute_format='NO ESCUCHO',
                    mouse_callbacks={"Button3": open_pulsemixer},
                    update_interval=1,
                    get_volume_command="pamixer --get-volume",
                ),
                widget.Image(
                    filename=f'{images}/2.png',
                ),
                widget.Backlight(
                    fmt="VEO {}", 
                    backlight_name="intel_backlight",
                    change_command="brightnessctl set {}%",
                ),
                widget.Image(
                    filename=f'{images}/5.png',
                    background='#353446',
                ),
                widget.TextBox(
                    font="Symbols Nerd Font",
                    fmt="",
                    background='232A2E',
                ),
                widget.Clock(
                    format="%I:%M:%S",
                    background='232A2E',
                    fmt="{}",
                ),
                widget.Spacer(
                    length=10,
                    background='232A2E',
                ),
            ],
            32,
            border_color='#282738',
            border_width=[0,0,0,0],
            margin=[6,10,4,10],
            # background="#00000000"
            # background="#ff0000.0", opacity=1
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),

        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
    Screen(
        wallpaper = "~/.config/qtile/wallpapers/wallpaper_6.jpg",
        wallpaper_mode = 'fill',
        ),
]

