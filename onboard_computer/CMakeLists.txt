cmake_minimum_required(VERSION 2.8.3)
project(onboard_computer)

add_definitions(-std=c++11)


find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
)


add_message_files(
  FILES
  TeleopCommand.msg
  StateCommand.msg
  OnboardStatus.msg
  JoystickMessage.msg
  Heartbeat.msg
  DriveControllerCommand.msg
  DriveControllerStatus.msg
)


generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(
   CATKIN_DEPENDS message_runtime
)


include_directories(
  ${catkin_INCLUDE_DIRS}
)
