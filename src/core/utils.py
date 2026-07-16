import os
import time
import json
import datetime
from pathlib import Path
import sys 
import subprocess

# TODO:
# - jednotný error handler
# - exception management
# - config loader



def clear_terminal():
    if sys.platform.startswith('win'):
        subprocess.run('cls', shell=True)
    else:
        subprocess.run('clear', shell=True)

def timestamp():
    #windows does not support ":" in file names, so we use "-" instead
    hour = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    print(hour)
    return hour


def create_directory():
    #test file
    file = (Path.cwd() / "logs" / "test.txt")
    json_file = (Path.cwd() / "logs" / "test.json")

    #the / automatically take it as a root directory
    #Path.cwd() gives the current working directory
    directory = (Path.cwd() / "logs").resolve() 
    if directory.exists() and directory.is_dir():
        print("Directory exists")
        if file.exists() and file.is_file():
            print("file exists")
        else:
            print("file doesnt exist, creating file")
            file.touch()
        if json_file.exists() and json_file.is_file():
            print("JSON file exists")
        else:
            print("JSON file doesnt exist, creating file")
            json_file.touch()
    else:
        print("path doesnt exist, creating directory and files")
        directory.mkdir(parents=True, exist_ok=True)
        file.touch()
        json_file.touch()


#data func
def save_json():
    test_data = [
    {
        "ssid": "Skola_Wifi_Free",
        "bssid": "00:11:22:33:44:55",
        "signal": -65,
        "encryption": "WPA2"
    },
    {
        "ssid": "Tajny_Urad_VPN",
        "bssid": "AA:BB:CC:DD:EE:FF",
        "signal": -82,
        "encryption": "WPA3"
    }
]



    file = Path.cwd() / "logs" / "test.json"
    with open(file, "w") as f:
        json.dump(test_data, f, indent=4)



def load_json():
    file = Path.cwd() /"logs" / "test.json"
    with open(file, "r") as f:
        data = json.load(f)
        print(data)
        return data


def check_dependencies():
    """
    Kontrola potřebných programů
    """





if __name__ == "__main__":
    # Testování funkcí
    clear_terminal()
    timestamp()
    create_directory()
    save_json()
    load_json()