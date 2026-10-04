// Calibration sketch: every second, send one CSV line
//   Ug,Ul,Uref,Temperature_TMP,Time
// Ug  = amplified Wheatstone bridge output (A0)
// Ul  = second bridge branch voltage (A1)
// Uref = bridge reference voltage (A2)
// Temperature_TMP = reference temperature from the TMP117 probe (°C)
// Time = seconds since start
#include <Arduino.h>
#include <ctime>
#include <cmath>
#include <Wire.h>            // serial communication on the I2C bus
#include <SparkFun_TMP117.h> // Used to send and receive specific information from our sensor
TMP117 sensor; // Initialize sensor

const float n_steps = 2047; // for 11 bits: 2^11 - 1

void setup() {
  Wire.begin();
  Serial.begin(115200);
  Wire.setClock(400000);   // I2C clock frequency (for reading)
  if (!sensor.begin()) {
    Serial.println("Error: TMP117 not found!");
    while (1); // stop the program if the sensor is not detected
  }
}

void loop() {
  float sensor_voltage = 4.82;

  // Setting analogReadResolution(11) only returns zeros, so we read
  // 12 bits and bit-shift down to 11 bits
  analogReadResolution(12);

  int Ug12 = analogRead(A0);
  int Ug11 = Ug12 >> 1;
  float Ug = (Ug11 / n_steps) * sensor_voltage; // convert to a voltage

  int Ul12 = analogRead(A1);
  int Ul11 = Ul12 >> 1;
  float Ul = (Ul11 / n_steps) * sensor_voltage; // convert to a voltage

  int Uref12 = analogRead(A2);
  int Uref11 = Uref12 >> 1; // fixed: the original read Uref11 before initializing it (Uref = 0 in the CSVs)
  float Uref = (Uref11 / n_steps) * sensor_voltage;

  float tempC = sensor.readTempC();

  unsigned long time_s = millis() / 1000;

  Serial.print(Ug, 5);
  Serial.print(",");
  Serial.print(Ul, 5);
  Serial.print(",");
  Serial.print(Uref, 5);
  Serial.print(",");
  Serial.print(tempC); // temperature in °C
  Serial.print(",");
  Serial.print(time_s);
  Serial.println();

  delay(1000);
}
