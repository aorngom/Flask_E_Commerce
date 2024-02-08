#! /usr/bin/python
# -*- coding:utf-8 -*-
from werkzeug.security import generate_password_hash
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
    tuple_select = (login)
    sql = "select * from utilisateur where login=%s"
    retour = mycursor.execute(sql, (login))
    user = mycursor.fetchone()
    if user:
        mdp_ok = check_password_hash(user['password'], password)
        if not mdp_ok:
            flash(u'Vérifier votre mot de passe et essayer encore.', 'alert-warning')
            return redirect('/login')
        else:
            session['login'] = user['login']
            session['role'] = user['role']
            session['id_user'] = user['id_utilisateur']
            print(user['login'], user['role'])
            if user['role'] == 'ROLE_admin':
                return redirect('/admin/commande/index')
            else:
                return redirect('/client/article/show')
    else:
        flash(u'Vérifier votre login et essayer encore.', 'alert-warning')
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
    tuple_select = (login, email)

    # Requête pour vérifier si le login ou l'email existe déjà
    sql_select = "SELECT * FROM utilisateur WHERE login = %s OR email = %s"
    retour = mycursor.execute(sql_select, tuple_select)
    user = mycursor.fetchone()

    if user:
        flash(u'Votre adresse email ou votre login existe déjà.', 'alert-warning')
        return redirect('/signup')

    # Ajouter un nouveau utilisateur
    # Spécifiez explicitement la méthode de hachage 'pbkdf2:sha256'
    password = generate_password_hash(password, method='pbkdf2:sha256')
    tuple_insert = (login, email, password, 'ROLE_client')

    # Requête pour insérer un nouvel utilisateur
    sql_insert = "INSERT INTO utilisateur (login, email, password, role) VALUES (%s, %s, %s, %s)"
    mycursor.execute(sql_insert, tuple_insert)

    # Commit pour sauvegarder les changements
    get_db().commit()

    # Requête pour obtenir l'ID du dernier utilisateur inséré
    sql_last_id = "SELECT last_insert_id() AS last_insert_id"
    mycursor.execute(sql_last_id)
    info_last_id = mycursor.fetchone()
    id_user = info_last_id['last_insert_id']
    print('last_insert_id', id_user)

    # Mise à jour de la session avec les informations de l'utilisateur
    session.pop('login', None)
    session.pop('role', None)
    session.pop('id_user', None)
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

