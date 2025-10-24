import pandas as pd
import csv
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
Ug=[]
Temperature=[]
Uref=[]
Temps=[]
Ul=[]
# 📥 Lire le fichier CSV
with open("mesures"+str(i-1)+".csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # saute la première ligne (en-tête)
    for row in reader:
        try:
            Ug.append(float(row[0]))       # 1ère colonne
            Ul.append(float(row[1]))
            Uref.append(float(row[2]))
            Temperature.append(float(row[3]))  # 3ème colonne
            Temps.append(float(row[4]))        # 4ème colonne
        except (ValueError, IndexError):
            # ignore les lignes vides ou incorrectes
            pass


plt.figure(figsize=(8, 5))
plt.plot(x, y, marker='o', linestyle='-', color='b', label='Ug en fonction de TMP')

plt.title("Courbe de Ug en fonction de TMP")
plt.xlabel("TMP (°C)")
plt.ylabel("Ug")
plt.grid(True)
plt.legend()

plt.show()
