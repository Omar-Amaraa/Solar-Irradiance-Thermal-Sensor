// Voltage reading for the heating-wire experiment (heat capacity CT).
// Every 0.5 s, send one CSV line:
//   Time,Uref,Ug,Uth,U_heating_wire
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
}

void loop() {
  analogReadResolution(12);

  float supply_voltage = 4.7;

  // Read the signal on 12 bits
  int A0_12 = analogRead(A0);
  // 12-bit -> 11-bit conversion
  int A0_11 = A0_12 >> 1; // divide by 2

  int A1_12 = analogRead(A1);
  int A1_11 = A1_12 >> 1;

  int A2_12 = analogRead(A2);
  int A2_11 = A2_12 >> 1;

  int A3_12 = analogRead(A3);
  int A3_11 = A3_12 >> 1;

  // Convert to real voltages
  float Ug = (A0_11 / n_steps) * supply_voltage;
  float Uth = (A1_11 / n_steps) * supply_voltage;
  float Uref = (A2_11 / n_steps) * supply_voltage;
  float U_heating_wire = (A3_11 / n_steps) * supply_voltage;
  // Time in seconds
  float time_s = millis() / 1000.0;

  // Print on the serial monitor
  Serial.print(time_s, 2); // 2 decimal places
  Serial.print(",");
  Serial.print(Uref, 5);   // 5 decimal places
  Serial.print(",");
  Serial.print(Ug, 5);
  Serial.print(",");
  Serial.print(Uth, 4);
  Serial.print(",");
  Serial.print(U_heating_wire, 3);
  Serial.println();

  delay(500);
}
