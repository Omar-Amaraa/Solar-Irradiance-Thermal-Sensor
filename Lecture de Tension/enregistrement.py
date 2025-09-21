import serial
import csv


port = "COM5"          # port sur lequel est branché l'arduino
baudrate = 9600        # Même que Serial.begin(9600)

#ouverture du port serie (merci chatgpt)
ser = serial.Serial(port, baudrate)

# Ouvre le fichier CSV en écriture
with open("mesures.csv", "w", newline="") as f:
    writer = csv.writer(f)

    print("Enregistrement des données... (Ctrl+C pour arrêter)")

    try:
        while True:
            # Lire une ligne depuis Arduino
            ligne = ser.readline().decode("utf-8").strip()
            print(ligne)  # affichage pour debug

            # Sauvegarder dans le CSV
            writer.writerow(ligne.split(","))
    except KeyboardInterrupt:
        print("Arrêt de l'enregistrement.")
