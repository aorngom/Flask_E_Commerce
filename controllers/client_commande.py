# Importation des modules nécessaires
from flask import Blueprint, request, render_template, redirect, flash, session
from connexion_db import get_db

# Création du blueprint pour les commandes client
client_commande = Blueprint('client_commande', __name__, template_folder='templates')

# Vue pour valider la commande
@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    # Récupération de la connexion à la base de données
    mycursor = get_db().cursor()

    # Récupération de l'identifiant du client depuis la session
    id_client = session['id_user']

    # Sélection des articles du panier
    sql = "SELECT * FROM panier WHERE id_client = %s"
    mycursor.execute(sql, (id_client,))
    articles_panier = mycursor.fetchall()

    # Calcul du prix total du panier
    prix_total = 0
    for article in articles_panier:
        prix_total += article['prix']

    # Renvoi du template avec les données nécessaires
    return render_template('client/boutique/panier_validation_adresses.html',
                           articles_panier=articles_panier,
                           prix_total=prix_total,
                           validation=1)

# Vue pour ajouter une commande
@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    # Récupération de la connexion à la base de données
    mycursor = get_db().cursor()

    # Récupération de l'identifiant du client depuis la session
    id_client = session['id_user']

    # Sélection du contenu du panier de l'utilisateur
    sql = "SELECT * FROM panier WHERE id_client = %s"
    mycursor.execute(sql, (id_client,))
    items_ligne_panier = mycursor.fetchall()

    # Création de la commande
    sql = "INSERT INTO commande (id_client) VALUES (%s)"
    mycursor.execute(sql, (id_client,))
    id_commande = mycursor.lastrowid

    # Ajout des lignes de commande
    for item in items_ligne_panier:
        sql = "INSERT INTO ligne_commande (id_commande, id_article, quantite) VALUES (%s, %s, %s)"
        mycursor.execute(sql, (id_commande, item['id_article'], item['quantite']))

    # Suppression des articles du panier
    sql = "DELETE FROM panier WHERE id_client = %s"
    mycursor.execute(sql, (id_client,))

    # Validation de la transaction
    get_db().commit()

    # Message de succès
    flash(u'Commande ajoutée', 'alert-success')

    # Redirection vers la page des articles
    return redirect('/client/article/show')

# Vue pour afficher les commandes du client
@client_commande.route('/client/commande/show', methods=['GET', 'POST'])
def client_commande_show():
    # Récupération de la connexion à la base de données
    mycursor = get_db().cursor()

    # Récupération de l'identifiant du client depuis la session
    id_client = session['id_user']

    # Sélection des commandes du client
    sql = "SELECT * FROM commande WHERE id_utilisateur = %s ORDER BY etat, date_achat DESC"
    mycursor.execute(sql, (id_client,))
    commandes = mycursor.fetchall()

    # Renvoi du template avec les données nécessaires
    return render_template('client/commandes/show.html',
                           commandes=commandes)
