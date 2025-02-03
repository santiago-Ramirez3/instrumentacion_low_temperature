#include <Adafruit_MAX31865.h>

Adafruit_MAX31865 thermo1 = Adafruit_MAX31865(8, 14, 16, 15); // Configura los pines CS, DI, DO y CLK del primer sensor.
Adafruit_MAX31865 thermo2 = Adafruit_MAX31865(9, 14, 16, 15); // Configura los pines CS, DI, DO y CLK del segundo sensor.

#define RREF      430.0
#define RNOMINAL  100.0

void setup() {
  Serial.begin(115200);
  Serial.println("Adafruit MAX31865 PT100 Sensor Test!");
  thermo1.begin(MAX31865_4WIRE);
  thermo2.begin(MAX31865_4WIRE);
}

void loop() {
  if (Serial.available() > 0) {
    char request = Serial.read();
    if (request == 'T') {
      float temperature1 = thermo1.temperature(RNOMINAL, RREF);
      float temperature2 = thermo2.temperature(RNOMINAL, RREF);
      
      //Serial.print("U");
      Serial.print(temperature1);
      Serial.print(";");
      Serial.println(temperature2);
    }
  }
  delay(5);
}
