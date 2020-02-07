import json
import netifaces

class MyVehicle:    
    ip = None              # IP adresa
    brand = None           # Značka
    model = None           # Model
    vrn = None             # EČV
    rotates = None         # Otáčky (za minútu)
    gear = None            # Prevodový stupeň
    direction = None       # Smer jazdy (číselný kód)
    directionAsText = None # Smer jazdy
    speed = None           # Rýchlosť (km/h)
    constantSpeed = None   # Konštantná rýchlosť (pomocná premenná)
    action = None          # Činnosť (číselný kód)
    actionAsText = None    # Činnosť
        
    def init(self, netIfName, infoFilename, nfs = netifaces):
        self._figureOutMyIp(netIfName, nfs)
        self._loadInfoAboutMe(infoFilename)
        
    
    def _figureOutMyIp(self, netIfName, netifaces):
        bat0 = netifaces.ifaddresses(netIfName)
        self.ip = bat0[netifaces.AF_INET][0]["addr"]
        
    
    def _loadInfoAboutMe(self, infoFilename):
        with open(infoFilename, "r") as fp:
            fp.readline()         # MAC adresa OBD skenera
            fp.readline()         # Bluetooth párovací kód
            brand = fp.readline() # Značka
            model = fp.readline() # Model
            vrn = fp.readline()   # EČV
            
            # Z konca odstrániť znak nového riadku
            self.brand = brand[:-1]
            self.model = model[:-1]
            self.vrn = vrn[:-1]


    def update(self, rotates, gear, speed):
        self.rotates = rotates
        
        self._updateGear(gear)
        self._updateDirection()
        
        # Činnosť sa určuje na základe porovnania
        # aktuálnej (speed) a predchádzajúcej
        # rýchlosti (self.speed)
        self._updateAction(speed)

        self.speed = speed
    
    
    def _updateGear(self, gear):
        if gear == None:
            self.gear = None
        elif gear == 0:
            self.gear = "N"
        elif gear < 0:
            self.gear = "R"
        else:
            self.gear = "D:" + str(gear)
    
    
    def _updateDirection(self):
        if self.gear == None:
            self.direction = None
            self.directionAsText = None
        elif self.gear == "N":
            self.direction = 0
            self.directionAsText = "Nikde"
        elif self.gear == "R":
            self.direction = -1
            self.directionAsText = "Dozadu"
        else:
            self.direction = 1
            self.directionAsText = "Dopredu"
    
    
    def _updateAction(self, speed):           
        if speed == None:
            self.action = None
            self.actionAsText = None
        elif speed == 0:
            self.action = 0
            self.actionAsText = "Stojí na mieste"
        # Pri zrýchľovaní rozlišujeme,
        # či je vozidlo v konštantnom pohybe
        elif self.action != 2 and speed > self.speed:
            self.action = 1
            self.actionAsText = "Zrýchľuje!"
        # Detto
        elif self.action == 2 and speed >= self.constantSpeed + 3:
            self.action = 1
            self.actionAsText = "Zrýchľuje!"
        elif speed <= self.speed - 10:
            self.action = -4
            self.actionAsText = "BRZDÍ!!!"
        elif speed <= 5 and speed < self.speed:
            self.action = -1
            self.actionAsText = "Takmer stojí na mieste"
        elif speed <= 15 and speed < self.speed:
            self.action = -2
            self.actionAsText = "Zastavuje!"
        elif speed <= self.speed - 3:
            self.action = -3
            self.actionAsText = "Spomaľuje!"
        else:
            self.constantSpeed = speed
            self.action = 2
            self.actionAsText = "V konštantnom pohybe"
        
        
    def toJson(self, forMyServer = False):
        data = {
            "aboutMe": forMyServer,
            "ip": self.ip,
            "brand": self.brand,
            "model": self.model,
            "vrn": self.vrn,
            "direction": self.direction,
            "directionAsText": self.directionAsText,
            "speed": self.speed,
            "action": self.action,
            "actionAsText": self.actionAsText,
        }
        
        if forMyServer:
            data.update({
                "rotates": self.rotates,
                "gear": self.gear,
            })
        
        return json.dumps(data)
    
    
    def toEncodedJson(self, forMyServer = False):
        return self.toJson(forMyServer).encode()
    
    
    def echo(self, name, alt = "Zisťujem..."):
        val = getattr(self, name)
        
        if val == None:
            return alt
        else:
            return val
