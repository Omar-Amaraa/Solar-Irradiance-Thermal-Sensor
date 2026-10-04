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
  float sensor_voltage = 4.82;
  
  //impossible de lire 11 bits en fixant à 11 analogReadResolution(11) ça n'affiche que des 0 donc on lit
  // les 12 premiers et on fait un bit shift pour 11 bit
  analogReadResolution(12);


  int Ug12 = analogRead(A0);
  int Ug11 = Ug12 >> 1; 
  float Ug= (Ug11/n_steps)*sensor_voltage; // on convertit en tension

  int Ul12 = analogRead(A1);
  int Ul11 = Ul12 >> 1; 
  float Ul= (Ul11/n_steps)*sensor_voltage; // on convertit en tension

  int Uref12 = analogRead(A2);
  int Uref11 = Uref12 >> 1; // corrigé : Uref11 était lu avant d'être initialisé (Uref = 0 dans les CSV)
  float Uref = (Uref11/n_steps)*sensor_voltage;

  float tempC = sensor.readTempC();
  
  float temperature0=298.15;
    
  unsigned long temps = millis() /1000;

  
  
  Serial.print(Ug, 5);
  Serial.print(",");
  Serial.print(Ul, 5);
  Serial.print(",");
  Serial.print(Uref,5);
  Serial.print(",");
  // print temperature in °C 
  Serial.print(tempC);  
  Serial.print(",");
  Serial.print(temps);
  Serial.println();

  delay(1000);

  
  
  

  
 
  
}