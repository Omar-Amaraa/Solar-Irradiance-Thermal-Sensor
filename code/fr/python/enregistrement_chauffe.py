"""
Enregistrement des mesures pendant l'expérience du fil chauffant (mesure de CT).

À utiliser avec le sketch Arduino `lecture_tension.ino`, qui envoie sur le port
série des lignes de la forme :
    Temps,Uref,Ug,Uth,Ufil_chauffant

Le script enregistre tout dans un CSV jusqu'à Ctrl+C, puis relit le fichier
et sauvegarde trois figures (PNG).
"""
import csv

import matplotlib.pyplot as plt
import numpy as np
import serial

Temps = []
Ug = []
Uth = []
Uref = []
Ufil_chauffant = []
i = 10
port = "COM5"          # port sur lequel est branché l'arduino
baudrate = 115200      # Même que Serial.begin(115200)

# ouverture du port serie
ser = serial.Serial(port, baudrate)
data = ['Temps', 'Uref', 'Ug', 'Uth', 'Ufil_chauffant']

# Ouvre le fichier CSV en écriture
with open("mesures" + str(i) + ".csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(data)
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
        i += 1

# on ferme le port série une fois l'acquisition terminée
ser.close()

# ========== LECTURE DU CSV ENREGISTRÉ ==========

filename = "mesures" + str(i - 1) + ".csv"
print("Lecture du fichier :", filename)

with open(filename, "r", newline="", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)  # saute la première ligne (en-tête)
    for row in reader:
        try:
            # row = [Temps, Uref, Ug, Uth, Ufil_chauffant]
            if len(row) < 5:
                continue
            Temps.append(float(row[0]))
            Uref.append(float(row[1]))
            Ug.append(float(row[2]))
            Uth.append(float(row[3]))
            Ufil_chauffant.append(float(row[4]))
        except (ValueError, IndexError):
            # ignore les lignes vides ou incorrectes
            pass

# conversion en numpy pour les traitements/fit
Temps = np.array(Temps)
Uref = np.array(Uref)
Ug = np.array(Ug)
Uth = np.array(Uth)
Ufil_chauffant = np.array(Ufil_chauffant)

# ========== FIGURE 1 : TOUTES LES TENSIONS EN FONCTION DU TEMPS ==========

fig1 = plt.figure(figsize=(12, 8))

plt.subplot(4, 1, 1)
plt.plot(Temps, Uref, marker=".", linestyle="-")
plt.ylabel("Uref (V)")
plt.title("Tensions en fonction du temps")
plt.grid(True, alpha=0.5)

plt.subplot(4, 1, 2)
plt.plot(Temps, Ug, marker=".", linestyle="-")
plt.ylabel("Ug (V)")
plt.grid(True, alpha=0.5)

plt.subplot(4, 1, 3)
plt.plot(Temps, Uth, marker=".", linestyle="-")
plt.ylabel("Uth (V)")
plt.grid(True, alpha=0.5)

plt.subplot(4, 1, 4)
plt.plot(Temps, Ufil_chauffant, marker=".", linestyle="-")
plt.xlabel("Temps (s)")
plt.ylabel("Ufil (V)")
plt.grid(True, alpha=0.5)

plt.tight_layout()

# Sauvegarde de la figure 1
fig1.savefig("tensions_vs_temps.png", dpi=300, bbox_inches="tight")
plt.close(fig1)   # ferme la figure pour ne pas l'afficher

# ========== FIGURE 2 : COURBE DE TRANSFERT Ug = f(Uref) (GAIN) ==========

fig2 = plt.figure(figsize=(8, 6))

plt.scatter(Uref, Ug, s=20, alpha=0.6, label="Mesures")
plt.xlabel("Uref (V)  (entrée)")
plt.ylabel("Ug (V)   (sortie)")
plt.title("Courbe de transfert de l'ampli : Ug = f(Uref)")
plt.grid(True, alpha=0.5)

# régression linéaire pour estimer le gain
if len(Uref) > 1:
    m, b = np.polyfit(Uref, Ug, 1)  # Ug ≈ m * Uref + b
    Ug_fit = m * Uref + b
    plt.plot(Uref, Ug_fit, linewidth=2,
             label=f"Ajustement : Ug ≈ {m:.3f}·Uref + {b:.3f}")

    print(f"Gain approximatif (pente m) = {m:.4f}")
    print(f"Offset b = {b:.4f} V")

plt.legend()

# Sauvegarde de la figure 2
fig2.savefig("Ug_vs_Uref_gain.png", dpi=300, bbox_inches="tight")
plt.close(fig2)

# ========== FIGURE 3 : CONDITIONS DU CIRCUIT (Uth & Ufil) ==========

fig3 = plt.figure(figsize=(10, 6))
plt.plot(Temps, Uth, marker=".", linestyle="-", label="Uth")
plt.plot(Temps, Ufil_chauffant, marker=".", linestyle="-", label="Ufil_chauffant")
plt.xlabel("Temps (s)")
plt.ylabel("Tension (V)")
plt.title("Évolution de Uth et Ufil_chauffant")
plt.grid(True, alpha=0.5)
plt.legend()

# Sauvegarde de la figure 3
fig3.savefig("Uth_Ufil_vs_temps.png", dpi=300, bbox_inches="tight")
plt.close(fig3)

print("Images sauvegardées :")
print("  - tensions_vs_temps.png")
print("  - Ug_vs_Uref_gain.png")
print("  - Uth_Ufil_vs_temps.png")
