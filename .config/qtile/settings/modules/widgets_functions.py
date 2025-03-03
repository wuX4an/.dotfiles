import subprocess
import socket
import re
# import struct


#### GET IP ####
def get_local_ip():
    try:
        command="ip -4 addr show | grep 'inet ' | grep -v '127.0.0.1' | awk '{print $2}' | cut -d/ -f1"
        result = subprocess.check_output(command, shell=True)
        return result.decode("utf-8").strip()
    except Exception:
        return "No IP"

##### CHECK INTERNET #####
def check_internet():
    try:
        socket.setdefaulttimeout(3)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
        internet = "󰇧"
    except socket.error:
        internet = "󰇨"
    try:
        result = subprocess.check_output("ip link show | grep 'state UP'", shell=True).decode("utf-8").strip()
        if result:
            network = "󰤨"
        else:
            network = "󰤮 else"
    except Exception:
        return "󰤮ex"

    return f" {network}   {internet} "


##### CHECK BLUETOOTH DEVICES #####
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
def check_bluetooth():
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

#### CAVA ####
# def get_audio_activity():
#     """Detecta la intensidad del sonido con ALSA y lo muestra como una barra tipo Cava"""
#     try:
#         # Ejecutamos arecord y capturamos 1 segundo de audio en formato binario
#         process = subprocess.Popen(
#             ["arecord", "-f", "S16_LE", "-d", "1", "-q"],  # "-d 1" graba 1 segundo sin mostrar mensajes
#             stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
#         )
#
#         # Leer los datos binarios (1 segundo de audio, 44.1kHz, 16 bits, 2 bytes por muestra)
#         raw_data = process.stdout.read(44100 * 2)  # 44.1kHz * 2 bytes por muestra * 1 segundo
#         process.stdout.close()
#
#         if not raw_data:
#             return "===#==="  # No hay audio
#
#         # Desempaquetamos los datos binarios en enteros de 16 bits
#         audio_data = struct.unpack("<" + "h" * (len(raw_data) // 2), raw_data)
#
#         # Calculamos la amplitud media absoluta
#         volume = sum(abs(sample) for sample in audio_data) / len(audio_data)
#
#         # Mapear los valores de volumen a barras tipo Cava
#         if volume < 100:
#             return "===#==="  # Silencio o muy bajo
#         elif volume < 750:
#             return "==<#>=="  # Bajo
#         elif volume < 1500:
#             return "=<=#=>="  # Medio
#         else:
#             return "<==#==>"  # Alto
#
#     except Exception:
#         return "===#==="  # Si hay un error, asumimos silencio


#### GET VOLUME

def get_volume():
    try:
        # Obtener el volumen y estado de mute con amixer
        output = subprocess.check_output("amixer get Master", shell=True).decode("utf-8")

        # Extraer el porcentaje de volumen
        volume_match = re.search(r"\[(\d+)%\]", output)
        volume = int(volume_match.group(1)) if volume_match else 0

        # Extraer el estado de mute
        mute_match = re.search(r"\[(on|off)\]", output)
        is_muted = mute_match and mute_match.group(1) == "off"

        # Dibujar la barra de volumen
        cava = "█" * (volume // 10) + "░" * (10 - (volume // 10))

        if is_muted:
            return f"🔇 [{cava}] 0%"  # Muteado
        return f"🔊 [{cava}] {volume}%"

    except Exception:
        return "❌ Error Volumen"

