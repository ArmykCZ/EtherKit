
MAC_VENDORS = {
    # Routery & Síťové prvky
    "F4:F5:DB": "TP-Link",
    "50:C7:BF": "TP-Link",
    "E8:48:B8": "TP-Link",
    "00:0A:EB": "TP-Link",  
    "80:AE:54": "TP-Link", 
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
    "1C:22:26": "Cisco",  
    "00:15:6D": "Ubiquiti", 
    "E0:63:DA": "Ubiquiti",  
    "FC:EC:DA": "Ubiquiti", 

    # Mobilní zařízení & Tablety
    "A4:C3:F0": "Apple",
    "FC:EC:DA": "Apple",
    "BC:D2:C7": "Apple",
    "F4:0F:24": "Apple",
    "A4:83:E7": "Apple",  
    "00:0D:93": "Apple",  
    "CC:07:AB": "Samsung",
    "8C:7A:3C": "Samsung",
    "50:85:69": "Samsung",
    "00:00:F0": "Samsung",  
    "00:07:AB": "Samsung", 
    "64:09:80": "Xiaomi",
    "18:59:36": "Xiaomi",
    "C8:02:10": "Huawei",
    "3C:5A:B4": "Google",  

    # Wi-Fi čipy v notebooku & PC (Intel, Realtek, Broadcom)
    "00:1E:67": "Intel",
    "A4:4E:31": "Intel",
    "48:89:E7": "Intel",
    "00:E0:4C": "Realtek",
    "52:54:00": "Realtek / QEMU Virtual",
    "00:10:18": "Broadcom",
    "00:03:7F": "Atheros / Qualcomm",

    # IoT, minipočítače a Virtualizace (Nové kategorie)
    "B8:27:EB": "Raspberry Pi",  
    "DC:A6:32": "Raspberry Pi",  
    "00:50:56": "VMware",  
    "00:0C:29": "VMware"   
}

def get_vendor(mac_address):
    if not mac_address or len(mac_address) < 8:
        return "Invalid MAC"
    
    prefix = mac_address[:8].upper()
    
    return MAC_VENDORS.get(prefix, "Unknown / Random MAC")
    