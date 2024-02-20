
#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import *
import datetime
from decimal import *
from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__,
                          template_folder='templates')

@fixtures_load.route('/base/init')
def fct_fixtures_load():

    mycursor = get_db().cursor()
    sql = "DROP TABLE IF EXISTS ligne_commande, ligne_panier, jean, commande, etat, taille, coupe_jean, utilisateur;"
    mycursor.execute(sql)
    sql = '''
    CREATE TABLE utilisateur(
    id_utilisateur INT AUTO_INCREMENT PRIMARY KEY,
    login VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    nom varchar(25) NULL,
    est_actif int,
    password VARCHAR(400) NOT NULL,
    role VARCHAR(50) NOT NULL
    ) DEFAULT CHARSET utf8;
    '''
    mycursor.execute(sql)

    sql = '''INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom,est_actif) VALUES
         (1,'admin','admin@admin.fr',
             'pbkdf2:sha256:600000$IvuDq71lXRGkEPVb$95a0bfa3cb4b8fc27822272940e2be85ef67c25d5ce3d5bcc4567dbc7a692a83','ROLE_admin','admin',1),
         (2,'client','client@client.fr',
             'pbkdf2:sha256:600000$yC12DqGQQJQdl1J2$f5b880027610cb813a8247e0bef6d016282e03743827c62b99e6bd596178665b',
             'ROLE_client','client',1),
         (3,'client2','client2@client2.fr',
             'pbkdf2:sha256:600000$6tsowjXSGSRdodCm$4dc4d8491a7c7e67c1d605db6b6fa42d852ca7215c73ddf891f08a1920726aa7 
',
             'ROLE_client','client2',1);'''
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE coupe_jean(
    id_coupe_jean INT AUTO_INCREMENT PRIMARY KEY,
    nom_coupe VARCHAR(100) NOT NULL
    )DEFAULT CHARSET utf8;  
    '''
    mycursor.execute(sql)

    sql = '''
    INSERT INTO coupe_jean (id_coupe_jean, nom_coupe) VALUES
    ('1', 'Slim'),
    ('2', 'Droit'),
    ('3', 'Bootcut'),
    ('4', 'Skinny'),
    ('5', 'Flare');
    '''
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE etat(
    id_etat INT AUTO_INCREMENT PRIMARY KEY,
    libelle VARCHAR(150) NOT NULL
    ) DEFAULT CHARSET=utf8;
    '''
    mycursor.execute(sql)

    sql = ''' INSERT INTO etat (id_etat, libelle) VALUES
    ('1', 'En cours de traitement'),
    ('2', 'Expédiée'),
    ('3', 'Livraison en attente'),
    ('4', 'Livrée'),
    ('5', 'Annulée');
    '''
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE taille(
    id_taille int AUTO_INCREMENT PRIMARY key,
    nom_taille VARCHAR(100) NOT NULL
    ) DEFAULT CHARSET=utf8;  
    '''
    mycursor.execute(sql)

    sql = '''INSERT INTO taille (id_taille, nom_taille) VALUES
    ('1', 'XS'),
    ('2', 'S'),
    ('3', 'M'),
    ('4', 'L'),
    ('5', 'XL');
    '''
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE jean(
    id_jean int AUTO_INCREMENT PRIMARY KEY,
    matiere VARCHAR(50) NOT NULL,
    couleur VARCHAR(50) NOT NULL,
    description VARCHAR(255) NOT NULL,
    stock INT NOT NULL,
    marque VARCHAR(50) NOT NULL,
    nom_jean VARCHAR(50) NOT NULL,
    prix_jean DECIMAL(15,3) NOT NULL,
    id_coupe_jean INT NOT NULL,
    id_taille INT NOT NULL,
    image VARCHAR(50) not null,
    FOREIGN KEY(id_coupe_jean) REFERENCES coupe_jean(id_coupe_jean),
    FOREIGN KEY(id_taille) REFERENCES taille(id_taille)
    ) DEFAULT CHARSET=utf8;  
    '''
    mycursor.execute(sql)

    sql = '''
    INSERT INTO jean (id_jean, matiere, couleur, description, marque, nom_jean, prix_jean, id_coupe_jean, id_taille, image, stock) VALUES
    ('1', 'Coton', 'Bleu', 'Jean slim en coton bleu', 'Levis', 'Slim Fit Blue', 49.99, '1', '1', 'jean1.jpg',10),
    ('2', 'Denim', 'Noir', 'Jean droit en denim noir', 'Wrangler', 'Classic Black', 59.99, '2', '2', 'jean2.jpg',10),
    ('3', 'Stretch', 'Gris', 'Jean bootcut stretch gris', 'Diesel', 'Flex Grey Bootcut', 69.99, '3', '3', 'jean3.jpg',10),
    ('4', 'Cuir', 'Marron', 'Jean skinny en cuir marron', 'Calvin Klein', 'Leather Brown Skinny', 79.99, '4', '4', 'jean4.jpg',10),
    ('5', 'Toile', 'Vert', 'Jean flare en toile verte', 'Guess', 'Flare Green Canvas', 89.99, '5', '5', 'jean5.jpg',10),
    ('6', 'Denim', 'Rouge', 'Jean slim en denim rouge', 'Tommy Hilfiger', 'Red Denim Slim', 49.99, '1', '1', 'jean6.jpg',10),
    ('7', 'Coton', 'Bleu', 'Jean droit en coton bleu', 'Levis', 'Classic Blue', 59.99, '2', '2', 'jean7.jpg',10),
    ('8', 'Stretch', 'Gris', 'Jean bootcut stretch gris', 'Diesel', 'Flex Grey Bootcut', 69.99, '3', '3', 'jean8.jpg',10),
    ('9', 'Denim', 'Noir', 'Jean skinny en denim noir', 'Calvin Klein', 'Black Denim Skinny', 79.99, '4', '4', 'jean9.jpg',10),
    ('10', 'Toile', 'Vert', 'Jean flare en toile verte', 'Guess', 'Flare Green Canvas', 89.99, '5', '5', 'jean10.jpg',10),
    ('11', 'Coton', 'Bleu', 'Jean slim en coton bleu', 'Levis', 'Slim Fit Blue', 49.99, '1', '1', 'jean11.jpg',10),
    ('12', 'Denim', 'Rouge', 'Jean droit en denim rouge', 'Wrangler', 'Red Denim Classic', 59.99, '2', '2', 'jean12.jpg',10),
    ('13', 'Stretch', 'Gris', 'Jean bootcut stretch gris', 'Diesel', 'Flex Grey Bootcut', 69.99, '3', '3', 'jean13.jpg',10),
    ('14', 'Cuir', 'Marron', 'Jean skinny en cuir marron', 'Calvin Klein', 'Leather Brown Skinny', 79.99, '4', '4', 'jean14.jpg',10),
    ('15', 'Toile', 'Vert', 'Jean flare en toile verte', 'Guess', 'Flare Green Canvas', 89.99, '5', '5', 'jean15.jpg',10);
    '''
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE commande(
    id_commande INT AUTO_INCREMENT PRIMARY KEY,
    date_achat DATE NOT NULL,
    id_utilisateur INT NOT NULL,
    id_etat INT NOT NULL,
    FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY(id_etat) REFERENCES etat(id_etat)
    ) DEFAULT CHARSET=utf8;
    '''
    mycursor.execute(sql)

    sql = '''
    INSERT INTO commande (id_commande, date_achat, id_utilisateur, id_etat) VALUES
    ('1', '2024-01-28', '1', '1'),
    ('2', '2024-01-27', '2', '2'),
    ('3', '2024-01-26', '3', '3'),
    ('4', '2024-01-25', '1', '4'),
    ('5', '2024-01-24', '3', '5');
    '''
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE ligne_commande(
    id_jean INT NOT NULL,
    id_commande INT NOT NULL,
    prix DECIMAL(15,3) NOT NULL,
    quantite INT NOT NULL,
    PRIMARY KEY(id_jean, id_commande),
    FOREIGN KEY(id_jean) REFERENCES jean(id_jean),
    FOREIGN KEY(id_commande) REFERENCES commande(id_commande)
    );  
    '''
    mycursor.execute(sql)

    sql = '''
    INSERT INTO ligne_commande (id_jean, id_commande, prix, quantite) VALUES
    ('1', '1', 45.99, 2),
    ('2', '2', 34.50, 1),
    ('3', '3', 55.75, 3),
    ('4', '4', 27.80, 1),
    ('5', '5', 39.99, 2);
    '''
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE ligne_panier(
    id_jean INT ,
    id_utilisateur INT,
    quantite INT NOT NULL,
    date_ajout DATE NOT NULL,
    PRIMARY KEY(id_jean, id_utilisateur),
    FOREIGN KEY(id_jean) REFERENCES jean(id_jean),
    FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
    );
    '''
    mycursor.execute(sql)

    sql = '''INSERT INTO ligne_panier (id_jean, id_utilisateur, quantite, date_ajout) VALUES
    ('1', '1', 2, '2024-01-28'),
    ('2', '2', 1, '2024-01-27'),
    ('3', '3', 3, '2024-01-26'),
    ('4', '2', 1, '2024-01-25'),
    ('5', '1', 2, '2024-01-24');
    '''
    mycursor.execute(sql)
    get_db().commit()
    return redirect('/')
