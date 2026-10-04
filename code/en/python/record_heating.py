"""
Record the measurements during the heating-wire experiment (heat capacity CT).

Use with the Arduino `voltage_reading.ino` sketch, which sends lines of the form:
    Time,Uref,Ug,Uth,U_heating_wire

The script saves everything to a CSV until Ctrl+C, then reloads the file and
saves three figures (PNG).
"""
import csv

import matplotlib.pyplot as plt
import numpy as np
import serial

Time = []
Ug = []
Uth = []
Uref = []
U_heating_wire = []
i = 10
port = "COM5"          # port the Arduino is plugged into
baudrate = 115200      # Same as Serial.begin(115200)

# open the serial port
ser = serial.Serial(port, baudrate)
header = ['Time', 'Uref', 'Ug', 'Uth', 'U_heating_wire']

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

# close the serial port once acquisition is over
ser.close()

# ========== READ BACK THE RECORDED CSV ==========

filename = "measurements" + str(i - 1) + ".csv"
print("Reading file:", filename)

with open(filename, "r", newline="", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)  # skip the header line
    for row in reader:
        try:
            # row = [Time, Uref, Ug, Uth, U_heating_wire]
            if len(row) < 5:
                continue
            Time.append(float(row[0]))
            Uref.append(float(row[1]))
            Ug.append(float(row[2]))
            Uth.append(float(row[3]))
            U_heating_wire.append(float(row[4]))
        except (ValueError, IndexError):
            # skip empty or malformed lines
            pass

# convert to numpy for processing / fitting
Time = np.array(Time)
Uref = np.array(Uref)
Ug = np.array(Ug)
Uth = np.array(Uth)
U_heating_wire = np.array(U_heating_wire)

# ========== FIGURE 1: ALL VOLTAGES OVER TIME ==========

fig1 = plt.figure(figsize=(12, 8))

plt.subplot(4, 1, 1)
plt.plot(Time, Uref, marker=".", linestyle="-")
plt.ylabel("Uref (V)")
plt.title("Voltages over time")
plt.grid(True, alpha=0.5)

plt.subplot(4, 1, 2)
plt.plot(Time, Ug, marker=".", linestyle="-")
plt.ylabel("Ug (V)")
plt.grid(True, alpha=0.5)

plt.subplot(4, 1, 3)
plt.plot(Time, Uth, marker=".", linestyle="-")
plt.ylabel("Uth (V)")
plt.grid(True, alpha=0.5)

plt.subplot(4, 1, 4)
plt.plot(Time, U_heating_wire, marker=".", linestyle="-")
plt.xlabel("Time (s)")
plt.ylabel("U_wire (V)")
plt.grid(True, alpha=0.5)

plt.tight_layout()

# Save figure 1
fig1.savefig("voltages_vs_time.png", dpi=300, bbox_inches="tight")
plt.close(fig1)   # close the figure instead of displaying it

# ========== FIGURE 2: AMPLIFIER TRANSFER CURVE Ug = f(Uref) (GAIN) ==========

fig2 = plt.figure(figsize=(8, 6))

plt.scatter(Uref, Ug, s=20, alpha=0.6, label="Measurements")
plt.xlabel("Uref (V)  (input)")
plt.ylabel("Ug (V)   (output)")
plt.title("Amplifier transfer curve: Ug = f(Uref)")
plt.grid(True, alpha=0.5)

# linear regression to estimate the gain
if len(Uref) > 1:
    m, b = np.polyfit(Uref, Ug, 1)  # Ug ≈ m * Uref + b
    Ug_fit = m * Uref + b
    plt.plot(Uref, Ug_fit, linewidth=2,
             label=f"Fit: Ug ≈ {m:.3f}·Uref + {b:.3f}")

    print(f"Approximate gain (slope m) = {m:.4f}")
    print(f"Offset b = {b:.4f} V")

plt.legend()

# Save figure 2
fig2.savefig("Ug_vs_Uref_gain.png", dpi=300, bbox_inches="tight")
plt.close(fig2)

# ========== FIGURE 3: CIRCUIT CONDITIONS (Uth & U_wire) ==========

fig3 = plt.figure(figsize=(10, 6))
plt.plot(Time, Uth, marker=".", linestyle="-", label="Uth")
plt.plot(Time, U_heating_wire, marker=".", linestyle="-", label="U_heating_wire")
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.title("Uth and U_heating_wire over time")
plt.grid(True, alpha=0.5)
plt.legend()

# Save figure 3
fig3.savefig("Uth_Uwire_vs_time.png", dpi=300, bbox_inches="tight")
plt.close(fig3)

print("Saved images:")
print("  - voltages_vs_time.png")
print("  - Ug_vs_Uref_gain.png")
print("  - Uth_Uwire_vs_time.png")
