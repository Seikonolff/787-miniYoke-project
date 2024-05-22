from enum import Enum

class MiniManche :
    MiniMancheState = Enum('MANUAL','AP_ENGAGED')
    def __init__(self):
        self.state = 'AP_ENGAGED' # NTS : checker si l'init se fait en mode manuel ou AP
        self.nx = 0
        self.nz = 0
        self.p = 0
        self.ready = False

    def parser(self, *msg):
        self.nx = msg[1]
        self.nz = msg[2]
        self.setReady(True) # miniManche data is ready to be sent

        print('Received message from MiniManche :')
        print('nx =', self.nx)
        print('nz =', self.nz)
    
    def setReady(self, ready):
        self.ready = ready


class ApLAT :
    def __init__(self):
        self.p = 0
        self.ready = False
    
    def parser(self, *msg):
        self.p = msg[1]
        self.setReady(True) # apLat data is ready to be sent

        print('Received message from AP_LAT :')
        print('p =', self.p)
        
    
    def setReady(self, ready):
        self.ready = ready
    

class ApLONG :
    def __init__(self):
        self.nx = 0
        self.nz = 0
        self.ready = False
    
    def parser(self, *msg):
        self.nx = msg[1]
        self.nz = msg[2]
        print('Received message from AP_LONG :')
        print('nx =', self.nx)
        print('nz =', self.nz)

        self.setReady(True) # apLong data is ready to be sent
    
    def setReady(self, ready):
        self.ready = ready

class FMGS : 
    def __init__(self):
        self.nxMax = 0
        self.nzMax = 0
        self.pMax = 0
    
    def parser(self, *msg):
        self.nxMax = msg[1]
        self.nzMax = msg[2]
        self.pMax = msg[3]

        print('Received message from FMGS :')
        print('nxMax =', self.nxMax)
        print('nzMax =', self.nzMax)
        print('pMax =', self.pMax)
        
class FCU :
    AP_STATE = Enum('ON','OFF')
    def __init__(self):
        self.ApState = 'ON'

    def parser(self, *msg):
        self.ApState = msg[1]

        print('Received message from FCU :')
        print('AP state =', self.ApState)