class ObdMonitor:
    lastUpdateAt = None
    
    def __init__(self, time, execute):
        self.time = time
        self.exec = execute
        
    
    def updateTime(self, _ = None):
        self.lastUpdateAt = self.time()
        
    
    def isAlive(self):
        if (self.time() > self.lastUpdateAt + 10):
            self.exec([
                "/bin/systemctl",
                "restart",
                "v2v-obd2rpi.service",
            ])
            
            return False
        else:
            return True
        