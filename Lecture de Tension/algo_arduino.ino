#include <Arduino.h>
#include <ctime>
const float n_steps = 2047; // pour 11 bits 2^11 - 1 
void setup() {
  Serial.begin(9600);
  
}

void loop() {
  float start_voltage = 5;
  //impossible de lire 11 bits en fixant à 11 analogReadResolution(11) ça n'affiche que des 0 donc on lit
  // les 12 premiers et on fait un bit shift pour 11 bit
  analogReadResolution(12);


  int sensorValue12 = analogRead(A0);
  int sensorValue11 = sensorValue12 >> 1; // un bit shift à droite de 1 est equivalent à une division par 2
  //(et inversement pour le bitshift gauche c'est une multiplication par deux)
  //pour notre cas on passe de 0–4095 à 0–2047 (11 bits) valeurs possibles


  float realVoltage = (sensorValue11/n_steps)*start_voltage; // on convertit en tension
  
  unsigned long temps = millis();
  Serial.print("temps: ");
  Serial.print(temps);
  Serial.print(",");

  Serial.print("Voltage: ");
  Serial.println(realVoltage, 5); // Print voltage with 3 decimal places



  delay(200); //pour eviter d'etre submerger avec les valeurs mdr

}
