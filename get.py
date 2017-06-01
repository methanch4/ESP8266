############################################################
#                                                          #
#  Kleiner Skript um die benutzung der SDS011 Bibliothek   #
#  zu demonstrieren.                                       #
#                                                          #
#  Author: Siegurt Skoda                                   #
#          sskoda(a)powerbb(dot)info                       #
#                                                          #
#  ver:    0.01 - 01.06.2017                               #
#                                                          #
############################################################

import sys                    # Benötigt für das Auslesen der Übergabeparameter
from SDS011 import sds011     # Die SDS011 Bibliothek.
    
def help():
#{
    print ("")
    print ("get.py [help] [port]")
    print ("[help] ruft diese Hilfeseite auf")
    print ("[port] physikalsicher Name des COM-Prots Ihres Betriebssystems.")
    print ("")
    print ("Beispiele:")
    print ("  Windows:  py get.py COM3")
    print ("  Linux:    py get.py /dev/ttyUSB0")
    print ("")
    print ("Dieses Skript wurde für Python 3.0 oder neue geschrieben. Getestet auf Python 3.5")
    print (sys.version)
    pass
#} def help()
    
    
# Vergebt einem alten C++ Programmierer....
def main():
#{
    
    #überprüfe ob der benötigte Übergabeparameter mit eingegeben wurde
    if((len(sys.argv) < 2)):
    #{
        print ("Zu wenige Parameter.")
        print ("")
        help()
        return
    #}
    
    #überprüfe ob um Hifle gebgen wurde
    if(sys.argv[1] == "help"):
    #{
        help()
        return
    #}
    
    #Initialisere das Objekt das sich um die daten des Sensors kümmert
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
            #{
                print("PM  2.5µm {0:5.1f} µg/m^3".format(data.pm25))
                print("PM 10µm   {0:5.1f} µg/m^3".format(data.pm10))
            #}
            else:
            #{
                print("Übertragungsfehler")
            #}
    except KeyboardInterrupt:
        pass        
#}#def main()

main()