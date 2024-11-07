import os
import subprocess
import re
import csv
from typing import List, Tuple, Optional
import tkinter as tk
from tkinter import filedialog, messagebox


# === Fonctions pour la gestion des dépôts Git ===

def lire_csv(fichier: str) -> List[Tuple[str, str]]:
    """Lit le fichier CSV et extrait les liens GitHub et les noms des apprenants."""
    apprenants = []
    try:
        with open(fichier, "r") as f:
            reader = csv.reader(f)
            next(reader)  # Sauter l'en-tête
            for row in reader:
                if len(row) >= 2:
                    apprenant = row[0].strip()  # Colonne "Apprenant"
                    lien_github = row[1].strip()  # Colonne "Lien Github"
                    apprenants.append((apprenant, lien_github))
    except FileNotFoundError:
        print(f"Erreur : Le fichier {fichier} est introuvable.")
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
    return apprenants


def valider_et_corriger_url(url: str) -> Optional[str]:
    """Valide et corrige l'URL GitHub."""
    regex = r'^https:\/\/github\.com\/[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+(\.git)?$'
    if re.match(regex, url):
        return url if url.endswith(".git") else url + ".git"
    return None


def creer_dossier_si_absent(dossier: str) -> None:
    """Crée un dossier s'il n'existe pas."""
    if not os.path.exists(dossier):
        os.makedirs(dossier)


def cloner_depot(apprenant: str, lien_github: str, dossier_apprenant: str) -> None:
    """Clone un dépôt GitHub."""
    print(f"\nClonage du dépôt pour {apprenant} : {lien_github}")
    try:
        subprocess.run(["git", "clone", lien_github, dossier_apprenant], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du clonage pour {apprenant} : {e}")


def mettre_a_jour_depot(apprenant: str, dossier_apprenant: str) -> None:
    """Met à jour un dépôt existant avec git pull."""
    print(f"\nMise à jour du dépôt pour {apprenant} (git pull)")
    subprocess.run(["git", "-C", dossier_apprenant, "pull"], check=True)


def committer_et_pousser_modifications(apprenant: str, dossier_apprenant: str, message: str) -> None:
    """Effectue un commit et un push des modifications."""
    print(f"Ajout, commit et push pour {apprenant}")
    try:
        subprocess.run(["git", "-C", dossier_apprenant, "add", "."], check=True)
        subprocess.run(["git", "-C", dossier_apprenant, "commit", "-m", message], check=True)
        subprocess.run(["git", "-C", dossier_apprenant, "push"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du commit/push pour {apprenant} : {e}")


def gerer_depot(apprenants: List[Tuple[str, str]], dossier_cible: str, clone: bool = True, pull: bool = True, commit_push_message: Optional[str] = None) -> None:
    """Gère les dépôts Git des apprenants."""
    creer_dossier_si_absent(dossier_cible)

    for apprenant, lien_github in apprenants:
        dossier_apprenant = os.path.join(dossier_cible, apprenant)

        # Validation et correction de l'URL
        lien_github = valider_et_corriger_url(lien_github)

        if lien_github:
            if os.path.exists(dossier_apprenant) and os.path.exists(os.path.join(dossier_apprenant, ".git")):
                if pull:
                    mettre_a_jour_depot(apprenant, dossier_apprenant)

                if commit_push_message:
                    committer_et_pousser_modifications(apprenant, dossier_apprenant, commit_push_message)
            else:
                if clone:
                    cloner_depot(apprenant, lien_github, dossier_apprenant)
        else:
            print(f"\nLien GitHub invalide pour {apprenant} : {lien_github}")


def gerer_dossiers(csv_file: str, clone: bool = True, pull: bool = True, commit_push_message: Optional[str] = None) -> None:
    """Gère les dossiers et les opérations Git."""
    dossier_cible = os.path.splitext(csv_file)[0]
    apprenants = lire_csv(csv_file)
    gerer_depot(apprenants, dossier_cible, clone, pull, commit_push_message)


# === Interface utilisateur ===

def executer_script(csv_file: str, action: str, commit_message: Optional[str] = None) -> None:
    """Exécute le script avec les options choisies depuis l'interface."""
    try:
        if action == "clone_pull":
            gerer_dossiers(csv_file, clone=True, pull=True)
        elif action == "commit_push" and commit_message:
            gerer_dossiers(csv_file, clone=False, pull=True, commit_push_message=commit_message)
        messagebox.showinfo("Succès", "L'exécution du script est terminée.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")


def choisir_fichier_csv() -> None:
    """Permet à l'utilisateur de choisir un fichier CSV."""
    csv_file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    entry_csv.delete(0, tk.END)
    entry_csv.insert(0, csv_file)


def activer_champ_commit() -> None:
    """Active ou désactive le champ de message de commit selon l'option choisie."""
    if var_action.get() == "commit_push":
        entry_commit.config(state="normal")
    else:
        entry_commit.config(state="disabled")


def executer() -> None:
    """Lance l'exécution selon les options choisies."""
    csv_file = entry_csv.get()
    action = var_action.get()
    commit_message = entry_commit.get().strip()

    if not csv_file:
        messagebox.showwarning("Avertissement", "Veuillez sélectionner un fichier CSV.")
        return

    if action == "commit_push" and not commit_message:
        messagebox.showwarning("Avertissement", "Veuillez entrer un message de commit.")
        return

    executer_script(csv_file, action, commit_message if action == "commit_push" else None)


# === Configuration de l'interface graphique ===

root = tk.Tk()
root.title("Gestion des Dépôts GitHub")

# Sélection du fichier CSV
frame_csv = tk.Frame(root)
frame_csv.pack(pady=10)
label_csv = tk.Label(frame_csv, text="Chemin du fichier CSV :")
label_csv.pack(side=tk.LEFT, padx=5)
entry_csv = tk.Entry(frame_csv, width=50)
entry_csv.pack(side=tk.LEFT, padx=5)
btn_browse = tk.Button(frame_csv, text="Parcourir", command=choisir_fichier_csv)
btn_browse.pack(side=tk.LEFT)

# Boutons radio pour choisir l'action
frame_radio = tk.Frame(root)
frame_radio.pack(pady=10)
var_action = tk.StringVar(value="clone_pull")
radio_clone_pull = tk.Radiobutton(frame_radio, text="Clone et Pull", variable=var_action, value="clone_pull", command=activer_champ_commit)
radio_clone_pull.pack(anchor="w")
radio_commit_push = tk.Radiobutton(frame_radio, text="Commit et Push", variable=var_action, value="commit_push", command=activer_champ_commit)
radio_commit_push.pack(anchor="w")

# Champ de message de commit
frame_commit = tk.Frame(root)
frame_commit.pack(pady=10)
label_commit = tk.Label(frame_commit, text="Message de commit :")
label_commit.pack(side=tk.LEFT, padx=5)
entry_commit = tk.Entry(frame_commit, width=50, state="disabled")
entry_commit.pack(side=tk.LEFT, padx=5)

# Bouton pour exécuter le script
btn_executer = tk.Button(root, text="Exécuter", command=executer, width=20)
btn_executer.pack(pady=20)

# Lancement de l'interface
root.mainloop()
