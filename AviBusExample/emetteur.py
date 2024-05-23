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
        
        IvySendMsg('FCUAP1 push')
        print("Sent FCU AP push")
        time.sleep(5)

        IvySendMsg('AP_LONGI nx=1 nz=2')
        print("Sent AP LONGI data nx=1 nz=2")
        time.sleep(5)

        IvySendMsg('AP_LAT p=3')
        print("Sent AP LAT data p=3")
        time.sleep(5)

        IvySendMsg('FCUAP1 push')
        print("Sent FCU AP push")
        time.sleep(5)