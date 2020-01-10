import netifaces
import signal
import socket
import sys
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
    NETWORK_INTERFACE_NAME = "bat0"
    BUFFER_SIZE = 1024
    
    _ip = None
    
    def __init__(self, new, vehicle, udpSock,
                 foreignVehicles, gui, addr = ADDR):
        self._addr = addr
        self._new = new
        self._vehicle = vehicle
        self._udpSock = udpSock
        self._foreignVehicles = foreignVehicles
        self._gui = gui
        
    
    def _registerShutdownHandler(self):
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)
        
        
    def _figureOutMyIp(self, netIfName, netifaces):
        bat0 = netifaces.ifaddresses(netIfName)
        self._ip = bat0[netifaces.AF_INET][0]["addr"]
    
    
    def _initUdpSock(self):
        self._udpSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self._udpSock.setblocking(False)
        self._udpSock.bind(self._addr)
        
        
    def _udpSockReceiver(self):
        try:
            bufferSize = VehicleServer.BUFFER_SIZE
            (json, (ip, port)) = self._udpSock.recvfrom(bufferSize)
            
            if ip == self._ip or ip == "127.0.0.1":
                if self._vehicle.fromJson(json, True) != None:
                    self._gui.updateMyVehicle()
                # Inak ignoruj nekompletné dáta o mne
            else:
                foreignVehicle = self._foreignVehicles.get(ip)
                
                if foreignVehicle == None:
                    foreignVehicle = self._new.foreignVehicle(json)
                    self._foreignVehicles.add(foreignVehicle)
                else:
                    foreignVehicle.fromJson(json)
        except BlockingIOError:
            pass
        
        self._foreignVehicles.removeAllUnreachable(time.time())
        self._gui.updateForeignVehicles()
        self._gui.invokeLater(self._udpSockReceiver)
     
    
    def start(self, netIfName = NETWORK_INTERFACE_NAME, nfs = netifaces):        
        self._registerShutdownHandler()
        self._figureOutMyIp(netIfName, nfs)
        self._initUdpSock()
        self._gui.show(self._udpSockReceiver)
        
        
    def stop(self, sigNum = None, csf = None):        
        try:
            self._gui.close()
        except Exception as e:
            print(e, file=sys.stderr)
        
        try:
            self._udpSock.close()
        except Exception as e:
            print(e, file=sys.stderr)


if __name__ == "__main__":
    new = ObjectMaker()
    vehicle = Vehicle()
    udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tk = Tk()
    foreignVehicles = ForeignVehicles()
    gui = Gui(master=tk, vehicle=vehicle,
              foreignVehicles=foreignVehicles)
    
    server = VehicleServer(new, vehicle, udpSock,
                           foreignVehicles, gui)
    
    try:
        server.start()
    except KeyboardInterrupt:
        pass
    finally:
       server.stop()
