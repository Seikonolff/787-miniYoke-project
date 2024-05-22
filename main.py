from systems import MiniManche, ApLAT, ApLONG, FMGS, FCU
from bus import AviBus

miniYoke = MiniManche()
apLat = ApLAT()
apLong = ApLONG()
fmgs = FMGS()
fcu = FCU()

aviBus = AviBus()

def init():
    # Bind msg here
    aviBus.bindMsg(fcu.parser, '^AP_STATE=(\S+)')
    aviBus.bindMsg(apLong.parser, '^AP_LONGI nx=(\S+) nz=(\S+)')
    aviBus.bindMsg(apLat.parser, '^AP_LAT p=(\S+)')

if __name__ == '__main__':
    init()
    while True:
        #print('miniYoke state =', miniYoke.state)

        match miniYoke.state :  # Manage states transitions
            case 'MANUAL':
                if fcu.ApState == 'ON':
                    print('miniYoke state switched to AP_ENGAGED')
                    aviBus.sendMsg('FCUAP1 on') # Send acknowledge message to the fcu

                    miniYoke.state = 'AP_ENGAGED'

            case 'AP_ENGAGED':
                if fcu.ApState == 'OFF':
                    print('miniYoke state switched to MANUAL')
                    aviBus.sendMsg('FCUAP1 off') # Send acknowledge message to the fcu

                    miniYoke.state = 'MANUAL'

            case _:
                print("Error : unknown miniYoke state")
            
        match miniYoke.state :  # Manage states actions
            case 'MANUAL':
                if miniYoke.ready:
                    aviBus.sendMsg('APNxControl nx={}'.format(miniYoke.nx))
                    aviBus.sendMsg('APNzControl nz={}'.format(miniYoke.nz))
                    aviBus.sendMsg('APLatControl p={}'.format(miniYoke.p))

                    print('Sent APNxControl nx={}'.format(miniYoke.nx))
                    print('Sent APNzControl nz={}'.format(miniYoke.nz))
                    print('Sent APLatControl p={}'.format(miniYoke.p))

                    miniYoke.setReady(False)

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