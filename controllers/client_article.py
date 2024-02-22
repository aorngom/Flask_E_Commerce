#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint, request, render_template, flash, session
from connexion_db import get_db

client_article = Blueprint('client_article', __name__, template_folder='templates')

@client_article.route('/client/index')
@client_article.route('/client/article/show')
def client_article_show():
    mycursor = get_db().cursor()
    id_client = session.get('id_user')  # Utilisation de get() pour éviter les erreurs si la clé n'existe pas
    filter_word = session.get('filter_word')
    filter_prix_min = session.get('filter_prix_min')
    filter_prix_max = session.get('filter_prix_max')
    filter_types = session.get('filter_types')
    param = []

    sql = '''SELECT jean.id_jean AS id_article,
                    jean.image AS image,
                    jean.nom AS nom,
                    jean.prix AS prix,
                    SUM(declinaison_jean.stock) AS stock
            FROM jean
            INNER JOIN declinaison_jean ON jean.id_jean = declinaison_jean.id_jean
        '''
    if filter_word or filter_prix_min or filter_prix_max or filter_types:
        sql += " WHERE "
        if filter_word:  # Vérification de filter_word sans besoin de comparer à None
            session['filter_word'] = filter_word
            sql += 'jean.nom LIKE %s '
            param.append("%" + filter_word + "%")
        if filter_prix_min or filter_prix_max:
            if filter_prix_max:
                filter_prix_max = filter_prix_max.replace(',', '.')
            if filter_prix_min:
                filter_prix_min = filter_prix_min.replace(',', '.')
            try:
                if filter_prix_max:
                    float(filter_prix_max)
                if filter_prix_min:
                    float(filter_prix_min)
                if (filter_prix_min and float(filter_prix_min) < 0) or (filter_prix_max and float(filter_prix_max) < 0):
                    message = u"Le prix doit être positif"
                    flash(message, 'alert-warning')
                elif filter_prix_min and not filter_prix_max:
                    if param:  # Vérifie si param contient déjà des éléments
                        sql += ' AND '
                    session['filter_prix_min'] = filter_prix_min
                    sql += "jean.prix >= %s "
                    param.append(float(filter_prix_min))
                elif not filter_prix_min and filter_prix_max:
                    if param:
                        sql += ' AND '
                    session['filter_prix_max'] = filter_prix_max
                    sql += "jean.prix <= %s "
                    param.append(float(filter_prix_max))
                elif float(filter_prix_min) < float(filter_prix_max):
                    if param:
                        sql += ' AND '
                    session['filter_prix_min'] = filter_prix_min
                    session['filter_prix_max'] = filter_prix_max
                    sql += "(jean.prix >= %s AND jean.prix <= %s) "
                    param.append(float(filter_prix_min))
                    param.append(float(filter_prix_max))
                else:
                    message = u'min < max'
                    flash(message, 'alert-warning')
            except ValueError:
                message = u"Le prix doit être un nombre"
                flash(message, 'alert-warning')

        if filter_types:
            if param:
                sql += ' AND '
            sql += "coupe_jean.id_coupe_jean IN (%s)" % ','.join(['%s'] * len(filter_types))
            param.extend(filter_types)

    sql += " GROUP BY jean.id_jean ORDER BY jean.id_jean;"
    mycursor.execute(sql, param)
    articles = mycursor.fetchall()

    sql = '''SELECT jean.id_jean AS id_article, COUNT(declinaison_jean.id_declinaison) AS nb_declinaisons FROM jean 
            INNER JOIN declinaison_jean ON jean.id_jean = declinaison_jean.id_jean
            GROUP BY jean.id_jean
            ORDER BY jean.id_jean;
            '''
    mycursor.execute(sql)
    nb_declinaisons = mycursor.fetchall()

    sql = '''SELECT coupe_jean.id_coupe_jean AS id_type_article, coupe_jean.libelle AS libelle FROM coupe_jean;'''
    mycursor.execute(sql)
    types_article = mycursor.fetchall()

    sql = '''SELECT ligne_panier.quantite as quantite, jean.prix as prix, jean.nom as nom , couleur.libelle as couleur  , couleur.id_couleur , taille.libelle as taille , taille.id_taille ,declinaison_jean.stock as stock , declinaison_jean.id_declinaison as id_declinaison 
            FROM ligne_panier
            INNER JOIN declinaison_jean ON declinaison_jean.id_declinaison = ligne_panier.id_declinaison
            INNER JOIN jean ON declinaison_jean.id_jean = jean.id_jean
            INNER JOIN couleur ON declinaison_jean.id_couleur = couleur.id_couleur
            INNER JOIN taille ON declinaison_jean.id_taille = taille.id_taille
            WHERE ligne_panier.id_utilisateur = %s;
            '''
    mycursor.execute(sql, (id_client,))
    articles_panier = mycursor.fetchall()

    prix_total = sum(article['quantite'] * article['prix'] for article in articles_panier) if articles_panier else None

    return render_template('client/boutique/panier_article.html',
                           articles=articles,
                           articles_panier=articles_panier,
                           prix_total=prix_total,
                           items_filtre=types_article,
                           session=session,
                           declinaisons=nb_declinaisons)
