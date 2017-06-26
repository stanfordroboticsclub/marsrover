import rospy
from onboard_computer import msg
import std_msgs
import threading

STATE_TIMEOUT = 1 #seconds

class ROSOnboard:
    def __init__(self):
        self.state = msg.StateCommand.DISABLED
        self.last_state_update_time = rospy.Time.now().secs
        self.ros_lock = threading.Lock()
        rospy.Subscriber("teleop_command_channel", msg.TeleopCommand, self.teleop_command_callback)
        rospy.Subscriber("state_command_channel", msg.StateCommand, self.state_command_callback)
        self.state_command_broadcast_publisher = rospy.Publisher('state_command_broadcast_channel', msg.StateCommand, queue_size=10)
        self.drive_controller_command_publisher = rospy.Publisher('drive_controller_command_channel', msg.DriveControllerCommand, queue_size=10)
        self.rate = rospy.Rate(10)

    def loop(self):
        while not rospy.is_shutdown():
            self.disable_if_needed()
            rospy.loginfo(rospy.get_caller_id() + " State: " + str(self.state))
            with self.ros_lock:
                state_command_broadcast = msg.StateCommand()
                state_command_broadcast.header = std_msgs.msg.Header()
                state_command_broadcast.header.stamp = rospy.Time.now()
                state_command_broadcast.state = self.state
                self.state_command_broadcast_publisher.publish(state_command_broadcast)
            self.rate.sleep()

    def disable_if_needed(self):
        with self.ros_lock:
            if self.state == msg.StateCommand.PERSISTENT_ENABLE_AUTO or self.state == msg.StateCommand.PERSISTENT_ENABLE_TELEOP:
                return
            if rospy.Time.now().secs - self.last_state_update_time > STATE_TIMEOUT:
                self.state = msg.StateCommand.DISABLED

    def teleop_command_callback(self, message):
        rospy.loginfo(rospy.get_caller_id() + " X axis: " + str(message.joysticks[0].l_x_axis))
        drive_controller_command = msg.DriveControllerCommand()
        drive_controller_command.header = std_msgs.msg.Header()
        drive_controller_command.header.stamp = rospy.Time.now()
        drive_controller_command.motor1_pwm = 1234
        self.drive_controller_command_publisher.publish(drive_controller_command)

    def state_command_callback(self, message):
        with self.ros_lock:
            self.state = message.state
            self.last_state_update_time = message.header.stamp.secs
        #rospy.loginfo(rospy.get_caller_id() + " State: " + str(message.state))
