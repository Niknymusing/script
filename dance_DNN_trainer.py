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

input_address = "input_address"

client = SimpleUDPClient(ip, port_send)


def input_handler(address: str, *args: List[Any]) -> None:



dispatcher = Dispatcher()

dispatcher.map(input_address, input_handler)


server = ThreadingOSCUDPServer((ip, port_listen), dispatcher)
server.serve_forever()  # Blocks forever