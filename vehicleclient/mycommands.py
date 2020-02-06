from obd import OBDCommand
from obd.protocols import ECU
from obd.utils import bytes_to_int

def gearDecoder(messages):
    data = messages[0].data
    
    # Odseknúť službu a PID 
    data = data[2:]
    
    # Konvertovať bajty na číslo
    gear = bytes_to_int(data) / 4
    
    return gear


# PID (A4, resp. 01A4) a počet bajtov (4) nájdený tu:
# https://en.wikipedia.org/wiki/OBD-II_PIDs
# Aj pri zaradenej rýchlosti však dostávame hodnotu 0.
# Skúšali sme aj iné (kvalitnejšie) OBD skenery,
# avšak pri nich sa aplikácia ani nespustila
GEAR = OBDCommand("GEAR", "Transmission Actual Gear",
                  b"01A4", 4, gearDecoder, ECU.ALL, False)
