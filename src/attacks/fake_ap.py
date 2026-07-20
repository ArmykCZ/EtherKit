import time
from scapy.all import RadioTap, Dot11, Dot11Beacon, Dot11Elt, sendp
import sys, subprocess

# TODO:
# - stav modulu
# - logování
# - cleanup po ukončení


class FakeAPModule:
    def __init__(self):
        self.state = "STOPPED"
        self.ap_ssid = {}

    def configure(self, networks_dict, interface="wlan0"):
        self.ap_ssid = networks_dict
        self.interface = interface

        if sys.platform.startswith('win'):
            subprocess.run('cls', shell=True)
        else:
            subprocess.run('clear', shell=True)

    def start(self):
        self.state = "RUNNING"
        mac_adress = "00:11:22:33:44:55"

        try:
            while self.state == "RUNNING":
                for ssid, password in self.ap_ssid.items():
                    print(f"Spouštím falešný AP s SSID: {ssid} a heslem: {password}")

                    if password is None:
                        packet = (RadioTap() / Dot11(type=0, subtype=8, addr1="ff:ff:ff:ff:ff:ff", addr2=mac_adress, addr3=mac_adress) / 
                                Dot11Beacon() / Dot11Elt(ID="SSID", info=ssid))
                        sendp(packet, iface=self.interface, count=1, verbose=False)
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("Zastavuji falešný AP modul...")

    def stop(self):
        if self.state == "STOPPED":
            print("Modul je již zastaven.")
            return
        self.state = "STOPPED"



    def status(self):
        ...


if __name__ == "__main__":
    fake_ap = FakeAPModule()
    fake_ap.configure({"FakeNetwork1": "password123", "FakeNetwork2": "password456"})
    fake_ap.start()