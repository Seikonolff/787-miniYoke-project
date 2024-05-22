import time
from bus import AviBus

aviBus = AviBus()

def testInit():
    # Bind msg here
    pass

def manualTest():
    # TO DO: Implement test
    # send AP_STATE=OFF
    # send AP_LONGI and AP_LAT data
    # Check that data is not sent
    # send nzMax, nxMax and pMax data from FMGS
    # Check that data is correctly used
    # moove the yoke and check that data is correctly calculated
    # check data is sent to the flight model

    pass

def apEngagedTest():
    # TO DO: Implement test
    # send AP_STATE=ON
    # send AP_LONGI and AP_LAT data
    # Check that data is sent
    # moove the yoke and check that data is not sent + state switch to MANUAL
    pass

if __name__ == '__main__':
    testInit()
    
    manualTest()
    time.sleep(5)
    apEngagedTest()
    time.sleep(5)

    #plot results