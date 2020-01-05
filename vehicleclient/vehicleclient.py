import mycommands
import netifaces
import obd
import signal
import socket
import subprocess
import sys
import time

from myvehicle import MyVehicle
from obdmonitor import ObdMonitor

class VehicleClient:
    SRV_IP = "127.0.0.1"
    SRV_PORT = 20000
    SRV_ADDR = (SRV_IP, SRV_PORT)
    ALL_IP = "169.254.0.255" # Všetci v dosahu (broadcast)
    ALL_PORT = 20001
    ALL_ADDR = (ALL_IP, ALL_PORT)
    INFO_FILENAME = "/home/pi/Desktop/v2v/vehicleinfo.txt"
    
    def __init__(self, srvAddr, allAddr,
                 vehicle, srvUdpSock, allUdpSock,
                 obd, obdMon):
        self.srvAddr = srvAddr
        self.allAddr = allAddr
        self.vehicle = vehicle
        self.srvUdpSock = srvUdpSock
        self.allUdpSock = allUdpSock
        self.obd = obd
        self.obdMon = obdMon
        
    
    def registerShutdownHandler(self):
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)
    
    def initSrvUdpSock(self):
        pass
    
    
    def initAllUdpSock(self):
        self.allUdpSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    
    def initObd(self):
        self.obd.supported_commands.add(mycommands.GEAR)
        self.obd.watch(obd.commands.RPM, self.obdMon.updateTime)
        self.obd.watch(mycommands.GEAR)
        self.obd.watch(obd.commands.SPEED)
        self.obd.start()
       
       
    def run(self, sleep):
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
            self.srvUdpSock.sendto(self.vehicle.toEncodedJson(True), self.srvAddr)

            # Odošleme informácie o našom vozidle do prostredia okolo nás
            self.allUdpSock.sendto(self.vehicle.toEncodedJson(), self.allAddr)

            sleep(1)
     
    
    def start(self, infoFilename, nfs = netifaces, sleep = time.sleep):
        self.registerShutdownHandler()
        self.vehicle.init(netifaces, infoFilename)
        self.initSrvUdpSock()
        self.initAllUdpSock()
        self.initObd()
        self.obdMon.updateTime()
        self.run(sleep)
        
        
    def stop(self, sigNum = None, csf = None):
        self.obd.close()
        self.allUdpSock.close()
        self.srvUdpSock.close()


if __name__ == "__main__":
    vehicle = MyVehicle()
    srvUdpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    allUdpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    obdConn = obd.Async()
    obdMon = ObdMonitor(time.time, subprocess.call)
    
    client = VehicleClient(VehicleClient.SRV_ADDR,
                           VehicleClient.ALL_ADDR,
                           vehicle, srvUdpSock, allUdpSock,
                           obdConn, obdMon)
    
    try:
        client.start(VehicleClient.INFO_FILENAME)
    except KeyboardInterrupt:
        pass
    finally:
        client.stop()
