#include <Arduino.h>
#include <ctime>
#include<cmath>
#include <Wire.h>            // serial communication on the I2C bus
#include <SparkFun_TMP117.h> // Used to send and recieve specific information from our sensor
TMP117 sensor; // Initalize sensor

const float n_steps = 2047; // pour 11 bits 2^11 - 1 

void setup() {
  Wire.begin();
  Serial.begin(115200);
  Wire.setClock(400000);   // frequence ( pour la lecture )
  if (!sensor.begin()) {
  Serial.println("Erreur: TMP117 introuvable !");
  while (1); // stoppe le programme si le capteur n'est pas détecté
}
  
}

void loop() {
  float resistance0=100.5;
  float start_voltage = 5;
  float beta=3096;
  
  //impossible de lire 11 bits en fixant à 11 analogReadResolution(11) ça n'affiche que des 0 donc on lit
  // les 12 premiers et on fait un bit shift pour 11 bit
  analogReadResolution(12);


  int sensorValue12 = analogRead(A0);
  int sensorValue11 = sensorValue12 >> 1; // un bit shift à droite de 1 est equivalent à une division par 2
  //(et inversement pour le bitshift gauche c'est une multiplication par deux)
  //pour notre cas on passe de 0–4095 à 0–2047 (11 bits) valeurs possibles
  float realVoltage = (sensorValue11/n_steps)*start_voltage; // on convertit en tension

  Serial.print("Voltage: ");
  Serial.println(realVoltage, 5);


  float tempC = sensor.readTempC();
  Serial.print("Temperature du thermometre a 15 balles: ");
  // print temperature in °C 
  Serial.println(tempC);
  float temperature0=298.15;
  
  float Rth = (resistance0*realVoltage)/(start_voltage-realVoltage);
  float temp = (1/    ( (log(Rth)-log(resistance0) )/beta + (1/temperature0) ))-273.15;
  Serial.print("Temperature :");
  
  Serial.println(temp,3); //  on affiche la temp du thermo rouge avec 3 décimaux
  
  unsigned long temps = millis();

  
  // Print temperature in °C 
  
  Serial.print("temps: ");
  Serial.print(temps);
  Serial.print(",");
  Serial.print("realVoltage: ");
  Serial.println(realVoltage, 5);
  Serial.print("Rth: ");
  Serial.println(Rth, 5);

  delay(500);

  
  
  

  
 
  
}
