import subprocess
import time

class ObdMonitor:    
    _lastUpdateAt = None
    
    def __init__(self, serviceName,
                 t = time.time, execute = subprocess.call):
        self._serviceName = serviceName
        self._time = t
        self._exec = execute
        
    
    def updateTime(self, _ = None):
        self._lastUpdateAt = self._time()
        
    
    def isAlive(self):
        if (self._time() > self._lastUpdateAt + 10):
            self._exec([
                "/bin/systemctl",
                "restart",
                self._serviceName,
            ])
            
            return False
        else:
            return True
        