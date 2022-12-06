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

client = SimpleUDPClient(ip, port_send)


def handler(address: str, *args: List[Any]) -> None:

    value1 = args[0]
    #value2 = args[1]
    #value3 = args[2]
    #osc_name = address[-1]
    
    client.send_message("mean_movement",  value1)

    #return value1, value2, value3 


dispatcher = Dispatcher()

#dispatcher.map('/miclevel/max/', handler)

dispatcher.map('/composition/tempcontrooller/tempo', handler)

server = ThreadingOSCUDPServer((ip, port_listen), dispatcher)
server.serve_forever()  # Blocks forever