import mycommands
import netifaces
import obd
import signal
import socket
import sys
import time

from myvehicle import MyVehicle
from obdmonitor import ObdMonitor
from obd import OBDStatus

class VehicleClient:
    ALL_IP = "169.254.0.255" # Všetci v dosahu (broadcast) vrátane nás
    ALL_PORT = 20000
    ALL_ADDR = (ALL_IP, ALL_PORT)
    INFO_FILENAME = "/home/pi/Desktop/v2v/vehicleinfo.txt"
    OBD_SERVICE_NAME = "v2v-obd2rpi.service"
    
    def __init__(self, vehicle, udpSock, obd, obdMon, allAddr = ALL_ADDR):
        self._allAddr = allAddr
        self._vehicle = vehicle
        self._udpSock = udpSock
        self._obd = obd
        self._obdMon = obdMon
        
    
    def _registerShutdownHandler(self):
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)
    
    
    def _initUdpSock(self):
        self._udpSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    
    def _initObd(self):
        self._obd.supported_commands.add(mycommands.GEAR)
        self._obd.watch(obd.commands.RPM, self._obdMon.updateTime)
        self._obd.watch(mycommands.GEAR)
        self._obd.watch(obd.commands.SPEED)
        self._obd.start()
       
       
    def _run(self, sleep):
        while self._obdMon.isAlive():
            rotates = self._obd.query(obd.commands.RPM).value
            gear = self._obd.query(mycommands.GEAR).value
            speed = self._obd.query(obd.commands.SPEED).value
            
            if rotates != None:
                rotates = rotates.magnitude
            
            if speed != None:
                speed = speed.magnitude
            
            self._vehicle.update(rotates, gear, speed)

            # Odošleme informácie o našom vozidle lokálnemu serveru
            self._udpSock.sendto(self._vehicle.toEncodedJson(True),
                                (self._vehicle.ip, self._allAddr[1]))

            # Odošleme informácie o našom vozidle do prostredia
            # okolo (vrátane) nás
            self._udpSock.sendto(self._vehicle.toEncodedJson(),
                                 self._allAddr)

            sleep(1)
     
    
    def start(self, infoFilename = INFO_FILENAME,
              nfs = netifaces, sleep = time.sleep):
        self._registerShutdownHandler()
        self._vehicle.init(netifaces, infoFilename)
        self._initUdpSock()
        self._initObd()
        self._obdMon.updateTime()
        self._run(sleep)
        
        
    def stop(self, sigNum = None, csf = None):
        try:
            self._obd.close()
        except Exception as e:
            print(e, file=sys.stderr)
        
        try:
            self._udpSock.close()
        except Exception as e:
            print(e, file=sys.stderr)


if __name__ == "__main__":
    vehicle = MyVehicle()
    udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    obdConn = obd.Async()
    obdMon = ObdMonitor(VehicleClient.OBD_SERVICE_NAME)
    
    client = VehicleClient(vehicle, udpSock, obdConn, obdMon)
    
    try:
        client.start()
    except KeyboardInterrupt:
        pass
    finally:
        client.stop()
