"""
Record the calibration data sent by the Arduino `calibration.ino` sketch.

The Arduino sends lines of the form:
    Ug,Ul,Uref,Temperature_TMP,Time

The script saves everything to a CSV until Ctrl+C, then reloads the file and
shows three plots: Ug vs time, temperature vs time, and Ug vs temperature
with a linear fit.
"""
import csv

import matplotlib.pyplot as plt
import numpy as np
import serial

Ug = []
Temperature = []
Time = []
Ul = []
Uref = []
i = 10
port = "COM5"          # port the Arduino is plugged into
baudrate = 115200      # Same as Serial.begin(115200)

# open the serial port
ser = serial.Serial(port, baudrate)
header = ['Ug', 'Ul', 'Uref', 'Temperature_TMP', 'Time']

# Open the CSV file for writing
with open("measurements" + str(i) + ".csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    print("Recording data... (Ctrl+C to stop)")

    try:
        while True:
            # Read one line from the Arduino
            line = ser.readline().decode("utf-8").strip()
            print(line)  # debug output

            # Save it to the CSV
            writer.writerow(line.split(","))
    except KeyboardInterrupt:
        print("Recording stopped.")
        i += 1

ser.close()

with open("measurements" + str(i - 1) + ".csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip the header line
    for row in reader:
        try:
            Ug.append(float(row[0]))           # 1st column
            Ul.append(float(row[1]))           # 2nd column
            Uref.append(float(row[2]))         # 3rd column
            Temperature.append(float(row[3]))  # 4th column
            Time.append(float(row[4]))         # 5th column
        except (ValueError, IndexError):
            # skip empty or malformed lines
            pass

plt.figure(figsize=(12, 9))

# Ug vs time
plt.subplot(3, 1, 1)
plt.plot(Time, Ug, color='royalblue', marker='o', markersize=4, linestyle='-')
plt.title("Ug over time", fontsize=14)
plt.xlabel("Time (s)")
plt.ylabel("Ug (V)")
plt.grid(True, alpha=0.5)

# Temperature vs time
plt.subplot(3, 1, 2)
plt.plot(Time, Temperature, color='crimson', marker='s', markersize=4, linestyle='-')
plt.title("Temperature over time", fontsize=14)
plt.xlabel("Time (s)")
plt.ylabel("Temperature (°C)")
plt.grid(True, alpha=0.5)

# Ug vs temperature (scatter + trend line)
plt.subplot(3, 1, 3)
plt.scatter(Temperature, Ug, color='green', s=50, alpha=0.2, label='Measurements')
# Linear fit
if len(Temperature) > 1:
    m, b = np.polyfit(Temperature, Ug, 1)
    plt.plot(Temperature, m * np.array(Temperature) + b, color='orange',
             label=f'Fit: y={m:.3f}x+{b:.3f}')
plt.title("Ug vs temperature", fontsize=14)
plt.xlabel("Temperature (°C)")
plt.ylabel("Ug (V)")
plt.grid(True, alpha=0.5)
plt.legend()

plt.tight_layout()
plt.show()
