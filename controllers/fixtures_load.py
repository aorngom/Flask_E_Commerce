from flask import Blueprint, redirect
from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__, template_folder='templates')

@fixtures_load.route('/base/init')
def fct_fixtures_load():
    mycursor = get_db().cursor()

    # Suppression des tables existantes
    drop_tables_queries = [
        "DROP TABLE IF EXISTS liste_envie;",
        "DROP TABLE IF EXISTS historique;",
        "DROP TABLE IF EXISTS commentaire;",
        "DROP TABLE IF EXISTS note;",
        "DROP TABLE IF EXISTS ligne_panier;",
        "DROP TABLE IF EXISTS ligne_commande;",
        "DROP TABLE IF EXISTS commande;",
        "DROP TABLE IF EXISTS declinaison_jean;",
        "DROP TABLE IF EXISTS adresse;",
        "DROP TABLE IF EXISTS jean;",
        "DROP TABLE IF EXISTS utilisateur;",
        "DROP TABLE IF EXISTS _date_update_;",
        "DROP TABLE IF EXISTS _date_commentaire_;",
        "DROP TABLE IF EXISTS _date_consultation_;",
        "DROP TABLE IF EXISTS etat;",
        "DROP TABLE IF EXISTS coupe_jean;",
        "DROP TABLE IF EXISTS Taille;",
        "DROP TABLE IF EXISTS couleur;"
    ]

    for query in drop_tables_queries:
        mycursor.execute(query)
        get_db().commit()

    # Création des tables
    create_tables_queries = [
        """
        CREATE TABLE couleur(
           id_couleur INT AUTO_INCREMENT,
           libelle VARCHAR(50) NOT NULL,
           code_couleur INT NOT NULL,
           PRIMARY KEY(id_couleur)
        );
        """,
        """
        CREATE TABLE Taille(
           id_taille INT AUTO_INCREMENT,
           libelle VARCHAR(50) NOT NULL,
           code_taille INT NOT NULL,
           PRIMARY KEY(id_taille)
        );
        """,
        """
        CREATE TABLE coupe_jean(
           id_coupe_jean INT AUTO_INCREMENT,
           libelle VARCHAR(50) NOT NULL,
           PRIMARY KEY(id_coupe_jean)
        );
        """,
        """
        CREATE TABLE etat(
           id_etat INT AUTO_INCREMENT,
           libelle VARCHAR(50) NOT NULL,
           PRIMARY KEY(id_etat)
        );
        """,
        """
        CREATE TABLE utilisateur(
           id_utilisateur INT AUTO_INCREMENT,
           login VARCHAR(50) NOT NULL,
           email VARCHAR(100) NOT NULL,
           nom VARCHAR(50) NOT NULL,
           password VARCHAR(200) NOT NULL,
           role VARCHAR(50) NOT NULL,
           PRIMARY KEY(id_utilisateur),
           UNIQUE(password),
           est_actif int
        );
        """,
        """
        CREATE TABLE jean(
           id_jean INT AUTO_INCREMENT,
           nom VARCHAR(50) NOT NULL,
           disponible VARCHAR(50) NOT NULL,
           prix DECIMAL(15,2) NOT NULL,
           description VARCHAR(250) NOT NULL,
           image VARCHAR(50) NOT NULL,
           id_coupe_jean INT NOT NULL,
           PRIMARY KEY(id_jean),
           FOREIGN KEY(id_coupe_jean) REFERENCES coupe_jean(id_coupe_jean)
        );
        """,
        """
        CREATE TABLE adresse(
           id_adresse INT AUTO_INCREMENT,
           nom VARCHAR(100) NOT NULL,
           rue VARCHAR(50) NOT NULL,
           code_postal INT NOT NULL,
           ville VARCHAR(50) NOT NULL,
           date_utilisation DATE NOT NULL,
           id_utilisateur INT NOT NULL,
           PRIMARY KEY(id_adresse),
           FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
        );
        """,
        """
        CREATE TABLE _date_consultation_(
           date_consultation DATE,
           PRIMARY KEY(date_consultation)
        );
        """,
        """
        CREATE TABLE _date_commentaire_(
           date_publication DATE,
           PRIMARY KEY(date_publication)
        );
        """,
        """
        CREATE TABLE _date_update_(
           date_update DATE,
           PRIMARY KEY(date_update)
        );
        """,
        """
        CREATE TABLE declinaison_jean(
           id_declinaison INT AUTO_INCREMENT,
           stock INT,
           prix_declinaison DECIMAL(15,2) NOT NULL,
           image VARCHAR(50) NOT NULL,
           id_jean INT NOT NULL,
           id_taille INT NOT NULL,
           id_couleur INT NOT NULL,
           PRIMARY KEY(id_declinaison),
           FOREIGN KEY(id_jean) REFERENCES jean(id_jean),
           FOREIGN KEY(id_taille) REFERENCES Taille(id_taille),
           FOREIGN KEY(id_couleur) REFERENCES couleur(id_couleur)
        );
        """,
        """
        CREATE TABLE commande(
           id_commande INT AUTO_INCREMENT,
           date_achat DATE NOT NULL,
           id_adresse_livraison INT NOT NULL,
           id_adresse_facturation INT NOT NULL,
           id_utilisateur INT NOT NULL,
           id_etat INT NOT NULL,
           PRIMARY KEY(id_commande),
           FOREIGN KEY(id_adresse_livraison) REFERENCES adresse(id_adresse),
           FOREIGN KEY(id_adresse_facturation) REFERENCES adresse(id_adresse),
           FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
           FOREIGN KEY(id_etat) REFERENCES etat(id_etat)
        );
        """,
        """
        CREATE TABLE ligne_commande(
           id_declinaison INT,
           id_commande INT,
           quantite DECIMAL(15,2) NOT NULL,
           prix DECIMAL(15,2) NOT NULL,
           PRIMARY KEY(id_declinaison, id_commande),
           FOREIGN KEY(id_declinaison) REFERENCES declinaison_jean(id_declinaison),
           FOREIGN KEY(id_commande) REFERENCES commande(id_commande)
        );
        """,
        """
        CREATE TABLE ligne_panier(
           id_declinaison INT,
           id_utilisateur INT,
           quantite DECIMAL(15,2) NOT NULL,
           date_ajout DATE NOT NULL,
           PRIMARY KEY(id_declinaison, id_utilisateur),
           FOREIGN KEY(id_declinaison) REFERENCES declinaison_jean(id_declinaison),
           FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
        );
        """,
        """
        CREATE TABLE note(
           id_utilisateur INT,
           id_jean INT,
           note VARCHAR(150) NOT NULL,
           PRIMARY KEY(id_utilisateur, id_jean),
           FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
           FOREIGN KEY(id_jean) REFERENCES jean(id_jean)
        );
        """,
        """
        CREATE TABLE commentaire(
           id_utilisateur INT,
           id_jean INT,
           date_publication DATE,
           commentaire VARCHAR(200) NOT NULL,
           valider VARCHAR(50) NOT NULL,
           PRIMARY KEY(id_utilisateur, id_jean, date_publication),
           FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
           FOREIGN KEY(id_jean) REFERENCES jean(id_jean),
           FOREIGN KEY(date_publication) REFERENCES _date_commentaire_(date_publication)
        );
        """,
        """
        CREATE TABLE historique(
           id_utilisateur INT,
           id_jean INT,
           date_consultation DATE,
           PRIMARY KEY(id_utilisateur, id_jean, date_consultation),
           FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
           FOREIGN KEY(id_jean) REFERENCES jean(id_jean),
           FOREIGN KEY(date_consultation) REFERENCES _date_consultation_(date_consultation)
        );
        """,
        """
        CREATE TABLE liste_envie(
           id_utilisateur INT,
           id_jean INT,
           date_update DATE,
           PRIMARY KEY(id_utilisateur, id_jean, date_update),
           FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
           FOREIGN KEY(id_jean) REFERENCES jean(id_jean),
           FOREIGN KEY(date_update) REFERENCES _date_update_(date_update)
        );
        """
    ]

    for query in create_tables_queries:
        mycursor.execute(query)
        get_db().commit()

    # Insertion des données
    insert_data_queries = [
        """
        INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom,est_actif) VALUES
        (1,'admin','admin@admin.fr',
            'pbkdf2:sha256:600000$IvuDq71lXRGkEPVb$95a0bfa3cb4b8fc27822272940e2be85ef67c25d5ce3d5bcc4567dbc7a692a83','ROLE_admin','admin',1),
        (2,'client','client@client.fr',
            'pbkdf2:sha256:600000$yC12DqGQQJQdl1J2$f5b880027610cb813a8247e0bef6d016282e03743827c62b99e6bd596178665b',
            'ROLE_client','client',1),
        (3,'client2','client2@client2.fr',
            'pbkdf2:sha256:600000$6tsowjXSGSRdodCm$4dc4d8491a7c7e67c1d605db6b6fa42d852ca7215c73ddf891f08a1920726aa7',
            'ROLE_client','client2',1);
        """,
        """
        INSERT INTO couleur (id_couleur, libelle, code_couleur) VALUES
        (1, 'Bleu', 001),
        (2, 'Noir', 002),
        (3, 'Gris', 003),
        (4, 'Marron', 004),
        (5, 'Vert', 005);
        """,
        """
        INSERT INTO Taille (id_taille, libelle, code_taille) VALUES
        (1, 'XS', 001),
        (2, 'S', 002),
        (3, 'M', 003),
        (4, 'L', 004),
        (5, 'XL', 005);
        """,
        """
        INSERT INTO coupe_jean (id_coupe_jean, libelle) VALUES
        (1, 'Slim'),
        (2, 'Droit'),
        (3, 'Bootcut'),
        (4, 'Skinny'),
        (5, 'Flare');
        """,
        """
        INSERT INTO etat (id_etat, libelle) VALUES
        (1, 'En cours de traitement'),
        (2, 'Expédiée'),
        (3, 'Livraison en attente'),
        (4, 'Livrée'),
        (5, 'Annulée');
        """,
        """
        INSERT INTO jean (id_jean, nom, disponible, prix, description, image, id_coupe_jean)
        VALUES
        (1, 'Slim Fit Blue', 'En stock', 49.99, 'Jean slim en coton bleu', 'jean1.jpg', 1),
        (2, 'Classic Black', 'En stock', 59.99, 'Jean droit en denim noir', 'jean2.jpg', 2),
        (3, 'Flex Grey Bootcut', 'En stock', 69.99, 'Jean bootcut stretch gris', 'jean3.jpg', 3),
        (4, 'Leather Brown Skinny', 'En stock', 79.99, 'Jean skinny en cuir marron', 'jean4.jpg', 4),
        (5, 'Flare Green Canvas', 'En stock', 89.99, 'Jean flare en toile verte', 'jean5.jpg', 5),
        (6, 'Red Denim Slim', 'En stock', 49.99, 'Jean slim en denim rouge', 'jean6.jpg', 1),
        (7, 'Classic Blue', 'En stock', 59.99, 'Jean droit en coton bleu', 'jean7.jpg', 2),
        (8, 'Flex Grey Bootcut', 'En stock', 69.99, 'Jean bootcut stretch gris', 'jean8.jpg', 3),
        (9, 'Black Denim Skinny', 'En stock', 79.99, 'Jean skinny en denim noir', 'jean9.jpg', 4),
        (10, 'Flare Green Canvas', 'En stock', 89.99, 'Jean flare en toile verte', 'jean10.jpg', 5),
        (11, 'Slim Fit Blue', 'En stock', 49.99, 'Jean slim en coton bleu', 'jean11.jpg', 1),
        (12, 'Red Denim Classic', 'En stock', 59.99, 'Jean droit en denim rouge', 'jean12.jpg', 2),
        (13, 'Flex Grey Bootcut', 'En stock', 69.99, 'Jean bootcut stretch gris', 'jean13.jpg', 3),
        (14, 'Leather Brown Skinny', 'En stock', 79.99, 'Jean skinny en cuir marron', 'jean14.jpg', 4),
        (15, 'Flare Green Canvas', 'En stock', 89.99, 'Jean flare en toile verte', 'jean15.jpg', 5);
        """,
        """
        INSERT INTO declinaison_jean (stock, prix_declinaison, image, id_jean, id_taille, id_couleur) 
        VALUES
            (10, 49.99, 'jean1.jpg', 1, 1, 1),
            (20, 49.99, 'jean2.jpg', 1, 2, 1),
            (30, 49.99, 'jean3.jpg', 1, 3, 1),
            
            (15, 59.99, 'jean4.jpg', 2, 1, 2),
            (25, 59.99, 'jean5.jpg', 2, 2, 2),
            (35, 59.99, 'jean6.jpg', 2, 3, 2),
            
            (12, 69.99, 'jean7.jpg', 3, 1, 3),
            (22, 69.99, 'jean8.jpg', 3, 2, 3),
            (32, 69.99, 'jean9.jpg', 3, 3, 3),
            
            (18, 79.99, 'jean10.jpg', 4, 1, 4),
            (28, 79.99, 'jean11.jpg', 4, 2, 4),
            (38, 79.99, 'jean12.jpg', 4, 3, 4),
            
            (13, 89.99, 'jean13.jpg', 5, 1, 5),
            (23, 89.99, 'jean14.jpg', 5, 2, 5),
            (33, 89.99, 'jean15.jpg', 5, 3, 5),
            
            (11, 49.99, 'jean16.jpg', 6, 1, 1),
            (21, 49.99, 'jean17.jpg', 6, 2, 1),
            (31, 49.99, 'jean18.jpg', 6, 3, 1),
            
            (16, 59.99, 'jean19.jpg', 7, 1, 2),
            (26, 59.99, 'jean20.jpg', 7, 2, 2),
            (36, 59.99, 'jean21.jpg', 7, 3, 2),
            
            (14, 69.99, 'jean22.jpg', 8, 1, 3),
            (24, 69.99, 'jean23.jpg', 8, 2, 3),
            (34, 69.99, 'jean24.jpg', 8, 3, 3),
            
            (19, 79.99, 'jean25.jpg', 9, 1, 4),
            (29, 79.99, 'jean26.jpg', 9, 2, 4),
            (39, 79.99, 'jean27.jpg', 9, 3, 4),
            
            (17, 89.99, 'jean28.jpg', 10, 1, 5),
            (27, 89.99, 'jean29.jpg', 10, 2, 5),
            (37, 89.99, 'jean30.jpg', 10, 3, 5),
            (10, 49.99, 'jean31.jpg', 11, 1, 1),
            (20, 49.99, 'jean32.jpg', 11, 2, 1),
            (30, 49.99, 'jean33.jpg', 11, 3, 1),
            
            (15, 59.99, 'jean34.jpg', 12, 1, 2),
            (25, 59.99, 'jean35.jpg', 12, 2, 2),
            (35, 59.99, 'jean36.jpg', 12, 3, 2),
            
            (12, 69.99, 'jean37.jpg', 13, 1, 3),
            (22, 69.99, 'jean38.jpg', 13, 2, 3),
            (32, 69.99, 'jean39.jpg', 13, 3, 3),
            
            (18, 79.99, 'jean40.jpg', 14, 1, 4),
            (28, 79.99, 'jean41.jpg', 14, 2, 4),
            (38, 79.99, 'jean42.jpg', 14, 3, 4),
            
            (13, 89.99, 'jean43.jpg', 15, 1, 5),
            (23, 89.99, 'jean44.jpg', 15, 2, 5),
            (33, 89.99, 'jean45.jpg', 15, 3, 5);
          """
    ]

    for query in insert_data_queries:
        mycursor.execute(query)
        get_db().commit()

    return redirect('/')
