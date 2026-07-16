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
    hour = datetime.datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    print(hour)


def create_directory():
    #the / automatically take it as a root directory
    #Path.cwd() gives the current working directory
    path = (Path.cwd() / "logs").resolve() 
    if path.exists() and path.is_dir():
        print(path.resolve())
    else:
        print("neexistuje" + str(path.resolve()))

def save_json(data,path):
    """
    Uložení výsledků
    """


def load_json(path):
    """
    Načtení výsledků
    """


def check_dependencies():
    """
    Kontrola potřebných programů
    """





if __name__ == "__main__":
    # Testování funkcí
    clear_terminal()
    timestamp()
    create_directory()