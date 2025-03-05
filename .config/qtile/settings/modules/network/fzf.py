import os
import subprocess
import time
from getpass import getpass
import network

def menu():

    items = network.scan()
    dir_path = '/tmp/net/'
    os.makedirs(dir_path, exist_ok=True)

    for wifi in items:
        ssid = wifi['SSID']
        file_path = os.path.join(dir_path, f"{ssid}")
        data = f"SSID: {wifi['SSID']}\nRATE: {wifi['RATE']}\nSIGNAL: {wifi['BARS']}\nSECURITY: {wifi['SECURITY']}\n\n"
        
        with open(file_path, 'w') as file:
            file.write(data)

    current_conection = network.current_conection()
    saved_password = network.show_password()
    security = network.show_security()
    qr = subprocess.Popen(
        f"qr --ascii 'WIFI:T:{security};S:{current_conection[1]};P:{saved_password};;'",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True
    )
    output, errors = qr.communicate()


    lines = output.splitlines()

    # Eliminar los bordes izquierdo y derecho
    lines = [line[1:-1] for line in lines] 

    output = '\n'.join(lines)
    lines = output.splitlines()

    # Eliminar los bordes superior e inferior
    if len(lines) > 2:
        output = '\n'.join(lines[1:-1])
    else:
        output = ''
    with open(f"{dir_path}/{current_conection[1]}", 'a') as file:
        file.write("\033[47m\033[30m" + output + "\033[0m")

    fzf = f"cd {dir_path} && fzf --header='Networks:{" "*10}Current: {current_conection[1]}' --preview 'cat {{}}' --bind 'focus:transform-preview-label:echo {{+}}'"
    ssids = [item['SSID'] for item in items]

    process = subprocess.Popen(
        fzf,
        shell=True,
        text=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    ssids = "\n".join(ssids)
    stdout, stderr = process.communicate(input=ssids)
    selected_item = stdout.strip()

    if process.returncode == 0:
        connect = network.connect(selected_item, "")
        if connect[0] == 0:
            print(f"Conectado correctamente a {selected_item}")
            time.sleep(1)
        elif connect[0] == 1:
            again = False
            while connect[0] == 1:
                if not again:
                    password = getpass("Enter password: ")
                    connect = network.connect(selected_item, password)
                    if connect[0] == 0:
                        print(f"Conectado correctamente a {selected_item}")
                        time.sleep(1)
                    again = True
                else:
                    password = getpass("Try again: ")
                    connect = network.connect(selected_item, password)
                    if connect[0] == 0:
                        print(f"Conectado correctamente a {selected_item}")
                        time.sleep(1)

menu()
