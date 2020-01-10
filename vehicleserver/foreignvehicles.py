class ForeignVehicles:
    _it = None
    
    def __init__(self):
        self._vehicles = []
        
    
    def __iter__(self):
        self._it = iter(self._vehicles)
        return self


    def __next__(self):
        return next(self._it)
    
    
    def __len__(self):
        return len(self._vehicles)
    
    
    def __getitem__(self, i):
        return self._vehicles[i]
    
    
    def has(self, ip):
        return self.get(ip) != None
        
        
    def get(self, ip):
        for v in self._vehicles:
            if v.ip == ip:
                return v
            
        return None
    
    
    def add(self, vehicle):
        self._vehicles.append(vehicle)
        
        
    def removeAllUnreachable(self, time):
        for i, v in enumerate(self._vehicles):
            if not v.isReachable(time):
                del self._vehicles[i]
