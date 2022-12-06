import pythonosc
import pythonosc.osc_server
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient
from typing import List, Any
import numpy as np

ip = "127.0.0.1"
port_listen = 3456
port_send = 62006

ClientID = 8 # need to be updated upon socket connection to specify ClientID of socket connection in the osc address string

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

#dispatcher.map('/miclevel/max/', handler)

dispatcher.map('/scene/dancer/poseMediapipe/'+ str(ClientID) +'/1', handler)
dispatcher.map('/scene/dancer/poseMediapipe/'+ str(ClientID) +'/2', handler)
dispatcher.map('/scene/dancer/poseMediapipe/'+ str(ClientID) +'/3', handler)
dispatcher.map('/scene/dancer/poseMediapipe/'+ str(ClientID) +'/4', handler)
dispatcher.map('/scene/dancer/poseMediapipe/'+ str(ClientID) +'/5', handler)
dispatcher.map('/scene/dancer/poseMediapipe/'+ str(ClientID) +'/6', handler)
dispatcher.map('/scene/dancer/poseMediapipe/'+ str(ClientID) +'/7', handler)
dispatcher.map('/scene/dancer/poseMediapipe/'+ str(ClientID) +'/8', handler)
dispatcher.map('/scene/dancer/poseMediapipe/'+ str(ClientID) +'/9', handler)
dispatcher.map('/scene/dancer/poseMediapipe/'+ str(ClientID) +'/10', handler)
dispatcher.map('/scene/dancer/poseMediapipe/'+ str(ClientID) +'/11', handler)
dispatcher.map('/scene/dancer/poseMediapipe/'+ str(ClientID) +'/12', handler)
dispatcher.map('/scene/dancer/poseMediapipe/'+ str(ClientID) +'/13', handler)
dispatcher.map('/scene/dancer/poseMediapipe/'+ str(ClientID) +'/14', handler)
dispatcher.map('/scene/dancer/poseMediapipe/'+ str(ClientID) +'/15', handler)
dispatcher.map('/scene/dancer/poseMediapipe/'+ str(ClientID) +'/16', handler)
dispatcher.map('/scene/dancer/poseMediapipe/'+ str(ClientID) +'/17', handler)
dispatcher.map('/scene/dancer/poseMediapipe/'+ str(ClientID) +'/18', handler)
dispatcher.map('/scene/dancer/poseMediapipe/'+ str(ClientID) +'/19', handler)
dispatcher.map('/scene/dancer/poseMediapipe/'+ str(ClientID) +'/20', handler)
dispatcher.map('/scene/dancer/poseMediapipe/'+ str(ClientID) +'/21', handler)
dispatcher.map('/scene/dancer/poseMediapipe/'+ str(ClientID) +'/22', handler)
dispatcher.map('/scene/dancer/poseMediapipe/'+ str(ClientID) +'/23', handler)
dispatcher.map('/scene/dancer/poseMediapipe/'+ str(ClientID) +'/24', handler)
dispatcher.map('/scene/dancer/poseMediapipe/'+ str(ClientID) +'/25', handler)
dispatcher.map('/scene/dancer/poseMediapipe/'+ str(ClientID) +'/26', handler)
dispatcher.map('/scene/dancer/poseMediapipe/'+ str(ClientID) +'/27', handler)
dispatcher.map('/scene/dancer/poseMediapipe/'+ str(ClientID) +'/28', handler)
dispatcher.map('/scene/dancer/poseMediapipe/'+ str(ClientID) +'/29', handler)
dispatcher.map('/scene/dancer/poseMediapipe/'+ str(ClientID) +'/30', handler)
dispatcher.map('/scene/dancer/poseMediapipe/'+ str(ClientID) +'/31', handler)
dispatcher.map('/scene/dancer/poseMediapipe/'+ str(ClientID) +'/32', handler)



server = ThreadingOSCUDPServer((ip, port_listen), dispatcher)
server.serve_forever()  # Blocks forever


