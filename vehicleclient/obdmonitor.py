import subprocess
import time

class ObdMonitor:
    SERVICE_NAME = "v2v-obd2rpi.service"
    
    _lastUpdateAt = None
    
    def __init__(self, serviceName = SERVICE_NAME,
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
        