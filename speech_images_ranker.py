import pythonosc
import pythonosc.osc_server
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient
from typing import List, Any
import numpy as np
import math 

import os
from pytextdist.edit_distance import levenshtein_distance, levenshtein_similarity
from pytextdist.edit_distance import jaro_similarity, jaro_winkler_similarity
from pytextdist.edit_distance import damerau_levenshtein_distance, damerau_levenshtein_similarity
from pytextdist.edit_distance import lcs_distance, lcs_similarity


ip = "127.0.0.1"
port_listen = 3466
port_send = 7066
client_list = SimpleUDPClient(ip, port_send)

R_path = "C:/Users/nilsk/Desktop/AI-bilder/AI-bilder/Röd"
G_path = "C:/Users/nilsk/Desktop/AI-bilder/AI-bilder/Grön"
B_path = "C:/Users/nilsk/Desktop/AI-bilder/AI-bilder/Blå"
Y_path = "C:/Users/nilsk/Desktop/AI-bilder/AI-bilder/Gul"

R = os.listdir(R_path)
G = os.listdir(G_path)
B = os.listdir(B_path)
Y = os.listdir(Y_path)

def calculate_prompt_dist(input_prompt, list):

    L = []
    for i in range(len(list)):
    
        L.append((jaro_winkler_similarity(input_prompt, list[i]) + lcs_similarity(input_prompt, list[i]) + levenshtein_similarity(input_prompt, list[i]) + damerau_levenshtein_similarity(input_prompt,list[i])))

    return L


def prompt_handler(address: str, *args: List[Any]) -> None:

    input_prompt = args[0]
    List_R = calculate_prompt_dist(input_prompt, R)
    List_G = calculate_prompt_dist(input_prompt, G)
    List_B = calculate_prompt_dist(input_prompt, B)
    List_Y = calculate_prompt_dist(input_prompt, Y)

    valueR = (sorted(range(len(List_R)), key=lambda k: List_R[k]))
    valueG = (sorted(range(len(List_G)), key=lambda k: List_G[k]))
    valueB = (sorted(range(len(List_B)), key=lambda k: List_B[k]))
    valueY = (sorted(range(len(List_Y)), key=lambda k: List_Y[k]))

    indices = (valueR[0], valueB[0], valueG[0], valueY[0])

    #order_each_list, grab original index of top value of ordered list
    # as values
    client_list.send_message('/list_address',  indices)

dispatcher = Dispatcher() 

dispatcher.map("/input_prompt", prompt_handler)


server = ThreadingOSCUDPServer((ip, port_listen), dispatcher)
server.serve_forever()  # Blocks forever  
