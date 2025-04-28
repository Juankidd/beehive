
#include <Arduino.h>

// sensor reading
float readET() { return random(200, 320) / 10.0; }
float readRH() { return random(600, 850) / 10.0; }
float readHT() { return random(310, 360) / 10.0; }
float readHH() { return random(500, 700) / 10.0; }
float readWS() { return random(0, 150) / 10.0; }

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("ESP32 Gateway iniciado");
}

void loop() {
  float ET = readET();
  float RH = readRH();
  float HT = readHT();
  float HH = readHH();
  float WS = readWS();

  String data = "{";
  data += "\"ET\":" + String(ET, 2) + ",";
  data += "\"RH\":" + String(RH, 2) + ",";
  data += "\"HT\":" + String(HT, 2) + ",";
  data += "\"HH\":" + String(HH, 2) + ",";
  data += "\"WS\":" + String(WS, 2);
  data += "}";

  Serial.println(data);

  delay(5000);
}
