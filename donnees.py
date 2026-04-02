# donnees.py
# 0: Réservoir, 1: Quartier A, 2: Quartier B, 3: Quartier C
# Les valeurs représentent le coût de pose des tuyaux en milliers d'euros.
# 0 signifie qu'il n'y a pas de connexion directe possible.

reseau_eau = [
    [0, 10, 20, 0],  # Connexions depuis le Réservoir
    [10, 0, 30, 5],   # Connexions depuis Quartier A
    [20, 30, 0, 15],  # Connexions depuis Quartier B
    [0, 5, 15, 0]     # Connexions depuis Quartier C
]