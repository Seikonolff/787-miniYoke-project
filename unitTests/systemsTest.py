import time,threading
import matplotlib.pyplot as plt

class FmgsTest():
    """
    This class represents the FMGS for testing purposes.

    Attributes:
        nxMax (float): The maximum value for nx.
        nxMin (float): The minimum value for nx.
        nzMax (float): The maximum value for nz.
        nzMin (float): The minimum value for nz.
        pMax (float): The maximum value for p.
        pMin (float): The minimum value for p.
        alphaMax (float): The maximum value for alpha.
        alphaMin (float): The minimum value for alpha.
        phiMaxManuel (float): The maximum value for phi (manuel).
        phiMinManuel (float): The minimum value for phi (manuel).
        phiMaxAutomatique (float): The maximum value for phi (automatique).
        fpaMax (float): The maximum value for fpa.
        fpaMin (float): The minimum value for fpa.
        regex (str): The regular expression pattern.

        nxMaxData (list): The list to store nxMax data.
        nxMinData (list): The list to store nxMin data.
        nzMaxData (list): The list to store nzMax data.
        nzMinData (list): The list to store nzMin data.
        pMaxData (list): The list to store pMax data.
        pMinData (list): The list to store pMin data.
        alphaMaxData (list): The list to store alphaMax data.
        alphaMinData (list): The list to store alphaMin data.
        phiMaxManuelData (list): The list to store phiMaxManuel data.
        phiMinManuelData (list): The list to store phiMinManuel data.
        phiMaxAutomatiqueData (list): The list to store phiMaxAutomatique data.
        fpaMaxData (list): The list to store fpaMax data.
        fpaMinData (list): The list to store fpaMin data.
    
    Methods:
        getRegex(): Get the regular expression pattern.
        setData(nxMax, nxMin, nzMax, nzMin, pMax, pMin, alphaMax, alphaMin, phiMaxManuel, phiMaxAutomatique, fpaMax, fpaMin): Set the data of the FMGS test.
        resetRecord(): Reset the data records.
    """

    def __init__(self):
        self.nxMax = 0
        self.nxMin = 0
        self.nzMax = 0
        self.nzMin = 0
        self.pMax = 0
        self.pMin = 0
        self.alphaMax = 0
        self.alphaMin = 0
        self.phiMaxManuel = 0
        self.phiMinManuel = 0
        self.phiMaxAutomatique = 0
        self.fpaMax = 0
        self.fpaMin = 0
        self.regex = 'Performances NxMax={} NxMin={} NzMax={} NzMin={} PMax={} PMin={} AlphaMax={} AlphaMin={} PhiMaxManuel={} PhiMaxAutomatique={} GammaMax={} GammaMin={}'

        self.nxMaxData = []
        self.nxMinData = []
        self.nzMaxData = []
        self.nzMinData = []
        self.pMaxData = []
        self.pMinData = []
        self.alphaMaxData = []
        self.alphaMinData = []
        self.phiMaxManuelData = []
        self.phiMinManuelData = []
        self.phiMaxAutomatiqueData = []
        self.fpaMaxData = []
        self.fpaMinData = []

    def getRegex(self):
        """
        Get the formated regular expression pattern.

        Returns:
            str: The regular expression pattern.
        """
        regexToSend = self.regex.format(self.nxMax, self.nxMin, self.nzMax, self.nzMin, self.pMax, self.pMin, self.alphaMax, self.alphaMin, self.phiMaxManuel, self.phiMaxAutomatique, self.fpaMax, self.fpaMin)
        return regexToSend

    def setData(self, nxMax, nxMin, nzMax, nzMin, pMax, pMin, alphaMax, alphaMin, phiMaxManuel, phiMaxAutomatique, fpaMax, fpaMin):
        """
        Set the data of the FMGS.

        Args:
            nxMax (float): The maximum value for nx.
            nxMin (float): The minimum value for nx.
            nzMax (float): The maximum value for nz.
            nzMin (float): The minimum value for nz.
            pMax (float): The maximum value for p.
            pMin (float): The minimum value for p.
            alphaMax (float): The maximum value for alpha.
            alphaMin (float): The minimum value for alpha.
            phiMaxManuel (float): The maximum value for phi (manuel).
            phiMaxAutomatique (float): The maximum value for phi (automatique).
            fpaMax (float): The maximum value for fpa.
            fpaMin (float): The minimum value for fpa.
        """
        self.nxMax = float(nxMax)
        self.nxMin = float(nxMin)
        self.nzMax = float(nzMax)
        self.nzMin = float(nzMin)
        self.pMax = float(pMax)
        self.pMin = float(pMin)
        self.alphaMax = float(alphaMax)
        self.alphaMin = float(alphaMin)
        self.phiMaxManuel = float(phiMaxManuel)
        self.phiMinManuel = - self.phiMaxManuel
        self.phiMaxAutomatique = float(phiMaxAutomatique)
        self.fpaMax = float(fpaMax)
        self.fpaMin = float(fpaMin)
    
    def resetRecord(self):
        """
        Reset the data records.
        """
        self.nxMaxData = []
        self.nxMinData = []
        self.nzMaxData = []
        self.nzMinData = []
        self.pMaxData = []
        self.pMinData = []
        self.alphaMaxData = []
        self.alphaMinData = []
        self.phiMaxManuelData = []
        self.phiMinManuelData = []
        self.phiMaxAutomatiqueData = []
        self.fpaMaxData = []
        self.fpaMinData = []
    
class ApLATTest():
    """
    This class represents the ApLAT system for testing purposes.

    Attributes:
        p (int): The value of p.
        regex (str): The regex pattern used for formatting.
        pData (list): A list to store data.

    Methods:
        getRegex(): Returns the formatted regex pattern.
        setData(p): Sets the value of p.
        resetRecord(): Resets the pData list.
    """

    def __init__(self):
        self.p = 0
        self.regex = 'AP_LAT p={}'

        self.pData = []
    
    def getRegex(self):
        """
        Returns the formatted regular expression pattern.

        Returns:
            str: The formatted regular expression pattern.
        """
        regexToSend = self.regex.format(self.p)
        
        return regexToSend
    
    def setData(self, p):
        """
        Sets the value of p.

        Parameters:
            p (int): The value of p.
        """
        self.p = p

    def resetRecord(self):
        """
        Resets the pData list.
        """
        self.pData = []

class ApLONGTest():
    """
    This class represents the ApLONG system for testing purposes.

    Attributes:
        nx (int): The value of nx.
        nz (int): The value of nz.
        nxData (list): A list to store nx data.
        nzData (list): A list to store nz data.
        regex (str): The regex pattern for formatting nx and nz values.

    Methods:
        getRegex(): Get the regex pattern with formatted nx and nz values.
        setData(nx, nz): Set the values of nx and nz.
        resetRecord(): Reset the nxData and nzData lists.
    """
    def __init__(self):
        self.nx = 0
        self.nz = 0

        self.nxData = []
        self.nzData = []

        self.regex = 'PaLong Nx={} Nz={}'

    def getRegex(self):
        """
        Get the regex pattern with formatted nx and nz values.

        Returns:
            str: The regex pattern.
        """
        regexToSend = self.regex.format(self.nx, self.nz)
        
        return regexToSend
    
    def setData(self, nx, nz):
        """
        Set the values of nx and nz.

        Args:
            nx (int): The value of nx.
            nz (int): The value of nz.
        """
        self.nx = nx
        self.nz = nz
    
    def resetRecord(self):
        """
        Reset the nxData and nzData lists.
        """
        self.nxData = []
        self.nzData = []

class StateVectorTest():
    """
    This class represents the StateVector for testing purposes.

    Attributes:
        x (float): The value of x.
        y (float): The value of y.
        z (float): The value of z.
        Vp (float): The value of Vp.
        fpa (float): The value of fpa.
        psi (float): The value of psi.
        phi (float): The value of phi.
        parserRegex (str): The regex pattern used for parsing.

        xData (list): A list to store x data.
        yData (list): A list to store y data.
        zData (list): A list to store z data.
        VpData (list): A list to store Vp data.
        fpaData (list): A list to store fpa data.
        psiData (list): A list to store psi data.
        phiData (list): A list to store phi data.

        regex (str): The regex pattern for formatting x, y, z, Vp, fpa, psi, and phi values.
        windregex (str): The regex pattern for formatting VWind and dirWind values.
        MagneticDeclination (str): The regex pattern for formatting MagneticDeclination value.

    Methods:
        initRegexs(VWind, dirWind, MagneticDeclination): Initialize the regex patterns with formatted values to initialize the simulation.
        parser(*msg): Parse the message and set the attribute values.
        resetRecord(): Reset the data records.
    """
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.Vp = 0
        self.fpa = 0
        self.psi = 0
        self.phi = 0
        self.parserRegex = '^StateVector x=(\S+) y=(\S+) z=(\S+) Vp=(\S+) fpa=(\S+) psi=(\S+) phi=(\S+)'

        self.xData = []
        self.yData = []
        self.zData = []
        self.VpData = []
        self.fpaData = []
        self.psiData = []
        self.phiData = []

        self.regex = 'InitStateVector x={} y={} z={} Vp={} fpa={} psi={} phi={}'
        self.windregex = 'VWind={} dirWind={}'
        self.MagneticDeclination = 'MagneticDeclination={}'

    def initRegexs(self, vWind, dirWind, magneticDeclination):
        """
        Initialize the regex patterns with formatted values to initialize the simulation.

        Parameters:
            vWind (float): The value of VWind.
            dirWind (float): The value of dirWind.
            magneticDeclination (float): The value of MagneticDeclination.

        Returns:
            tuple: A tuple containing the formatted regex patterns.
        """
        regexToSend = self.regex.format(0, 0, 10668, 100, 0, 0, 0)  # Level flight at FL350
        windRegexToSend = self.windregex.format(vWind, dirWind)
        MagneticDeclinationRegexToSend = self.MagneticDeclination.format(magneticDeclination)

        return regexToSend, windRegexToSend, MagneticDeclinationRegexToSend

    def parser(self, *msg):
        """
        Parse the message and set the attribute values.

        Parameters:
            *msg: The message to parse.
        """
        self.x = float(msg[1])
        self.y = float(msg[2])
        self.z = float(msg[3])
        self.Vp = float(msg[4])
        self.fpa = float(msg[5])
        self.psi = float(msg[6])
        self.phi = float(msg[7])

    def resetRecord(self):
        """
        Reset the data records.
        """
        self.xData = []
        self.yData = []
        self.zData = []
        self.VpData = []
        self.fpaData = []
        self.psiData = []
        self.phiData = []

class FcuTest():
    """
    This class represents the Flight Control Unit (FCU) for testing purposes.
    
    Attributes:
        apState (str): The current state of the autopilot.
        regex (str): The regular expression used for matching a specific pattern.
        apStateData (list): A list to store the recorded autopilot states.
    """
    
    def __init__(self):
        self.apState = 'off'
        self.regex = 'FCUAP1 push'
        self.apStateData = []
    
    def getRegex(self):
        """
        Returns the regular expression of the  FCU.
        
        Returns:
            str: The regular expression.
        """
        return self.regex
    
    def setApState(self, apState):
        """
        Sets the current state of the autopilot.
        
        Args:
            apState (str): The new state of the autopilot.
        """
        self.apState = apState
    
    def resetRecord(self):
        """
        Resets the recorded autopilot states.
        """
        self.apStateData = []
    
class FccTest():
    """
    This class represents a test for the Flight Control Computer (FCC).
    It stores various data related to the FCC and provides methods for parsing and resetting the data.

    Attributes:
        nx (float): The value of nx control.
        nz (float): The value of nz control.
        p (float): The value of roll rate control.
        flaps (float): The state of the flaps.
        gear (bool): The state of the landing gear.
        fcu (object): The Flight Control Unit (FCU) object.
        nxData (list): A list to store nx data.
        nzData (list): A list to store nz data.
        pData (list): A list to store p data.
        nxRegex (str): The regular expression pattern for nx control.
        nzRegex (str): The regular expression pattern for nz control.
        pRegex (str): The regular expression pattern for roll rate control.
        flapsRegex (str): The regular expression pattern for flaps state.
        gearRegex (str): The regular expression pattern for landing gear state.
        apAckRegex (str): The regular expression pattern for AP Acknowledgement.

    Methods:
        nxParser: Parses the nx control data.
        nzParser: Parses the nz control data.
        pParser: Parses the roll rate control data.
        flapsParser: Parses the flaps state data.
        gearParser: Parses the landing gear state data.
        apAckParser: Parses the AP Acknowledgement data.
        resetRecord: Resets the stored data.
    """

    def __init__(self, fcu):
        self.nx = 0
        self.nz = 0
        self.p = 0
        self.flaps = 0
        self.gear = False
        self.fcu = fcu

        self.nxData = []
        self.nzData = []
        self.pData = []

        self.nxRegex = '^APNxControl nx=(\S+)'
        self.nzRegex = '^APNzControl nz=(\S+)'
        self.pRegex = '^APLatControl rollRate=(\S+)'
        self.flapsRegex = '^VoletState=(\S+)'
        self.gearRegex = '^LandingGearState=(\S+)'
        self.apAckRegex = '^FCUAP1 (.*)'
    
    def nxParser(self, *msg):
        self.nx = float(msg[1])
    
    def nzParser(self, *msg):
        self.nz = float(msg[1])
    
    def pParser(self, *msg):
        self.p = float(msg[1])
    
    def flapsParser(self, *msg):
        self.flaps = float(msg[1])
    
    def gearParser(self, *msg):
        if msg[1] == 'True':
            self.gear = True
        else:
            self.gear = False
    
    def apAckParser(self, *msg):
        print("AP Ack: ", msg[1])
        self.fcu.apState = msg[1]
    
    def resetRecord(self):
        self.nxData = []
        self.nzData = []
        self.pData = []

class DataSampler():
    """
    A class that samples datas from various components of the system.

    Attributes:
        fmgs (FMGS): The FMGS component.
        apLat (APLat): The APLat component.
        apLong (APLong): The APLong component.
        stateVector (StateVector): The StateVector component.
        fcu (FCU): The FCU component.
        fcc (FCC): The FCC component.
        sampleThread (Thread): The thread used for sampling.
        doSample (bool): Flag indicating whether to perform sampling.
        threadRunning (bool): Flag indicating whether the thread is running.

    Methods:
        start(self): Sets the doSample flag to True, indicating to start sampling.
        fetch(self): The function that runs in the sampling thread.
        sampleFmgs(self, fmgs): Samples data from the FMGS component.
        sampleApLat(self, apLat): Samples data from the APLat component.
        sampleApLong(self, apLong): Samples data from the APLong component.
        sampleStateVector(self, stateVector): Samples data from the StateVector component.
        sampleFcu(self, fcu): Samples data from the FCU component.
        samplefcc(self, fcc): Samples data from the FCC component.
        stop(self): Stops the sampling process.
        reset(self): Resets the recorded data in all components.
        end(self): Ends the sampling thread.
        plotNzLimitation(self): Plots the limitation of Nz values.
        plotFpaLimitation(self): Plots the limitation of FPA values.
        plotPLimitationTest(self): Plots the limitation of P values.
        plotPhiLimitationTest(self): Plots the limitation of Phi values.
    """
    def __init__(self, fmgs, apLat, apLong, stateVector, fcu, fcc):
        self.fmgs = fmgs
        self.apLat = apLat
        self.apLong = apLong
        self.stateVector = stateVector
        self.fcu = fcu
        self.fcc = fcc

        self.sampleThread = None
        self.doSample = False
        self.threadRunning = True

        self.sampleThread = threading.Thread(target=self.fetch)
        self.sampleThread.start()
    
    def start(self):
        """
        Sets the doSample flag to True, indicating to start sampling.
        """
        self.doSample = True

    def fetch(self):
        """
        The function that runs in the sampling thread.
        Continuously samples data from the components if doSample flag is True.
        """
        while self.threadRunning:
            if self.doSample:
                #print(".")
                self.sampleFmgs(self.fmgs)
                self.sampleApLat(self.apLat)
                self.sampleApLong(self.apLong)
                self.sampleStateVector(self.stateVector)
                self.sampleFcu(self.fcu)
                self.samplefcc(self.fcc)
                
            time.sleep(0.1)

    def sampleFmgs(self, fmgs):
        """
        Samples data from the FMGS component and appends it to the corresponding data lists.
        
        Args:
            fmgs (FMGS): The FMGS component.
        """
        fmgs.nxMaxData.append(fmgs.nxMax)
        fmgs.nxMinData.append(fmgs.nxMin)
        fmgs.nzMaxData.append(fmgs.nzMax)
        fmgs.nzMinData.append(fmgs.nzMin)
        fmgs.pMaxData.append(fmgs.pMax)
        fmgs.pMinData.append(fmgs.pMin)
        fmgs.alphaMaxData.append(fmgs.alphaMax)
        fmgs.alphaMinData.append(fmgs.alphaMin)
        fmgs.phiMaxManuelData.append(fmgs.phiMaxManuel)
        fmgs.phiMinManuelData.append(fmgs.phiMinManuel)
        fmgs.phiMaxAutomatiqueData.append(fmgs.phiMaxAutomatique)
        fmgs.fpaMaxData.append(fmgs.fpaMax)
        fmgs.fpaMinData.append(fmgs.fpaMin)
        
    def sampleApLat(self, apLat):
        """
        Samples data from the APLat component and appends it to the corresponding data lists.
        
        Args:
            apLat (APLat): The APLat component.
        """
        apLat.pData.append(apLat.p)
        pass
    
    def sampleApLong(self, apLong):
        """
        Samples data from the APLong component and appends it to the corresponding data lists.
        
        Args:
            apLong (APLong): The APLong component.
        """
        apLong.nxData.append(apLong.nx)
        pass

    def sampleStateVector(self, stateVector):
        """
        Samples data from the StateVector component and appends it to the corresponding data lists.
        
        Args:
            stateVector (StateVector): The StateVector component.
        """
        stateVector.xData.append(stateVector.x)
        stateVector.yData.append(stateVector.y)
        stateVector.zData.append(stateVector.z)
        stateVector.VpData.append(stateVector.Vp)
        stateVector.fpaData.append(stateVector.fpa)
        stateVector.psiData.append(stateVector.psi)
        stateVector.phiData.append(stateVector.phi)
        
    def sampleFcu(self, fcu):
        """
        Samples data from the FCU component and appends it to the corresponding data lists.
        
        Args:
            fcu (FCU): The FCU component.
        """
        fcu.apStateData.append(fcu.apState)
    
    def samplefcc(self, fcc):
        """
        Samples data from the FCC component and appends it to the corresponding data lists.
        
        Args:
            fcc (FCC): The FCC component.
        """
        fcc.nxData.append(fcc.nx)
        fcc.nzData.append(fcc.nz)
        fcc.pData.append(fcc.p)
    
    def stop(self):
        """
        Stops the sampling process by setting the doSample flag to False.
        """
        self.doSample = False
    
    def reset(self):
        """
        Resets the recorded data in all components.
        """
        self.fmgs.resetRecord()
        self.apLat.resetRecord()
        self.apLong.resetRecord()
        self.stateVector.resetRecord()
        self.fcu.resetRecord()
        self.fcc.resetRecord()
    
    def end(self):
        """
        Ends the sampling thread by setting the threadRunning flag to False.
        """
        self.threadRunning = False
    
    def plotNzLimitation(self):
        """
        Plots the limitation of Nz values.
        """
        nz = self.fcc.nzData
        nzMax = self.fmgs.nzMaxData
        nzMin = self.fmgs.nzMinData

        plt.figure(figsize=(10, 6))

        plt.plot(nz, label='Nz')
        plt.plot(nzMax, label='NzMax')
        plt.plot(nzMin, label='NzMin')
        plt.title('FCC Nz vs FMGS NzMax & NzMin')
        plt.xlabel('time (ds)')
        plt.ylabel('Nz')
        plt.legend()

        plt.tight_layout()
        plt.show()

    def plotFpaLimitation(self):
        """
        Plots the limitation of FPA values.
        """
        fpa = self.stateVector.fpaData
        fpaMax = self.fmgs.fpaMaxData
        fpaMin = self.fmgs.fpaMinData

        plt.figure(figsize=(10, 6))

        plt.plot(fpa, label='fpa (rad)')
        plt.plot(fpaMax, label='fpa max (rad)')
        plt.plot(fpaMin, label='fpa min (rad)')
        plt.title('StateVector FPA vs FMGS FpaMax & FpaMin')
        plt.xlabel('time (ds)')
        plt.ylabel('FPA')
        plt.legend()

        plt.tight_layout()
        plt.show()

    def plotPLimitationTest(self):
        """
        Plots the limitation of P values.
        """
        p = self.fcc.pData
        pMax = self.fmgs.pMaxData
        pMin = self.fmgs.pMinData

        plt.figure(figsize=(10, 6))

        plt.plot(p, label='p (rad/s)')
        plt.plot(pMax, label='p Max (rad/s)')
        plt.plot(pMin, label='p Min (rad/s)')
        plt.title('FCC P vs FMGS PMax & PMin')
        plt.xlabel('time (ds)')
        plt.ylabel('P')
        plt.legend()

        plt.tight_layout()
        plt.show()
    
    def plotPhiLimitationTest(self):
        """
        Plots the limitation of Phi values.
        """
        phiMax = self.fmgs.phiMaxManuelData
        phiMin = self.fmgs.phiMinManuelData
        phi = self.stateVector.phiData

        plt.figure(figsize=(10, 6))

        plt.plot(phi, label='Phi (rad)')
        plt.plot(phiMax, label='PhiMax (rad)')
        plt.plot(phiMin, label='PhiMin (rad)')
        plt.title('FCC Phi Limitation')
        plt.xlabel('time (ds)')
        plt.ylabel('Phi')
        plt.legend()

        plt.tight_layout()
        plt.show()