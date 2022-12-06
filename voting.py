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

#votes = {"red": [0], "green" : [0], "blue": [0], "yellow": [0]}
votes = [[0],[0],[0],[0]]

def voting_algorithm(list):
    
    red_votes = len(list[0])
    green_votes = len(list[1]) 
    blue_votes = len(list[2]) 
    yellow_votes = len(list[3])
    total_votes = red_votes + green_votes + blue_votes + yellow_votes + 0.01
  
    value_x, value_y = (green_votes - blue_votes)/total_votes, (red_votes - yellow_votes)/total_votes 
    print(value_x, value_y)
    return value_x, value_y



def red_votes(address: str, *args: List[Any]) -> None:

    votes[0].append(1)
    value = voting_algorithm(votes)
    client.send_message('/ableton_address',  value)
    client.send_message('/resolume_address',  value)
    print("hej")
  

def green_votes(address: str, *args: List[Any]) -> None:
    
    votes[1].append(1)
    value = voting_algorithm(votes)
    client.send_message('/ableton_address',  value)
    client.send_message('/resolume_address',  value)

def blue_votes(address: str, *args: List[Any]) -> None:
    
    votes[2].append(1)
    value = voting_algorithm(votes)
    client.send_message('/ableton_address',  value)
    client.send_message('/resolume_address',  value)

def yellow_votes(address: str, *args: List[Any]) -> None:
    
    votes[3].append(1)
    value = voting_algorithm(votes)
    client.send_message('/ableton_address',  value)
    client.send_message('/resolume_address',  value)

dispatcher = Dispatcher() 

dispatcher.map("/blueVote", blue_votes)
dispatcher.map("/greenVote", green_votes)
dispatcher.map("/yellowVote", yellow_votes)
dispatcher.map("/redVote", red_votes)

server = ThreadingOSCUDPServer((ip, port_listen), dispatcher)
server.serve_forever()  # Blocks forever   