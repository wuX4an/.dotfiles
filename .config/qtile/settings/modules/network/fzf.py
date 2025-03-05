import network
import subprocess
from getpass import getpass
import time
import os

def menu():

    items = network.scan()
    dir_path = '/tmp/net/'
    os.makedirs(dir_path, exist_ok=True)

    for wifi in items:
        ssid = wifi['SSID']
        file_path = os.path.join(dir_path, ssid)
        data = f"SSID: {wifi['SSID']}\nRATE: {wifi['RATE']}\nSIGNAL: {wifi['BARS']}\nSECURITY: {wifi['SECURITY']}"
        with open(file_path, 'w') as file:
            file.write(data)

    fzf = "cd /tmp/net && fzf --header='Networks:' --preview 'cat {}' --bind 'focus:transform-preview-label:echo {+}'"
    # items = ["item_1", "item_2", "item_3", "item_4"]
    ssids= [item['SSID'] for item in items]

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
        # print("funcionó:", selected_item)
        connect = network.connect(selected_item, "")
        if connect[0] == 0:
            print(f"Conectado correctamente a {selected_item}")
            time.sleep(1)
        elif connect[0] == 1:
            again = False
            while connect[0] == 1:
                if again == False:
                    password = getpass("Enter password: ")
                    connect = network.connect(selected_item, password)
                    if connect[0] == 0:
                        print(f"Conectado correctamente a {selected_item}")
                        time.sleep(1)
                    again = True
                elif again == True:
                    password = getpass("Try again: ")
                    connect = network.connect(selected_item, password)
                    if connect[0] == 0:
                        print(f"Conectado correctamente a {selected_item}")
                        time.sleep(1)
menu()
