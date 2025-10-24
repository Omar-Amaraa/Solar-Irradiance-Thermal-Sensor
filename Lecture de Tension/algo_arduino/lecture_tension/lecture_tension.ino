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



  


  //Serial.print("temps: ");

  delay(500);

  
  
  

  
 
  
}
