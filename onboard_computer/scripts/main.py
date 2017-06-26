#!/usr/bin/env python

import rospy


import time

import ros_onboard



def main():
    rospy.init_node('onboard_computer', anonymous=False)
    ro = ros_onboard.ROSOnboard()
    ro.loop()
    

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass