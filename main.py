import tkinter as tk
from tkinter import simpledialog, messagebox
import math
from algorithme_prim import executer_prim


class ApplicationMasterEau:
    def __init__(self, root):
        self.root = root
        self.root.title("Optimisation de distribution d'eau par le problème d'arbre couvrant de poids minimal à l'aide l'algorithme de Prim")
        self.root.geometry("1100x750")

        self.noeuds = []
        self.matrice = []
        self.mode = "ajouter"
        self.selection = None

        # --- BARRE D'OUTILS ---
        self.toolbar = tk.Frame(root, bg="#ecf0f1", height=50, bd=1, relief=tk.RAISED)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.creer_bouton_outil("➕ Ajouter Quartier", "ajouter")
        self.creer_bouton_outil("🔗 Lier / Modifier Distance", "lier")
        self.creer_bouton_outil("❌ Supprimer", "supprimer")

        tk.Label(self.toolbar, text=" | ", font=("Arial", 15), bg="#ecf0f1").pack(side=tk.LEFT)

        tk.Button(self.toolbar, text="🚀 LANCER OPTIMISATION", command=self.calculer_prim,
                  bg="#27ae60", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10, pady=5)

        tk.Button(self.toolbar, text="🧹 Réinitialiser", command=self.reset_graph,
                  bg="#95a5a6", fg="white").pack(side=tk.RIGHT, padx=10)

        # --- ZONE CENTRALE ---
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.sidebar = tk.Frame(self.main_frame, width=250, bg="#2c3e50")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(self.sidebar, text="RÉSULTATS D'OPTIMISATION (m)", fg="#2ecc71", bg="#2c3e50", font=("Arial", 11, "bold")).pack(
            pady=10)

        self.result_zone = tk.Text(self.sidebar, bg="#34495e", fg="white", width=28, font=("Consolas", 10))
        self.result_zone.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.canvas = tk.Canvas(self.main_frame, bg="white", highlightthickness=0)
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.gerer_clic)

    def creer_bouton_outil(self, texte, mode):
        btn = tk.Button(self.toolbar, text=texte, command=lambda: self.changer_mode(mode))
        btn.pack(side=tk.LEFT, padx=5, pady=5)

    def changer_mode(self, nouveau_mode):
        self.mode = nouveau_mode
        self.selection = None
        self.refresh_canvas()

    def gerer_clic(self, event):
        cible = None
        for i, (x, y, nom) in enumerate(self.noeuds):
            if math.hypot(event.x - x, event.y - y) < 20:
                cible = i
                break

        if self.mode == "ajouter":
            if cible is None:
                self.ajouter_quartier(event.x, event.y)
        elif self.mode == "lier":
            if cible is not None:
                if self.selection is None:
                    self.selection = cible
                    self.canvas.itemconfig(f"n{cible}", width=3, outline="blue")
                else:
                    self.ajouter_ou_modifier_lien(self.selection, cible)
                    self.selection = None
        elif self.mode == "supprimer":
            if cible is not None:
                self.supprimer_noeud(cible)

    def ajouter_quartier(self, x, y):
        idx = len(self.noeuds)
        nom = "Réservoir" if idx == 0 else f"Quartier {idx}"
        self.noeuds.append((x, y, nom))
        for ligne in self.matrice: ligne.append(0)
        self.matrice.append([0] * len(self.noeuds))
        self.refresh_canvas()

    def ajouter_ou_modifier_lien(self, n1, n2):
        if n1 == n2: return
        dist = simpledialog.askfloat("Saisie", f"Distance entre {self.noeuds[n1][2]} et {self.noeuds[n2][2]} (m) :",
                                     minvalue=0)
        if dist is not None:
            self.matrice[n1][n2] = self.matrice[n2][n1] = dist
        self.refresh_canvas()

    def supprimer_noeud(self, idx):
        self.noeuds.pop(idx)
        self.matrice.pop(idx)
        for ligne in self.matrice: ligne.pop(idx)
        self.refresh_canvas()

    def refresh_canvas(self):
        self.canvas.delete("all")
        for i in range(len(self.noeuds)):
            for j in range(i + 1, len(self.noeuds)):
                if self.matrice[i][j] > 0:
                    x1, y1, _ = self.noeuds[i]
                    x2, y2, _ = self.noeuds[j]
                    self.canvas.create_line(x1, y1, x2, y2, fill="#dfe6e9", width=2)
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=f"{self.matrice[i][j]}m", fill="red")

        for i, (x, y, nom) in enumerate(self.noeuds):
            couleur = "#0984e3" if i == 0 else "#ffffff"
            self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill=couleur, outline="black", tags=f"n{i}")
            self.canvas.create_text(x, y + 25, text=nom, font=("Arial", 8, "bold"))

        self.canvas.create_text(550, 20, text=f"MODE ACTIF : {self.mode.upper()}", font=("Arial", 10, "bold"),
                                fill="blue")

    def calculer_prim(self):
        if len(self.noeuds) < 2: return
        self.result_zone.delete('1.0', tk.END)
        try:
            parents, total = executer_prim(self.matrice)
            self.result_zone.insert(tk.END, f"✅ OPTIMISATION\nDISTANCE TOTALE : {total:.2f} m\n" + "=" * 18 + "\n")
            for enfant, pere in enumerate(parents):
                if pere is not None:
                    x1, y1, _ = self.noeuds[pere]
                    x2, y2, _ = self.noeuds[enfant]
                    self.canvas.create_line(x1, y1, x2, y2, fill="#27ae60", width=4)
                    dist = self.matrice[pere][enfant]
                    self.result_zone.insert(tk.END,
                                            f"• {self.noeuds[pere][2]}\n  -> {self.noeuds[enfant][2]}\n  ({dist} m)\n\n")
        except:
            messagebox.showerror("Erreur", "Le réseau n'est pas entièrement connecté !")

    def reset_graph(self):
        self.noeuds, self.matrice = [], []
        self.refresh_canvas()
        self.result_zone.delete('1.0', tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = ApplicationMasterEau(root)
    root.mainloop()
