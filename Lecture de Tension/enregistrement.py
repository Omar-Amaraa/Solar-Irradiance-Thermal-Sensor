import serial
import csv
import matplotlib.pyplot as plt
Temps=[]
Ug=[]
Uth=[]
Uref=[]
i=10
port = "COM8"          # port sur lequel est branché l'arduino
baudrate = 115200        # Même que Serial.begin(9600)

#ouverture du port serie (merci chatgpt)
ser = serial.Serial(port, baudrate)
data =['Temps','Uref','Ug','Uth']
# Ouvre le fichier CSV en écriture
with open("mesures"+str(i)+".csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(data)
    print("Enregistrement des données... (Ctrl+C pour arrêter)")

    try:
        while True:
            # Lire une ligne depuis Arduino
            ligne = ser.readline().decode("utf-8").strip()
            print(ligne)  # affichage pour debTemps

            # Sauvegarder dans le CSV
            writer.writerow(ligne.split(","))
    except KeyboardInterrupt:
        print("Arrêt de l'enregistrement.")
        i+=1
    
with open("mesures"+str(i-1)+".csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # saute la première ligne (en-tête)
    for row in reader:
        try:
            Temps.append(float(row[0]))       # 1ère colonne
            Ug.append(float(row[2]))  # 3ème colonne
            Uth.append(float(row[3]))        # 4ème colonne
        except (ValueError, IndexError):
            # ignore les lignes vides ou incorrectes
            pass

plt.figure(figsize=(12, 9))

#  Temps vs Uth
plt.subplot(3, 1, 1)
plt.plot(Uth, Temps, color='royalblue', marker='o', markersize=4, linestyle='-')
plt.title("Évolution de Temps dans le Uth", fontsize=14)
plt.xlabel("Uth (s)")
plt.ylabel("Temps (V)")
plt.grid(True, alpha=0.5)

#  Température vs Uth
plt.subplot(3, 1, 2)
plt.plot(Uth, Ug, color='crimson', marker='s', markersize=4, linestyle='-')
plt.title("Évolution de la Température dans le Uth", fontsize=14)
plt.xlabel("Uth (s)")
plt.ylabel("Température (°C)")
plt.grid(True, alpha=0.5)

#  Temps vs Température (nuage de points + ligne de tendance)
import numpy as np
plt.subplot(3, 1, 3)
plt.scatter(Ug, Temps, color='green', s=50, alpha=0.2, label='Mesures')
# Ajustement linéaire
if len(Ug) > 1:
    m, b = np.polyfit(Ug, Temps, 1)
    plt.plot(Ug, m*np.array(Ug)+b, color='orange', label=f'Fit : y={m:.3f}x+{b:.3f}')
plt.title("Relation entre Temps et la Température", fontsize=14)
plt.xlabel("Température (°C)")
plt.ylabel("Temps (V)")
plt.grid(True, alpha=0.5)
plt.legend()

plt.tight_layout()
plt.show()