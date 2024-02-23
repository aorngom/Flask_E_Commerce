#! /usr/bin/python
# -*- coding:utf-8 -*-
import datetime
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__, template_folder='templates')

@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_jean = request.form.get('id_jean', None)
    quantite = request.form.get('quantite', None)
    if id_jean is not None and quantite is not None:
        # Vérifier si la quantité est valide
        if quantite.isdigit() and int(quantite) > 0:
            # Vérifier si l'article est déjà dans le panier
            sql = '''SELECT * FROM ligne_panier WHERE id_jean = %s AND id_utilisateur = %s'''
            mycursor.execute(sql, (id_jean, id_client))
            panier_exist = mycursor.fetchone()
            if panier_exist:
                # Mise à jour de la quantité dans le panier
                new_quantity = panier_exist['quantite'] + int(quantite)
                sql = '''UPDATE ligne_panier SET quantite = %s WHERE id_jean = %s AND id_utilisateur = %s'''
                mycursor.execute(sql, (new_quantity, id_jean, id_client))
            else:
                # Ajout d'un nouvel article dans le panier
                sql = '''INSERT INTO ligne_panier (id_jean, id_utilisateur, quantite, date_ajout) VALUES (%s, %s, %s, %s)'''
                date_ajout = datetime.datetime.now().strftime('%Y-%m-%d')
                mycursor.execute(sql, (id_jean, id_client, quantite, date_ajout))
            get_db().commit()
        else:
            flash('Quantité invalide', 'error')
    else:
        flash('Données manquantes pour ajouter au panier', 'error')

    return redirect('/client/article/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_jean = request.form.get('id_jean', None)
    if id_jean is not None:
        sql = '''DELETE FROM ligne_panier WHERE id_jean = %s AND id_utilisateur = %s'''
        mycursor.execute(sql, (id_jean, id_client))
        get_db().commit()
    else:
        flash('Données manquantes pour supprimer du panier', 'error')

    return redirect('/client/article/show')

@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    # Vider le panier
    sql = '''DELETE FROM ligne_panier WHERE id_utilisateur = %s'''
    mycursor.execute(sql, (id_client,))
    get_db().commit()
    flash('Votre panier est vide', 'info')

    return redirect('/client/article/show')

# Les routes pour filtrer et supprimer le filtre restent inchangées
# car elles ne dépendent pas directement de la structure de la table des articles ou du panier.
