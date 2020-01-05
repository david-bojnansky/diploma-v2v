import netifaces
import signal
import socket
import time

from foreignvehicles import ForeignVehicles
from gui import Gui
from objectmaker import ObjectMaker
from tkinter import Tk
from vehicle import Vehicle

class VehicleServer:
    # Uvedená IP ("") reprezentuje priradenú IP-čku z rozsahu
    # 169.254.0.1-254 (unicast) a 169.254.0.255 (broadcast).
    # To znamená, že server počúva na dvoch IP-čkách
    IP = ""
    PORT = 20000
    ADDR = (IP, PORT)
    INFO_FILENAME = "/home/pi/Desktop/v2v/vehicleinfo.txt"
    NETWORK_INTERFACE_NAME = "bat0"
    BUFFER_SIZE = 1024
    
    ip = None
    
    def __init__(self, addr, new, vehicle,
                 udpSock, foreignVehicles, gui):
        self.addr = addr
        self.new = new
        self.vehicle = vehicle
        self.udpSock = udpSock
        self.foreignVehicles = foreignVehicles
        self.gui = gui
        
    
    def _registerShutdownHandler(self):
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)
        
        
    def _figureOutMyIp(self, netifaces):
        bat0 = netifaces.ifaddresses(VehicleServer.NETWORK_INTERFACE_NAME)
        self.ip = bat0[netifaces.AF_INET][0]["addr"]
    
    
    def _initUdpSock(self):
        self.udpSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.udpSock.setblocking(False)
        self.udpSock.bind(self.addr)
        
        
    def _udpSockReceiver(self):
        try:
            (json, (ip)) = self.udpSock.recvfrom(VehicleServer.BUFFER_SIZE)

            if ip == self.ip:
                if self.vehicle.fromJson(json, True) != None:
                    self.gui.updateMyVehicle()
            else:
                foreignVehicle = self.foreignVehicles.get(ip)
            
                if (foreignVehicle == None):
                    foreignVehicle = self.new.foreignVehicle(json)
                    self.foreignVehicles.add(foreignVehicle)
                else:
                    foreignVehicle.fromJson(json)
        except BlockingIOError:
            pass
        
        self.foreignVehicles.removeAllUnreachable(time.time())
        self.gui.updateForeignVehicles()
        self.gui.invokeLater(self._udpSockReceiver)
     
    
    def start(self, nfs = netifaces):        
        self._registerShutdownHandler()
        self._figureOutMyIp(nfs)
        self._initUdpSock()
        self.gui.show(self._udpSockReceiver)
        
        
    def stop(self, sigNum = None, csf = None):
        self.gui.close()
        self.udpSock.close()


if __name__ == "__main__":
    new = ObjectMaker()
    vehicle = Vehicle()
    udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tk = Tk()
    foreignVehicles = ForeignVehicles()
    gui = Gui(master=tk, vehicle=vehicle,
              foreignVehicles=foreignVehicles)
    
    server = VehicleServer(VehicleServer.ADDR,
                           new, vehicle, udpSock,
                           foreignVehicles, gui)
    
    try:
        server.start()
    except KeyboardInterrupt:
        pass
    finally:
       server.stop()
