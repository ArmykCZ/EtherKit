
MAC_VENDORS = {
        # Routery & Síťové prvky
    "F4:F5:DB": "TP-Link",
    "50:C7:BF": "TP-Link",
    "E8:48:B8": "TP-Link",
    "C8:3A:35": "Tenda",
    "04:95:E6": "MikroTik",
    "B8:69:F4": "MikroTik",
    "00:11:32": "Synology",
    "00:18:E7": "ASUS",
    "04:D4:C4": "ASUS",
    "00:14:D1": "TrendsNet / Netgear",
    "28:FF:3C": "Netgear",
    "00:0D:67": "Cisco",
    "00:1A:A1": "Cisco / Linksys",

    # Mobilní zařízení & Tablety
    "A4:C3:F0": "Apple",
    "FC:EC:DA": "Apple",
    "BC:D2:C7": "Apple",
    "F4:0F:24": "Apple",
    "CC:07:AB": "Samsung",
    "8C:7A:3C": "Samsung",
    "50:85:69": "Samsung",
    "64:09:80": "Xiaomi",
    "18:59:36": "Xiaomi",
    "C8:02:10": "Huawei",

    # Wi-Fi čipy v notebooku & PC (Intel, Realtek, Broadcom)
    "00:1E:67": "Intel",
    "A4:4E:31": "Intel",
    "48:89:E7": "Intel",
    "00:E0:4C": "Realtek",
    "52:54:00": "Realtek / QEMU Virtual",
    "00:10:18": "Broadcom",
    "00:03:7F": "Atheros / Qualcomm"
    }

def get_vendor(mac_address):
    if not mac_address or len(mac_address) < 8:
        return "Invalid MAC"
    
    # Získám prvních 8 znaků v velkých písmenech (např. "F4:F5:DB")
    prefix = mac_address[:8].upper()
    
    # .get() najde klíč, a pokud neexistuje, vrátí výchozí hodnotu "Unknown"
    return MAC_VENDORS.get(prefix, "Unknown / Random MAC")
    