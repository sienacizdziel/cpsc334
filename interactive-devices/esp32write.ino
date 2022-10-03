// initializations
int joystickXPin = 35;
int joystickYPin = 33; 

void setup()
{
    pinMode(joystickXPin, INPUT);
    pinMode(joystickYPin, INPUT);
    Serial.begin(115200);
}

void loop()
{
  // read data
  int joystickX, joystickY, spstSwitch, button;
  joystickX = analogRead(joystickXPin); 
  joystickY = analogRead(joystickYPin); 
  joystickX = map(joystickX, 0, 1023, -512, 512);
  joystickY = map(joystickY, 0, 1023, 512, -512);

  // serial print data
  Serial.print("x: ");
  Serial.print(joystickX);
  Serial.print(", y: ");
  Serial.println(joystickY);
}
