/* 
 * rosserial Subscriber Example
 * Blinks an LED on callback
 */

#include <ros.h>
#include <onboard_computer/StateCommand.h>
#include <onboard_computer/DriveControllerCommand.h>
#include <onboard_computer/DriveControllerStatus.h>
#include <Servo.h>

#define STATE_TIMEOUT 1

ros::NodeHandle  nh;
uint16_t global_state = onboard_computer::StateCommand::DISABLED;
uint32_t last_state_update_time = 0;
Servo motor1, motor2, motor3, motor4;

void stateCommandHandler( const onboard_computer::StateCommand& state_msg){
  last_state_update_time = state_msg.header.stamp.sec;
  global_state = state_msg.state;
}

void driveControllerCommandHandler(const onboard_computer::DriveControllerCommand& drive_command){
  if(global_state == onboard_computer::StateCommand::DISABLED) return;

  motor1.write(drive_command.motor1_pwm);
  motor2.write(drive_command.motor2_pwm);
  motor3.write(drive_command.motor3_pwm);
  motor4.write(drive_command.motor4_pwm);
}

ros::Subscriber<onboard_computer::StateCommand> state_command_subscriber("state_command_broadcast_channel", &stateCommandHandler);
ros::Subscriber<onboard_computer::DriveControllerCommand> drive_controller_command_subscriber("drive_controller_command_channel", &driveControllerCommandHandler);

onboard_computer::DriveControllerStatus status_msg;
ros::Publisher drive_controller_status_publisher("drive_controller_status_channel", &status_msg);



void setup()
{ 
  motor1.attach(12);
  motor2.attach(13);
  motor3.attach(14);
  motor4.attach(15);

  nh.initNode();
  last_state_update_time = nh.now().sec;
  nh.subscribe(state_command_subscriber);
  nh.subscribe(drive_controller_command_subscriber);
  nh.advertise(drive_controller_status_publisher);
}

void disableIfNecessary(){
  if(millis() - last_state_update_time > STATE_TIMEOUT){
    global_state = onboard_computer::StateCommand::DISABLED;
  }
}

void sendStatusInfo(){
  
}

void loop()
{ 
  disableIfNecessary();
  sendStatusInfo();
  nh.spinOnce();
  delay(1);
}

