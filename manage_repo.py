import os
import subprocess
import argparse
import re
import csv


# Fonction pour lire le fichier CSV et extraire les liens GitHub et les noms des apprenants
def lire_csv(fichier):
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


# Fonction pour vérifier si l'URL GitHub est valide
def url_valide(url):
    regex = r'https:\/\/github\.com\/[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+(\.git)?'
    return re.match(regex, url)


# Fonction pour cloner ou faire un git pull selon que le dossier existe ou non
def cloner_ou_mettre_a_jour(apprenants, dossier_cible):
    # Vérifier si le dossier cible existe, sinon le créer
    if not os.path.exists(dossier_cible):
        os.makedirs(dossier_cible)
    
    for apprenant, lien_github in apprenants:
        apprenant_folder = os.path.join(dossier_cible, apprenant)
        
        if os.path.exists(apprenant_folder):
            if os.path.exists(os.path.join(apprenant_folder, ".git")):
                # Si le dossier existe et contient un dépôt Git, faire un git pull
                print(f"\nMise à jour du dépôt pour {apprenant} (git pull)")
                subprocess.run(["git", "-C", apprenant_folder, "pull"], check=True)
            else:
                print(f"Le dossier {apprenant} existe, mais ce n'est pas un dépôt Git. Ignoré.")
        else:
            # Si le dossier n'existe pas, vérifier l'URL et faire un git clone
            if url_valide(lien_github):
                print(f"\nClonage du dépôt pour {apprenant} : {lien_github}")
                try:
                    subprocess.run(["git", "clone", lien_github, apprenant_folder], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Erreur lors du clonage pour {apprenant} : {e}")
            else:
                print(f"\nLien GitHub invalide pour {apprenant} : {lien_github}")


# Fonction principale pour gérer les dépôts
def gerer_dossiers(csv_file):
    # Générer le nom du dossier cible à partir du nom du fichier CSV (sans .csv)
    dossier_cible = os.path.splitext(csv_file)[0]
    
    # Lecture du fichier CSV
    apprenants = lire_csv(csv_file)

    # Cloner ou mettre à jour les dépôts Git dans le dossier cible
    cloner_ou_mettre_a_jour(apprenants, dossier_cible)


if __name__ == "__main__":
    # Utilisation d'argparse pour obtenir les paramètres de la ligne de commande
    parser = argparse.ArgumentParser(description="Gestion des dépôts Git des apprenants.")
    parser.add_argument("csv_file", help="Chemin vers le fichier CSV contenant les informations des apprenants.")
    args = parser.parse_args()

    # Exécuter la fonction principale avec les paramètres
    gerer_dossiers(args.csv_file)
