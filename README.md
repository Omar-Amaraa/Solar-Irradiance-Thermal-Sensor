# 📌 Projet : Acquisition et Visualisation de Mesures Arduino

Ce projet permet **d’enregistrer des mesures envoyées par un Arduino via le port série**, de les sauvegarder dans un fichier CSV, puis de générer différents graphiques (tensions, température, relations entre variables).

Deux scripts sont fournis :

- **`enregistrement.py`** — acquisition + CSV + graphiques  
- **`drawplot.py`** — tracé à partir d’un CSV existant

---

## 📁 Contenu du projet

```
enregistrement.py      # Script principal : acquisition + CSV + graphiques
drawplot.py            # Script secondaire : lecture CSV + tracé
mesures0.csv           # Exemple de données
README.md              # Documentation du projet
```

---

## ⚙️ Fonctionnement

### 🔹 1. `enregistrement.py`

Ce script :

1. Ouvre le port série (COM5, 115200 bauds)  
2. Lit en continu les lignes envoyées par l’Arduino sous la forme :  
   ```
   Ug,Ul,Temperature TMP,Temps
   ```
3. Enregistre les mesures dans un fichier CSV :  
   ```
   mesures<i>.csv
   ```
4. Affiche les données pour le debug  
5. À l’arrêt (Ctrl + C), recharge le CSV et génère 3 graphiques :
   - Ug (V) vs Temps (s)  
   - Température (°C) vs Temps (s)  
   - Ug vs Température (fit linéaire)

---

### 🔹 2. `drawplot.py`

Ce script :

- Lit un fichier CSV existant (`mesures<i-1>.csv`)  
- Trace la courbe **Ug en fonction de la température (TMP)**  

⚠️ Attention : certaines variables doivent être définies (i, x, y).

---

## 🛠️ Installation

Installer les dépendances Python :

```bash
pip install pyserial matplotlib numpy pandas
```

---

## ▶️ Utilisation

### 🔸 1. Lancer l’enregistrement des mesures

```bash
python enregistrement.py
```

Arrêt : **Ctrl + C**

Le fichier suivant sera généré automatiquement :

```
mesures0.csv, mesures1.csv…
```

---

### 🔸 2. Générer une courbe depuis un CSV existant

```bash
python drawplot.py
```

---

## 📊 Graphiques générés

### Depuis `enregistrement.py`
- Ug (V) en fonction du temps (s)
- Température (°C) en fonction du temps (s)
- Ug en fonction de la température (avec régression linéaire)

### Depuis `drawplot.py`
- Ug en fonction de la température (TMP)

---

## 🚀 Améliorations possibles

- Détection automatique du port série  
- Choix du fichier CSV via argument ou interface  
- Correction des variables manquantes dans `drawplot.py`  
- Interface graphique (Tkinter / PyQt)  
- Séparation claire acquisition / analyse  

---

## 📄 Licence

Projet libre d'utilisation, modification et redistribution.
