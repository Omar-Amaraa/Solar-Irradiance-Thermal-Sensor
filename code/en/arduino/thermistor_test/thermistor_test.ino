// First test: read the thermistor through a simple voltage divider and compare
// the temperature computed with the Beta model to the TMP117 reference probe.
#include <Arduino.h>
#include <ctime>
#include <cmath>
#include <Wire.h>            // Used to establish serial communication on the I2C bus
#include <SparkFun_TMP117.h> // Used to send and receive specific information from our sensor
TMP117 sensor; // Initialize sensor

const float n_steps = 2047; // for 11 bits: 2^11 - 1

void setup() {
  Wire.begin();
  Serial.begin(115200);
  Wire.setClock(400000);   // Set clock speed to be the fastest for better communication (fast mode)
  if (!sensor.begin()) {
    Serial.println("Error: TMP117 not found!");
    while (1); // stop the program if the sensor is not detected
  }
}

void loop() {
  float resistance0 = 100.5;
  float supply_voltage = 5;
  float beta = 3096;

  // Setting analogReadResolution(11) only returns zeros, so we read
  // 12 bits and bit-shift down to 11 bits
  analogReadResolution(12);

  int sensorValue12 = analogRead(A0);
  int sensorValue11 = sensorValue12 >> 1; // a right shift by 1 is the same as dividing by 2
  // (and a left shift is a multiplication by 2)
  // here we go from 0–4095 to 0–2047 (11 bits) possible values
  float realVoltage = (sensorValue11 / n_steps) * supply_voltage; // convert to a voltage

  Serial.print("Voltage: ");
  Serial.println(realVoltage, 5);

  float tempC = sensor.readTempC();
  Serial.print("TMP117 reference temperature: ");
  // Print temperature in °C
  Serial.println(tempC);
  float temperature0 = 298.15;

  // Thermistor resistance from the divider, then temperature from the Beta model
  float Rth = (resistance0 * realVoltage) / (supply_voltage - realVoltage);
  float temp = (1 / ((log(Rth) - log(resistance0)) / beta + (1 / temperature0))) - 273.15;
  Serial.print("Temperature: ");
  Serial.println(temp, 3); // Print temperature with 3 decimal places

  unsigned long time_ms = millis();

  Serial.print("time: ");
  Serial.print(time_ms);
  Serial.print(",");
  Serial.print("realVoltage: ");
  Serial.println(realVoltage, 5);
  Serial.print("Rth: ");
  Serial.println(Rth, 5);

  delay(500);
}
