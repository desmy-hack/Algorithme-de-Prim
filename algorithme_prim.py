

def executer_prim(graph):
    n = len(graph)

    inf = float('inf')
    poids_min = [inf] * n
    parent = [None] * n
    visite = [False] * n

  
    poids_min[0] = 0
    cout_total = 0

    print("--- Début de l'optimisation du réseau ---")

    for _ in range(n):
 
        u = -1
        for i in range(n):
            if not visite[i] and (u == -1 or poids_min[i] < poids_min[u]):
                u = i

        if poids_min[u] == inf:
            break  # Le graphe n'est pas connexe

        visite[u] = True
        cout_total += poids_min[u]

        if parent[u] is not None:
            print(f"Connexion établie : Nœud {parent[u]} -> Nœud {u} (Coût: {poids_min[u]})")

 
        for v in range(n):
          
            if graph[u][v] != 0 and not visite[v]:
                if graph[u][v] < poids_min[v]:
                    poids_min[v] = graph[u][v]
                    parent[v] = u

    return parent, cout_total
