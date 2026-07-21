import os
import time
import json
import datetime
from pathlib import Path
import sys, subprocess

# TODO:
# - jednotný error handler
# - exception management
# - config loader


def check_platform():
        if sys.platform.startswith('win'):
            print("Program is not supported on Windows. Please use Linux.")
            sys.exit(1) #bruh
        else:
            subprocess.run('clear', shell=True)
    

def timestamp():
    #windows does not support ":" in file names, so we use "-" instead
    hour = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    print(hour)
    return hour

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
    directories = [
        "docs",
        "captures",
        "logs",
    ]

    logs_files = [
        "test.txt",
        "test.json",
    ]

    for directory in directories:
        directory = Path.cwd() / directory
        if directory.exists() and directory.is_dir():
            print(f"Directory {directory} exists")
        else:
            print(f"Directory {directory} does not exist, creating it")
            directory.mkdir(parents=True, exist_ok=True)
    
    for file in logs_files:
        file = Path.cwd() / "logs" / file
        if file.exists() and file.is_file():
            print(f"File {file} exists")
        else:
            print(f"File {file} does not exist, creating it")
            file.touch()
    

def check_utils():
    check_platform()
    check_dependencies()
    timestamp()
    save_json()
    load_json()
    print("All utility functions are working correctly.")




if __name__ == "__main__":
    # Testování funkcí
    check_utils()