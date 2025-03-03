from libqtile.config import Key, Drag, Click, Group
from libqtile.lazy import lazy
from libqtile import layout
# from libqtile import qtile, widget
import os, subprocess
from settings import settings
# from time import sleep
import threading

mod = "mod4"
settings = settings()

# Prompt
@lazy.function
def prompt(qtile):
    def callback(text):
        def wait():
            # sleep(1)
            # subprocess.call(["dunstify", text])
            subprocess.call(["dunstify", text])
            ai = subprocess.run([f"{home}/.config/qtile/ui/ai", text], capture_output=True, text=True)
            subprocess.call(["dunstify", ai.stdout])
            command = f"gtts-cli -l es '{ai.stdout}' | play -t mp3 - tempo 1.3 &"
            subprocess.Popen(os.system(command)).wait()

        yarn = threading.Thread(target=wait)
        yarn.start()
        pass

    prompt = qtile.widgets_map["prompt"]
    prompt.start_input("", callback)

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    Key([mod], "p", prompt, desc="Use Prompt"),
    Key([mod], "l", lazy.spawn(f"{settings["dirs"]["SCRIPTS"]}/lockscreen.sh"), desc="Lock Screen"),
    # Switch between windows
    Key([mod], "left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "up", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(settings["terminal"]["DEFAULT"]), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "d", lazy.spawn(settings["rofi"]["DEFAULT"]), desc="Open rofi"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f11",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd("exec"), desc="Spawn a command using a prompt widget"),
    # XF86 Keys
    Key([], "XF86AudioMute", lazy.spawn("pamixer -t"), desc="Mute/Unmute Volume"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pamixer -i 5"), desc='Volume Up'),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pamixer -d 5"), desc='volume down'),

    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl s 10%+"), desc='brightness UP'),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl s 10%-"), desc='brightness Down'),

    Key([mod], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc='playerctl'),
    Key([mod], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc='playerctl'),
    Key([mod], "XF86AudioNext", lazy.spawn("playerctl next"), desc='playerctl'),
    Key([], "XF86AudioPlay", lazy.spawn("mpc toggle"), desc='mpd'),
    Key([], "XF86AudioPrev", lazy.spawn("mpc prev"), desc='mpd'),
    Key([], "XF86AudioNext", lazy.spawn("mpc next"), desc='mpd'),

    # LAYOUTS
    # TreeTab
    Key([mod, "shift"], "left",
        lazy.layout.shuffle_left(),
        lazy.layout.move_left().when(layout=["treetab"]),
        desc="Move window to the left/move tab left in treetab"),
    Key([mod, "shift"], "right",
        lazy.layout.shuffle_right(),
        lazy.layout.move_right().when(layout=["treetab"]),
        desc="Move window to the right/move tab right in treetab"),
    Key([mod, "shift"], "down",
        lazy.layout.shuffle_down(),
        lazy.layout.section_down().when(layout=["treetab"]),
        desc="Move window down/move down a section in treetab"
    ),
    Key([mod, "shift"], "up",
        lazy.layout.shuffle_up(),
        lazy.layout.section_up().when(layout=["treetab"]),
        desc="Move window downup/move up a section in treetab"
    ),
    Key([mod, "control"], "9", lazy.to_screen(1), lazy.group["9"].toscreen(1), desc="Move Screen 1 to WS 9"),
]


# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )

groups = [Group(f"{i+1}") for i in range(9)]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.toggle_floating()),
]
