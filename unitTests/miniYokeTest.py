import time
from systemsTest import FmgsTest, ApLATTest, ApLONGTest, StateVectorTest, FcuTest, FccTest, DataSampler
from busTest import AviBusTest

aviBus = AviBusTest(appName="MiniYokeTest", adress="192.168.0.255:2010")

fmgs = FmgsTest()
apLat = ApLATTest()
apLong = ApLONGTest()
stateVector = StateVectorTest()
fcuTest = FcuTest()
fccTest = FccTest()
dataSampler = DataSampler(fmgs, apLat, apLong, stateVector, fcuTest, fccTest)

def testInit():
    global run
    run = True

    print("Welcome to the miniYoke test program")
    # Bind msg here
    aviBus.bindMsg(stateVector.parser, stateVector.parserRegex)
    aviBus.bindMsg(fccTest.nxParser, fccTest.nxRegex)
    aviBus.bindMsg(fccTest.nzParser, fccTest.nzRegex)
    aviBus.bindMsg(fccTest.pParser, fccTest.pRegex)

    time.sleep(10)

def nzLimitationTest():
    print("Begin nzMax and alphaMax test")
    for msg in stateVector.initRegexs(30, 120, 12.69):
        aviBus.sendMsg(msg)

    dataSampler.run()
    
    fmgs.setData(nxMax=0.5, 
                 nxMin=-1, 
                 nzMax=2.5, 
                 nzMin=-1.5, 
                 pMax=0.7, 
                 pMin=-0.7, 
                 alphaMax=0.5, 
                 alphaMin=-0.5, 
                 phiMaxManuel=1.152, 
                 phiMaxAutomatique=1.52, 
                 fpaMax=0.175, 
                 fpaMin=-0.5)
    msg = fmgs.getRegex()
    aviBus.sendMsg(msg)

    print("please pull the yoke for 10 secs")
    time.sleep(3)
    fmgs.setData(nxMax=0.5, 
                 nxMin=-1, 
                 nzMax=1, 
                 nzMin=-0.5, 
                 pMax=0.7, 
                 pMin=-0.7, 
                 alphaMax=0.5, 
                 alphaMin=-0.5, 
                 phiMaxManuel=1.152, 
                 phiMaxAutomatique=1.52, 
                 fpaMax=0.175, 
                 fpaMin=-0.5)
    msg = fmgs.getRegex()
    aviBus.sendMsg(msg)
    time.sleep(3)

    fmgs.setData(nxMax=0.5, 
                 nxMin=-1, 
                 nzMax=1.75, 
                 nzMin=-1, 
                 pMax=0.7, 
                 pMin=-0.7, 
                 alphaMax=0.5, 
                 alphaMin=-0.5, 
                 phiMaxManuel=1.152, 
                 phiMaxAutomatique=1.52, 
                 fpaMax=0.175, 
                 fpaMin=-0.5)
    msg = fmgs.getRegex()

    aviBus.sendMsg(msg)
    time.sleep(4)
    
    dataSampler.stop()
    dataSampler.plotNzLimitationTest()
    dataSampler.reset()
    
def nzAlphaMintest():
    pass

def pLimitationTest():
    print("Begin p limitation test")
    for msg in stateVector.initRegexs(30, 120, 12.69):
        aviBus.sendMsg(msg)
    
    dataSampler.run()

    fmgs.setData(nxMax=0.5, 
                 nxMin=-1, 
                 nzMax=2.5, 
                 nzMin=-1.5, 
                 pMax=0.7, 
                 pMin=-0.7, 
                 alphaMax=0.5, 
                 alphaMin=-0.5, 
                 phiMaxManuel=1.152, 
                 phiMaxAutomatique=1.52, 
                 fpaMax=0.175, 
                 fpaMin=-0.5)
    msg = fmgs.getRegex()
    aviBus.sendMsg(msg)

    print("please roll the yoke for 10 secs")
    time.sleep(3)

    fmgs.setData(nxMax=0.5, 
                 nxMin=-1, 
                 nzMax=2.5, 
                 nzMin=-1.5, 
                 pMax=1.1, 
                 pMin=-1.1, 
                 alphaMax=0.5, 
                 alphaMin=-0.5, 
                 phiMaxManuel=1.152, 
                 phiMaxAutomatique=1.52, 
                 fpaMax=0.175, 
                 fpaMin=-0.5)
    msg = fmgs.getRegex()
    aviBus.sendMsg(msg)

    time.sleep(3)

    fmgs.setData(nxMax=0.5, 
                 nxMin=-1, 
                 nzMax=2.5, 
                 nzMin=-1.5, 
                 pMax=0.3, 
                 pMin=-0.3, 
                 alphaMax=0.5, 
                 alphaMin=-0.5, 
                 phiMaxManuel=1.152, 
                 phiMaxAutomatique=1.52, 
                 fpaMax=0.175, 
                 fpaMin=-0.5)
    
    msg = fmgs.getRegex()
    aviBus.sendMsg(msg)
    time.sleep(4)

    dataSampler.stop()
    dataSampler.plotPLimitaionTest()

    dataSampler.reset()

def nxAlphaMaxtest():
    pass

def main():
    pass

if __name__ == '__main__':
    testInit()
    nzLimitationTest()
    pLimitationTest()
    try :
        while run:
            main()
    except KeyboardInterrupt:
        run = False
        aviBus.stop()
    #plot results