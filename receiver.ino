#include <SPI.h>
#include <LoRa.h>

#define NSS 5
#define RST 27
#define DIO0 2


void setup() {
  Serial.begin(9600);
  while (!Serial);

  LoRa.setPins(NSS, RST, DIO0);

  if (!LoRa.begin(433E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
}

void loop() {
  // try to parse packet
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    // received a packet

    // read packet
    while (LoRa.available()) {
      Serial.print((char)LoRa.read());
    }
  } 
  delay(1000);

}
