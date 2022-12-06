import pythonosc
import pythonosc.osc_server
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient
from typing import List, Any
import numpy as np
import math 

ip = "127.0.0.1"
port_listen = 3456
port_send = 7600



client = SimpleUDPClient(ip, port_send)


def handler(address: str, *args: List[Any]) -> None:

    # map incoming OSC addresses /scene/dancer/poseMediapipe/ClientID/X (X = 1,..32)
    # to OSC addresses corresponding to the Resolume composition.
    # Ideally Resolume addresess are set up for the visual composition
    # there such that each pose joint from mediapipe activates a visually 
    # responsive parameter giving feedback to dancers movement input in 
    # an intuitive way. The Resolume composition also integrates 
    # audio responsiveness through some VST plugin that is
    # connected to parameters of the composition (but at a different composition layer)

    # initialise parameter values -> 


    value1 = args[0]
    value2 = args[1]
    value3 = args[2]
    osc_name = address[-1]
    #print(value1, value2, value3)

    
    

    client.send_message("hej", value1)
    client.send_message("hej2", value2)
    client.send_message("hej3",  value3)
   
    return value1, value2, value3 



dispatcher = Dispatcher()


dispatcher.map('/OSC1', handler1)
dispatcher.map('/OSC2', handler2)
dispatcher.map('/OSC3', handler3)
dispatcher.map('/OSC4', handler4)
dispatcher.map('/OSC5', handler5)
dispatcher.map('/OSC6', handler6)
dispatcher.map('/OSC7', handler7)
dispatcher.map('/OSC8', handler8)
dispatcher.map('/OSC9', handler9)



server = ThreadingOSCUDPServer((ip, port_listen), dispatcher)
server.serve_forever()  # Blocks forever