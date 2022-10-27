// https://randomnerdtutorials.com/esp32-stepper-motor-28byj-48-uln2003/
#include <Stepper.h>
#include <ESP32Servo.h>

const int stepsPerRevolution = 2048;

// ULN2003 Motor Driver Pins
#define IN1 19
#define IN2 18
#define IN3 5
#define IN4 17
#define SERVO_PIN 26 

Stepper myStepper(stepsPerRevolution, IN1, IN3, IN2, IN4);
Servo servoMotor;
int pos = 0;

void setup() {
  myStepper.setSpeed(5);
  servoMotor.attach(SERVO_PIN);
  Serial.begin(115200);
}

void loop() {
  // step one revolution in one direction:
  Serial.println("clockwise");
  myStepper.step(stepsPerRevolution);

  if (pos == 180) {
    pos = 0;
  } else {
    pos += 10;
  }
  
  delay(250);
  Serial.printf("%d\n", pos);
  servoMotor.write(pos);
}