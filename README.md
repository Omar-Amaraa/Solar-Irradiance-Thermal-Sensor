Projet : Acquisition et Visualisation de Mesures Arduino

Ce projet permet d’enregistrer des mesures envoyées par un Arduino via
le port série, de les sauvegarder dans un fichier CSV, puis de générer
différents graphiques (tensions, température, relation entre variables).

Deux scripts sont fournis : - enregistrement.py : acquisition + CSV +
graphiques - drawplot.py : tracé à partir d’un CSV existant

------------------------------------------------------------------------

Contenu du projet

enregistrement.py : Script principal (acquisition + enregistrement +
graphiques) drawplot.py : Script secondaire (lecture CSV + tracé)
mesures0.csv : Exemple de fichier de mesures

------------------------------------------------------------------------

Fonctionnement

1. Script enregistrement.py

-   Ouvre le port série (COM5, 115200 bauds).
-   Lit en continu les données envoyées par l’Arduino.
-   Sauvegarde les mesures dans un fichier CSV nommé automatiquement :
    mesures.csv
-   Affiche les données reçues pour le debug.
-   À l’arrêt manuel (Ctrl + C), recharge le CSV et génère 3 graphiques
    :
    -   Ug en fonction du temps
    -   Température en fonction du temps
    -   Ug en fonction de la température (avec ligne de tendance)

Format attendu des données envoyées par l’Arduino : Ug,Ul,Temperature
TMP,Temps

------------------------------------------------------------------------

2. Script drawplot.py

-   Lit un fichier CSV existant (mesures.csv).
-   Trace une courbe de Ug en fonction de la température.
-   Attention : certaines variables doivent être définies (i, x, y).

------------------------------------------------------------------------

Installation des dépendances

pip install pyserial matplotlib numpy pandas

------------------------------------------------------------------------

Utilisation

1. Enregistrer les mesures depuis l’Arduino

python enregistrement.py (Arrêt : Ctrl + C)

2. Tracer une courbe depuis un fichier CSV

python drawplot.py

------------------------------------------------------------------------

Graphiques générés

Depuis enregistrement.py : - Ug (V) vs Temps (s) - Température (°C) vs
Temps (s) - Ug vs Température + régression linéaire

Depuis drawplot.py : - Ug en fonction de la température (TMP)

------------------------------------------------------------------------

Améliorations possibles

-   Détection automatique du port série
-   Choix du fichier CSV via arguments ou interface
-   Correction des variables non définies dans drawplot.py
-   Interface graphique (Tkinter, PyQt)
-   Séparation acquisition / analyse

------------------------------------------------------------------------

Licence

Projet libre d’utilisation, modification et redistribution.
