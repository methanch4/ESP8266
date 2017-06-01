#!/usr/bin/env python3

"""Kleines Skript um die benutzung der SDS011 Bibliothek
zu demonstrieren."""

__author__ = "Siegurt Skoda"
__copyright__ = "Copyright 2017, Siegurt Skoda"
__credits__ = ["Siegurt Skoda"]

__license__ = "GPL-3"
__version__ = "0.0.1"
__maintainer__ = "Siegurt Skoda"
__email__ = "sskoda(a)powerbb(dot)info"
__status__ = "Alpha"


import sys                    # Benötigt für das Auslesen der Übergabeparameter
from SDS011 import sds011     # Die SDS011 Bibliothek.
    
def help():
    """dies ist die Hilfe
    """

    print("""
get.py [help] [port]
[help] ruft diese Hilfeseite auf
[port] physikalischer Name des COM-Prots Ihres Betriebssystems.

Beispiele:
  Windows:  py get.py COM3
  Linux:    py get.py /dev/ttyUSB0

Dieses Skript wurde für Python 3.0 oder neuer geschrieben. Getestet auf Python 3.5

Es läuft gerade Python %s
"""%(sys.version))

 
def main():
    # überprüfe ob der benötigte Übergabeparameter mit eingegeben wurde
    if((len(sys.argv) < 2)):
        print("Zu wenige Parameter.")
        help()
        return
    
    # überprüfe ob um Hifle gebgen wurde
    if((sys.argv[1] == "-h") or (sys.argv[1] == "--help")):
        help()
        return
    
    # Initialisere das Objekt das sich um die daten des Sensors kümmert
    sds = sds011(sys.argv[1])
    
    # Endlosschleife, die mit STRG+C ohne Abbruchbedinung beenden lässt
    print("Dieses Skript wird mit STRG+C unterbrochen.")
    try:
        while True:
            print()
            
            # Rufe aus der sds011 Klasse ein datenpacket ab. dieser Wartet so lange
            # bis der Sensor ein neues Datenpacket liefert.
            # Die Rückgabe ist eine neue Instanz der Klasse sds011_data
            data = sds.get_data()
            
            # Hat die übertragung geklappt?
            if(data.status == 0):
                print("PM  2.5 µm {0:5.1f} µg/m^3".format(data.pm25))
                print("PM 10   µm {0:5.1f} µg/m^3".format(data.pm10))
            else:
                print("Übertragungsfehler")

    except KeyboardInterrupt:
        pass        

main()