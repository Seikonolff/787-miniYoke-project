from ivy.std_api import *

def on_cx_proc(agent, connected):
    print("Agent {} is {}connected".format(agent, "" if connected else "dis"))

def on_die_proc(agent):
    print("Agent {} has died".format(agent))

app_name = "getMsgApp"
ivy_bus = "127.0.0.1:5000"
IvyInit(app_name, "Ready to test", 0, on_cx_proc, on_die_proc)
IvyStart(ivy_bus)

def onMsg(agent, msg):
    print('Received message !')
    print("Received from {} : {}".format(agent, msg))

def parseMsg(agent, *msg):
    print('data0 =', msg[0])
    print('data =', msg[1])

def nullCb(*args):
    pass

#IvyBindMsg(onMsg, ".*")
IvyBindMsg(onMsg, '^PythonExample=(.*)')
IvyBindMsg(parseMsg, '^AP_Longi to AP_Lat data0=(\S+) data=(\S+)')
IvyBindMsg()

if __name__ == "__main__":
    while True:
        pass