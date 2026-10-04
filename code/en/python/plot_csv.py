"""
Plot Ug against the TMP117 temperature from an already recorded calibration CSV.
Columns are looked up by name, so it works with the files in data/02_calibration
(header "Temperature TMP") and with files from record_calibration.py
(header "Temperature_TMP").

Usage:
    python plot_csv.py ../../../data/02_calibration/mesures0.csv
"""
import csv
import sys

import matplotlib.pyplot as plt

if len(sys.argv) < 2:
    sys.exit("Usage: python plot_csv.py <file.csv>")
filename = sys.argv[1]

Ug = []
Temperature = []

# Read the CSV file
with open(filename, "r", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    temp_col = "Temperature TMP" if "Temperature TMP" in reader.fieldnames else "Temperature_TMP"
    for row in reader:
        try:
            ug = float(row["Ug"])
            t = float(row[temp_col])
        except (ValueError, TypeError, KeyError):
            # skip empty or malformed lines
            continue
        if t <= -0.01:
            # the TMP117 returns -0.01 when a reading fails
            continue
        Ug.append(ug)
        Temperature.append(t)

plt.figure(figsize=(8, 5))
plt.plot(Temperature, Ug, marker='o', markersize=2, linestyle='', color='b',
         label='Ug vs TMP')

plt.title("Ug as a function of the TMP117 temperature")
plt.xlabel("TMP (°C)")
plt.ylabel("Ug (V)")
plt.grid(True)
plt.legend()

plt.show()
