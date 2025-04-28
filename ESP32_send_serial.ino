
#include <Arduino.h>  // Include necessary library

// sensor reading
float readET() { return random(200, 320) / 10.0; }  // temperature reading
float readRH() { return random(600, 850) / 10.0; }  // humidity reading
float readHT() { return random(310, 360) / 10.0; }  // temperature reading
float readHH() { return random(500, 700) / 10.0; }  // humidity reading
float readWS() { return random(0, 150) / 10.0; }  // wind speed reading

void setup() {  // Setup function runs once at startup
  Serial.begin(115200);  // Initialize serial communication
  delay(1000);  // Pause execution for a specified time
  Serial.println("ESP32 Gateway iniciado");  // Send data to serial monitor without newline
}  // Code execution

void loop() {  // Loop function runs repeatedly after setup
  float ET = readET();  // Code execution
  float RH = readRH();  // Code execution
  float HT = readHT();  // Code execution
  float HH = readHH();  // Code execution
  float WS = readWS();  // Code execution

  String data = "{";  // Code execution
  data += "\"ET\":" + String(ET, 2) + ",";  // Code execution
  data += "\"RH\":" + String(RH, 2) + ",";  // Code execution
  data += "\"HT\":" + String(HT, 2) + ",";  // Code execution
  data += "\"HH\":" + String(HH, 2) + ",";  // Code execution
  data += "\"WS\":" + String(WS, 2);  // Code execution
  data += "}";  // Code execution

  Serial.println(data);  // Send data to serial monitor without newline

  delay(5000);  // Pause execution for a specified time
}  // Code execution
