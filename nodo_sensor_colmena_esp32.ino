
#include <esp_now.h>
#include <WiFi.h>
#include <DHT.h>
#include "HX711.h"

#define DHTPIN 4
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

// HX711 configuración (celda de carga)
#define LOADCELL_DOUT_PIN  5
#define LOADCELL_SCK_PIN   18
HX711 balanza;

// Dirección MAC del gateway (ESP32 receptor)
uint8_t gatewayAddress[] = {0x24, 0x6F, 0x28, 0xAB, 0xCD, 0xEF}; // REEMPLAZAR con la MAC real

typedef struct struct_message {
  float ET;   // Temp ambiente
  float RH;   // Humedad ambiente
  float WS;   // Velocidad viento (opcional)
  float Weight; // Peso colmena (kg)
} sensor_data;

sensor_data datos;

// Confirmación de envío
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial.print(" Envío: ");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? " Exitoso" : " Fallido");
}

void setup() {
  Serial.begin(115200);
  dht.begin();
  balanza.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  balanza.set_scale(2280.f);  // Calibrar según tu celda
  balanza.tare();

  WiFi.mode(WIFI_STA);
  Serial.println(WiFi.macAddress());

  if (esp_now_init() != ESP_OK) {
    Serial.println(" Error inicializando ESP-NOW");
    return;
  }

  esp_now_register_send_cb(OnDataSent);

  esp_now_peer_info_t peerInfo = {};
  memcpy(peerInfo.peer_addr, gatewayAddress, 6);
  peerInfo.channel = 0;
  peerInfo.encrypt = false;

  if (esp_now_add_peer(&peerInfo) != ESP_OK) {
    Serial.println(" Error añadiendo peer");
    return;
  }

  Serial.println(" Nodo sensor iniciado");
}

void loop() {
  datos.ET = dht.readTemperature();
  datos.RH = dht.readHumidity();
  datos.Weight = balanza.get_units(5);
  datos.WS = random(0, 150) / 10.0;  // Simulación viento

  if (isnan(datos.ET) || isnan(datos.RH)) {
    Serial.println(" Fallo en sensor DHT");
    return;
  }

  esp_err_t result = esp_now_send(gatewayAddress, (uint8_t *) &datos, sizeof(datos));
  if (result == ESP_OK) {
    Serial.println(" Datos enviados correctamente");
  } else {
    Serial.println(" Error al enviar datos");
  }

  delay(5000);  // Enviar cada 5 segundos
}
