# Gestion Automatisée des Dépôts GitHub pour Apprenants

Ce projet contient un script Python unique `manage_repo.py`, combinant à la fois la logique de gestion des dépôts GitHub et une interface utilisateur graphique construite avec Tkinter. Le script permet de cloner les dépôts, de les mettre à jour et de commettre/pousser les changements vers GitHub si un message de commit est fourni.

## Fonctionnalités

1. **Clonage des dépôts GitHub** : Clonage automatique des dépôts si le dossier de l'apprenant n'existe pas.
2. **Mise à jour des dépôts existants** : Effectue un `git pull` pour synchroniser les dépôts existants.
3. **Commit et Push des modifications** : Effectue `git add .`, `git commit` et `git push` avec un message fourni.
4. **Vérification et correction des URL GitHub** : Valide et ajuste les URL des dépôts avant toute action. Ajoute le `.git` en fin de chaine s'il n'existe pas.
5. **Interface utilisateur (Tkinter)** : Interface intuitive pour sélectionner un fichier CSV et gérer les actions.
6. **Exécutable disponible** : Un fichier exécutable Windows `.exe` est déjà exporté et disponible sur le dépôt GitHub.

## Prérequis

### 1. Python et Git

- Assurez-vous que Python est installé sur votre machine : [Télécharger Python](https://www.python.org/downloads/).
- Assurez-vous que Git est installé : [Installer Git](https://git-scm.com/).

### 2. Fichier CSV

Le fichier CSV doit contenir les noms des apprenants et les liens vers leurs dépôts GitHub précisément dans cette ordre. Les colonnes sont nommées "Apprenant" et "Lien Github", mais leur nom importe peu. Par contre il faut obligatoirement une ligne d'en-tête, même vide.

Exemple (`template.csv`) :

```csv
"Apprenant","Lien Github"
"Etudiant 1","https://github.com/Etudiant1/Projet1"
"Etudiant 2","https://github.com/Etudiant2/Projet2.git"
"Etudiant 3","https://github.com/Etudiant3/Projet3"
```

## Utilisation

### Exécution de l'interface graphique

1. **Depuis l'exécutable** : Vous pouvez télécharger et utiliser l'exécutable Windows disponible dans le dépôt GitHub (`manage_repo.exe`). Placez le fichier CSV à l'emplacement que vous voulez clone les projets.
2. **Depuis le script Python** : Si vous préférez utiliser Python directement, lancez le script :

   ```bash
   python manage_repo.py
   ```

### Utilisation de l'interface

- **Sélectionner un fichier CSV** : Cliquez sur "Parcourir" pour choisir un fichier CSV contenant les données.
- **Choisir l'action** :
  - **Clone et Pull** : Clonage et mise à jour des dépôts.
  - **Commit et Push** : Nécessite un message de commit.
- **Message de commit** : Entrez un message si l'option "Commit et Push" est sélectionnée.
- **Exécuter** : Cliquez sur "Exécuter" pour lancer l'opération choisie.

## Exemple de sortie

Lors de l'exécution, les messages suivants peuvent s'afficher :

- **Clonage réussi** : `Clonage du dépôt pour Etudiant1 : https://github.com/Etudiant1/Projet1`
- **Mise à jour réussie** : `Mise à jour du dépôt pour Etudiant2 (git pull)`
- **Erreur de lien invalide** : `Lien GitHub invalide pour Etudiant3`

## Exécutable Windows

Un fichier `.exe` exporté avec **PyInstaller** est déjà disponible sur le dépôt GitHub pour simplifier l'utilisation sur Windows. Cela permet d'exécuter l'application sans nécessiter Python.

Pour créer un exécutable vous-même, utilisez la commande :

```bash
pyinstaller --onefile manage_repo.py
```

Quelques options courantes :

- `--onefile` : crée un fichier exécutable unique.
- `--name <nom_du_programme>` : donne un nom spécifique à l'exécutable.