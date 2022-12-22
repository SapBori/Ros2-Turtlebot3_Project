
import numpy as np
from numpy import Infinity
import rclpy
import my_bot.comm as comm
import cv2
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import Image
#import my_bot.arrowdect as arrow
def main():
    rclpy.init(args=None)
    my_bot_pub = comm.ClientPublisher()
    my_bot_sub = comm.ClientSubscriber()
    my_range = [0,0,0,0,0,0,0,0,0,0,0,0]
    s=0
    while(1):
        rclpy.spin_once(my_bot_pub)
        rclpy.spin_once(my_bot_sub)
        my_range = my_bot_sub.get_range()
        #state = statej(my_range)
        if(my_range[0]<0.9 and my_range[0]>0.7):
            my_image = my_bot_sub.get_img()
            my_bot_pub.set_vel(-0.0 , 0.0)
            judge = statearrow(my_image)
            my_bot_pub.set_vel(-0.0 , 0.0)
            s = statej(my_range,judge)

        if(s ==1):
            my_bot_pub.set_vel(-0.05 , 0.0)
            my_bot_pub.set_vel(0.05 , -0.75)
        elif(s==2):
            my_bot_pub.set_vel(-0.05 , 0.0)
            my_bot_pub.set_vel(0.05 , +0.75) 
        elif(s==3):
            my_bot_pub.set_vel(0.0 , 0.0)
            my_bot_pub.set_vel(-0.08 , -0.0)
        elif(s==10):
            my_bot_pub.set_vel(0.0 , 0.0)
            my_bot_pub.set_vel(0.0 , 0.0)
            my_bot_pub.set_vel(0.0 , 0.0)
            my_bot_pub.set_vel(0.0 , 0.0)
            rclpy.shutdown
            break
        elif(my_range[0]<3.0):
            my_bot_pub.set_vel(0.05 , 0.0)
        #statec = statecolor(my_color)
        #print(sta  tec)
        #if(state == 3):
             #my_bot_pub.set_vel(-0.16 , 0.0)
        #else : my_bot_pub.set_vel(0.16 , 0.0) 
    my_bot_pub.set_vel(0.0 , 0.0)
rclpy.shutdown

def statej(range,j):
    c=0
    if(range[0]<0.5):
        if(c ==1):
            print('stop')
            return 10
        if j=='left':
            print(j)
            p=1
            return p
        elif j=='right':
            print(j)
            p=2
            return p
        else:
            return 100


if __name__ == '__main__':
    main()

def statecolor(color):
    if color<150 and color>135:
        print(color)
        return 1
    else : return 0

def statearrow(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,50,150,apertureSize = 3)
    cv2.imshow("canny'd image", edges)
    cv2.waitKey(1)
    lines = cv2.HoughLines(edges,1,np.pi/180,20)
    left = [0, 0]
    right = [0, 0]
    for object in lines:
        theta = object[0][1]
        rho = object[0][0]
    #cases for right/left arrows
        if ((np.round(theta, 2)) >= 1.0 and (np.round(theta, 2)) <= 1.1) or ((np.round(theta,2)) >= 2.0 and (np.round(theta,2)) <= 2.1):
            if (rho >= 20 and rho <=  30):
                left[0] += 1
            elif (rho >= 60 and rho <= 65):
                left[1] +=1
            elif (rho >= -73 and rho <= -57):
                right[0] +=1
            elif (rho >=148 and rho <= 176):
                right[1] +=1
    #cases for up/down arrows

    if left[0] >= 1 and left[1] >= 1:
        print('left')
        return 'left'
    elif right[0] >= 1 and right[1] >= 1:
        print('right')
        return 'right'        