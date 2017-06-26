import rospy
from onboard_computer import msg
import std_msgs

class ROSDriver:
    def __init__(self, ros_lock):
        self.ros_lock = ros_lock
        self.teleop_command_publisher = rospy.Publisher('teleop_command_channel', msg.TeleopCommand, queue_size=10)
        self.state_command_publisher = rospy.Publisher('state_command_channel', msg.StateCommand, queue_size=10)
        self.rate = rospy.Rate(10) # 10hz
        #self.teleop_command = msg.TeleopCommand()
        #self.teleop_command.joysticks.append(msg.JoystickMessage())
        self.state = msg.StateCommand.DISABLED

    def send_teleop_command(self, message):
        with self.ros_lock:
            message.header = std_msgs.msg.Header()
            message.header.stamp = rospy.Time.now()
            self.teleop_command_publisher.publish(message)

    def set_state(self, state):
        with self.ros_lock:
            self.state = state

    def loop(self):
        while True:
            with self.ros_lock:
                if rospy.is_shutdown():
                    break
                state_command = msg.StateCommand()
                state_command.header = std_msgs.msg.Header()
                state_command.header.stamp = rospy.Time.now()
                state_command.state = self.state
                self.state_command_publisher.publish(state_command)
            self.rate.sleep()
