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

}
  


void loop() {
  analogReadResolution(12);

  float start_voltage = 4.7; 


  // Lecture du signal en 12 bits
  int A012 = analogRead(A0);

  // Conversion 12 bits -> 11 bits
  int A011 = A012 >> 1; // division par 2
  
  int A112 = analogRead(A1);
  int A111 = A112 >> 1; 
  
  int A212 = analogRead(A2);
  int A211 = A212 >> 1; 

  int A312 = analogRead(A3);
  int A311 = A312 >> 1; 
  // Conversion en tension réelle
  float Ug =  ((A011) / n_steps ) * start_voltage ;
  float Uth =  ((A111) / n_steps ) * start_voltage ;
  float Uref =  ((A211) / n_steps ) * start_voltage ;
  float Ufil_chauffant = ((A311) / n_steps ) * start_voltage ;
  // Temps en secondes
  float temps = millis() / 1000.0;

  // Affichage sur le moniteur série

  Serial.print(temps, 2); // affichage avec 2 décimales
  Serial.print(",");
  Serial.print(Uref, 5); // affichage avec 5 décimales
  Serial.print(",");
  Serial.print(Ug, 5);
  Serial.print(",");
  Serial.print(Uth,4);
  Serial.print(",");
  Serial.print(Ufil_chauffant, 3);
  Serial.println();




  


  //Serial.print("temps: ");

  delay(500);

  
  
  

  
 
  
}