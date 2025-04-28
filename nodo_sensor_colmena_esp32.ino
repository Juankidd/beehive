
#include <esp_now.h>
#include <WiFi.h>
#include <DHT.h>
#include "HX711.h"

#define DHTPIN 4
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

// HX711 configuration (load cell)
#define LOADCELL_DOUT_PIN  5
#define LOADCELL_SCK_PIN   18
HX711 balanza;

// MAC address of the gateway (ESP32 receiver)
uint8_t gatewayAddress[] = {0x24, 0x6F, 0x28, 0xAB, 0xCD, 0xEF}; // Change to the MAC you have

typedef struct struct_message {
  float ET;   // Ambient temp
  float RH;   // Ambient humidity
  float WS;   // Wind speed 
  float Weight; // Hive weight (kg)
} sensor_data;

sensor_data datos;

// Confirmation of shipment
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial.print(" Envío: ");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? " Successful" : " Failed");
}

void setup() {
  Serial.begin(115200);
  dht.begin();
  balanza.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  balanza.set_scale(2280.f);  // Calibrate according to your cell
  balanza.tare();

  WiFi.mode(WIFI_STA);
  Serial.println(WiFi.macAddress());

  if (esp_now_init() != ESP_OK) {
    Serial.println(" Error initializing ESP-NOW");
    return;
  }

  esp_now_register_send_cb(OnDataSent);

  esp_now_peer_info_t peerInfo = {};
  memcpy(peerInfo.peer_addr, gatewayAddress, 6);
  peerInfo.channel = 0;
  peerInfo.encrypt = false;

  if (esp_now_add_peer(&peerInfo) != ESP_OK) {
    Serial.println("  Error adding peer");
    return;
  }

  Serial.println(" Sensor node started");
}

void loop() {
  datos.ET = dht.readTemperature();
  datos.RH = dht.readHumidity();
  datos.Weight = balanza.get_units(5);
  datos.WS = random(0, 150) / 10.0;  

  if (isnan(datos.ET) || isnan(datos.RH)) {
    Serial.println(" DHT sensor failure");
    return;
  }

  esp_err_t result = esp_now_send(gatewayAddress, (uint8_t *) &datos, sizeof(datos));
  if (result == ESP_OK) {
    Serial.println(" Data sent correctly");
  } else {
    Serial.println(" Error sending data");
  }

  delay(5000);  // Send every 5 seconds
}
