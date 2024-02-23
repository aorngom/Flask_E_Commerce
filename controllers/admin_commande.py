#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin')
@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['GET', 'POST'])
def admin_commande_show():
    mycursor = get_db().cursor()
    # Sélectionner toutes les commandes pour l'administration
    sql = '''
    SELECT commande.id_commande, commande.date_achat, utilisateur.nom, etat.libelle_etat AS etat
    FROM commande
    JOIN utilisateur ON commande.utilisateur_id = utilisateur.id_utilisateur
    JOIN etat ON commande.etat_id = etat.id_etat
    ORDER BY commande.date_achat DESC;
    '''
    mycursor.execute(sql)
    commandes = mycursor.fetchall()

    articles_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    if id_commande:
        # Sélectionner les articles pour une commande spécifique
        sql = '''
        SELECT ligne_commande.*, jean.nom AS nom_jean, jean.prix, ligne_commande.quantite * jean.prix AS total
        FROM ligne_commande
        JOIN jean ON ligne_commande.id_jean = jean.id_jean
        WHERE ligne_commande.id_commande = %s;
        '''
        mycursor.execute(sql, (id_commande,))
        articles_commande = mycursor.fetchall()

        # Vous pourriez également avoir besoin de récupérer des informations sur les adresses liées à la commande ici

    return render_template('admin/commandes/show.html', commandes=commandes, articles_commande=articles_commande, commande_adresses=commande_adresses)


@admin_commande.route('/admin/commande/valider', methods=['GET', 'POST'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    commande_id = request.form.get('id_commande', None)
    if commande_id:
        # Mettre à jour l'état de la commande à "validée" ou un autre état approprié
        sql = '''
        UPDATE commande
        SET etat_id = (SELECT id_etat FROM etat WHERE libelle_etat = 'validé')
        WHERE id_commande = %s;
        '''
        mycursor.execute(sql, (commande_id,))
        get_db().commit()
        flash('Commande validée avec succès.', 'success')
    else:
        flash('Erreur lors de la validation de la commande.', 'danger')
    return redirect('/admin/commande/show')
