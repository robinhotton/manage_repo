# Gestion Automatisée des Dépôts GitHub pour Apprenants

Ce projet contient un script Python converti en exécutable, qui gère automatiquement les dépôts GitHub de plusieurs apprenants à partir d'un fichier Markdown. Le script permet de cloner les dépôts s'ils n'existent pas et de les mettre à jour via `git pull` s'ils sont déjà clonés. Les dépôts sont clonés dans un dossier spécifique indiqué par l'utilisateur.

## Fonctionnalités

1. **Clonage des dépôts GitHub** : Si un dossier pour un apprenant n'existe pas dans le répertoire cible, le script clone le dépôt GitHub associé.
2. **Mise à jour des dépôts existants** : Si un dépôt est déjà cloné, le script effectue un `git pull` pour récupérer les dernières modifications.
3. **Vérification des liens GitHub** : Le script vérifie que les URL GitHub des apprenants sont valides avant de tenter de les cloner.

## Prérequis

### 1. Git

Le script utilise Git pour cloner et mettre à jour les dépôts. Assurez-vous que Git est installé sur votre machine.

- [Installer Git](https://git-scm.com/)

### 2. Fichier Markdown

Le fichier markdown doit être placé dans le même répertoire que le script ou l'exécutable. Ce fichier contient un tableau des apprenants avec leurs noms et les liens vers leurs dépôts GitHub.

Exemple :

```python
"Apprenant","LienGithub"
"Etudiant1","https://github.com/Etudiant1/TP_POO"
"Etudiant2","https://github.com/Etudiant2/TP_POO"
"Etudiant3","https://github.com/Etudiant3/TP_POO"
```

## Utilisation

1. Placez l'exécutable (`manage_repos.exe`) dans le même répertoire que le fichier markdown.
2. Ouvrez un terminal ou une invite de commande dans ce répertoire.
   - Sous Windows, vous pouvez faire un **Shift + Clic droit** dans le répertoire et choisir "Ouvrir une fenêtre PowerShell ici".
3. Lancez l'exécutable avec la commande suivante, en spécifiant le fichier Markdown et le dossier cible :

   ```bash
   manage_repos.exe template.csv
   ```

Le script va :

- Cloner les dépôts qui n'existent pas dans le dossier cible spécifié.
- Faire un `git pull` pour mettre à jour les dépôts existants.

### Remarque importante

Le script effectue des opérations Git (clone et pull) dans le dossier spécifié comme dossier cible. Assurez-vous que vous disposez des permissions nécessaires pour effectuer des opérations Git dans ce dossier.

## Exemple de sortie du script

Lors de l'exécution, le script affiche les actions effectuées dans le terminal, telles que :

- **Clonage d'un dépôt** :

   ```bash
   Clonage du dépôt pour ETUDIANT1 : https://github.com/etudiant1/PythonTP
   ```

- **Mise à jour d'un dépôt existant** :

   ```bash
   Mise à jour du dépôt pour ETUDIANT2 (git pull)
   ```

- **Erreur avec un lien GitHub invalide** :

   ```bash
   Lien GitHub invalide pour ETUDIANT3 : https://github.com/etudiant3/Python_POO_Project
   ```

- **Erreur avec un lien github valide, mais repository inexistant**

   ```bash
   remote: Repository not found.
   fatal: repository 'https://github.com/etudiant3/Python_POO_Project/' not found
   ```

## Création de l'exécutable windows

Pour transformer ton fichier Python `manage_repo.py` en un exécutable avec **PyInstaller**, voici la commande de base que tu peux utiliser :

```bash
pyinstaller --onefile manage_repo.py
```

Quelques options courantes :

- `--onefile` : crée un fichier exécutable unique.
- `--name <nom_du_programme>` : donne un nom spécifique à l'exécutable.
