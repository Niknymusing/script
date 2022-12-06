import pythonosc
import pythonosc.osc_server
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient
from typing import List, Any
import numpy as np
import math 
import torch
import torch.nn.functional as F
from torch import nn
import time


ip = "127.0.0.1"
port_listen = 3456
port_send = 7501

client = SimpleUDPClient(ip, port_send)

input_address = "/scene/dancer/poseMediapipe//"
output_address = "output_address"
update_address = "update_address"

input_size = 33
hidden_size = 10
output_size = 1

model_input = np.zeros(input_size)


def model_creator(input_size, hidden_size, output_size):
    
    model = nn.Sequential(nn.Linear(input_size, hidden_size),
                      nn.ReLU(),
                      nn.Linear(hidden_size, output_size),
                      nn.Sigmoid())
    return model

model = model_creator(input_size, hidden_size, output_size)

#def model_updater(weights):








def input_handler(address: str, *args: List[Any]) -> None:

    joint_nr = int(address[(len(address)-2):len(address)])
    model_input[joint_nr] = np.array(args) 
    output = model(model_input)
    client.send_message(output_address, output)
    

def model_update_handler(address: str, *args: List[Any]) -> None:

    model[0].weight = args[0]
    model[2].weight = args[1]



dispatcher = Dispatcher()

dispatcher.map(input_address, input_handler)
dispatcher.map(update_address, model_update_handler)

server = ThreadingOSCUDPServer((ip, port_listen), dispatcher)
server.serve_forever()  # Blocks forever