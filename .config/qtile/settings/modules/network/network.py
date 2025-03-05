import subprocess


def scan():
    scan = subprocess.Popen(
        "nmcli device wifi", 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True
    )
    output, errors = scan.communicate()

    nmcli_output = output.strip().replace("*", " ")

    wifi_list = []

    for line in nmcli_output.splitlines():
        # Ignorar líneas vacías y encabezados
        if line.startswith("IN-USE") or line.strip() == "":
            continue

        parts = line.split()

        wifi_info = {
            'SSID': parts[1],
            'RATE': f"{parts[4]} {parts[5]}",
            'BARS': parts[7],  
            'SECURITY': ' '.join(parts[8:]),
        }
        wifi_list.append(wifi_info)

    return wifi_list
# print(scan())
# for wifi in scan():
#     print(wifi)

def connect(ssid, password):
    try:
        result = subprocess.run(
            ["nmcli", "device", "wifi", "connect", ssid],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode == 0:
            return f"Conectado exitosamente a {ssid} sin contraseña."
        else:
            # Si falla la conexión sin contraseña, intentamos con la contraseña
            if password:
                result = subprocess.run(
                    ["nmcli", "device", "wifi", "connect", ssid, "password", password],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                if result.returncode == 0:
                    return [0, f"Conectado exitosamente a {ssid} con la contraseña proporcionada."]
                else:
                    return [1, f"Error al conectar a {ssid} con la contraseña: {result.stderr.strip()}"]
            else:
                return [1, f"La red {ssid} está protegida por contraseña. No se proporcionó una contraseña."]

    except Exception as e:
        return f"Error al intentar conectar: {str(e)}"
# print(connect("LIB-6378456"))

def current_conection():
    current_connection = subprocess.Popen(
        "nmcli device wifi show-password | grep SSID | awk -F: '{print $2}'",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True
    )
    output, errors = current_connection.communicate()
    if errors:
        return [1, None]
    else:
        return [0, output.strip()]
# print(current_conection())

def show_password():
    show_password = subprocess.Popen(
        "nmcli device wifi show-password | head -n 3 | tail -n 1 | awk -F: '{print $2}'",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True
    )
    output, errors = show_password.communicate()
    if errors:
        return errors
    else:
        return output.strip()
# print(show_password())

def show_security():
    show_security = subprocess.Popen(
        "nmcli device wifi show-password | head -n 2 | tail -n 1 | awk -F: '{print $2}'",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True
    )
    output, errors = show_security.communicate()
    if errors:
        return errors
    else:
        return output.strip()

