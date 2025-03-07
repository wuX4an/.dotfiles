import os

def settings():
    # DIRECTORIES
    HOME      = os.getenv("HOME")
    QTILE     = f"{HOME}/.config/qtile"
    CONFIG    = f"{QTILE}/config.d"
    SETTINGS  = f"{QTILE}/settings"
    SCRIPTS   = f"{QTILE}/scripts"
    WALPAPERS = f"{QTILE}/wallpapers"
    IMAGES    = f"{SETTINGS}/images"

    # TERMINAL
    TERMINAL            = "kitty"
    TERMINAL_DEFAULT    = f"{TERMINAL} --single-instance -c {CONFIG}/kitty/kitty.conf"
    TERMINAL_FLOATING   = f"{TERMINAL} --class='floatterm' --single-instance -c {CONFIG}/kitty/apps.conf"
    # ROFI
    ROFI = "rofi"
    ROFI_DEFAULT = f"rofi -config {CONFIG}/rofi/config.rasi -show drun"
    # WIDGET DEFAULTS
    WIDGET_DEFAULTS = dict(
        font="Departure Mono Bold",
        fontsize=14,
        padding=3,
        background='#343F44',
        foreground='#9da9a0'
    )
    return {
        "dirs": {
            "HOME": HOME,
            "QTILE": QTILE,
            "CONFIG": CONFIG,
            "SETTINGS": SETTINGS,
            "SCRIPTS": SCRIPTS,
            "WALPAPERS": WALPAPERS,
            "IMAGES": IMAGES,
        },
        "terminal": {
            "DEFAULT": TERMINAL_DEFAULT,
            "FLOATING": TERMINAL_FLOATING,
        },
        "rofi": {
            "DEFAULT": ROFI_DEFAULT,
        },
        "widget_defautls": {
            "DEFAULT": WIDGET_DEFAULTS,
        }
    }
