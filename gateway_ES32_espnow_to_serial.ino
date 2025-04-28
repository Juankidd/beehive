
#include <esp_now.h>
#include <WiFi.h>

// Structure for receiving data
typedef struct struct_message {
  float ET;
  float RH;
  float WS;
  float Weight;
} sensor_data;

sensor_data incomingData;

// Callback when receiving data via ESP-NOW
void OnDataRecv(const uint8_t * mac, const uint8_t *incoming, int len) {
  memcpy(&incomingData, incoming, sizeof(incomingData));
  
  // Display on serial monitor (to be read by Raspberry Pi)
  Serial.print("{");
  Serial.print("\"ET\":"); Serial.print(incomingData.ET, 2); Serial.print(",");
  Serial.print("\"RH\":"); Serial.print(incomingData.RH, 2); Serial.print(",");
  Serial.print("\"HT\":"); Serial.print(0); Serial.print(","); // Placeholder if no HT
  Serial.print("\"HH\":"); Serial.print(0); Serial.print(","); // Placeholder if no HH
  Serial.print("\"WS\":"); Serial.print(incomingData.WS, 2); Serial.print(",");
  Serial.print("\"Weight\":"); Serial.print(incomingData.Weight, 2);
  Serial.println("}");
}

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  Serial.println("📡 ESP32 Gateway Start);

  if (esp_now_init() != ESP_OK) {
    Serial.println("Error Start ESP-NOW");
    return;
  }

  esp_now_register_recv_cb(OnDataRecv);
}

void loop() {
  // No additional logic required
}
