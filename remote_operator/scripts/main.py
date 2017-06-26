#!/usr/bin/env python

import rospy


import time, threading

import ros_driver
import gui



def main():
    rospy.init_node('remote_operator', anonymous=False)
    ros_lock = threading.Lock()
    rd = ros_driver.ROSDriver(ros_lock)
    ros_thread = threading.Thread(target=rd.loop)
    ros_thread.start()
    ui = gui.GUI(rd, ros_lock)
    

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass