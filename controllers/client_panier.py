#! /usr/bin/python
# -*- coding:utf-8 -*-
import datetime
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')
@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_declinaison = request.form.get('id_declinaison', None)
    quantite = request.form.get('quantite', None)
    if id_declinaison is not None and quantite is not None:
        # Vérifier si la quantité est valide
        if quantite.isdigit() and int(quantite) > 0:
            sql = '''SELECT stock FROM declinaison_jean WHERE id_declinaison = %s'''
            mycursor.execute(sql, (id_declinaison,))
            result = mycursor.fetchone()
            if result and result['stock'] >= int(quantite):
                # Vérifier si l'article est déjà dans le panier
                sql = '''SELECT * FROM ligne_panier WHERE id_declinaison = %s AND id_utilisateur = %s'''
                mycursor.execute(sql, (id_declinaison, id_client))
                panier_exist = mycursor.fetchone()
                if panier_exist:
                    # Mise à jour de la quantité dans le panier
                    new_quantity = panier_exist['quantite'] + int(quantite)
                    sql = '''UPDATE ligne_panier SET quantite = %s WHERE id_declinaison = %s AND id_utilisateur = %s'''
                    mycursor.execute(sql, (new_quantity, id_declinaison, id_client))
                else:
                    # Ajout d'un nouvel article dans le panier
                    sql = '''INSERT INTO ligne_panier (id_declinaison, id_utilisateur, quantite, date_ajout) VALUES (%s, %s, %s, %s)'''
                    date_ajout = datetime.datetime.now().strftime('%Y-%m-%d')
                    mycursor.execute(sql, (id_declinaison, id_client, quantite, date_ajout))
                # Mettre à jour le stock de l'article
                sql = '''UPDATE declinaison_jean SET stock = stock - %s WHERE id_declinaison = %s'''
                mycursor.execute(sql, (quantite, id_declinaison))
                get_db().commit()
            else:
                flash('Stock insuffisant pour cet article', 'error')
        else:
            flash('Quantité invalide', 'error')
    else:
        flash('Données manquantes pour ajouter au panier', 'error')

    return redirect('/client/article/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_declinaison = request.form.get('id_declinaison', None)
    quantite = request.form.get('quantite', 1)
    if id_declinaison is not None:
        # Récupérer la quantité actuelle dans le panier
        sql = '''SELECT quantite FROM ligne_panier WHERE id_declinaison = %s AND id_utilisateur = %s'''
        mycursor.execute(sql, (id_declinaison, id_client))
        panier_item = mycursor.fetchone()
        if panier_item:
            # Supprimer l'article du panier ou mettre à jour la quantité
            if panier_item['quantite'] > 1:
                sql = '''UPDATE ligne_panier SET quantite = quantite - %s WHERE id_declinaison = %s AND id_utilisateur = %s'''
                mycursor.execute(sql, (quantite, id_declinaison, id_client))
            else:
                sql = '''DELETE FROM ligne_panier WHERE id_declinaison = %s AND id_utilisateur = %s'''
                mycursor.execute(sql, (id_declinaison, id_client))
            # Mettre à jour le stock de l'article
            sql = '''UPDATE declinaison_jean SET stock = stock + %s WHERE id_declinaison = %s'''
            mycursor.execute(sql, (quantite, id_declinaison))
            get_db().commit()
        else:
            flash('Cet article n\'est pas dans votre panier', 'error')
    else:
        flash('Données manquantes pour supprimer du panier', 'error')

    return redirect('/client/article/show')

@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''SELECT id_declinaison, quantite FROM ligne_panier WHERE id_utilisateur = %s'''
    mycursor.execute(sql, (id_client,))
    items_panier = mycursor.fetchall()
    if items_panier:
        for item in items_panier:
            # Restituer le stock pour chaque article dans le panier
            sql = '''UPDATE declinaison_jean SET stock = stock + %s WHERE id_declinaison = %s'''
            mycursor.execute(sql, (item['quantite'], item['id_declinaison']))
        # Vider le panier
        sql = '''DELETE FROM ligne_panier WHERE id_utilisateur = %s'''
        mycursor.execute(sql, (id_client,))
        get_db().commit()
    else:
        flash('Votre panier est déjà vide', 'info')

    return redirect('/client/article/show')

@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_declinaison = request.form.get('id_declinaison')
    if id_declinaison:
        # Récupérer la quantité actuelle dans le panier
        sql = '''SELECT quantite FROM ligne_panier WHERE id_declinaison = %s AND id_utilisateur = %s'''
        mycursor.execute(sql, (id_declinaison, id_client))
        panier_item = mycursor.fetchone()
        if panier_item:
            # Supprimer l'article du panier
            sql = '''DELETE FROM ligne_panier WHERE id_declinaison = %s AND id_utilisateur = %s'''
            mycursor.execute(sql, (id_declinaison, id_client))
            # Mettre à jour le stock de l'article
            sql = '''UPDATE declinaison_jean SET stock = stock + %s WHERE id_declinaison = %s'''
            mycursor.execute(sql, (panier_item['quantite'], id_declinaison))
            get_db().commit()
        else:
            flash('Cet article n\'est pas dans votre panier', 'error')
    else:
        flash('Données manquantes pour supprimer du panier', 'error')

    return redirect('/client/article/show')
@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)

    if filter_word:
        session['filter_word'] = filter_word
    else:
        session.pop('filter_word', None)
    if filter_prix_min:
        session['filter_prix_min'] = filter_prix_min
    else:
        session.pop('filter_prix_min', None)
    if filter_prix_max:
        session['filter_prix_max'] = filter_prix_max
    else:
        session.pop('filter_prix_max', None)
    if filter_types:
        session['filter_types'] = filter_types
    else:
        session.pop('filter_types', None)

    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    if 'filter_word' in session:
        session.pop('filter_word', None)
    if 'filter_prix_min' in session:
        session.pop('filter_prix_min', None)
    if 'filter_prix_max' in session:
        session.pop('filter_prix_max', None)
    if 'filter_types' in session:
        session.pop('filter_types', None)
    return redirect('/client/article/show')
