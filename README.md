# Projet MOOREV : Annotation et Analyse d'Images et Vidéos des Espèces Sous-marines

## 🎯 L'objectif du projet 
1. **Annotation des Images et Vidéos :** Les méthodes d'annotation d'images en déploiant l'outil [VIAME](https://github.com/VIAME/VIAME?tab=readme-ov-file) qui offre l'annotation d'images et de vidéos pour l'annotation par divers utilisateurs, tels que des chercheurs, des étudiants, des enseignants et des animateurs pédagogiques, ainsi que des bénévoles. La platforme web est accessible depuis [viame.kitware.com](https://viame.kitware.com/#/)

2. **Reconnaissance des Espèces par Machine Learning :** La reconnaissance des espèces cibles en utilisant des techniques d'IA en entraînant des modèles pour la reconnaissance, segmentation et tracking avec [Ultralytics](https://www.ultralytics.com/fr/) [YOLOv8](https://github.com/ultralytics/ultralytics).

3. **Quantification de Caractères Morphologiques et Comportementaux :** Investigation de la quantification de caractères morphologiques d'individus (taille, forme et couleur) et de leur comportement, à partir des outils de la bibliothèque [OpenCV](https://opencv.org/) en Python.

4. **Accès aux Outils :** Tous les outils sont accessibles sur le portail [Galaxy Europe](https://usegalaxy.eu/) afin de rendre ces méthodes d'annotation et d'analyse d'images accessibles à des utilisateurs en ligne.

## Utilisation de l'Interface Web

L'interface web fournit aux utilisateurs un moyen convivial d'annoter des images, de partager des données, de visualiser des résultats et d'analyser des données en écologie. Cela ouvre de nouvelles perspectives pour la participation citoyenne (citizen sciences) dans le domaine de l'écologie.

## Structure du Projet

- **`/code` :** Contient le code source de l'interface utilisateur et des scripts pour l'annotation et l'analyse d'images.
- **`/data` :** Emplacement des données d'images et de labels utilisées pour l'entraînement et les tests.
- **`/docs` :** Documentation détaillée du projet, des méthodologies et des guides d'utilisation.
- **`/results` :** Stockage des résultats obtenus à partir des analyses et expérimentations.

## Comment Contribuer

1. Clonez le dépôt localement : `git clone https://github.com/votre-utilisateur/nom-du-repo.git`
2. Créez votre branche de fonctionnalité : `git checkout -b nom-de-votre-fonctionnalité`
3. Effectuez vos modifications et commit : `git commit -m "Ajout de la fonctionnalité X"`
4. Poussez vos modifications vers la branche : `git push origin nom-de-votre-fonctionnalité`
5. Créez une Pull Request pour discuter des modifications apportées.

Nous encourageons toute contribution, qu'il s'agisse de rapports de bugs, de nouvelles fonctionnalités ou d'améliorations de la documentation.

---

N'oubliez pas de personnaliser ce modèle en fonction des spécificités de votre projet. Cette structure offre une vue d'ensemble claire de l'objectif du projet, des fonctionnalités, de l'utilisation de l'interface web, de la structure du projet et des instructions pour contribuer.

# *GBIF :*
https://www.gbif.org/fr/

# *DORIS :*
https://doris.ffessm.fr/

# *BERNIC&CLIC :*
https://bernic.bzh/application/

# *VIAME :*
https://viame.kitware.com/#/

# Projet Gestion De Bases De Donnees
## 📁 *Dataset* : 
  (No need to download it, it is already in the project)
  Bases de donnees annuelles des accidents corporels de la circulation routiere annees de 2005 a 2022
  https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2022/
  
## 🤝 *Autors* :
Alhussein JAMIL
Lynda FEDDAK

## 🎯 *Project Structure*:
- *config* : contains the config files
- *data* : contains the data files
- *schemas* : contains the generated schemas of the database, this includes the MCD(Modele Conceptuel de Donnees) and the MLD(Modele Logique de Donnees). 
- *src* : contains the source code of the project


## ⚙️ *Requirements*:
- python >= 3.10.11
install python : https://www.python.org/downloads/

## ⬇️ *Installation*:
- create a virtual environment using venv, pyenv or conda
- install requirements.txt
```bash
pip install --upgrade -r requirements.txt
```

## ⌛ *Prepare Database*:
We use mysql database, we provide the .sql script to create the database and tables.
- create a database named "accidentsroutiers": 
```bash
mysql -u root -p
CREATE DATABASE accidentsroutiers;
```
- create tables and populate them:
```bash
mysql -u root -p accidentsroutiers < accidentsroutiers.sql
```
- create a user named "some_user_name" with password "some_password" and grant him all privileges on the database "accidentsroutiers".
- change the config file config/user_config.yaml with the user name and password you created.

## 🚀 *Run*:
```bash
python main.py 
```
you can use the following arguments:
  - -p : to show the plots only 
  - -a : to not run the application
