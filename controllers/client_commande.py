# validation de la commande : partie 2 -- vue pour choisir les adresses (livraison et facturation)
#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')
@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_utilisateur = session['id_user']

    # Sélection des articles du panier de l'utilisateur
    sql_panier = "SELECT dj.id_declinaison, j.nom, dj.prix_declinaison, lp.quantite, (dj.prix_declinaison * lp.quantite) AS sous_total FROM ligne_panier lp JOIN declinaison_jean dj ON lp.id_declinaison = dj.id_declinaison JOIN jean j ON dj.id_jean = j.id_jean WHERE lp.id_utilisateur = %s;"
    mycursor.execute(sql_panier, (id_utilisateur,))
    articles_panier = mycursor.fetchall()

    # Calcul du prix total du panier si le panier n'est pas vide
    prix_total = None
    if articles_panier:
        prix_total = sum(article['sous_total'] for article in articles_panier)

    # Sélection des adresses de l'utilisateur
    sql_adresses = "SELECT * FROM adresse WHERE id_utilisateur = %s;"
    mycursor.execute(sql_adresses, (id_utilisateur,))
    adresses = mycursor.fetchall()

    return render_template('client/boutique/panier_validation_adresses.html', adresses=adresses,
                           articles_panier=articles_panier, prix_total=prix_total, validation=1)


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()

    id_utilisateur = session['id_user']

    # Insérer la nouvelle commande dans la table commande
    sql_commande = "INSERT INTO commande (date_achat, id_adresse_livraison, id_adresse_facturation, id_utilisateur, id_etat) VALUES (NOW(), %s, %s, %s, 1)"
    mycursor.execute(sql_commande,
                     (request.form['adresse_livraison'], request.form['adresse_facturation'], id_utilisateur))
    id_commande = mycursor.lastrowid

    # Sélectionner les articles du panier de l'utilisateur
    sql_panier = "SELECT * FROM ligne_panier WHERE id_utilisateur = %s;"
    mycursor.execute(sql_panier, (id_utilisateur,))
    items_ligne_panier = mycursor.fetchall()

    # Insérer les articles de la commande dans la table ligne_commande
    for item in items_ligne_panier:
        sql_insert_ligne_commande = "INSERT INTO ligne_commande (id_declinaison, id_commande, quantite, prix) VALUES (%s, %s, %s, %s)"
        mycursor.execute(sql_insert_ligne_commande,
                         (item['id_declinaison'], id_commande, item['quantite'], item['prix']))

    # Supprimer les articles du panier de l'utilisateur
    sql_supprimer_panier = "DELETE FROM ligne_panier WHERE id_utilisateur = %s"
    mycursor.execute(sql_supprimer_panier, (id_utilisateur,))

    # Valider la transaction
    get_db().commit()

    flash(u'Commande ajoutée', 'alert-success')
    return redirect('/client/article/show')


@client_commande.route('/client/commande/show', methods=['GET', 'POST'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_utilisateur = session['id_user']

    # Sélectionner toutes les commandes de l'utilisateur
    sql_commandes = "SELECT * FROM commande WHERE id_utilisateur = %s ORDER BY id_etat, date_achat DESC"
    mycursor.execute(sql_commandes, (id_utilisateur,))
    commandes = mycursor.fetchall()

    articles_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    if id_commande is not None:
        # Sélectionner les articles de la commande spécifiée
        sql_articles_commande = "SELECT dj.id_declinaison, j.nom, dj.prix_declinaison, lc.quantite, (dj.prix_declinaison * lc.quantite) AS sous_total FROM ligne_commande lc JOIN declinaison_jean dj ON lc.id_declinaison = dj.id_declinaison JOIN jean j ON dj.id_jean = j.id_jean WHERE lc.id_commande = %s"
        mycursor.execute(sql_articles_commande, (id_commande,))
        articles_commande = mycursor.fetchall()

        # Sélectionner les adresses de livraison et de facturation de la commande spécifiée
        sql_commande_adresses = "SELECT * FROM commande WHERE id_commande = %s"
        mycursor.execute(sql_commande_adresses, (id_commande,))
        commande_adresses = mycursor.fetchone()

    return render_template('client/commandes/show.html', commandes=commandes,
                           articles_commande=articles_commande, commande_adresses=commande_adresses)
