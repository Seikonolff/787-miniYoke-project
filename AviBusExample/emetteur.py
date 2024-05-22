import time
from ivy.std_api import *

def on_cx_proc(agent, connected):
    print("Agent {} is {}connected".format(agent, "" if connected else "dis"))

def on_die_proc(agent):
    print("Agent {} has died".format(agent))

app_name = "sendMsgApp"
ivy_bus = "127.0.0.1:5000"
IvyInit(app_name, "Ready to test", 0, on_cx_proc, on_die_proc)
IvyStart(ivy_bus)

if __name__ == "__main__":
    while True:
        #IvySendMsg('PythonExample=Hello, world!')
        
        IvySendMsg('AP_STATE=ON')
        print("Sent AP is ON")
        time.sleep(5)

        IvySendMsg('AP_LONGI nx=1 nz=2')
        time.sleep(5)

        IvySendMsg('AP_LAT p=3')
        time.sleep(5)

        IvySendMsg('AP_STATE=OFF')
        print("Sent AP is OFF")
        time.sleep(5)