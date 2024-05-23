import threading
from systems import FCC, MiniYoke, ApLAT, ApLONG, FMGS, FCU
from bus import AviBus

fcc = FCC()
miniYoke = MiniYoke(fcc)
apLat = ApLAT()
apLong = ApLONG()
fmgs = FMGS()
fcu = FCU()

aviBus = AviBus(appName="MiniYokeModule", prod=False)

def init():
    while not miniYoke.begin() :
        pass

    yokeThread = threading.Thread(target=miniYoke.listener)
    yokeThread.start()

    # Bind avi bus msg here
    aviBus.bindMsg(fcu.parser, '^FCUAP1 push')
    aviBus.bindMsg(apLong.parser, '^AP_LONGI nx=(\S+) nz=(\S+)')
    aviBus.bindMsg(apLat.parser, '^AP_LAT p=(\S+)')

if __name__ == '__main__':
    init()
    while True:
        #print('miniYoke state =', miniYoke.state)

        match fcc.state :  # Manage states transitions
            case 'MANUAL':
                if fcu.ApState == 'ON':
                    print('fcc state switch from MANUAL to AP_ENGAGED')
                    aviBus.sendMsg('FCUAP1 on') # Send acknowledge message to the fcu

                    fcc.setState('AP_ENGAGED')

            case 'AP_ENGAGED':
                if fcu.ApState == 'OFF':
                    print('fcc state switch from AP_ENGAGED to MANUAL')
                    aviBus.sendMsg('FCUAP1 off') # Send acknowledge message to the fcu

                    fcc.setState('MANUAL')
                
                elif miniYoke.moved : 
                    print('miniYoke state switch from AP_ENGAGED to MANUAL')
                    aviBus.sendMsg('FCUAP1 off') # Send AP off message to the fcu

                    fcc.setState('MANUAL')
                    miniYoke.setMoved(False) # NTS : verifier si quand l'ap vient d'être bougé ça nique pas tout

            case _:
                print("Error : unknown miniYoke state")
            
        match fcc.state :  # Manage states actions
            case 'MANUAL':
                if fcc.ready:
                    aviBus.sendMsg('APNxControl nx={}'.format(fcc.nx))
                    aviBus.sendMsg('APNzControl nz={}'.format(fcc.nz))
                    aviBus.sendMsg('APLatControl p={}'.format(fcc.p))

                    print('Sent APNxControl nx={}'.format(fcc.nx))
                    print('Sent APNzControl nz={}'.format(fcc.nz))
                    print('Sent APLatControl p={}'.format(fcc.p))

                    fcc.setReady(False)

            case 'AP_ENGAGED':
                if apLat.ready and apLong.ready :
                    aviBus.sendMsg('APNxControl nx={}'.format(apLong.nx))
                    aviBus.sendMsg('APNzControl nz={}'.format(apLong.nz))
                    aviBus.sendMsg('APLatControl p={}'.format(apLat.p))

                    print('Sent APNxControl nx={}'.format(apLong.nx))
                    print('Sent APNzControl nz={}'.format(apLong.nz))
                    print('Sent APLatControl p={}'.format(apLat.p))

                    apLat.setReady(False)
                    apLong.setReady(False)
                
            case _:
                print("Error : unknown miniYoke state")