# Gestion Automatisée des Dépôts GitHub pour Apprenants

Ce projet contient un script Python qui gère automatiquement les dépôts GitHub de plusieurs apprenants à partir d'un fichier CSV. Le script permet de cloner les dépôts s'ils n'existent pas et de les mettre à jour via `git pull` s'ils sont déjà clonés. Il permet aussi de commettre et de pousser les changements vers GitHub si un message de commit est fourni. Les dépôts sont clonés dans un dossier spécifique indiqué par l'utilisateur.

## Fonctionnalités

1. **Clonage des dépôts GitHub** : Si un dossier pour un apprenant n'existe pas dans le répertoire cible, le script clone le dépôt GitHub associé.
2. **Mise à jour des dépôts existants** : Si un dépôt est déjà cloné, le script effectue un `git pull` pour récupérer les dernières modifications.
3. **Commit et Push des changements** : Si un message de commit est fourni, le script ajoutera, commitera et poussera les modifications locales vers le dépôt distant.
4. **Vérification des liens GitHub** : Le script vérifie que les URL GitHub des apprenants sont valides avant de tenter de les cloner.
5. **Options par défaut** : Le clonage et la mise à jour (`git pull`) sont activés par défaut, mais peuvent être désactivés via des arguments de ligne de commande.

## Prérequis

### 1. Git

Le script utilise Git pour cloner et mettre à jour les dépôts. Assurez-vous que Git est installé sur votre machine.

- [Installer Git](https://git-scm.com/)

### 2. Fichier CSV

Le fichier CSV doit être placé dans le même répertoire que le script ou l'exécutable. Ce fichier contient un tableau des apprenants avec leurs noms et les liens vers leurs dépôts GitHub.

Exemple de contenu d'un fichier CSV (`template.csv`):

```csv
"Apprenant","LienGithub"
"Etudiant1","https://github.com/Etudiant1/TP_POO"
"Etudiant2","https://github.com/Etudiant2/TP_POO"
"Etudiant3","https://github.com/Etudiant3/TP_POO"
```

## Utilisation

1. Placez l'exécutable (`manage_repos.exe`) dans le même répertoire que le fichier CSV.
2. Ouvrez un terminal ou une invite de commande dans ce répertoire.
   - Sous Windows, vous pouvez faire un **Shift + Clic droit** dans le répertoire et choisir "Ouvrir une fenêtre PowerShell ici".
3. Lancez l'exécutable avec la commande suivante, en spécifiant le fichier CSV et le dossier cible :

   ```bash
   manage_repos.exe template.csv
   ```

Le script va :

- Cloner les dépôts qui n'existent pas dans le dossier cible spécifié.
- Faire un `git pull` pour mettre à jour les dépôts existants.

### Arguments supplémentaires

Le script accepte les options suivantes pour personnaliser son comportement :

- **`-c` ou `--clone`** : Désactive le clonage des dépôts. Par défaut, le clonage est activé. Si vous spécifiez cette option, les dépôts ne seront pas clonés, mais seulement mis à jour si déjà présents.
  
- **`-p` ou `--pull`** : Désactive l'opération de mise à jour des dépôts (`git pull`). Par défaut, cette option est activée et le script mettra à jour les dépôts clonés.
  
- **`-cp` ou `--commit-push`** : Permet d'ajouter un message de commit pour effectuer un `git add .`, `git commit` et `git push` dans les dépôts clonés ou mis à jour. Exemple d'utilisation :

   ```bash
   manage_repos.exe template.csv -cp "Message de commit"
   ```

### Remarque importante

Le script effectue des opérations Git (clone et pull) dans le dossier spécifié comme dossier cible. Assurez-vous que vous disposez des permissions nécessaires pour effectuer des opérations Git dans ce dossier.

## Exemple de sortie du script

Lors de l'exécution, le script affiche les actions effectuées dans le terminal, telles que :

- **Clonage d'un dépôt** :

   ```bash
   Clonage du dépôt pour Etudiant1 : https://github.com/etudiant1/PythonTP
   ```

- **Mise à jour d'un dépôt existant** :

   ```bash
   Mise à jour du dépôt pour Etudiant2 (git pull)
   ```

- **Erreur avec un lien GitHub invalide** :

   ```bash
   Lien GitHub invalide pour Etudiant3 : https://github.com/etudiant3/Python_POO_Project
   ```

- **Erreur avec un lien GitHub valide, mais repository inexistant** :

   ```bash
   remote: Repository not found.
   fatal: repository 'https://github.com/etudiant3/Python_POO_Project/' not found
   ```

## Création de l'exécutable Windows

Pour transformer ton fichier Python `manage_repo.py` en un exécutable avec **PyInstaller**, voici la commande de base que tu peux utiliser :

```bash
pyinstaller --onefile manage_repo.py
```

Quelques options courantes :

- `--onefile` : crée un fichier exécutable unique.
- `--name <nom_du_programme>` : donne un nom spécifique à l'exécutable.
