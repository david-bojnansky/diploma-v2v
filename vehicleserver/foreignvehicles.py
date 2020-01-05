class ForeignVehicles:
    it = None
    
    def __init__(self):
        self.vehicles = []
        
    
    def __iter__(self):
        self.it = iter(self.vehicles)
        return self


    def __next__(self):
        return next(self.it)
    
    
    def __len__(self):
        return len(self.vehicles)
    
    
    def __getitem__(self, i):
        return self.vehicles[i]
    
    
    def has(self, ip):
        return self.get(ip) != None
        
        
    def get(self, ip):
        for v in self.vehicles:
            if v.ip == ip:
                return v
            
        return None
    
    
    def add(self, vehicle):
        self.vehicles.append(vehicle)
        
        
    def removeAllUnreachable(self, time):        
        for i, v in enumerate(self.vehicles):
            if not v.isReachable(time):
                del self.vehicles[i]
