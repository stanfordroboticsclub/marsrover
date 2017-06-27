# marsrover
Marsrover central repository

onboard_computer -- ros node that runs on the main rover computer (eventually Jetson TX2), handles communication with remote_operator
and drive_controller

remote_operator -- ros node that runs on a desktop with a GUI, allows remote robot control

drive_controller (untested) -- ros node that runs on an Arduino teensy, controls drive motors

Build and run instructions (to start onboard_computer and remote_operator on the same computer for testing):

1. Install ros kinetic in Ubuntu 14.04 and follow the ROS tutorial to set up your catkin workspace (i.e.
create a folder in your home directory called catkin_ws, and create a src folder in that)
2. Install arduino and teensyduino, and follow the setup instructions for rosserial_arduino
3. Clone the marsrover repository into ~/catkin_ws/src
4. From the ~/catkin_ws folder, run catkin_make
5. Run "source devel/setup.bash"
6. Start roscore
7. In a new terminal (after sourcing devel/setup.bash), type "rosrun remote_operator main.py" and "rosrun onboard_computer main.py" to start each node

Build instructions for teensy:

1. Follow steps for other nodes first
2. Sorce devel/setup.bash and run "rosserial_arduino make_libraries.py [path-to-arduino-libraries], where path-to-arduino-libraries
is the directory Arduino libraries are stored in (often ~/Arduino/libraries)
3. Open the drive_controller sketch in the Arduino IDE and deploy
