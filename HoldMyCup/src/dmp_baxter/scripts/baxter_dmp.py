#import rospy
#import baxter_interface
import numpy as np
import matplotlib.pyplot as plt
from train_dmp import train_dmp
from DMP_runner import DMP_runner
#from simple_trajectories import y_cubed_trajectory
#from simple_trajectories import y_lin_trajectory
import simple_trajectories
import bax


#Name of the file
filename = []
for i in range(0,7):
    A='{}{}{}'.format('joint',i,'.xml')
    filename.append(A)

#Set no. of basis functions
n_rfs = 200

#Set the time-step
dt = 0.001


##### TRAJECTORY  FOR TRAINING ########
""" Available trajectories: ('ok')

    Linear = simple_trajectories.y_lin_trajectory(dt)
    Exponential = simple_trajectories.y_exp_trajectory(dt)
    Step = simple_trajectories.y_step_trajectory(dt)
    Baxter_s0 = simple_trajectories.bax_trajectory(dt,x) [x = 9 to x = 15 for the 7 baxter joints]
"""
X = []
for i in range(1,8):
    T = simple_trajectories.bax_trajectory(dt,i+8)
    X.append(T)
#T = simple_trajectories.bax_trajectory(dt,9)
#T = simple_trajectories.y_exp_trajectory(dt)
#Obtain w, c & D (in that order) from below function, and generate XML file

for i in range(0,7):
    Important_values = train_dmp(filename[i], n_rfs, X[i], dt)

#start = 0
#goal = 1
Y = []
####BELOW IS GIVEN A NEW POSITION, YOU CAN TEST THE "GOAL" AS THIS POSITION FOR THE JOINTS TO TRY IT OUT.########

position = [0.43707952457256116, 0.030886485048354118, -0.9100930412938544,-0.049960844259059556,0.11294876661665842, -0.7784898036329784, 0.026319462646594793]

for x in range(0,7):
    start = X[x][0]
    #goal = X[x][-1]
    goal = position[x]
    my_runner = DMP_runner(filename[x],start,goal)

    tau = 1
    a=[]
    for i in np.arange(0,int(tau/dt)+1):

        '''Dynamic change in goal'''
        #if i > 0.1*int(tau/dt):     	
        #	my_runner.setGoal(position[x],1)
        '''Dynamic change in goal'''    
        
        my_runner.step(tau,dt)
        a.append(my_runner.y)
    Y.append(a)

time = np.arange(0,tau+dt,dt)
#plt.title("2-D DMP demonstration")
#plt.xlabel("Time(t)")
#plt.ylabel("Position(y)")
#plt.plot(time,X[1])
#plt.plot(time,Y[1])
#plt._show()


commands = []
for i in range(0,int((tau/dt)+1)):
    a = {'right_s0': Y[0][i], 'right_s1': Y[1][i], 'right_e0': Y[2][i], 'right_e1': Y[3][i], 'right_w0': Y[4][i], 'right_w1': Y[5][i], 'right_w2': Y[6][i]}
    commands.append(a)
#### BAXTER RUN CODE ######## 
bax.module(commands)


