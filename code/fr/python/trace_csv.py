"""
Trace Ug en fonction de la température TMP117 à partir d'un CSV d'étalonnage
déjà enregistré. Les colonnes sont lues par leur nom ("Ug" et "Temperature TMP"),
donc ça marche avec mesures0.csv, mesures4.csv et mesures6.csv.

Utilisation :
    python trace_csv.py ../../../data/02_calibration/mesures0.csv
"""
import csv
import sys

import matplotlib.pyplot as plt

if len(sys.argv) < 2:
    sys.exit("Utilisation : python trace_csv.py <fichier.csv>")
fichier = sys.argv[1]

Ug = []
Temperature = []

# Lire le fichier CSV
with open(fichier, "r", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            ug = float(row["Ug"])
            t = float(row["Temperature TMP"])
        except (ValueError, TypeError, KeyError):
            # ignore les lignes vides ou incorrectes
            continue
        if t <= -0.01:
            # le TMP117 renvoie -0.01 quand la lecture échoue
            continue
        Ug.append(ug)
        Temperature.append(t)

plt.figure(figsize=(8, 5))
plt.plot(Temperature, Ug, marker='o', markersize=2, linestyle='', color='b',
         label='Ug en fonction de TMP')

plt.title("Courbe de Ug en fonction de TMP")
plt.xlabel("TMP (°C)")
plt.ylabel("Ug (V)")
plt.grid(True)
plt.legend()

plt.show()
