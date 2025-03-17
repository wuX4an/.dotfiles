import subprocess


def get_battery_percent():
    command = "upower -i /org/freedesktop/UPower/devices/battery_BAT1 | grep percentage | awk '{print $2}'"
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    stdout, stderr = process.communicate()
    if stderr:
        return 0
    percent_int = int(stdout.replace("%", ""))
    return percent_int


def get_battery_state():
    command = "upower -i /org/freedesktop/UPower/devices/battery_BAT1 | grep state | awk '{print $2}'"
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    stdout, stderr = process.communicate()
    if stderr:
        return 0
    state = stdout.strip()
    return state


def battery():
    percent = get_battery_percent()
    status = get_battery_state()

    # Charging
    if percent >= 90 and status == "charging":
        return "󰂄 "
    elif percent >= 80 and status == "charging":
        return "󰂊 "
    elif percent >= 60 and status == "charging":
        return "󰂉 "
    elif percent >= 40 and status == "charging":
        return "󰂈 "
    elif percent >= 20 and status == "charging":
        return "󰂆 "
    elif percent < 20 and status == "charging":
        return "󰢟 "
    # Discharging
    elif percent >= 90 and status == "discharging":
        return "󱈑 "
    elif percent >= 80 and status == "discharging":
        return "󰂁 "
    elif percent >= 60 and status == "discharging":
        return "󰁿 "
    elif percent >= 40 and status == "discharging":
        return "󰁽 "
    elif percent >= 20 and status == "discharging":
        return "󰁻 "
    elif percent < 20 and status == "discharging":
        return "󱃍 "
