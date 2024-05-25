import pygame
import time
from enum import Enum

class FCC :
    fccState = Enum('MANUAL','AP_ENGAGED')
    def __init__(self, fcu, aviBus):
        self.state = 'MANUAL'
        self.nx = 0
        self.nz = 0
        self.p = 0

        self.ready = False
        self.fcu = fcu
        self.aviBus = aviBus

    def setFlightInputs(self, nx, nz, p):
        self.nx = nx
        self.nz = nz
        self.p = p
        self.setReady(True)

    def setState(self, state):
        self.state = state
    
    def setReady(self, ready):
        self.ready = ready
    
    def sendButtonsState(self, flapsUp, flapsDown, apDisconnect, gearDown, previousFlapsUp, previousFlapsDown, previousApDisconnect, previousGearDown):
        if flapsUp and not previousFlapsUp :
            print('Flaps up button pushed')
            self.aviBus.sendMsg('FLAPS UP')
        if flapsDown and not previousFlapsDown :
            print('Flaps down button pushed')
            self.aviBus.sendMsg('FLAPS DOWN')
        if apDisconnect and not previousApDisconnect :
            print('AP disconnect button pushed')
            if self.state == 'AP_ENGAGED':
                print('fcc state switch from AP_ENGAGED to MANUAL')
                self.aviBus.sendMsg('FCUAP1 off') # Send acknowledge message to the fcu
                self.state = 'MANUAL'
                self.fcu.setApState('OFF')

        if gearDown and not previousGearDown :
            print('Gear down button pushed')
            self.aviBus.sendMsg('GEAR DOWN')

class MiniYoke :
    def __init__(self, fcc):
        self.nx = 0
        self.nz = 0
        self.p = 0
        self.joystick = None # joystick object from pygame
        self.threadRunning = True
        self.moved = False
        self.fcc = fcc

        self.throttleAxis = 3
        self.pitchAxis = 1
        self.rollAxis = 0

        self.throttleAxisValue = 0 # throttle axis value from joystick to compute nx
        self.pitchAxisValue = 0 # pitch axis value from joystick to compute nz
        self.rollAxisValue = 0 # roll axis value from joystick to compute p


        self.flapsUpButton = 11
        self.flapsDownButton = 10
        self.apDisconnectButton = 3
        self.gearDownButton = 9

        self.flapsUpPushed = False
        self.flapsDownPushed = False
        self.apDisconnectPushed = False
        self.gearDownPushed = False

        self.previousFlapsUpPushed = False
        self.previousFlapsDownPushed = False
        self.previousApDisconnectPushed = False
        self.previousGearDownPushed = False

        self.pitchAxisMax = 1
        self.pitchAxisMin = -1
        self.rollAxisMax = 1
        self.rollAxisMin = -1

        self.pMax = 0.35
        self.pMin = -0.35

        self.nzMax = 4
        self.nzMin = -2


    def begin(self):
        pygame.init()
        pygame.joystick.init()
        
        joystickCount = pygame.joystick.get_count()
        if joystickCount == 0:
            print("No joystick found. Please plug one.")
            pygame.quit()
            time.sleep(2)
            return False
        else:
            print(f"{joystickCount} joystick found.")

        joystick = pygame.joystick.Joystick(0)
        joystick.init()

        print(f"Nom du joystick : {joystick.get_name()}")
        print(f"Nombre d'axes : {joystick.get_numaxes()}")
        print(f"Nombre de boutons : {joystick.get_numbuttons()}")

        self.joystick = joystick

        return True
    
    def listener(self):
        while self.threadRunning :
            pygame.event.pump()
            self.throttleAxisValue = self.joystick.get_axis(self.throttleAxis)
            self.pitchAxisValue = self.joystick.get_axis(self.pitchAxis)
            self.rollAxisValue = self.joystick.get_axis(self.rollAxis)

            self.flapsUpPushed = self.joystick.get_button(self.flapsUpButton)
            self.flapsDownPushed = self.joystick.get_button(self.flapsDownButton)
            self.apDisconnectPushed = self.joystick.get_button(self.apDisconnectButton)
            self.gearDownPushed = self.joystick.get_button(self.gearDownButton)

            self.fcc.sendButtonsState(self.flapsUpPushed, self.flapsDownPushed, self.apDisconnectPushed, self.gearDownPushed, self.previousFlapsUpPushed, self.previousFlapsDownPushed, self.previousApDisconnectPushed, self.previousGearDownPushed)

            self.previousFlapsUpPushed = self.flapsUpPushed
            self.previousFlapsDownPushed = self.flapsDownPushed
            self.previousApDisconnectPushed = self.apDisconnectPushed
            self.previousGearDownPushed = self.gearDownPushed
            
            self.moved = True if self.pitchAxisValue != 0 and self.rollAxisValue != 0 else False

            self.getInputs(self.pitchAxisValue, self.rollAxisValue)
            
            time.sleep(0.1)

    def getInputs(self, pitchAxisValue, rollAxisValue):
        self.nx = self.getNx()
        self.nz = self.getNz(pitchAxisValue)
        self.p = self.getP(rollAxisValue)
        self.fcc.setFlightInputs(self.nx, self.nz, self.p)
    
    def getNx(self):
        return 1

    def getNz(self, pitchAxisValue):
        nz = self.nzMin + (self.nzMax - self.nzMin) * (pitchAxisValue - self.pitchAxisMin) / (self.pitchAxisMax - self.pitchAxisMin)
        
        return max(self.nzMin, min(self.nzMax, nz))

    def getP(self, rollAxisValue):
        p = self.pMin + (self.pMax - self.pMin) * (rollAxisValue - self.rollAxisMin) / (self.rollAxisMax - self.rollAxisMin)

        return max(self.pMin, min(self.pMax, p))
    
    def setMoved(self, moved):
        self.moved = moved
    
    def close(self):
        pygame.quit()
        pygame.joystick.quit()

        self.threadRunning = False

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
        self.ApState = 'OFF'

    def parser(self, *msg):
        print('Ap button pushed on FCU')
        self.ApState = 'ON' if self.ApState == 'OFF' else 'OFF'

        print('AP state =', self.ApState)
    
    def setApState(self, state):
        self.ApState = state