import time
from scapy.all import RadioTap, Dot11, Dot11Beacon, Dot11Elt, sendp, RandMac
import sys, subprocess

# TODO:
# - stav modulu
# - logování
# - cleanup po ukončení

# airmon-ng check kill

# airmon-ng start wlan0
# airmon-ng stop wlan0
#sudo systemctl start NetworkManager

class FakeAPModule:
    def __init__(self):
        self.state = "STOPPED"
        self.ap_ssid = {}
        self.interface = "wlan0"
        self.ap_macs = {}
        self.channel = 6

    def configure(self, networks_dict, interface="wlan0", channel=6):
        self.ap_ssid = networks_dict
        self.interface = interface
        self.channel = channel
        self.ap_macs = {ssid: str(RandMac()) for ssid in networks_dict}

    def start(self):
        self.state = "RUNNING"
        channel_byte = bytes([self.channel])

        try:
            print(f"Turning on monitor mode on interface {self.interface}...")
            subprocess.run(["systemctl", "stop", "NetworkManager"], check=True)
            subprocess.run(["ip", "link", "set", self.interface, "down"], check=True)
            subprocess.run(["iw", self.interface, "set",  "type", "monitor"], check=True)
            subprocess.run(["ip", "link", "set", self.interface, "up"], check=True)
            subprocess.run(["iw", "dev", self.interface, "set", "channel", str(self.channel)], check=True)
            print(f"Monitor mode enabled on {self.interface}.")

        except subprocess.CalledProcessError as e:
            print(f"Error during subprocess execution: {e} on interface {self.interface}.")
            print("Make sure the interface is correct and you started the script with root privileges.")
            return

        try:
            while self.state == "RUNNING":
                for ssid, password in self.ap_ssid.items():
                    mac_address = self.ap_macs[ssid]
                    if password is None:
                        packet = (RadioTap() / 
                                Dot11(type=0, subtype=8, addr1="ff:ff:ff:ff:ff:ff", addr2=mac_address, addr3=mac_address) / 
                                Dot11Beacon(cap="ESS") / 
                                Dot11Elt(ID="SSID", info=ssid) /
                                Dot11Elt(ID="Rates", info=b"\x82\x84\x8b\x96")/
                                Dot11Elt(ID="DSset", info=channel_byte))
                    else:
                        packet = (RadioTap() / 
                                Dot11(type=0, subtype=8, addr1="ff:ff:ff:ff:ff:ff", addr2=mac_address, addr3=mac_address) / 
                                Dot11Beacon(cap="ESS+privacy") / 
                                Dot11Elt(ID="SSID", info=ssid) /
                                Dot11Elt(ID=48, info=b"\x01\x00\x00\x0f\xac\x04\x01\x00\x00\x0f\xac\x04\x01\x00\x00\x0f\xac\x02\x00\x00") /
                                Dot11Elt(ID="Rates", info=b"\x82\x84\x8b\x96")/
                                Dot11Elt(ID="DSset", info=channel_byte))
                    sendp(packet, iface=self.interface, count=1, verbose=False)  

                time.sleep(0.1)

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
            subprocess.run(["systemctl", "start", "NetworkManager"], check=True)
            print(f"Interface {self.interface} successfully reset to managed mode.")

        except subprocess.CalledProcessError as e:
            print(f"Error during subprocess execution: {e} on interface {self.interface}.")
            return




    def status(self):
        print("=" * 30)
        print(f"Module Status:  {self.state}")
        print(f"Interface:     {self.interface}")
        print(f"Running APs:  {len(self.ap_ssid)}")
        for ssid, mac in self.ap_macs.items():
            print(f"  - {ssid} [{mac}]")
        print("=" * 30)


if __name__ == "__main__":
    fake_ap = FakeAPModule()
    fake_ap.configure({"FakeNetwork1": None, "FakeNetwork2": None, "SkibidyRizzler": None, "FakeNetwork3": "12345", "FakeNetwork4": "1234"}, interface="wlan0", channel=6)
    fake_ap.start()
    fake_ap.status()