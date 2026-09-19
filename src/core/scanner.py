"""
scanner.py
-----------
Tenhle modul umí "poslouchat" Wi-Fi provoz v okolí a najít tak
seznam sítí (access pointů), které jsou v dosahu.

Základní princip (pro ty, co vidí Scapy poprvé):

  * Wi-Fi karta se musí přepnout do tzv. MONITOR MÓDU. V běžném módu
    karta poslouchá jen provoz určený přímo jí, v monitor módu ale
    "slyší" úplně všechno kolem sebe.
  * Access pointy (routery) samy od sebe pravidelně vysílají tzv.
    BEACON rámce - něco jako "Ahoj, jsem síť XY, jedu na kanálu 6,
    mám/nemám heslo...". Kromě toho odpovídají tzv. PROBE RESPONSE
    rámci, když se jich někdo zeptá "kdo tu je?".
  * My si tyhle dva typy rámců odchytáváme funkcí sniff() a z
    každého vytáhneme informace, které nás zajímají.
"""

import json
from dataclasses import dataclass, asdict
import subprocess
import sys

from rich.console import Console
from rich.table import Table
from scapy.all import sniff, Dot11, Dot11Elt, Dot11Beacon, Dot11ProbeResp, RadioTap


@dataclass
class Network:
    """Jedna nalezená Wi-Fi síť a informace o ní."""
    ssid: str          # jméno sítě
    bssid: str         # MAC adresa access pointu
    channel: int        # Wi-Fi kanál (1-13 na 2.4 GHz)
    encryption: str     # OPEN / WEP / WPA / WPA2
    signal: int          # síla signálu v dBm (čím blíž k 0, tím lepší)


class WifiScanner:
    """Skenuje okolí a hledá Wi-Fi sítě pomocí Scapy."""

    def __init__(self, interface: str, timeout: int = 15):
        self.interface = interface   # jméno síťové karty, např. "wlan0"
        self.timeout = timeout       # jak dlouho (v sekundách) budeme skenovat
        self.networks = {}           # sem ukládáme nalezené sítě (klíč = BSSID)
        self.console = Console()

    # ------------------------------------------------------------------
    # Monitor mód
    # ------------------------------------------------------------------

    def enable_monitor_mode(self):
        """Přepne síťovou kartu do monitor módu pomocí příkazů ip a iw."""
        self.console.print(f"[yellow]Enabling monitor mode on {self.interface}...[/yellow]")
        try:
            # wpa_supplicant by nám mohl do monitor módu kecat, tak ho vypneme
            subprocess.run(["sudo", "pkill", "wpa_supplicant"], stderr=subprocess.DEVNULL)

            subprocess.run(["sudo", "ip", "link", "set", self.interface, "down"], check=True)
            subprocess.run(["sudo", "iw", "dev", self.interface, "set", "type", "monitor"], check=True)
            subprocess.run(["sudo", "ip", "link", "set", self.interface, "up"], check=True)

            self.console.print(f"[green]Monitor mode enabled on {self.interface}.[/green]")
        except subprocess.CalledProcessError as e:
            self.console.print(f"[red]Failed to enable monitor mode: {e}[/red]")
            self.console.print("[red]Please ensure you have the necessary permissions and that the interface exists.[/red]")
            sys.exit(1)

    def disable_monitor_mode(self):
        """Vrátí síťovou kartu zpátky do běžného (managed) módu."""
        self.console.print(f"[yellow]Disabling monitor mode on {self.interface}...[/yellow]")
        try:
            subprocess.run(["sudo", "ip", "link", "set", self.interface, "down"], check=True)
            subprocess.run(["sudo", "iw", "dev", self.interface, "set", "type", "managed"], check=True)
            subprocess.run(["sudo", "ip", "link", "set", self.interface, "up"], check=True)

            self.console.print(f"[green]Monitor mode disabled on {self.interface}.[/green]")
        except subprocess.CalledProcessError as e:
            self.console.print(f"[red]Failed to disable monitor mode: {e}[/red]")
            sys.exit(1)

    # ------------------------------------------------------------------
    # Zpracování zachycených rámců
    # ------------------------------------------------------------------

    def packet_handler(self, packet):
        """
        Tahle metoda se zavolá pro úplně KAŽDÝ zachycený rámec.
        Naším úkolem je zjistit, jestli nás zajímá, a pokud ano,
        vytáhnout z něj informace o síti.
        """
        # Dot11 je základní vrstva všech Wi-Fi (802.11) rámců.
        # Pokud ji rámec nemá, vůbec to není Wi-Fi provoz a nezajímá nás.
        if not packet.haslayer(Dot11):
            return

        # type=0   -> "management" rámec
        # subtype=8 -> Beacon (AP se pravidelně sám hlásí)
        # subtype=5 -> Probe Response (AP odpovídá na dotaz "kdo tu je?")
        is_beacon_or_probe_response = packet.type == 0 and packet.subtype in (8, 5)
        if not is_beacon_or_probe_response:
            return

        # addr2 je v těchto rámcích MAC adresa vysílajícího access pointu = BSSID.
        bssid = packet[Dot11].addr2
        if not bssid or bssid in self.networks:
            # Buď BSSID chybí, nebo tuhle síť už máme uloženou - nic dalšího neděláme.
            return

        ssid = self._extract_ssid(packet)
        channel, encryption = self._extract_channel_and_encryption(packet)
        signal = self._extract_signal(packet)

        self.networks[bssid] = Network(
            ssid=ssid,
            bssid=bssid,
            channel=channel,
            encryption=encryption,
            signal=signal,
        )

    def _extract_ssid(self, packet):
        """
        Vytáhne jméno sítě (SSID).

        SSID je uložené v prvním "Information Elementu" (Dot11Elt) v
        rámci - Scapy nám ho dá jednoduše přes packet[Dot11Elt].info.
        """
        if not packet.haslayer(Dot11Elt):
            return "<neznámé jméno>"

        raw_ssid = packet[Dot11Elt].info
        if not raw_ssid:
            return "<hidden>"  # skrytá síť - AP schválně posílá prázdné jméno

        try:
            return raw_ssid.decode("utf-8").strip() or "<hidden>"
        except UnicodeDecodeError:
            return "<neplatné jméno>"

    def _extract_channel_and_encryption(self, packet):
        """
        Projde všechny "Information Elementy" (Dot11Elt) v rámci a najde
        v nich kanál a typ šifrování.

        Rámec je poskládaný z několika Dot11Elt "kostiček" za sebou -
        každá má svoje ID (co obsahuje) a info (samotná data). Projdeme
        je jednu po druhé, dokud nedojdeme na konec.
        """
        channel = 0
        encryption = "OPEN"  # dokud nenarazíme na nic jiného, bereme síť jako otevřenou

        element = packet[Dot11Elt]
        while isinstance(element, Dot11Elt):
            if element.ID == 3:
                # ID 3 = "DSset" = na tomhle kanálu síť běží
                try:
                    channel = int(element.info[0])
                except (TypeError, IndexError):
                    pass

            elif element.ID == 48:
                # ID 48 = "RSN" element = síť používá WPA2 (případně WPA3)
                encryption = "WPA2"

            elif element.ID == 221 and element.info.startswith(b"\x00P\xf2\x01\x01\x00"):
                # Konkrétní vendor-specific element používaný staršími WPA sítěmi
                if encryption == "OPEN":
                    encryption = "WPA"

            element = element.payload  # posuneme se na další "kostičku"

        if encryption == "OPEN" and self._has_privacy_bit(packet):
            # Žádný z výše uvedených prvků jsme nenašli, ale AP i tak
            # říká "je potřeba heslo" - nejspíš jde o starou síť se šifrováním WEP.
            encryption = "WEP"

        return channel, encryption

    def _has_privacy_bit(self, packet):
        """
        Zkontroluje bit "privacy" v capability poli rámce - ten říká,
        jestli síť vyžaduje heslo. Rámec může být Beacon nebo Probe
        Response, tak zkusíme obě varianty.
        """
        if packet.haslayer(Dot11Beacon):
            capability = packet[Dot11Beacon].sprintf("%Dot11Beacon.cap%")
        elif packet.haslayer(Dot11ProbeResp):
            capability = packet[Dot11ProbeResp].sprintf("%Dot11ProbeResp.cap%")
        else:
            return False

        return "privacy" in capability

    def _extract_signal(self, packet):
        """
        Vrátí sílu signálu v dBm. Tahle informace přichází z RadioTap
        hlavičky, kterou k rámci přidává naše síťová karta.
        """
        if packet.haslayer(RadioTap):
            # getattr() s výchozí hodnotou None - pole totiž může existovat,
            # ale u konkrétního rámce nemusí být vyplněné.
            signal = getattr(packet[RadioTap], "dBm_AntSignal", None)
            if signal is not None:
                return int(signal)
        return -100  # neznámý / velmi slabý signál

    # ------------------------------------------------------------------
    # Skenování a výstup
    # ------------------------------------------------------------------

    def scan_networks(self):
        """Spustí samotné skenování na self.timeout sekund."""
        self.networks.clear()

        with self.console.status(f"[bold green]Scanning on {self.interface} for {self.timeout}s...", spinner="dots"):
            sniff(iface=self.interface, prn=self.packet_handler, timeout=self.timeout, store=False)

        return self._sorted_networks()

    def display_networks(self):
        """Vypíše nalezené sítě do hezké tabulky v terminálu."""
        sorted_networks = self._sorted_networks()

        if not sorted_networks:
            self.console.print(f"[red]No networks found on {self.interface}.[/red]")
            return

        table = Table(title="WiFi Scan Results")
        table.add_column("ID", justify="right", style="cyan", no_wrap=True)
        table.add_column("SSID", style="magenta")
        table.add_column("BSSID", style="green")
        table.add_column("CH", justify="right")
        table.add_column("ENC", justify="left")
        table.add_column("PWR", justify="right")

        for idx, network in enumerate(sorted_networks, start=1):
            table.add_row(
                str(idx),
                network.ssid,
                network.bssid,
                str(network.channel),
                network.encryption,
                f"{network.signal} dBm",
            )

        self.console.print(table)

    def export_scan(self, filename="scan_results.json"):
        """Uloží nalezené sítě do JSON souboru."""
        if not self.networks:
            return

        sorted_networks = self._sorted_networks()
        with open(filename, "w") as f:
            json.dump([asdict(net) for net in sorted_networks], f, indent=4)

    def _sorted_networks(self):
        """Vrátí nalezené sítě seřazené od nejsilnějšího signálu."""
        return sorted(self.networks.values(), key=lambda net: net.signal, reverse=True)