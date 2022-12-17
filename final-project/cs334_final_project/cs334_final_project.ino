#include <ESP32Servo.h>
#include <WebServer.h>
#include <WiFi.h>
#include <WiFiUdp.h>

#define LIGHT_PIN1 32
#define LIGHT_PIN2 33
#define SERVO_PIN1 22
#define SERVO_PIN2 23
#define BUTTON_PIN1_LEFT 16
#define BUTTON_PIN1_RIGHT 21
#define BUTTON_PIN2_LEFT 26
#define BUTTON_PIN2_RIGHT 25
#define STEPPER_IN1 19
#define STEPPER_IN2 18
#define STEPPER_IN3 5
#define STEPPER_IN4 17
#define SERVO_PIN3 18

const int delay_time = 100;
int started = 0;
int p1_score = 0;
int prev_photo_p1 = 0;
int p2_score = 0;
int prev_photo_p2 = 0;
int threshold = 600;
int pause_score = 0;
int p2_pos = 0;
int p1_pos = 0;
int shaker_pos = 0;
int shaker_move = 180;

Servo player1_servo;
Servo player2_servo;
Servo shaker_servo;

TaskHandle_t player1_task;
TaskHandle_t player2_task;

const char* ssid = "yale wireless";
WiFiUDP Udp;
unsigned int localUdpPort = 4210;
char incomingPacket[255];
const char * udpAddress = "172.29.33.169";
char packetBuffer[255];

void setup() {
  Serial.begin(115200);
  pinMode(LIGHT_PIN1, INPUT);
  pinMode(LIGHT_PIN2, INPUT);
  pinMode(BUTTON_PIN1_LEFT, INPUT_PULLUP);
  pinMode(BUTTON_PIN1_RIGHT, INPUT_PULLUP);
  pinMode(BUTTON_PIN2_LEFT, INPUT_PULLUP);
  pinMode(BUTTON_PIN2_RIGHT, INPUT_PULLUP);
  player1_servo.attach(SERVO_PIN1);
  player2_servo.attach(SERVO_PIN2);
  shaker_servo.attach(SERVO_PIN3);

  // multithreading for different players
  xTaskCreatePinnedToCore(
      player1, /* Function to implement the task */
      "player 1", /* Name of the task */
      10000,  /* Stack size in words */
      NULL,  /* Task input parameter */
      tskIDLE_PRIORITY,  /* Priority of the task */
      &player1_task,  /* Task handle. */
      0); /* Core where the task should run */

  // // multithreading for task 1 (rotating servo)
  xTaskCreatePinnedToCore(
      player2, /* Function to implement the task */
      "player 2", /* Name of the task */
      10000,  /* Stack size in words */
      NULL,  /* Task input parameter */
      1,  /* Priority of the task */
      &player2_task,  /* Task handle. */
      1); /* Core where the task should run */

  player1_servo.write(0);
  player2_servo.write(0);
  shaker_servo.write(0);
  p1_pos = 0;
  p2_pos = 0;
  shaker_pos = 0;
  prev_photo_p1 = analogRead(LIGHT_PIN1); 
  prev_photo_p2 = analogRead(LIGHT_PIN2); 

  int status = WL_IDLE_STATUS;  
  WiFi.begin(ssid);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("Connected to wifi");
  Serial.println(WiFi.localIP());
  Udp.begin(WiFi.localIP(), localUdpPort);
  Serial.printf("Now listening at IP %s, UDP port %d\n", WiFi.localIP().toString().c_str(), localUdpPort);
}

void loop() {}

void player1(void *parameter) {  
  while (true) {
    // if (started == 0) {
    //   Udp.read(packetBuffer, 255);
    //   Serial.println(packetBuffer);
    //   delay(500);
    //   continue;
    // }

    int button_left = digitalRead(BUTTON_PIN1_LEFT); 
    int button_right = digitalRead(BUTTON_PIN1_RIGHT);

      int goal = analogRead(LIGHT_PIN1); 
      if (goal < prev_photo_p1 - threshold && goal < 50 && button_left != LOW) {
        if (pause_score == 0) {
          p1_score += 1;
          Serial.printf("new score p1! %d -> %d\n", prev_photo_p1, goal);
        }
        pause_score = 1;
      }
      prev_photo_p1 = goal;

    if (button_left == LOW) {
      shaker_pos = shaker_move;
      shaker_servo.write(shaker_move);
      delay(200);
      shaker_pos = 0;
      shaker_servo.write(0);
      delay(delay_time);
      pause_score = 0; 
      Serial.println("player 1 button left"); 
    } else if (button_right == LOW) {
      if (p1_pos == 0) {
        p1_pos = 150;
        player1_servo.write(150);
      } else {
        p1_pos = 0;
        player1_servo.write(0);
      }
      delay(delay_time);
      Serial.println("player 1 button right");     
      pause_score = 0; 
    }
    
    // player1_servo.write(90);
    delay(delay_time);

    Serial.printf("%d, %d\n", p1_score, p2_score);
    Udp.beginPacket(udpAddress, localUdpPort);
    Udp.printf("%d, %d\n", p1_score, p2_score);
    Udp.endPacket();
  }
}

void player2(void *parameter) {
  while (true) {
    // if (started == 0) {
    //   Udp.read(packetBuffer, 255);
    //   Serial.println(packetBuffer);  
    //   delay(500);
    //   continue;    
    // }

    int goal = analogRead(LIGHT_PIN2); 
    if (goal < prev_photo_p2 - threshold) {
      if (pause_score == 0) {
        p2_score += 1;      
        Serial.printf("new score p2! %d -> %d\n", prev_photo_p2, goal);
      }
      pause_score = 1;
    }
    prev_photo_p2 = goal;
    
    // Serial.printf("player2 photoresistor: %d\n", goal);
    int button_left = digitalRead(BUTTON_PIN2_LEFT); 
    int button_right = digitalRead(BUTTON_PIN2_RIGHT);

    if (button_left == LOW) {
      shaker_pos = shaker_move;
      shaker_servo.write(shaker_move);
      delay(200);
      shaker_pos = 0;
      shaker_servo.write(0);
      delay(delay_time);
      pause_score = 0; 
      Serial.println("player 2 button left");      
    } else if (button_right == LOW) {
      if (p2_pos == 0) {
        p2_pos = 150;
        player2_servo.write(150);
      } else {
        p2_pos = 0;
        player2_servo.write(0);
      }
      delay(delay_time);
      Serial.println("player 2 button right");     
      pause_score = 0;  
    }
    
    // player2_servo.write(90);
    delay(delay_time);
  }
}
