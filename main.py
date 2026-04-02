import tkinter as tk
from tkinter import simpledialog, messagebox
import math
from algorithme_prim import executer_prim


class ApplicationDistributionEau:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire de Réseau d'Eau - Optimisation de Prim")
        self.root.geometry("900x650")

        # Données du graphe
        self.noeuds = []  # Liste de (x, y, nom)
        self.matrice = []  # Matrice d'adjacence

        # --- Panneau de gauche (Contrôles) ---
        self.sidebar = tk.Frame(root, width=250, bg="#2c3e50")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(self.sidebar, text="MENU", fg="white", bg="#2c3e50", font=("Arial", 14, "bold")).pack(pady=20)

        self.btn_reset = tk.Button(self.sidebar, text="Réinitialiser", command=self.reset_graph, width=20)
        self.btn_reset.pack(pady=10)

        self.btn_optim = tk.Button(self.sidebar, text="Lancer l'Optimisation", command=self.calculer_prim,
                                   bg="#27ae60", fg="white", font=("Arial", 10, "bold"), width=20)
        self.btn_optim.pack(pady=10)

        self.info_text = tk.Text(self.sidebar, height=15, width=25, bg="#34495e", fg="white", font=("Consolas", 9))
        self.info_text.pack(pady=20, padx=10)
        self.info_text.insert(tk.END,
                              "Instructions :\n1. Cliquez sur la zone blanche pour placer le Réservoir (Bleu).\n2. Cliquez pour ajouter des Quartiers (Orange).\n3. Reliez-les en cliquant sur deux points successivement.")

        # --- Zone de dessin (Canvas) ---
        self.canvas = tk.Canvas(root, bg="white", highlightthickness=2, highlightbackground="#bdc3c7")
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.clic_canvas)

        self.selection = None  # Pour stocker le premier nœud cliqué lors d'une liaison

    def reset_graph(self):
        self.noeuds = []
        self.matrice = []
        self.canvas.delete("all")
        self.info_text.delete('1.0', tk.END)

    def clic_canvas(self, event):
        # Vérifier si on clique sur un nœud existant pour créer une liaison
        for i, (x, y, nom) in enumerate(self.noeuds):
            if math.hypot(event.x - x, event.y - y) < 20:
                if self.selection is None:
                    self.selection = i
                    self.canvas.itemconfig(f"noeud{i}", outline="red", width=3)
                else:
                    self.creer_liaison(self.selection, i)
                    self.canvas.itemconfig(f"noeud{self.selection}", outline="black", width=1)
                    self.selection = None
                return

        # Sinon, créer un nouveau nœud
        id_noeud = len(self.noeuds)
        nom = "Réservoir" if id_noeud == 0 else f"Quartier {id_noeud}"
        couleur = "#3498db" if id_noeud == 0 else "#e67e22"

        self.noeuds.append((event.x, event.y, nom))
        # Agrandir la matrice
        for ligne in self.matrice: ligne.append(0)
        self.matrice.append([0] * len(self.noeuds))

        # Dessin
        self.canvas.create_oval(event.x - 15, event.y - 15, event.x + 15, event.y + 15,
                                fill=couleur, tags=(f"noeud{id_noeud}", "noeud"))
        self.canvas.create_text(event.x, event.y + 25, text=nom, font=("Arial", 9, "bold"))

    def creer_liaison(self, n1, n2):
        if n1 == n2: return
        poids = simpledialog.askfloat("Coût",
                                      f"Coût de raccordement entre {self.noeuds[n1][2]} et {self.noeuds[n2][2]} :",
                                      minvalue=0.1)
        if poids:
            self.matrice[n1][n2] = self.matrice[n2][n1] = poids
            x1, y1, _ = self.noeuds[n1]
            x2, y2, _ = self.noeuds[n2]
            self.canvas.create_line(x1, y1, x2, y2, fill="#bdc3c7", width=2, tags="liaison")
            self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(poids), fill="red")

    def calculer_prim(self):
        if len(self.noeuds) < 2:
            messagebox.showwarning("Attention", "Ajoutez au moins deux points !")
            return

        # Appel de votre algorithme (indépendant de l'interface)
        parents, cout_total = executer_prim(self.matrice)

        # Nettoyage des anciennes lignes d'optimisation
        self.canvas.delete("optim")
        self.info_text.delete('1.0', tk.END)
        self.info_text.insert(tk.END, f"RÉSULTATS :\nTotal : {cout_total:.2f} €\n\n")

        # Dessin de l'arbre optimal
        for enfant, pere in enumerate(parents):
            if pere is not None:
                x1, y1, _ = self.noeuds[pere]
                x2, y2, _ = self.noeuds[enfant]
                self.canvas.create_line(x1, y1, x2, y2, fill="#2ecc71", width=5, tags="optim")
                res = f"De {self.noeuds[pere][2]}\nVers {self.noeuds[enfant][2]}\n--------\n"
                self.info_text.insert(tk.END, res)


if __name__ == "__main__":
    root = tk.Tk()
    app = ApplicationDistributionEau(root)
    root.mainloop()