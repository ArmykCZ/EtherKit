import scapy

# TODO:
# - stav modulu
# - logování
# - cleanup po ukončení


class FakeAPModule:
    def __init__(self):
        self.state = "stopped"
        self.ap_ssid = []

    def configure(self):
        self.ap_ssid = ["FakeAP", "EvilTwin", "FreeWiFi"]
        print(f"Konfigurace načtena. SSID: {self.ap_ssid}")


    def start(self):
        ...

    def stop(self):
        ...

    def status(self):
        ...