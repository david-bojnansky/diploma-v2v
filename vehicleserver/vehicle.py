import json
import time

class Vehicle:
    ip = None
    brand = None
    model = None
    vrn = None
    rotates = None
    gear = None
    direction = None
    directionAsText = None
    speed = None
    action = None
    actionAsText = None
    lastUpdateAt = None       
        
    def update(self, ip, brand, model, vrn, rotates, gear,
               direction, directionAsText, speed, action,
               actionAsText, t = time.time):
        self.ip = ip
        self.brand = brand
        self.model = model
        self.vrn = vrn
        self.rotates = rotates
        self.gear = gear
        self.direction = direction
        self.directionAsText = directionAsText
        self.speed = speed
        self.action = action
        self.actionAsText = actionAsText
        self.lastUpdateAt = t()
        
        
    def isReachable(self, time):
        return time <= self.lastUpdateAt + 3
    
    
    def echo(self, name, alt = "Zisťujem..."):
        val = getattr(self, name)
        
        if (val == None):
            return alt
        else:
            return val
    
    
    def fromJson(self, data, needsAboutMe = False):
        data = json.loads(data)
        
        if needsAboutMe and not data.get("aboutMe"):
            return None
        
        if (self == None):
            self = Vehicle()
        
        self.update(data.get("ip"),
                    data.get("brand"),
                    data.get("model"),
                    data.get("vrn"),
                    data.get("rotates"),
                    data.get("gear"),
                    data.get("direction"),
                    data.get("directionAsText"),
                    data.get("speed"),
                    data.get("action"),
                    data.get("actionAsText"))
        
        return self
    