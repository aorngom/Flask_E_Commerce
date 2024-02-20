# -*- coding:utf-8 -*-
from flask import Blueprint, request, render_template, redirect, abort, session
from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__, template_folder='templates')

@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_jean = request.form.get('id_jean')
    quantite = request.form.get('quantite')

    # Ajout dans le panier d'un article
    sql = '''INSERT INTO ligne_panier (id_jean, id_utilisateur, quantite, date_ajout) VALUES (%s, %s, %s, NOW())'''
    mycursor.execute(sql, (id_jean, id_client, quantite))

    return redirect('/client/article/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_jean = request.form.get('id_jean','')
    quantite = 1

    # Suppression d'une ligne de panier
    sql = '''DELETE FROM ligne_panier WHERE id_jean = %s AND id_utilisateur = %s'''
    mycursor.execute(sql, (id_jean, id_client))

    # Mise à jour du stock de l'article après suppression
    sql = '''UPDATE jean SET stock = stock + %s WHERE id_jean = %s'''
    mycursor.execute(sql, (quantite, id_jean))

    return redirect('/client/article/show')

@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']

    # Suppression de toutes les lignes de panier d'un utilisateur
    sql = '''DELETE FROM ligne_panier WHERE id_utilisateur = %s'''
    mycursor.execute(sql, (client_id,))

    # Mise à jour du stock de tous les articles supprimés
    sql = '''UPDATE jean SET stock = stock + quantite WHERE id_jean IN (SELECT id_jean FROM ligne_panier WHERE id_utilisateur = %s)'''
    mycursor.execute(sql, (client_id,))

    return redirect('/client/article/show')

@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_jean = request.form.get('id_jean')

    # Suppression d'une ligne de panier spécifique
    sql = '''DELETE FROM ligne_panier WHERE id_jean = %s AND id_utilisateur = %s'''
    mycursor.execute(sql, (id_jean, id_client))

    # Mise à jour du stock de l'article après suppression
    sql = '''UPDATE jean SET stock = stock + quantite WHERE id_jean = %s'''
    mycursor.execute(sql, (id_jean,))

    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)

    # Mise en session des filtres
    session['filter_word'] = filter_word
    session['filter_prix_min'] = filter_prix_min
    session['filter_prix_max'] = filter_prix_max
    session['filter_types'] = filter_types

    # Redirection vers la page de visualisation du panier
    return redirect('/client/panier/show')

@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    # suppression  des variables en session
    print("suppr filtre")
    return redirect('/client/article/show')
