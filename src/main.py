import argparse
from core.scanner import WifiScanner
from core.utils import *
from core.utils import check_utils
from attacks.fake_ap import FakeAPModule


# TODO:
# - vytvořit CLI argumenty
# - přidat --interface
# - přidat --scan
# - přidat --report
# - přidat verbose mód


def banner():
    """
    ASCII logo EtherKit
    """

def parse_arguments():
    """
    CLI argumenty
    """

def main_menu():
    """
    Hlavní menu programu
    """

def load_modules():
    """
    Načte dostupné moduly
    """
def fake_ap_setting():
    networks_dict =  {
        "Fake_AP": None,
        "Evil_Twin": 12345,
        "FreeWiFi": "Password123",
        "Open_Network": None
    }
    attack = FakeAPModule()
    attack.configure(networks_dict)
    

import argparse

# 1. Vytvoření parseru
parser = argparse.ArgumentParser(description="Můj skript")

# 2. Přidání parametru
parser.add_argument("jmeno", help="Zadej své jméno")

# 3. Zpracování a vypsání
args = parser.parse_args()
print(f"Ahoj, {args.jmeno}!")