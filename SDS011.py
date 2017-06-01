"""Ein Python Script um die Daten aus dem SDS011 Sensor"""

__author__ = "Siegurt Skoda"
__copyright__ = "Copyright 2017, Siegurt Skoda"
__credits__ = ["Siegurt Skoda"]

__license__ = "GPL-3"
__version__ = "0.0.1"
__maintainer__ = "Siegurt Skoda"
__email__ = "sskoda(a)powerbb(dot)info"
__status__ = "Alpha"
                          

""" Der SDS011 sendet über den TTL-UART (3.3V) jede Sekunde ein Datenpaket von
    10 Byte.
    
    vgl.  https://nettigo.pl/attachments/398
    
    Bytes Hex   Bedeutung
    0     aa    Packetanfang
    1     c0    Kommando 
    2     .     PM 2.5 low Byte
    3     .     PM 2.5 high Byte
    4     .     PM 10 low Byte
    5     .     PM 10 high Byte
    6     .     ID low byte         (undokumentiert)
    7     .     ID high Byte        (undokumentiert)
    8     .     CRC
    9     ab    Packetende

    CRC = (s[2]+s[3]+s[4]+s[5]+s[6]+s[7]) Modulo 265
"""
import serial

# Diese Klasse steuert die Verbindung zum SDS011
class sds011:
    # Serial handler
    ser    = None
    
    # Konstruktor des Hardwartreibers
    # @param tty string     Der OS-Bezeichner des COM-Ports
    def __init__(self, tty):
        #Vorgaben für die Kommunikation mit dem Sensor
        # vgl.  https://nettigo.pl/attachments/398 
        self.ser = serial.Serial(
            port = tty,
            baudrate = 9600,
            bytesize = serial.EIGHTBITS,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE
        )

        #Öffne den Port
        self.ser.isOpen()
        
        # Warte bis der aktuelle Block abgeschlossen ist, um eine sauberer
        # startposition für den nächsten Fetch zu haben.
        x = 0
        while x != 0xab:
            x = ord(self.ser.read())
    
    # Ruf ein neues datenpaket vom Sensor ab indem eine neue Instanz der Klasse
    # sds011_data erstellt und zurückgegeben wird.
    #
    # @return: sds011_data
    def get_data(self):
        ret = sds011_data(self.ser)
        return ret


# Diese Klasse representiert ein Datum 
class sds011_data:
    # Hat der Auslesevorgang geklappt?
    # 0 = ok
    # 1 = Grenzen wurden nicht gefunden
    # 2 = crc fehler
    # 3 = serial Verbundung noch nicht initialisiert
    status = 0
    
    # Partikel der Größe 10,0µm in µg/m³
    pm10   = 0
    
    # Partikel der Größe  2,5µm in µg/m³
    pm25   = 0
        
    # ID des Sensors (?)
    id     = 0
    
    # Der Konstrukter dieser Klasse
    # @param ser serial         Die instanz der klasse der die Seriele Schnitt-
    #                           stelle zum Treibr hällt
    def __init__(self, ser):
        #Lese die nächsen 10 byte aus dem RS232-Puffer
        s = ser.read(10)
        
        #Überprüfe ob die festen bestandteile des Skriptes 
        if((s[0] != 0xaa) or (s[1] != 0xc0) or (s[9] != 0xab)):
            self.status = 1
            return 

        # Überprüfe ob das übertragene Datum mit dem CRC Code übereinstimmt
        crc = (s[2]+s[3]+s[4]+s[5]+s[6]+s[7]) % 0xff
        if(crc != s[8]):
            self.status = 2
            return
        
        #decodiert die Daten und legt sie in Eigenschaftenspeicher dieser
        #Instanz ab.
        self.id   =  s[7]+s[6]*0xff
        self.pm25 = (s[2]+s[3]*0xff)/10
        self.pm10 = (s[4]+s[5]*0xff)/10