
#include "DHT.h"
#include <SPI.h>
#include <LoRa.h>

#define NSS 5
#define RST 27
#define DIO0 2


#define DHTPIN 4     // Digital pin connected to the DHT sensor


#define DHTTYPE DHT11   // DHT 11


DHT dht(DHTPIN, DHTTYPE);

int counter = 0;

void setup() {

  Serial.begin(9600);
  while (!Serial);

  LoRa.setPins(NSS, RST, DIO0);

  Serial.println(F("Iniciado"));

  dht.begin();

  
  delay(1000);

  if (!LoRa.begin(433E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
  delay(1000);
  
}

void loop() {
  
  delay(2000);

  float h = dht.readHumidity();
  float t = dht.readTemperature();

  // Checa se houve erros
  if (isnan(h) || isnan(t)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }



  Serial.print(F("Temperature: "));
  Serial.print(t);
  Serial.println(F("°C"));
  Serial.print(F("Humidity: "));
  Serial.print(h);
  Serial.println(F("% "));


  Serial.print("Sending packet: ");
  Serial.println(counter);

  // send packet
  LoRa.beginPacket();
  LoRa.print(t);
  LoRa.print(",");
  LoRa.print(h);
  LoRa.endPacket();
  
    counter++;

  delay(5000);
}
// aproximadamente 2 segundos por leitura, com 7 segundos de intervalo entre envios. 