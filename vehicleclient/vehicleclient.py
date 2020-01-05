import mycommands
import netifaces
import obd
import signal
import socket
import subprocess
import time

from myvehicle import MyVehicle
from obdmonitor import ObdMonitor

class VehicleClient:
    ALL_IP = "169.254.0.255" # Všetci v dosahu (broadcast) vrátane nás
    ALL_PORT = 20000
    ALL_ADDR = (ALL_IP, ALL_PORT)
    INFO_FILENAME = "/home/pi/Desktop/v2v/vehicleinfo.txt"
    
    def __init__(self, allAddr, vehicle, udpSock, obd, obdMon):
        self.allAddr = allAddr
        self.vehicle = vehicle
        self.udpSock = udpSock
        self.obd = obd
        self.obdMon = obdMon
        
    
    def _registerShutdownHandler(self):
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)
    
    
    def _initUdpSock(self):
        self.udpSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    
    def _initObd(self):
        self.obd.supported_commands.add(mycommands.GEAR)
        self.obd.watch(obd.commands.RPM, self.obdMon.updateTime)
        self.obd.watch(mycommands.GEAR)
        self.obd.watch(obd.commands.SPEED)
        self.obd.start()
       
       
    def _run(self, sleep):
        while self.obdMon.isAlive():
            rotates = self.obd.query(obd.commands.RPM).value
            gear = self.obd.query(mycommands.GEAR).value
            speed = self.obd.query(obd.commands.SPEED).value
            
            if rotates != None:
                rotates = rotates.magnitude
            
            if speed != None:
                speed = speed.magnitude
            
            self.vehicle.update(rotates, gear, speed)

            # Odošleme informácie o našom vozidle nášmu serveru
            self.udpSock.sendto(self.vehicle.toEncodedJson(True),
                                (self.vehicle.ip, self.allAddr[1]))

            # Odošleme informácie o našom vozidle do prostredia okolo (vrátane) nás
            self.udpSock.sendto(self.vehicle.toEncodedJson(), self.allAddr)

            sleep(1)
     
    
    def start(self, infoFilename = INFO_FILENAME,
              nfs = netifaces, sleep = time.sleep):
        self._registerShutdownHandler()
        self.vehicle.init(netifaces, infoFilename)
        self._initUdpSock()
        self._initObd()
        self.obdMon.updateTime()
        self._run(sleep)
        
        
    def stop(self, sigNum = None, csf = None):
        self.obd.close()
        self.udpSock.close()


if __name__ == "__main__":
    vehicle = MyVehicle()
    udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    obdConn = obd.Async()
    obdMon = ObdMonitor(time.time, subprocess.call)
    
    client = VehicleClient(VehicleClient.ALL_ADDR, vehicle,
                           udpSock, obdConn, obdMon)
    
    try:
        client.start()
    except KeyboardInterrupt:
        pass
    finally:
        client.stop()
