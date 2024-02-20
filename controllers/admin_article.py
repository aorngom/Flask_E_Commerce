#! /usr/bin/python
# -*- coding:utf-8 -*-
import math
import os.path
from random import random

from flask import Blueprint
from flask import request, render_template, redirect, flash
#from werkzeug.utils import secure_filename

from connexion_db import get_db

admin_article = Blueprint('admin_article', __name__,
                          template_folder='templates')


@admin_article.route('/admin/article/show')
def show_article():
    mycursor = get_db().cursor()
    sql = '''SELECT * FROM jean;'''
    mycursor.execute(sql)
    articles = mycursor.fetchall()
    return render_template('admin/article/show_article.html', articles=articles)


@admin_article.route('/admin/article/add', methods=['GET'])
def add_article():
    mycursor = get_db().cursor()

    return render_template('admin/article/add_article.html'
                           #,types_article=type_article,
                           #,couleurs=colors
                           #,tailles=tailles
                            )


@admin_article.route('/admin/article/add', methods=['POST'])
def valid_add_article():
    mycursor = get_db().cursor()

    nom_jean = request.form.get('nom_jean', '')
    image = request.files.get('image', None)
    prix_jean = request.form.get('prix_jean', '')
    id_coupe_jean = request.form.get('id_coupe_jean', '')
    description = request.form.get('description', '')
    matiere = request.form.get('matiere', '')
    couleur = request.form.get('couleur', '')
    marque = request.form.get('marque', '')
    id_taille = request.form.get('id_taille', '')
    stock = request.form.get('stock', '')

    if image:
        filename = 'img_upload'+ str(int(2147483647 * random())) + '.png'
        image.save(os.path.join('static/images/', filename))
    else:
        print("erreur")
        filename=None

    sql = '''INSERT INTO jean (nom_jean, image, prix_jean, id_coupe_jean, description, matiere, couleur, marque, id_taille, stock) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

    tuple_add = (nom_jean, image, prix_jean, id_coupe_jean, description, matiere, couleur, marque, id_taille, stock)
    print(tuple_add)
    mycursor.execute(sql, tuple_add)
    get_db().commit()

    print(u'article ajouté , nom: ', nom_jean, ' - type_jean:', id_coupe_jean, ' - prix:', prix_jean,
          ' - description:', description, ' - image:', image)
    message = u'article ajouté , nom:' + nom_jean + '- type_jean:' + id_coupe_jean + ' - prix:' + prix_jean + ' - description:' + description + ' - image:' + str(
        image)
    flash(message, 'alert-success')
    return redirect('/admin/article/show')


@admin_article.route('/admin/article/delete', methods=['GET'])
def delete_article():
    id_jean=request.args.get('id_jean')
    mycursor = get_db().cursor()
    sql = ''' SELECT COUNT(*) AS nb_declinaison FROM declinaison_jean WHERE id_jean = %s; '''
    mycursor.execute(sql, (id_jean,))
    nb_declinaison = mycursor.fetchone()
    if nb_declinaison['nb_declinaison'] > 0:
        message= u'il y a des declinaisons dans cet article : vous ne pouvez pas le supprimer'
        flash(message, 'alert-warning')
    else:
        sql = ''' SELECT image FROM jean WHERE id_jean = %s; '''
        mycursor.execute(sql, (id_jean,))
        article = mycursor.fetchone()
        print(article)
        image = article['image']

        sql = ''' DELETE FROM jean WHERE id_jean = %s; '''
        mycursor.execute(sql, (id_jean,))
        get_db().commit()
        if image != None:
            os.remove('static/images/' + image)

        print("un article supprimé, id :", id_jean)
        message = u'un article supprimé, id : ' + id_jean
        flash(message, 'alert-success')

    return redirect('/admin/article/show')


@admin_article.route('/admin/article/edit', methods=['GET'])
def edit_article():
    id_jean=request.args.get('id_jean')
    mycursor = get_db().cursor()
    sql = "SELECT id_jean, matiere, couleur, description, marque, nom_jean, prix_jean, id_coupe_jean, id_taille, image, stock FROM jean WHERE id_jean = %s;"
    mycursor.execute(sql, (id_jean,))
    article = mycursor.fetchone()
    print(article)
    sql = "SELECT id_coupe_jean, nom_coupe FROM coupe_jean;"
    mycursor.execute(sql)
    types_article = mycursor.fetchall()

    # sql = '''
    # requête admin_article_6
    # '''
    # mycursor.execute(sql, id_article)
    # declinaisons_article = mycursor.fetchall()

    return render_template('admin/article/edit_article.html'
                           ,article=article
                           ,types_article=types_article
                         #  ,declinaisons_article=declinaisons_article
                           )


@admin_article.route('/admin/article/edit', methods=['POST'])
def valid_edit_article():
    mycursor = get_db().cursor()
    nom = request.form.get('nom')
    id_article = request.form.get('id_article')
    image = request.files.get('image', '')
    type_article_id = request.form.get('type_article_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description')
    sql = "SELECT image FROM jean WHERE id_jean = %s;"

    mycursor.execute(sql, id_article)
    image_nom = mycursor.fetchone()
    image_nom = image_nom['image']
    if image:
        if image_nom != "" and image_nom is not None and os.path.exists(
                os.path.join(os.getcwd() + "/static/images/", image_nom)):
            os.remove(os.path.join(os.getcwd() + "/static/images/", image_nom))
        # filename = secure_filename(image.filename)
        if image:
            filename = 'img_upload_' + str(int(2147483647 * random())) + '.png'
            image.save(os.path.join('static/images/', filename))
            image_nom = filename

    sql = '''UPDATE jean SET nom_jean = %s, image = %s, prix_jean = %s, id_coupe_jean = %s, description = %s WHERE id_jean = %s; '''
    mycursor.execute(sql, (nom, image_nom, prix, type_article_id, description, id_article))

    get_db().commit()
    if image_nom is None:
        image_nom = ''
    message = u'article modifié , nom:' + nom + '- type_article :' + type_article_id + ' - prix:' + prix  + ' - image:' + image_nom + ' - description: ' + description
    flash(message, 'alert-success')
    return redirect('/admin/article/show')







@admin_article.route('/admin/article/avis/<int:id>', methods=['GET'])
def admin_avis(id):
    mycursor = get_db().cursor()
    article=[]
    commentaires = {}
    return render_template('admin/article/show_avis.html'
                           , article=article
                           , commentaires=commentaires
                           )


@admin_article.route('/admin/comment/delete', methods=['POST'])
def admin_avis_delete():
    mycursor = get_db().cursor()
    article_id = request.form.get('idArticle', None)
    userId = request.form.get('idUser', None)

    return admin_avis(article_id)
