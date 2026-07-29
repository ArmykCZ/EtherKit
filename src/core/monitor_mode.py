import subprocess

class MonitorMode:
    def __init__(self, interface="wlan0"):
        self.interface = interface

    def enable(self):
        try:
            print(f"Turning on monitor mode on interface {self.interface}...")
            subprocess.run(["systemctl", "stop", "NetworkManager"], check=True)
            subprocess.run(["ip", "link", "set", self.interface, "down"], check=True)
            subprocess.run(["iw", self.interface, "set",  "type", "monitor"], check=True)
            subprocess.run(["ip", "link", "set", self.interface, "up"], check=True)
            print(f"Monitor mode enabled on {self.interface}.")
        except subprocess.CalledProcessError as e:
            print(f"Error during subprocess execution: {e} on interface {self.interface}.")
            print("Make sure the interface is correct and you started the script with root privileges.")
            return

    def disable(self):
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
