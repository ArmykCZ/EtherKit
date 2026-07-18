import scapy

# TODO:
# - stav modulu
# - logování
# - cleanup po ukončení


class FakeAPModule:
    def __init__(self):
        self.state = "stopped"
        self.ap_ssid = {}

    def configure(self, networks_dict):
        self.ap_ssid = networks_dict
        print(f"Konfigurace načtena. SSID: {self.ap_ssid}")


    def start(self):
        for ssid, password in self.ap_ssid.items():
            print("Test")

    def stop(self):
        ...

    def status(self):
        ...