import subprocess
import os

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

NOTIFY_STATE_FILE = "/tmp/.battery_notify_level"

def notify_battery(percent, charging):
    last_notified = None
    if os.path.exists(NOTIFY_STATE_FILE):
        with open(NOTIFY_STATE_FILE, "r") as f:
            last_notified = int(f.read().strip())

    if charging:
        if os.path.exists(NOTIFY_STATE_FILE):
            os.remove(NOTIFY_STATE_FILE)
        return

    if percent <= 10 and (last_notified is None or last_notified > 10):
        msg = f"󱃍 Batería muy baja: {percent}% restante."
        level = 10
    elif percent <= 20 and (last_notified is None or last_notified > 20):
        msg = f"󰁺 Batería baja: {percent}% restante."
        level = 20
    else:
        return

    subprocess.call([
        "dunstify", "-u", "critical",
        "-h", "string:fgcolor:#e67e80",
        "-h", "string:bgcolor:#2b3339",
        "-h", "string:frame_color:#a7c080",
        msg
    ])

    with open(NOTIFY_STATE_FILE, "w") as f:
        f.write(str(level))

def percent():
    percent_value = get_battery_percent()
    charging = get_battery_state() == "charging"
    notify_battery(percent_value, charging)
    return f"{percent_value}%"
