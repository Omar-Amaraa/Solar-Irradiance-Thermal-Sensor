#include <Arduino.h>

const float n_steps = 2047.0; // pour 11 bits (2^11 - 1)

void setup() {
  Serial.begin(115200);
  analogReadResolution(12); // on lit en 12 bits
}

void loop() {
  float start_voltage = 4.82; 
  analogReference(5);


  // Lecture du signal en 12 bits
  int A012 = analogRead(A0);

  // Conversion 12 bits -> 11 bits
  int A011 = A012 >> 1; // division par 2
  
  int A112 = analogRead(A1);
  int A111 = A112 >> 1; 
  
  int A212 = analogRead(A2);
  int A211 = A212 >> 1; 
  // Conversion en tension réelle
  float Ug =  ((A011) / n_steps ) * start_voltage ;
  float Uth =  ((A111) / n_steps ) * start_voltage ;
  float Uref =  ((A211) / n_steps ) * start_voltage ;
  // Temps en secondes
  float temps = millis() / 1000.0;

  // Affichage sur le moniteur série
  Serial.print("Temps (s): ");
  Serial.print(temps, 2); // affichage avec 2 décimales
  Serial.print(" | Uref (V): ");
  Serial.println(Uref, 5); // affichage avec 5 décimales
  Serial.print(" | Ug (V): ");
  Serial.println(Ug, 5);
  Serial.print(" | Uth");
  Serial.print(Uth, 3);

  // Attendre 1 seconde
  delay(1000);
}

