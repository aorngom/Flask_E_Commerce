#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from connexion_db import get_db

auth_security = Blueprint('auth_security', __name__,
                        template_folder='templates')

@auth_security.route('/login')
def auth_login():
    return render_template('auth/login.html')


@auth_security.route('/login', methods=['POST'])
def auth_login_post():
    mycursor = get_db().cursor()
    login = request.form.get('login')
    password = request.form.get('password')

    # Requête pour récupérer l'utilisateur basé sur le login
    sql = "SELECT * FROM utilisateur WHERE login = %s"
    mycursor.execute(sql, (login,))
    user = mycursor.fetchone()

    if user:
        # Vérification du mot de passe
        if check_password_hash(user['password'], password):
            # Authentification réussie
            session['login'] = user['login']
            session['role'] = user['role']
            session['id_user'] = user['id_utilisateur']

            if user['role'] == 'ROLE_admin':
                return redirect('/admin/commande/index')
            else:
                return redirect('/client/article/show')
        else:
            # Mot de passe incorrect
            flash(u'Mot de passe incorrect. Veuillez réessayer.', 'alert-warning')
            return redirect('/login')
    else:
        # Utilisateur non trouvé
        flash(u'Utilisateur non trouvé. Veuillez vérifier votre login et réessayer.', 'alert-warning')
        return redirect('/login')
@auth_security.route('/signup')
def auth_signup():
    return render_template('auth/signup.html')


@auth_security.route('/signup', methods=['POST'])
def auth_signup_post():
    mycursor = get_db().cursor()
    email = request.form.get('email')
    login = request.form.get('login')
    password = request.form.get('password')

    # Vérifier si l'email ou le login existe déjà
    sql_select = "SELECT id_utilisateur, email, login, password FROM utilisateur WHERE email = %s OR login = %s"
    mycursor.execute(sql_select, (email, login,))
    user = mycursor.fetchone()
    if user:
        flash(u'L\'adresse e-mail ou le login existe déjà', 'alert-warning')
        return redirect('/signup')

    # Ajouter un nouvel utilisateur
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    sql_insert = "INSERT INTO utilisateur (login, email, password, role) VALUES (%s, %s, %s, %s)"
    tuple_insert = (login, email, hashed_password, 'ROLE_client')
    mycursor.execute(sql_insert, tuple_insert)
    get_db().commit()

    # Récupérer l'ID de l'utilisateur nouvellement inséré
    sql_last_id = "SELECT LAST_INSERT_ID() AS last_id"
    mycursor.execute(sql_last_id)
    id_user = mycursor.fetchone()['last_id']

    # Mettre à jour la session de l'utilisateur
    session.clear()  # Supprimer toutes les clés de session existantes
    session['login'] = login
    session['role'] = 'ROLE_client'
    session['id_user'] = id_user

    return redirect('/client/article/show')

@auth_security.route('/logout')
def auth_logout():
    session.pop('login', None)
    session.pop('role', None)
    session.pop('id_user', None)
    return redirect('/')

@auth_security.route('/forget-password', methods=['GET'])
def forget_password():
    return render_template('auth/forget_password.html')

