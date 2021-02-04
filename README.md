## Extraire les livrables du github sur votre poste de travail :
	`git clone https://github.com/Bruno-M44/book-scrapping.git`

## Se positionner dans le répertoire
	` cd book-scrapping/` 

## Créer l'environnement virtuel :
	`virtualenv -p python3 env`

## Activer l'environnement virtuel :
	`source env/bin/activate` (sous Windows : `C:\\{venv}\\Scripts\\activate.bat`)

## Installer les dépendances :	
	`pip install -r requirements.txt`

## Lancer le programme : 
	`python main.py`

Un nouveau dossier `Results` est apparu qui contient toutes les données scrappés par catégorie ainsi que les images de chaque livre.