import socket
import subprocess

def wifi():
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
            return "󰤮"
    except Exception:
        return "󰤮"

    return f" {network}   {internet} "
