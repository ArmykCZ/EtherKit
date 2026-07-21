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

    def configure(self, networks_dict, interface):
        self.ap_ssid = networks_dict
        self.interface = interface

    def start(self):
        self.state = "RUNNING"

        try:
            print(f"Turning off monitor mode on interface {self.interface}...")
            subprocess.run(["ip", "link", "set", self.interface, "down"], check=True)
            subprocess.run(["iw", self.interface, "set",  "type", "monitor"], check=True)
            subprocess.run(["ip", "link", "set", self.interface, "up"], check=True)
            print(f"Monitor mode disabled on {self.interface}.")

        except subprocess.CalledProcessError as e:
            print(f"Error during subprocess execution: {e} on interface {self.interface}.")
            print("Make sure the interface is correct and you started the script with root privileges.")
            return


        mac_adress = "00:11:22:33:44:55"

        try:
            while self.state == "RUNNING":
                for ssid, password in self.ap_ssid.items():
                    if password is None:
                        packet = (RadioTap() / 
                                Dot11(type=0, subtype=8, addr1="ff:ff:ff:ff:ff:ff", addr2=mac_adress, addr3=mac_adress) / 
                                Dot11Beacon() / 
                                Dot11Elt(ID="SSID", info=ssid))
                        
                        sendp(packet, iface=self.interface, count=1, verbose=False)

                time.sleep(0.5)

        except KeyboardInterrupt:
            print("\n[!] Turning off fake APs...")
            self.stop()

    def stop(self):
        if self.state == "STOPPED":
            print("Modul is already stopped.")
            return
        self.state = "STOPPED"

        try:
            print(f"Switching interface {self.interface} back to managed mode...")
            subprocess.run(["ip", "link", "set", self.interface, "down"], check=True)
            subprocess.run(["iw", self.interface, "set",  "type", "managed"], check=True)
            subprocess.run(["ip", "link", "set", self.interface, "up"], check=True)
            print(f"Interface {self.interface} successfully reset to managed mode.")

        except subprocess.CalledProcessError as e:
            print(f"Error during subprocess execution: {e} on interface {self.interface}.")
            return




    def status(self):
        ...


if __name__ == "__main__":
    fake_ap = FakeAPModule()
    fake_ap.configure({"FakeNetwork1": "password123", "FakeNetwork2": "password456"})
    fake_ap.start()