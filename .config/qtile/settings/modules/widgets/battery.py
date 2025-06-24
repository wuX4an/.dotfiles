import subprocess

def get_battery_percent():
    command = "cat /sys/class/power_supply/BAT1/capacity"
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    stdout, stderr = process.communicate()
    if stderr or not stdout.strip().isdigit():
        return 0
    return int(stdout.strip())

def get_battery_state():
    command = "cat /sys/class/power_supply/BAT1/status"
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    stdout, stderr = process.communicate()
    if stderr:
        return "Unknown"
    return stdout.strip().lower()

def battery():
    percent = get_battery_percent()
    status = get_battery_state()

    # Charging
    if percent >= 90 and status == "charging":
        return "󰂅 "
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
        return "󰁹 "
    elif percent >= 80 and status == "discharging":
        return "󰂁 "
    elif percent >= 60 and status == "discharging":
        return "󰁿 "
    elif percent >= 40 and status == "discharging":
        return "󰁽 "
    elif percent >= 20 and status == "discharging":
        return "󰁻 "
    elif percent <= 20 and status == "discharging":
        return "󱃍 "

def percent():
    return f"{get_battery_percent()}%"
