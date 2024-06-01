import pygame
import time
from enum import Enum

class FCC:
    """
    Flight Control Computer (FCC) class.

    This class represents the Flight Control Computer of an aircraft. 
    It manages the state and control laws for the flight control parameters.

    Attributes:
        fccState (Enum): Enumeration of possible FCC states ('MANUAL', 'AP_ENGAGED').
        state (str): The current state of the FCC.
        nx (float): The value of the nx parameter.
        nz (float): The value of the nz parameter.
        p (float): The value of the p parameter.
        flaps (int): The current flaps position (0, 1, 2, 3).
        gear (bool): The current landing gear position (False = down, True = up).
        ready (bool): Indicates if the FCC is ready to receive manual commands.
        nzMargin (float): The margin for the nz control law.
        pMargin (float): The margin for the p control law.
        fcu (object): The Flight Control Unit object.
        fmgs (object): The Flight Management and Guidance System object.
        flightModel (object): The Flight Model object.
        aviBus (object): The Avionics Bus object.

    Methods:
        setState(state): Sets the state of the FCC.
        setReady(ready): Sets the ready status of the FCC.
        setManualCommands(nx, nz, p, throttleAxisValue, pitchAxisValue, rollAxisValue): Sets the manual commands for the FCC.
        nxLaw(nx, throttleAxisValue, fmgs, flightModel): Computes the nx control law.
        nzLaw(nz, pitchAxisValue, fmgs, flightModel): Computes the nz control law.
        pLaw(p, rollAxisValue, fmgs, flightModel): Computes the p control law.
        sendButtonsState(flapsUp, flapsDown, apDisconnect, gear, previousFlapsUp, previousFlapsDown, previousApDisconnect, previousGear): Sends the rising edge of the buttons to the Avionics Bus.
    """

    fccState = Enum('MANUAL', 'AP_ENGAGED')

    def __init__(self, fcu, fmgs, flightModel, aviBus):
        """
        Initializes a new instance of the FCC class.

        Args:
            fcu (object): The Flight Control Unit object.
            fmgs (object): The Flight Management and Guidance System object.
            flightModel (object): The Flight Model object.
            aviBus (object): The Avionics Bus object.
        """
        self.state = 'MANUAL'
        self.nx = 0
        self.nz = 0
        self.p = 0
        self.flaps = 0  # 0, 1, 2, 3
        self.gear = False  # False = down, True = up
        self.ready = False

        self.nzMargin = 0.80
        self.pMargin = 0.90

        self.fcu = fcu
        self.fmgs = fmgs
        self.flightModel = flightModel
        self.aviBus = aviBus

    def setState(self, state):
        """
        Sets the state of the FCC.

        Args:
            state (str): The state to set.
        """
        self.state = state

    def setReady(self, ready):
        """
        Sets the ready status of the FCC.

        Args:
            ready (bool): The ready status to set.
        """
        self.ready = ready

    def setManualCommands(self, nx, nz, p, throttleAxisValue, pitchAxisValue, rollAxisValue):
        """
        Sets the manual commands for the FCC.

        Args:
            nx (float): The value of the nx parameter.
            nz (float): The value of the nz parameter.
            p (float): The value of the p parameter.
            throttleAxisValue (float): The value of the throttle axis.
            pitchAxisValue (float): The value of the pitch axis.
            rollAxisValue (float): The value of the roll axis.
        """
        if self.state == 'MANUAL':
            self.nx = self.nxLaw(nx, throttleAxisValue, self.fmgs, self.flightModel)
            self.nz = self.nzLaw(nz, pitchAxisValue, self.fmgs, self.flightModel)
            self.p = self.pLaw(p, rollAxisValue, self.fmgs, self.flightModel)
            self.ready = True

    def nxLaw(self, nx, throttleAxisValue, fmgs, flightModel):
        """
        Calculates the nx control law.

        Args:
            nx (float): The value of the nx parameter.
            throttleAxisValue (float): The value of the throttle axis.
            fmgs (object): The Flight Management and Guidance System object.
            flightModel (object): The Flight Model object.

        Returns:
            float: The calculated nx value.
        """
        # currently not implemented
        return None

    def nzLaw(self, nz, pitchAxisValue, fmgs, flightModel):
        """
        Calculates the nz control law.

        Args:
            nz (float): The value of the nz parameter.
            pitchAxisValue (float): The value of the pitch axis.
            fmgs (object): The Flight Management and Guidance System object.
            flightModel (object): The Flight Model object.

        Returns:
            float: The nz value either limited in nz or fpa.
        """
        if flightModel.fpa <= fmgs.fpaMin * self.nzMargin and pitchAxisValue < 0:
            return self.fmgs.nzMax

        elif flightModel.fpa >= fmgs.fpaMax * self.nzMargin and pitchAxisValue > 0:
            return self.fmgs.nzMin

        return max(fmgs.nzMin, min(fmgs.nzMax, nz))

    def pLaw(self, p, rollAxisValue, fmgs, flightModel):
        """
        Calculates the p control law.

        Args:
            p (float): The value of the p parameter.
            rollAxisValue (float): The value of the roll axis.
            fmgs (object): The Flight Management and Guidance System object.
            flightModel (object): The Flight Model object.

        Returns:
            float: The p value either limited in p or phi.
        """
        if flightModel.phi < fmgs.phiMin * self.pMargin and rollAxisValue < 0:
            return 0
        elif flightModel.phi > fmgs.phiMax * self.pMargin and rollAxisValue > 0:
            return 0

        return max(fmgs.pMin, min(fmgs.pMax, p))

    def sendButtonsState(self, flapsUp, flapsDown, apDisconnect, gear, previousFlapsUp, previousFlapsDown,
                         previousApDisconnect, previousGear):
        """
        Sends the rising edge of the buttons to the Avionics Bus.

        Args:
            flapsUp (bool): Indicates if the flaps up button is pushed.
            flapsDown (bool): Indicates if the flaps down button is pushed.
            apDisconnect (bool): Indicates if the AP disconnect button is pushed.
            gear (bool): Indicates if the gear down button is pushed.
            previousFlapsUp (bool): The previous state of the flaps up button.
            previousFlapsDown (bool): The previous state of the flaps down button.
            previousApDisconnect (bool): The previous state of the AP disconnect button.
            previousGear (bool): The previous state of the gear down button.
        """
        if flapsUp and not previousFlapsUp:
            print('Flaps up button pushed')
            self.flaps -= 1
            self.flaps = 0 if self.flaps < 0 else self.flaps
            print('Flaps =', self.flaps)
            self.aviBus.sendMsg('VoletState={}'.format(self.flaps))
        if flapsDown and not previousFlapsDown:
            print('Flaps down button pushed')
            self.flaps += 1
            self.flaps = 3 if self.flaps > 3 else self.flaps
            print('Flaps =', self.flaps)
            self.aviBus.sendMsg('VoletState={}'.format(self.flaps))
        if apDisconnect and not previousApDisconnect:
            print('AP disconnect button pushed')
            if self.state == 'AP_ENGAGED':
                self.aviBus.sendMsg('FCUAP1 off')  # Send acknowledge message to the fcu
                self.state = 'MANUAL'
                self.fcu.setApState('OFF')
        if gear and not previousGear:
            self.gear = True if not self.gear else False
            print("Gear = ", self.gear, "(False = down, True = up)")
            self.aviBus.sendMsg('LandingGearState={}'.format(self.gear))

class MiniYoke :
    """
    Represents a mini yoke controller for a flight simulator.

    Attributes:
    - fcc: The flight control computer object associated with the mini yoke.
    - alphaFilter: The coefficient for the low pass filter used to filter the joystick inputs.
    - throttleAxisValue: The throttle axis value from the joystick to compute nx.
    - pitchAxisValue: The pitch axis value from the joystick to compute nz.
    - rollAxisValue: The roll axis value from the joystick to compute p.
    - joystick: The joystick object from the pygame library.
    - threadRunning: A boolean indicating whether the listener thread is running.
    - moved: A boolean indicating whether the mini yoke has moved.
    - throttleAxis: The index of the throttle axis on the joystick.
    - pitchAxis: The index of the pitch axis on the joystick.
    - rollAxis: The index of the roll axis on the joystick.
    - nzMin: The minimum value of nz on the axis of the joystick.
    - nzMax: The maximum value of nz on the axis of the joystick.
    - pMin: The minimum value of p on the axis of the joystick.
    - pMax: The maximum value of p on the axis of the joystick.
    - flapsUpButton: The index of the button for raising the flaps on the joystick.
    - flapsDownButton: The index of the button for lowering the flaps on the joystick.
    - apDisconnectButton: The index of the button for disconnecting the autopilot on the joystick.
    - gearButton: The index of the button for controlling the landing gear on the joystick.
    - flapsUpPushed: A boolean indicating whether the flaps up button is pushed.
    - flapsDownPushed: A boolean indicating whether the flaps down button is pushed.
    - apDisconnectPushed: A boolean indicating whether the autopilot disconnect button is pushed.
    - gearPushed: A boolean indicating whether the gear button is pushed.
    - previousFlapsUpPushed: A boolean indicating the previous state of the flaps up button.
    - previousFlapsDownPushed: A boolean indicating the previous state of the flaps down button.
    - previousApDisconnectPushed: A boolean indicating the previous state of the autopilot disconnect button.
    - previousGearPushed: A boolean indicating the previous state of the gear button.
    - pitchAxisMax: The maximum value of the pitch axis.
    - pitchAxisMin: The minimum value of the pitch axis.
    - rollAxisMax: The maximum value of the roll axis.
    - rollAxisMin: The minimum value of the roll axis.
    - filteredPitchAxisValue: The filtered value of the pitch axis using a low pass filter.
    - filteredRollAxisValue: The filtered value of the roll axis using a low pass filter.

    Methods:
    - begin(): Initializes the pygame library and the joystick.
    - listener(): Listens for joystick events and updates the mini yoke attributes accordingly.
    - getNx(throttleAxisValue): Computes the value of nx based on the throttle axis value.
    - getNz(pitchAxisValue): Computes the value of nz based on the pitch axis value.
    - getP(rollAxisValue): Computes the value of p based on the roll axis value.
    - end(): Stops the listener thread and cleans up the pygame library and joystick.
    """
    def __init__(self, fcc, alphaFilter):
        """
        Initializes a new instance of the MiniYoke class.

        Args:
        - fcc: The flight control computer object associated with the mini yoke.
        - alphaFilter: The coefficient for the low pass filter used to filter the joystick inputs.
        """
        self.fcc = fcc

        self.throttleAxisValue = 0 # throttle axis value from joystick to compute nx
        self.pitchAxisValue = 0 # pitch axis value from joystick to compute nz
        self.rollAxisValue = 0 # roll axis value from joystick to compute p
        
        self.joystick = None # joystick object from pygame
        self.threadRunning = True
        self.moved = False

        self.throttleAxis = 3
        self.pitchAxis = 1
        self.rollAxis = 0

        self.nzMin = -2
        self.nzMax = 3
        self.pMin = -0.35
        self.pMax = 0.35

        self.flapsUpButton = 11
        self.flapsDownButton = 10
        self.apDisconnectButton = 3
        self.gearButton = 9

        self.flapsUpPushed = False
        self.flapsDownPushed = False
        self.apDisconnectPushed = False
        self.gearPushed = False

        self.previousFlapsUpPushed = False
        self.previousFlapsDownPushed = False
        self.previousApDisconnectPushed = False
        self.previousGearPushed = False

        self.pitchAxisMax = 1
        self.pitchAxisMin = -1
        self.rollAxisMax = 1
        self.rollAxisMin = -1

        self.filteredPitchAxisValue = 0
        self.filteredRollAxisValue = 0
        self.alpha = alphaFilter  # Coefficient for low pass filter


    def begin(self):
        """
        Initializes the pygame library and the joystick.

        Returns:
        - True if the joystick is successfully initialized, False otherwise.
        """
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

        self.joystick = joystick

        return True
    
    def listener(self):
        """
        Listens for joystick events and updates the mini yoke attributes accordingly.
        """
        while self.threadRunning :
            pygame.event.pump()
            self.throttleAxisValue = self.joystick.get_axis(self.throttleAxis)
            self.pitchAxisValue = self.joystick.get_axis(self.pitchAxis)
            self.rollAxisValue = self.joystick.get_axis(self.rollAxis)

            self.flapsUpPushed = self.joystick.get_button(self.flapsUpButton)
            self.flapsDownPushed = self.joystick.get_button(self.flapsDownButton)
            self.apDisconnectPushed = self.joystick.get_button(self.apDisconnectButton)
            self.gearPushed = self.joystick.get_button(self.gearButton)

            self.fcc.sendButtonsState(self.flapsUpPushed, self.flapsDownPushed, self.apDisconnectPushed, self.gearPushed, self.previousFlapsUpPushed, self.previousFlapsDownPushed, self.previousApDisconnectPushed, self.previousGearPushed)

            self.previousFlapsUpPushed = self.flapsUpPushed
            self.previousFlapsDownPushed = self.flapsDownPushed
            self.previousApDisconnectPushed = self.apDisconnectPushed
            self.previousGearPushed = self.gearPushed
            
            self.moved = True if self.pitchAxisValue != 0 and self.rollAxisValue != 0 else False

            self.fcc.setManualCommands(self.getNx(self.throttleAxisValue), self.getNz(self.pitchAxisValue), self.getP(self.rollAxisValue), self.throttleAxis, self.pitchAxisValue, self.rollAxisValue)
            time.sleep(0.1)
    
    def getNx(self, throttleAxisValue):
        """
        Computes the value of nx based on the throttle axis value.

        Args:
        - throttleAxisValue: The throttle axis value from the joystick.

        Returns:
        - The computed value of nx.
        """
        # currently not implemented
        return None
        
    def getNz(self, pitchAxisValue):
        """
        Computes the value of nz based on the pitch axis value.

        Args:
        - pitchAxisValue: The pitch axis value from the joystick.

        Returns:
        - The computed value of nz.
        """
        self.filteredPitchAxisValue = self.alpha * pitchAxisValue + (1 - self.alpha) * self.filteredPitchAxisValue
        nz = self.nzMin + (self.nzMax - self.nzMin) * (self.filteredPitchAxisValue - self.pitchAxisMin) / (self.pitchAxisMax - self.pitchAxisMin)
        return nz
    
    def getP(self, rollAxisValue):
        """
        Computes the value of p based on the roll axis value.

        Args:
        - rollAxisValue: The roll axis value from the joystick.

        Returns:
        - The computed value of p.
        """
        self.filteredRollAxisValue = self.alpha * rollAxisValue + (1 - self.alpha) * self.filteredRollAxisValue
        p = self.pMin + (self.pMax - self.pMin) * (self.filteredRollAxisValue - self.rollAxisMin) / (self.rollAxisMax - self.rollAxisMin)
        return p
    
    def end(self):
        """
        Stops the listener thread and cleans up the pygame library and joystick.
        """
        self.threadRunning = False
        pygame.quit()
        pygame.joystick.quit()

class ApLAT:
    """
    Represents the lateral autopilot system.

    Attributes:
        p (float): The value of p.
        ready (bool): Indicates if the apLat data is ready to be sent.
        regex (str): The regular expression pattern for parsing ApLAT's messages.

    Methods:
        parser(*msg): Parses the message and updates the p value.
        setReady(ready): Sets the ready status of the apLat data.
    """

    def __init__(self):
        self.p = 0
        self.ready = False
        self.regex = '^AP_LAT p=(\S+)'
    
    def parser(self, *msg):
        """
        Parses the message and updates the p value.

        Args:
            *msg: Variable number of message arguments.

        Returns:
            None
        """
        self.p = float(msg[1])
        self.ready = True  # apLat data is ready to be sent

        print('Received message from AP_LAT :')
        print('p =', self.p)
        
    def setReady(self, ready):
        """
        Sets the ready status of the apLat data.

        Args:
            ready (bool): The ready status.

        Returns:
            None
        """
        self.ready = ready
    
class ApLONG:
    """
    This class represents the longitutidal autopilot system.

    Attributes:
        nx (float): The value of nx.
        nz (float): The value of nz.
        ready (bool): Indicates if the apLong data is ready to be sent.
        regex (str): The regular expression used for parsing ApLONG's messages.

    Methods:
        parser(*msg): Parses the given message and updates nx and nz values.
        setReady(ready): Sets the ready attribute to the given value.
    """

    def __init__(self):
        self.nx = 0
        self.nz = 0
        self.ready = False
        self.regex = '^PaLong Nx=(\S+) Nz=(\S+)'

    def parser(self, *msg):
        """
        Parses the given message and updates nx and nz values.

        Args:
            *msg: Variable number of message arguments.
        """
        self.nx = float(msg[1])
        self.nz = float(msg[2])
        print('Received message from AP_LONG :')
        print('nx =', self.nx)
        print('nz =', self.nz)

        self.ready = True  # apLong data is ready to be sent

    def setReady(self, ready):
        """
        Sets the ready attribute to the given value.

        Args:
            ready (bool): The value to set for the ready attribute.
        """
        self.ready = ready

class FMGS:
    """
    The Flight Management and Guidance System (FMGS) class represents the fmgs of an aircraft.

    Attributes:
        nxMax (float): The maximum value for nx.
        nxMin (float): The minimum value for nx.
        nzMax (float): The maximum value for nz.
        nzMin (float): The minimum value for nz.
        pMax (float): The maximum value for p.
        pMin (float): The minimum value for p.
        phiMax (float): The maximum value for phi.
        phiMin (float): The minimum value for phi.
        fpaMax (float): The maximum value for fpa.
        fpaMin (float): The minimum value for fpa.
        regex (str): The regular expression used for parsing FMGS's messages.

    Methods:
        parser: Parses the received message and updates the attribute values accordingly.
    """

    def __init__(self):
        self.nxMax = 0.5
        self.nxMin = -1
        self.nzMax = 2.5
        self.nzMin = -1.5
        self.pMax = 0.7
        self.pMin = -0.7
        self.phiMax = 1.152  # 1.152 rad = 66°
        self.phiMin = -self.phiMax
        self.fpaMax = 0.175  # 0.175 rad = 10° # Flight Path Angle = Gamma here
        self.fpaMin = -0.262
        self.regex = '^Performances NxMax=(\S+) NxMin=(\S+) NzMax=(\S+) NzMin=(\S+) PMax=(\S+) PMin=(\S+) AlphaMax=(\S+) AlphaMin=(\S+) PhiMaxManuel=(\S+) PhiMaxAutomatique=(\S+) GammaMax=(\S+) GammaMin=(\S+)'

    def parser(self, *msg):
        """
        Parses the received message and updates the attribute values accordingly.

        Args:
            *msg: Variable number of arguments representing the message to be parsed.
        """
        self.nxMax = float(msg[1])
        self.nxMin = float(msg[2])
        self.nzMax = float(msg[3])
        self.nzMin = float(msg[4])
        self.pMax = float(msg[5])
        self.pMin = float(msg[6])
        self.phiMax = float(msg[9])
        self.fpaMax = float(msg[11])
        self.fpaMin = float(msg[12])
        
class FCU:
    """
    The Flight Control Unit class represents the fcu of an aircraft.
    It manages the autopilot state and provides methods to control it.

    Attributes:
        apState (Enum): The current state of the autopilot. Possible values are 'ON' and 'OFF'.
        regex (str): The regular expression pattern used for parsing messages.

    Methods:
        parser(*msg): Parses the message and updates the autopilot state accordingly.
        setApState(state): Sets the autopilot state to the specified state.
    """

    apState = Enum('ON', 'OFF')

    def __init__(self):
        """
        Initializes the FCU object with the autopilot state set to 'OFF'.
        """
        self.apState = 'OFF'
        self.regex = '^FCUAP1 push'

    def parser(self, *msg):
        """
        Parses the message and updates the autopilot state accordingly.

        Args:
            *msg: Variable number of message arguments.
        """
        print('Ap button pushed on FCU')
        self.apState = 'ON' if self.apState == 'OFF' else 'OFF'
        print('AP state =', self.apState)

    def setApState(self, state):
        """
        Sets the autopilot state to the specified state.

        Args:
            state (str): The state to set the autopilot to.
        """
        self.apState = state

class FlightModel:
    """
    Represents the flight model of an aircraft.

    Attributes:
        x (float): The x-coordinate of the aircraft.
        y (float): The y-coordinate of the aircraft.
        z (float): The z-coordinate of the aircraft.
        Vp (float): The velocity of the aircraft.
        fpa (float): The flight path angle of the aircraft.
        psi (float): The heading angle of the aircraft.
        phi (float): The roll angle of the aircraft.
        regex (str): The regular expression used for parsing the state vector message.
        ready (bool): Indicates whether the flight model's state vector has been received.
    
    Methods:
        parser(*msg): Parses the state vector message and updates the flight model attributes.
        setReady(ready): Sets either the data of the flightModel has been received or not.
    """

    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.Vp = 0
        self.fpa = 0
        self.psi = 0
        self.phi = 0
        self.regex = '^StateVector x=(\S+) y=(\S+) z=(\S+) Vp=(\S+) fpa=(\S+) psi=(\S+) phi=(\S+)'
        self.ready = False

    def parser(self, *msg):
        """
        Parses the state vector message and updates the flight model attributes.

        Args:
            *msg: Variable number of arguments representing the state vector message.
        """
        self.x = float(msg[1])
        self.y = float(msg[2])
        self.z = float(msg[3])
        self.Vp = float(msg[4])
        self.fpa = float(msg[5])
        self.psi = float(msg[6])
        self.phi = float(msg[7])

        self.ready = True
    
    def setReady(self, ready):
        """
        Sets either the data of the flightModel has been received or not.

        Args:
            ready (bool): The readiness status of the flight model.
        """
        self.ready = ready