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
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import torch.optim as optim
import time



ip = "127.0.0.1"
port_listen = 9042
port_send = 7501

client = SimpleUDPClient(ip, port_send)

input_addresses = []

for i in range(34):

    input_addresses.append("/scene/dancer/poseMediapipe//"+str(i))

output_address = "output_address"
update_address = "update_address"
train_address = "train_address" 

input_size = 99
hidden_size = 13
output_size = 1

model_input = torch.zeros(33, input_size)

training_data = torch.zeros((999999, 2, output_size))
counter = [0]


def model_creator(input_size, hidden_size, output_size):
    
    model = nn.Sequential(nn.Linear(input_size, hidden_size),
                      nn.ReLU(),
                      nn.Linear(hidden_size, output_size),
                      nn.Sigmoid())
    return model

model = model_creator(input_size, hidden_size, output_size)

loss_function = nn.MSELoss()
learning_rate = 0.01
batch_size = 10
optimizer = optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

def NN_trainer(x, y):

    loss = loss_function(x, y)
    loss.backward()
    optimizer.step()

#def model_updater(weights):


def input_handler(address: str, *args: List[Any]) -> None:

    joint_nr = int(address[29:len(address)])
    a =  torch.tensor(args) 
    model_input[joint_nr], model_input[joint_nr + 1], model_input[joint_nr + 2] = a[0], a[1], a[2]
    output = model(model_input)
    training_data[counter[0]][0] = output
    send = output.detach.numpy.tolist()
    client.send_message(output_address, send)
    counter[0] += 1     # increments counter value by 1 to assign corret tensor position for the (x, y) training values
    print(model_input[joint_nr])
    

def model_update_handler(address: str, *args: List[Any]) -> None:

    model[0].weight = args[0]
    model[2].weight = args[1]
    print(args)

def model_trainer(address: str, *args: List[Any]) -> None:
    
    a = torch.tensor(args)
    training_data[counter[0]][1] = a
    NN_trainer(training_data[counter[0]][0], training_data[counter[0]][1])


dispatcher = Dispatcher()

dispatcher.map(input_addresses[0], input_handler)
dispatcher.map(input_addresses[1], input_handler)
dispatcher.map(input_addresses[2], input_handler)
dispatcher.map(input_addresses[3], input_handler)
dispatcher.map(input_addresses[4], input_handler)
dispatcher.map(input_addresses[5], input_handler)
dispatcher.map(input_addresses[6], input_handler)
dispatcher.map(input_addresses[7], input_handler)
dispatcher.map(input_addresses[8], input_handler)
dispatcher.map(input_addresses[9], input_handler)
dispatcher.map(input_addresses[10], input_handler)
dispatcher.map(input_addresses[11], input_handler)
dispatcher.map(input_addresses[12], input_handler)
dispatcher.map(input_addresses[13], input_handler)
dispatcher.map(input_addresses[14], input_handler)
dispatcher.map(input_addresses[15], input_handler)
dispatcher.map(input_addresses[16], input_handler)
dispatcher.map(input_addresses[17], input_handler)
dispatcher.map(input_addresses[18], input_handler)
dispatcher.map(input_addresses[19], input_handler)
dispatcher.map(input_addresses[20], input_handler)
dispatcher.map(input_addresses[21], input_handler)
dispatcher.map(input_addresses[22], input_handler)
dispatcher.map(input_addresses[23], input_handler)
dispatcher.map(input_addresses[24], input_handler)
dispatcher.map(input_addresses[25], input_handler)
dispatcher.map(input_addresses[26], input_handler)
dispatcher.map(input_addresses[27], input_handler)
dispatcher.map(input_addresses[28], input_handler)
dispatcher.map(input_addresses[29], input_handler) 
dispatcher.map(input_addresses[30], input_handler)
dispatcher.map(input_addresses[31], input_handler)
dispatcher.map(input_addresses[32], input_handler)
dispatcher.map(input_addresses[33], input_handler)

dispatcher.map(train_address, model_trainer)

dispatcher.map(update_address, model_update_handler)

server = ThreadingOSCUDPServer((ip, port_listen), dispatcher)
server.serve_forever()  # Blocks forever     