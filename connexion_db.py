import pymysql.cursors
import os
from dotenv import load_dotenv
from flask import g

# Chemin d'accès au dossier du projet
project_folder = os.path.expanduser('~/Clone_GitHub/Flask_E_Commerce')

# Charger les variables d'environnement à partir du fichier .env dans le dossier du projet
dotenv_path = os.path.join(project_folder, '.env')
load_dotenv(dotenv_path)


def get_db():
    try:
        if 'db' not in g:
            g.db = pymysql.connect(
                host=os.getenv("HOST"),
                user=os.getenv("LOGIN"),
                password=os.getenv("PASSWORD"),
                database=os.getenv("DATABASE"),
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
    except Exception as e:
        print("Erreur lors du chargement du fichier .env:", e)
        return None
    return g.db
