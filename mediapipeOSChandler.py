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

ClientID = 8 # need to be updated upon socket connection to specify ClientID of socket connection in the osc address string

client = SimpleUDPClient(ip, port_send)

initial_step_size = 0.01

C1 = initial_step_size
C2 = initial_step_size
C3 = initial_step_size

buffer = 100
prev_args = [[0, 0, 0, 0]]

#save new args to form movement-difference in handler functions 
def save_args(args):
    
    prev_args.clear() 
    prev_args.append(args)

    


    

  #      data_list.append((list, name))
   # else:
    #    pass
        #print((list, name)) ## define NN to be the neural network outputting C1, C2, C3 parameters
        #data_list = []
    #return data_list



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


    x_new = prev_args[0][0] + C1*(args[0] - prev_args[0][0]) 
    y_new = prev_args[0][1] +  C2*(args[1] - prev_args[0][1])
    z_new = prev_args[0][2] + C3*(args[2] - prev_args[0][2])
    
    mean_new = (1/3)*(prev_args[0][0] + prev_args[0][1] + prev_args[0][2]) 
    + ((C1 + C2 + C3)/3)*( (1/3)*(args[0] + args[1] + args[2]) - prev_args[0][3])
    
    osc_name = address[-1]
    #print(value1, value2, value3)
    #mean_value = (1/(C1+C2+C3))*(C1*x + C2*y + C3*z)
    new_args = [x_new, y_new, z_new, mean_new]

    print((x_new, y_new, z_new))

    
    
# C1, C2, C3 constants given by ML process to deternmine step-size

    client.send_message("x_axis_movement",x_new)
    client.send_message("y_axis_movement", y_new)
    client.send_message("z_axis_movement", z_new)
    client.send_message("mean_movement",  mean_new)
    save_args(new_args)


   
    #return value1, value2, value3#, mean_value 



dispatcher = Dispatcher()

#dispatcher.map('/miclevel/max/', handler)

dispatcher.map('/scene/dancer/poseMediapipe//0', handler) 
dispatcher.map('/scene/dancer/poseMediapipe//1', handler) 
dispatcher.map('/scene/dancer/poseMediapipe//2', handler)
dispatcher.map('/scene/dancer/poseMediapipe//3', handler)
dispatcher.map('/scene/dancer/poseMediapipe//4', handler)
dispatcher.map('/scene/dancer/poseMediapipe//5', handler)
dispatcher.map('/scene/dancer/poseMediapipe//6', handler)
dispatcher.map('/scene/dancer/poseMediapipe//7', handler)
dispatcher.map('/scene/dancer/poseMediapipe//8', handler)
dispatcher.map('/scene/dancer/poseMediapipe//9', handler)
dispatcher.map('/scene/dancer/poseMediapipe//10', handler)
dispatcher.map('/scene/dancer/poseMediapipe//11', handler)
dispatcher.map('/scene/dancer/poseMediapipe//12', handler)
dispatcher.map('/scene/dancer/poseMediapipe//13', handler)
dispatcher.map('/scene/dancer/poseMediapipe//14', handler)
dispatcher.map('/scene/dancer/poseMediapipe//15', handler)
dispatcher.map('/scene/dancer/poseMediapipe//16', handler)
dispatcher.map('/scene/dancer/poseMediapipe//17', handler)
dispatcher.map('/scene/dancer/poseMediapipe//18', handler)
dispatcher.map('/scene/dancer/poseMediapipe//19', handler)
dispatcher.map('/scene/dancer/poseMediapipe//20', handler)
dispatcher.map('/scene/dancer/poseMediapipe//21', handler)
dispatcher.map('/scene/dancer/poseMediapipe//22', handler)
dispatcher.map('/scene/dancer/poseMediapipe//23', handler)
dispatcher.map('/scene/dancer/poseMediapipe//24', handler)
dispatcher.map('/scene/dancer/poseMediapipe//25', handler)            
dispatcher.map('/scene/dancer/poseMediapipe//26', handler)
dispatcher.map('/scene/dancer/poseMediapipe//27', handler)
dispatcher.map('/scene/dancer/poseMediapipe//28', handler)
dispatcher.map('/scene/dancer/poseMediapipe//29', handler)
dispatcher.map('/scene/dancer/poseMediapipe//30', handler)
dispatcher.map('/scene/dancer/poseMediapipe//31', handler)
dispatcher.map('/scene/dancer/poseMediapipe//32', handler)



server = ThreadingOSCUDPServer((ip, port_listen), dispatcher)
server.serve_forever()  # Blocks forever


## ML stuff          