from ivy.std_api import *

def on_cx_proc(agent, connected):
    print("Agent {} is {}connected".format(agent, "" if connected else "dis"))

def on_die_proc(agent):
    print("Agent {} has died".format(agent))

class AviBus :
    def __init__(self):
        self.app_name = "MiniYokeModule"
        #self.adress = "224.255.255.255:2010" # Prod
        self.adress = "127.0.0.1:5000" # Test

        IvyInit(self.app_name, "zbi", 0, on_cx_proc, on_die_proc)
        IvyStart(self.adress)

    def sendMsg(self, msg):
        IvySendMsg(msg)
    
    def bindMsg(self, callback, regex):
        IvyBindMsg(callback, regex)