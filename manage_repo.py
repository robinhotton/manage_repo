import os
import subprocess
import argparse
import re
import csv
from typing import List, Tuple, Optional


def lire_csv(fichier: str) -> List[Tuple[str, str]]:
    """
    Fonction pour lire le fichier CSV et extraire les liens GitHub et les noms des apprenants.
    Cette fonction prend un fichier CSV, en lit les lignes et récupère le nom de l'apprenant 
    et l'URL du dépôt GitHub, puis les retourne sous forme de liste de tuples.
    """
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
    """
    Fonction pour valider et corriger l'URL GitHub.
    Vérifie si l'URL est bien formée et ajoute '.git' à la fin si nécessaire.
    Si l'URL n'est pas valide, elle retourne None.
    """
    regex = r'^https:\/\/github\.com\/[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+(\.git)?$'
    if re.match(regex, url):
        return url if url.endswith(".git") else url + ".git"
    return None


def creer_dossier_si_absent(dossier: str) -> None:
    """
    Fonction pour créer un dossier s'il n'existe pas.
    Si le dossier n'existe pas, il sera créé pour accueillir les dépôts.
    """
    if not os.path.exists(dossier):
        os.makedirs(dossier)


def cloner_depot(apprenant: str, lien_github: str, dossier_apprenant: str) -> None:
    """
    Fonction pour cloner un dépôt GitHub.
    Utilise l'URL GitHub et le nom de l'apprenant pour cloner le dépôt dans un dossier dédié.
    """
    print(f"\nClonage du dépôt pour {apprenant} : {lien_github}")
    try:
        subprocess.run(["git", "clone", lien_github, dossier_apprenant], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du clonage pour {apprenant} : {e}")


def mettre_a_jour_depot(apprenant: str, dossier_apprenant: str) -> None:
    """
    Fonction pour mettre à jour un dépôt existant.
    Effectue un `git pull` pour récupérer les dernières modifications du dépôt.
    """
    print(f"\nMise à jour du dépôt pour {apprenant} (git pull)")
    subprocess.run(["git", "-C", dossier_apprenant, "pull"], check=True)


def committer_et_pousser_modifications(apprenant: str, dossier_apprenant: str, message: str) -> None:
    """
    Fonction pour effectuer un commit et un push dans un dépôt existant.
    Ajoute les changements, les commit avec un message, puis pousse les modifications vers le dépôt distant.
    """
    print(f"Ajout, commit et push pour {apprenant}")
    try:
        subprocess.run(["git", "-C", dossier_apprenant, "add", "."], check=True)
        subprocess.run(["git", "-C", dossier_apprenant, "commit", "-m", message], check=True)
        subprocess.run(["git", "-C", dossier_apprenant, "push"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du commit/push pour {apprenant} : {e}")


def gerer_depot(apprenants: List[Tuple[str, str]], dossier_cible: str, clone: bool = True, pull: bool = True, commit_push_message: Optional[str] = None) -> None:
    """
    Fonction principale pour gérer les dépôts des apprenants.
    Pour chaque apprenant, vérifie si le dépôt existe déjà. Si ce n'est pas le cas, il sera cloné.
    Si le dépôt existe, il peut être mis à jour avec un pull. Ensuite, si un message de commit est fourni, 
    les modifications seront ajoutées, committées et poussées.
    """
    creer_dossier_si_absent(dossier_cible)

    for apprenant, lien_github in apprenants:
        dossier_apprenant = os.path.join(dossier_cible, apprenant)

        # Validation et correction de l'URL
        lien_github = valider_et_corriger_url(lien_github)

        if lien_github:
            # Vérifier si le dossier existe et contient un dépôt Git
            if os.path.exists(dossier_apprenant) and os.path.exists(os.path.join(dossier_apprenant, ".git")):
                # Faire un pull si l'option -p est fournie ou si -cp est utilisé
                if pull:
                    mettre_a_jour_depot(apprenant, dossier_apprenant)

                # Faire un commit/push si un message est fourni
                if commit_push_message:
                    committer_et_pousser_modifications(apprenant, dossier_apprenant, commit_push_message)
            else:
                # Faire un clone si le dossier n'existe pas et que l'option -c est fournie
                if clone:
                    cloner_depot(apprenant, lien_github, dossier_apprenant)
        else:
            print(f"\nLien GitHub invalide pour {apprenant} : {lien_github}")


def gerer_dossiers(csv_file: str, clone: bool = True, pull: bool = True, commit_push_message: Optional[str] = None) -> None:
    """
    Fonction principale pour gérer les dossiers et les opérations Git.
    Cette fonction gère le processus complet en prenant un fichier CSV contenant les informations des apprenants,
    en créant les dossiers nécessaires et en exécutant les opérations Git correspondantes.
    """
    # Générer le nom du dossier cible à partir du nom du fichier CSV (sans .csv)
    dossier_cible = os.path.splitext(csv_file)[0]

    # Lecture du fichier CSV
    apprenants = lire_csv(csv_file)

    # Gérer les dépôts Git pour chaque apprenant
    gerer_depot(apprenants, dossier_cible, clone, pull, commit_push_message)


if __name__ == "__main__":
    # Utilisation d'argparse pour obtenir les paramètres de la ligne de commande
    parser = argparse.ArgumentParser(description="Gestion des dépôts Git des apprenants.")
    parser.add_argument("csv_file", help="Chemin vers le fichier CSV contenant les informations des apprenants.")
    parser.add_argument("-c", "--clone", action="store_true", help="Effectuer git clone pour les dépôts manquants")
    parser.add_argument("-p", "--pull", action="store_true", help="Effectuer git pull pour les dépôts existants")
    parser.add_argument("-cp", "--commit-push", type=str, help="Message de commit pour git add, git commit et git push")
    args = parser.parse_args()

    # Vérification de la compatibilité des options
    if args.clone and args.commit_push:
        print("Erreur : L'option --clone ne peut pas être utilisée avec --commit-push.")
        print("Utilisez uniquement --clone pour cloner les dépôts.")
    else:
        # Si l'option --commit-push est utilisée, activer l'option --pull par défaut
        if args.commit_push:
            args.pull = True

        # Si l'option --clone est passée, mettre `clone` à False, sinon garder True par défaut
        clone_option = not args.clone

        # Exécuter la fonction principale avec les options spécifiées
        gerer_dossiers(args.csv_file, clone=clone_option, pull=args.pull, commit_push_message=args.commit_push)
