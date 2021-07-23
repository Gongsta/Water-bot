/*
  Stepper Motor Demonstration 3
  Stepper-Demo3.ino
  Demonstrates NEMA 17 Bipolar Stepper with L298N Driver
  Uses Potentiometer on Analog Input A0
  Uses Arduino Stepper Library
 
*/
 
// Include the Arduino Stepper Library
#include <Stepper.h>
 
// Define Constants
 
// Number of steps per output rotation
const int STEPS_PER_REV = 200;
int motorSpeed = 100; //Value between 0 - 100
//const int SPEED_CONTROL = A0;
 
// Create Instance of Stepper Class
// Specify Pins used for motor coils
// The pins used are 8,9,10,11 
// Connected to L298N Motor Driver In1, In2, In3, In4 
// Pins entered in sequence 1-2-3-4 for proper step sequencing
 
Stepper stepper_NEMA17(STEPS_PER_REV, 8, 9, 10, 11);


void setup() {
  stepper_NEMA17.setSpeed(motorSpeed);
  Serial.begin(9600);
}

void setStepperIdle() {
  digitalWrite(8, LOW);
  digitalWrite(9, LOW);
  digitalWrite(10, LOW);
  digitalWrite(11, LOW);
}


void loop() {

  stepper_NEMA17.step(STEPS_PER_REV);
  Serial.println("clockwise");
  setStepperIdle();
  delay(500);
  //To add if you want the user to control the motor speed
//  // read the sensor value:
//  int sensorReading = analogRead(SPEED_CONTROL);
//  // map it to a range from 0 to 100:
//  int motorSpeed = map(sensorReading, 0, 1023, 0, 100);
//  if (motorSpeed > 0) {
//    stepper_NEMA17.setSpeed(motorSpeed);
//    // step 1/100 of a revolution:
//    stepper_NEMA17.step(STEPS_PER_REV / 100);
//  }
}
