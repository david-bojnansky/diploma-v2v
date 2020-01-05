import json

class MyVehicle:
    NETWORK_INTERFACE_NAME = "bat0"
    
    ip = None
    brand = None
    model = None
    vrn = None             # EČV
    rotates = None
    gear = None
    direction = None
    directionAsText = None
    speed = None
    constantSpeed = None
    action = None
    actionAsText = None
        
    def init(self, netifaces, infoFilename):
        self.figureOutMyIp(netifaces)
        self.loadInfoAboutMe(infoFilename)
        
    
    def figureOutMyIp(self, netifaces):
        bat0 = netifaces.ifaddresses(MyVehicle.NETWORK_INTERFACE_NAME)
        self.ip = bat0[netifaces.AF_INET][0]["addr"]
        
    
    def loadInfoAboutMe(self, infoFilename):
        with open(infoFilename, "r") as fp:
            fp.readline()         # MAC adresa OBD skenera
            fp.readline()         # Bluetooth párovací kód
            brand = fp.readline() # Značka vozidla
            model = fp.readline() # Model vozidla
            vrn = fp.readline()   # EČV
            
            # Z konca odstrániť znak nového riadku
            self.brand = brand[:-1]
            self.model = model[:-1]
            self.vrn = vrn[:-1]


    def update(self, rotates, gear, speed):
        self.rotates = rotates
        
        self.updateGear(gear)
        self.updateDirection()
        
        # Preskoč úplne prvú, prípadne bez hodnotovú,
        # aktualizáciu činnosti.
        # Najskôr treba získať skutočnú rýchlosť a otáčky
        if self.speed != None:
            self.updateAction(speed)

        self.speed = speed       
    
    
    def updateGear(self, gear):
        if gear == None:
            self.gear = None
        elif gear == 0:
            self.gear = "N"
        elif gear < 0:
            self.gear = "R"
        else:
            self.gear = "D:" + str(gear)
    
    
    def updateDirection(self):
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
    
    
    def updateAction(self, speed):           
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
        # Keď prudko brzdíme,
        # nechceme potom zobraziť že spomaľujeme,
        # pretože prudké brzdenie má vyššiu prioritu
        elif self.action != -4 and speed <= self.speed - 3:
            self.action = -3
            self.actionAsText = "Spomaľuje!"
        else:
            self.constantSpeed = speed
            self.action = 2
            self.actionAsText = "V konštantnom pohybe"
        
        
    def toJson(self, forServer = False):
        data = {
            "aboutMe": forServer,
            "ip": self.ip,
            "brand": self.brand,
            "model": self.model,
            "vrn": self.vrn,
            "rotates": self.rotates,
            "direction": self.direction,
            "directionAsText": self.directionAsText,
            "speed": self.speed,
            "action": self.action,
            "actionAsText": self.actionAsText,
        }
        
        if forServer:
            data.update({
                #"rotates": self.rotates,
                "gear": self.gear,
            })
        
        return json.dumps(data)
    
    
    def toEncodedJson(self, forServer = False):
        return self.toJson(forServer).encode()
    
    
    def echo(self, name, alt = "Zisťujem..."):
        val = getattr(self, name)
        
        if (val == None):
            return alt
        else:
            return val
