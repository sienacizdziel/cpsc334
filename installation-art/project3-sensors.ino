#include <WebServer.h>
#include <WiFi.h>
#include <WiFiUdp.h>

const int touchPin1 = 15;
const int lightPin1 = 34;
const int touchPin2 = 2;
const int lightPin2 = 35; 
const int touchPin3 = 4;
const char* ssid = "yale wireless";
WiFiUDP Udp;
unsigned int localUdpPort = 4210;
char incomingPacket[255];
const char * udpAddress = "172.29.135.237";

void setup() {
  Serial.begin(115200);
  pinMode(touchPin1, INPUT);
  pinMode(lightPin1, INPUT);
  pinMode(touchPin2, INPUT);
  pinMode(lightPin2, INPUT);
  pinMode(touchPin3, INPUT);

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

void loop() {
  int result1 = analogRead(lightPin1);
  long val1 = touchRead(touchPin1);
  int result2 = analogRead(lightPin2);
  long val2 = touchRead(touchPin2);
  long val3 = touchRead(touchPin3);
  Serial.printf("%d,%d,%d,%d,%d\n", val1, val2, val3, result1, result2);
  Udp.beginPacket(udpAddress, localUdpPort);
  Udp.printf("%d,%d,%d,%d,%d\n", val1, val2, val3, result1, result2);
  Udp.endPacket();
  delay(100);
}
