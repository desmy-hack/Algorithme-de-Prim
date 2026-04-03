"""
FICHIER : donnees.py
OBJET : Matrice d'adjacence du réseau de distribution d'eau
UNITÉ : Les poids représentent des distances

Indexation des sommets du graphe :
0 : Réservoir Central (Source)
1 : Quartier A
2 : Quartier B
3 : Quartier C
La matrice 'reseau_eau' définit les distances entre les points.
Une valeur de 0 indique qu'aucune connexion directe n'est possible.
"""
reseau_eau = [
    [0, 100, 200, 0],    
    [100, 0, 300, 50],  
    [200, 300, 0, 150], 
    [0, 50, 150, 0]      
]
"""
Note pour le rapport : L'algorithme de Prim utilisera cette matrice 
pour extraire l'Arbre Couvrant de Poids Minimal (ACPM), ce qui 
correspond ici au tracé de longueur totale minimale en mètre.
"""
