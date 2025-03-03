import subprocess
import re
def get_connected_devices():
    """Obtiene la lista de dispositivos conectados y sus nombres."""
    try:
        output = subprocess.check_output("bluetoothctl devices Connected", shell=True).decode("utf-8").strip()
        devices = re.findall(r"Device ([0-9A-F:]+) (.+)", output)  # Extrae MAC y nombre
        return devices if devices else None
    except subprocess.CalledProcessError:
        return None

def get_device_type(mac_address):
    """Intenta detectar el tipo de dispositivo según su clase o nombre."""
    try:
        info = subprocess.check_output(f"bluetoothctl info {mac_address}", shell=True).decode("utf-8").strip()
        if "Class: 0x" in info:
            class_match = re.search(r"Class: 0x([0-9A-F]+)", info)
            if class_match:
                device_class = int(class_match.group(1), 16)
                if device_class & 0x200400:  # Audio (auriculares, bocinas)
                    return "󰋋"
                elif device_class & 0x002580:  # Mouse
                    return "󰍽"
                elif device_class & 0x002540:  # Teclado
                    return "⌨️"
        name_match = re.search(r"Name: (.+)", info)
        if name_match:
            name = name_match.group(1).lower()
            if any(x in name for x in ["headphone", "headset", "buds", "airpods"]):
                return "󰋋"
            if any(x in name for x in ["mouse", "mice"]):
                return "󰍽"
            if any(x in name for x in ["keyboard", "keychron", "logitech k"]):
                return "⌨️"
        return ""  # Dispositivo Bluetooth genérico
    except subprocess.CalledProcessError:
        return ""
def bluetooth():
    """Verifica el estado del Bluetooth y los dispositivos conectados."""
    try:
        power_status = subprocess.check_output("bluetoothctl show | grep 'Powered: yes'", shell=True).decode("utf-8").strip()
        bluetooth_on = "󰂯" if power_status else "󰂲"
    except subprocess.CalledProcessError:
        return "󰂲"
    devices = get_connected_devices()
    if devices:
        device_icons = " ".join(get_device_type(mac) for mac, _ in devices)
        return f" {bluetooth_on}   {device_icons}"
    else:
        return f" {bluetooth_on}"
