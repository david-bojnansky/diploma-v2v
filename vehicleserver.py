import mycommands
import netifaces
import signal
import socket
import sys
import time

from foreignvehicles import ForeignVehicles
from vehicleserver.gui import Gui
from objectmaker import ObjectMaker
from tkinter import Tk
from vehicle import Vehicle

class VehicleServer:
    SRV_IP = "127.0.0.1"
    SRV_PORT = 20000
    SRV_ADDR = (SRV_IP, SRV_PORT)
    # Uvedená IP ("") reprezentuje priradenú IP-čku z rozsahu
    # 169.254.0.1-254 (unicast) a 169.254.0.255 (broadcast).
    # To znamená, že server počúva na dvoch IP-čkách
    ALL_IP = ""
    ALL_PORT = 20001
    ALL_ADDR = (ALL_IP, ALL_PORT)
    INFO_FILENAME = "/home/pi/Desktop/vehicleinfo.txt"
    BUFFER_SIZE = 1024
    
    def __init__(self, srvAddr, allAddr, new,
                 vehicle, srvUdpSock, allUdpSock,
                 foreignVehicles, gui):
        self.srvAddr = srvAddr
        self.allAddr = allAddr
        self.new = new
        self.vehicle = vehicle
        self.srvUdpSock = srvUdpSock
        self.allUdpSock = allUdpSock
        self.foreignVehicles = foreignVehicles
        self.gui = gui
        
    
    def registerShutdownHandler(self):
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)
    
    
    def initSrvUdpSock(self):
        self.srvUdpSock.setblocking(False)
        self.srvUdpSock.bind(self.srvAddr)
    
    
    def initAllUdpSock(self):
        self.allUdpSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.allUdpSock.setblocking(False)
        self.allUdpSock.bind(self.allAddr)
        
        
    def srvUdpSockReceiver(self):
        try:
            (json, ip) = self.srvUdpSock.recvfrom(VehicleServer.BUFFER_SIZE)

            self.vehicle.fromJson(json)
        except BlockingIOError:
            pass
        
        self.gui.updateMyVehicle()
        self.gui.invokeLater(self.allUdpSockReceiver)
        
        
    def allUdpSockReceiver(self):
        try:
            (json, ip) = self.allUdpSock.recvfrom(VehicleServer.BUFFER_SIZE)

            foreignVehicle = self.foreignVehicles.get(ip)
            
            if (foreignVehicle == None):
                foreignVehicle = self.new.vehicle(json)
                self.foreignVehicles.add(foreignVehicle)
            else:
                foreignVehicle.fromJson(json)
                
            self.foreignVehicles.removeAllUnreachable(time.time())
        except BlockingIOError:
            pass
        
        self.gui.updateForeignVehicles()
        self.gui.invokeLater(self.srvUdpSockReceiver)
     
    
    def start(self, infoFilename, nfs = netifaces, sleep = time.sleep):        
        self.registerShutdownHandler()
        self.initSrvUdpSock()
        self.initAllUdpSock()
        self.gui.show(self.srvUdpSockReceiver)
        
        
    def stop(self, sigNum = None, csf = None):
        self.gui.close()
        self.allUdpSock.close()
        self.srvUdpSock.close()


if __name__ == "__main__":
    new = ObjectMaker()
    vehicle = Vehicle()
    srvUdpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    allUdpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tk = Tk()
    foreignVehicles = ForeignVehicles()
    gui = Gui(master=tk, vehicle=vehicle,
              foreignVehicles=foreignVehicles)
    
    server = VehicleServer(VehicleServer.SRV_ADDR,
                           VehicleServer.ALL_ADDR, new,
                           vehicle, srvUdpSock, allUdpSock,
                           foreignVehicles, gui)
    
    try:
        server.start(VehicleServer.INFO_FILENAME)
    except KeyboardInterrupt:
        pass
    finally:
       server.stop()
