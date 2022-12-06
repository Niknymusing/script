import pythonosc
import pythonosc.osc_server
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient
from typing import List, Any
import numpy as np
import math 
from scipy.spatial.distance import cdist

ip = "127.0.0.1"
ip_send = "127.0.0.1"
port_listen = 3456
port_send = 7501

client = SimpleUDPClient(ip_send, port_send)

Rate_of_changes = {1:1, 2:1, 3:1}

joint_dist_1 = '/scene/dancer/poseMediapipe//15'
joint_dist_2 = '/scene/dancer/poseMediapipe//16'

vertical_1 = '/scene/dancer/poseMediapipe//15'
vertical_2 = '/scene/dancer/poseMediapipe//16'

right_hand = "/right_hand"
rh_range = [0, 1]
rhand_past_values = {'past_value': [0,0,0], 'derivative': [0,0,0], '2nd_derivative':[0,0,0] }
left_hand = "/left_hand"
lh_range = [0, 1]
lhand_past_values = {'past_value': [0,0,0], 'derivative': [0,0,0], '2nd_derivative':[0,0,0] }
hands_dist = "/hands_dist"
hands_dist_range = [0, 5]
dist_past_values = {'past_value': [0,0,0], 'derivative': [0,0,0], '2nd_derivative':[0,0,0] }

last_L = {0:[[0, 0, 0]]}
last_R = {0:[[0, 0, 0]]}

grid_xdim = 100
grid_ydim = 100

grid_matrix = np.zeros((grid_xdim, grid_ydim))


def parameter_scaler(parameter, range):

    dilation = (range[1]-range[0])/20
    translation = -10
    return dilation * (parameter - translation)

def deform_grid(args, joint):

    x_index, y_index = int((grid_xdim/20)*args[0] + 10), int((grid_xdim/20)*args[1] + 10) 
    grid_matrix[x_index][0] += joint['derivative'][0]
    grid_matrix[y_index][1] += joint['derivative'][0]
    
   # multiprocess, process A (over grid x axis)

    if grid_matrix[x_index][0] > 0:
        
        for i in range(grid_xdim - x_index):

            grid_matrix[x_index + i][0] += (1/((grid_xdim - x_index)*math.factorial(i+1)))*joint['derivative'][0]

    elif grid_matrix[x_index][0] < 0:

        for i in range(grid_xdim):

            grid_matrix[x_index - i][0] += (1/(grid_xdim*math.factorial(i+1)))*joint['derivative'][0]

    else:
        pass

 # multiprocess, process B (over grid y axis)

    if grid_matrix[y_index][1] > 0:
        
        for i in range(grid_ydim - y_index):

            grid_matrix[y_index + i][1] += (1/((grid_ydim - y_index)*math.factorial(i+1)))*joint['derivative'][1]

    elif grid_matrix[y_index][1] < 0:

        for i in range(grid_xdim):

            grid_matrix[x_index - i][1] += (1/((grid_ydim)*math.factorial(i+1)))*joint['derivative'][1]

    else:
        pass


    




def vertical_L(address: str, *args: List[Any]) -> None:
    
    last_L[0] = [args]
    client.send_message(left_hand, parameter_scaler(args[1], lh_range) * Rate_of_changes[1] * args[1])

def vertical_R(address: str, *args: List[Any]) -> None:
    
    last_R[0] = [args]
    client.send_message(right_hand, parameter_scaler(args[1], rh_range) * Rate_of_changes[2] * args[1])
    D1 = [args] - rhand_past_values['past_value']
    rhand_past_values['2nd_derivative'] = D1 - rhand_past_values['derivative'] 
    rhand_past_values['derivative'] = D1
    rhand_past_values['past_value'] = [args]
    deform_grid(args, rhand_past_values)


def dist_LR(address: str, *args: List[Any]) -> None:
    
    last_L[0] = [args]
    d = cdist(last_L[0], last_R[0])
    client.send_message(hands_dist, parameter_scaler(d, hands_dist_range) * Rate_of_changes[3] * d)
    

def dist_RL(address: str, *args: List[Any]) -> None:

    last_R[0] = [args]
    d = cdist(last_L[0], last_R[0])
    client.send_message(hands_dist, parameter_scaler(d, hands_dist_range) * Rate_of_changes[3] * d)

# def dist_RL(address: str, *args: List[Any]) -> None:




def change_C1(address: str, *args: List[Any]) -> None:

    Rate_of_changes[1] = args[0]

def change_C2(address: str, *args: List[Any]) -> None:

    Rate_of_changes[2] = args[0]

def change_C3(address: str, *args: List[Any]) -> None:

    Rate_of_changes[3] = args[0]
    

dispatcher = Dispatcher()

#dispatcher.map('/miclevel/max/', handler)


dispatcher.map(joint_dist_2, dist_RL)
dispatcher.map(joint_dist_1, dist_LR)
dispatcher.map(vertical_2, vertical_R)
dispatcher.map(vertical_1, vertical_L)

dispatcher.map('/change_C1', change_C1)
dispatcher.map('/change_C2', change_C2)
dispatcher.map('/change_C3', change_C3)

server = ThreadingOSCUDPServer((ip, port_listen), dispatcher)
server.serve_forever()  # Blocks forever