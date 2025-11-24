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
<<<<<<< Updated upstream
  float resistance0=100.5;
  float start_voltage = 5;
  float beta=3096;
  
  //impossible de lire 11 bits en fixant à 11 analogReadResolution(11) ça n'affiche que des 0 donc on lit
  // les 12 premiers et on fait un bit shift pour 11 bit
  analogReadResolution(12);


  int sensorValue12 = analogRead(A0);
  int sensorRead2 = analogRead(A1);
  int sensorValue11 = sensorValue12 >> 1; // un bit shift à droite de 1 est equivalent à une division par 2
  //(et inversement pour le bitshift gauche c'est une multiplication par deux)
  //pour notre cas on passe de 0–4095 à 0–2047 (11 bits) valeurs possibles
  int sensorRead11_2 = sensorRead2 >>1;
  float Utest = (sensorRead11_2/n_steps)*start_voltage; // on convertit en tension
  float Ug = (sensorValue11/n_steps)*start_voltage; // on convertit en tension

  Serial.print("Ug: ");
  Serial.println(Ug, 5);
  Serial.print("Utest:");
  Serial.println(Utest,5);
=======
  float start_voltage = 4.82; 


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
  Serial.print(Uth, 3);
  Serial.print(",");
  Serial.print(Ufil_chauffant, 3);
  Serial.println();

>>>>>>> Stashed changes



  


  //Serial.print("temps: ");

  delay(500);

  
  
  

  
 
  
}
