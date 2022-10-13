#include <WebServer.h>
#include <WiFi.h>
#include <WiFiUdp.h>

const int sensorPin = 32;
const char* ssid = "yale wireless";
WiFiUDP Udp;
unsigned int localUdpPort = 4210;
char incomingPacket[255];
const char * udpAddress = "172.29.33.215";

void setup() {
  Serial.begin(115200);
  pinMode(sensorPin, INPUT);

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

  // bool readPacket = false;
  // while (!readPacket) {
  //   int packetSize = Udp.parsePacket();
  //   if (packetSize)
  //    {
  //     Serial.printf("Received %d bytes from %s, port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
  //     int len = Udp.read(incomingPacket, 255);
  //     if (len > 0)
  //     {
  //       incomingPacket[len] = 0;
  //     }
  //     Serial.printf("UDP packet contents: %s\n", incomingPacket);
  //     readPacket = true;
  //   } 
  //   // Serial.printf("still searching...\n");
  // }
}

void loop() {
  int result = analogRead(sensorPin);
  Udp.beginPacket(udpAddress, localUdpPort);
  Udp.printf("%d", result);
  Udp.endPacket();
}
