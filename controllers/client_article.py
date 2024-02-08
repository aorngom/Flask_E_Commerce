# Importez ces fonctions pour utiliser la méthode generate_password_hash
from flask import Blueprint, render_template, session
from connexion_db import get_db

client_article = Blueprint('client_article', __name__, template_folder='templates')


@client_article.route('/client/index')
@client_article.route('/client/article/show')
def client_article_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    # Sélection des articles (jeans)
    sql = '''
    SELECT jean.id_jean, jean.matiere, jean.couleur, jean.description, jean.marque, jean.nom_jean, jean.prix_jean,
           coupe_jean.nom_coupe, taille.nom_taille,jean.image
    FROM jean
    JOIN coupe_jean ON jean.id_coupe_jean = coupe_jean.id_coupe_jean
    JOIN taille ON jean.id_taille = taille.id_taille
    '''
    mycursor.execute(sql)
    jeans = mycursor.fetchall()

    # Pour le filtre
    sql_filtre = '''SELECT DISTINCT nom_coupe FROM coupe_jean'''
    mycursor.execute(sql_filtre)
    coupe_jean = mycursor.fetchall()

    articles_panier = []

    if len(articles_panier) >= 1:
        # Calcul du prix total du panier
        sql_prix_total = ''' Calcul du prix total du panier '''
        mycursor.execute(sql_prix_total)
        prix_total = mycursor.fetchone()['prix_total']
    else:
        prix_total = None

    return render_template('client/boutique/panier_article.html',
                           jeans = jeans,
                           articles_panier=articles_panier,
                           prix_total=prix_total,
                           items_filtre=coupe_jean)
