import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F
from torch import nn
import time
import matplotlib

input_size = 1 
hidden_size = 1
output_size = 1 
learning_rate = 0.001
iteration_range = 4001

x_train_np = np.random.randn(25, 1).astype(np.float32)

#np.array ([[4.7], [2.4], [7.5], [7.1], [4.3], 
#                     [7.8], [8.9], [5.2], [4.59], [2.1], 
#                     [8], [5], [7.5], [5], [4],
#                     [8], [5.2], [4.9], [3], [4.7], 
#                     [4], [4.8], [3.5], [2.1], [4.1]],
#                    dtype = np.float32)

y_train_np = np.random.randn(25, 1).astype(np.float32)

#y_train_np = np.array ([[2.6], [1.6], [3.09], [2.4], [2.4], 
#3                     [3.3], [2.6], [1.96], [3.13], [1.76], 
#3                     [3.2], [2.1], [1.6], [2.5], [2.2], 
#3                     [2.75], [2.4], [1.8], [1], [2], 
##                     [1.6], [2.4], [2.6], [1.5], [3.1]], 
#                    dtype = np.float32)

X_train = torch.from_numpy(x_train_np) 
Y_train = torch.from_numpy(y_train_np)
print('requires_grad for X_train: ', X_train.requires_grad)
print('requires_grad for Y_train: ', Y_train.requires_grad)

w1 = torch.rand(input_size, 
                hidden_size, 
                requires_grad=True)

b1 = torch.rand(hidden_size, 
                output_size, 
                requires_grad=True)


for iter in range(iteration_range):
    
    y_pred = X_train.mm(w1).clamp(min=0).add(b1)
    loss = (y_pred - Y_train).pow(2).sum() 
    #if iter % 100 ==0:
    #    print(iter, loss.item())
    loss.backward()
    with torch.no_grad():
        w1 -= learning_rate * w1.grad
        b1 -= learning_rate * b1.grad
        w1.grad.zero_()
        b1.grad.zero_()

print("the parameters are:")
print(w1, b1)


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        # 1 input image channel, 6 output channels, 5x5 square convolution
        # kernel
        self.conv1 = nn.Conv2d(1, 6, 5)
        self.conv2 = nn.Conv2d(6, 16, 5)
        # an affine operation: y = Wx + b
        self.fc1 = nn.Linear(16 * 5 * 5, 120)  # 5*5 from image dimension
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        # Max pooling over a (2, 2) window
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        # If the size is a square, you can specify with a single number
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = torch.flatten(x, 1) # flatten all dimensions except the batch dimension
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


net = Net()

x = torch.randn(6, 1, 5, 5)


##print(Net(x))

def model(input_size, hidden_size, output_size):
    
    model = nn.Sequential(nn.Linear(input_size, hidden_size),
                      nn.ReLU(),
                      nn.Linear(hidden_size, output_size),
                      nn.Sigmoid())
    return model



r = np.random.rand(input_size, 1).astype(np.float32)
r = torch.from_numpy(r)

for i in range(30):
    t1 = time.time()  
    print(model(r), time.time()-t1)


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        # 1 input image channel, 6 output channels, 5x5 square convolution
        # kernel
        self.conv1 = nn.Conv2d(1, 6, 5)
        self.conv2 = nn.Conv2d(6, 16, 5)
        # an affine operation: y = Wx + b
        self.fc1 = nn.Linear(16 * 5 * 5, 120)  # 5*5 from image dimension
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        # Max pooling over a (2, 2) window
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        # If the size is a square, you can specify with a single number
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = torch.flatten(x, 1) # flatten all dimensions except the batch dimension
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x 