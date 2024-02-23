from flask import Blueprint, redirect
from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__, template_folder='templates')

@fixtures_load.route('/base/init')
def fct_fixtures_load():
    mycursor = get_db().cursor()

    # Suppression des tables existantes en respectant les dépendances
    drop_tables_queries = [
        "DROP TABLE IF EXISTS ligne_panier;",
        "DROP TABLE IF EXISTS ligne_commande;",
        "DROP TABLE IF EXISTS commande;",
        "DROP TABLE IF EXISTS jean;",
        "DROP TABLE IF EXISTS utilisateur;",
        "DROP TABLE IF EXISTS etat;",
        "DROP TABLE IF EXISTS coupe_jean;",
        "DROP TABLE IF EXISTS taille;",
        "DROP TABLE IF EXISTS couleur;"
    ]


    for query in drop_tables_queries:
        mycursor.execute(query)
        get_db().commit()

    # Création des tables en fonction de votre script SQL
    create_tables_queries = [
        """
        CREATE TABLE utilisateur(
            id_utilisateur INT AUTO_INCREMENT,
            login VARCHAR(255),
            email VARCHAR(255),
            nom VARCHAR(255),
            password VARCHAR(255),
            role VARCHAR(255),
            est_actif TINYINT(1),
            PRIMARY KEY (id_utilisateur)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """,
        """
        CREATE TABLE etat(
            id_etat INT AUTO_INCREMENT,
            libelle_etat VARCHAR(255),
            PRIMARY KEY (id_etat)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """,
        """
        CREATE TABLE commande(
            id_commande INT AUTO_INCREMENT,
            date_achat DATE,
            utilisateur_id INT,
            etat_id INT,
            PRIMARY KEY (id_commande),
            CONSTRAINT fk_utilisateur_commande FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
            CONSTRAINT fk_etat FOREIGN KEY (etat_id) REFERENCES etat(id_etat)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """,
        """
        CREATE TABLE taille(
            id_taille INT AUTO_INCREMENT,
            libelle_taille VARCHAR(255),
            PRIMARY KEY (id_taille)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """,
        """
        CREATE TABLE coupe_jean(
            id_coupe_jean INT AUTO_INCREMENT,
            libelle VARCHAR(50) NOT NULL,
            PRIMARY KEY (id_coupe_jean)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """,
        """
        CREATE TABLE couleur(
            id_couleur INT AUTO_INCREMENT,
            libelle_couleur VARCHAR(255),
            code_couleur VARCHAR(50),
            PRIMARY KEY (id_couleur)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
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
            PRIMARY KEY (id_jean),
            FOREIGN KEY (id_coupe_jean) REFERENCES coupe_jean(id_coupe_jean)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """,
        """
        CREATE TABLE ligne_commande(
            id_jean INT,
            id_commande INT,
            quantite DECIMAL(15,2) NOT NULL,
            prix DECIMAL(15,2) NOT NULL,
            PRIMARY KEY (id_jean, id_commande),
            FOREIGN KEY (id_jean) REFERENCES jean(id_jean),
            FOREIGN KEY (id_commande) REFERENCES commande(id_commande)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """,
        """
        CREATE TABLE ligne_panier(
            id_jean INT,
            id_utilisateur INT,
            quantite DECIMAL(15,2) NOT NULL,
            date_ajout DATE NOT NULL,
            PRIMARY KEY (id_jean, id_utilisateur),
            FOREIGN KEY (id_jean) REFERENCES jean(id_jean),
            FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
    ]



        # Insertion des données
        insert_data_queries = [
        # Utilisateurs
        """
        INSERT INTO utilisateur (login, email, password, nom, role, est_actif) VALUES
        ('admin', 'admin@admin.fr', 'sha256$dPL3oH9ug1wjJqva$2b341da75a4257607c841eb0dbbacb76e780f4015f0499bb1a164de2a893fdbf', 'admin', 'ROLE_admin', 1),
        ('client', 'client@client.fr', 'sha256$1GAmexw1DkXqlTKK$31d359e9adeea1154f24491edaa55000ee248f290b49b7420ced542c1bf4cf7d', 'client', 'ROLE_client', 1),
        ('client2', 'client2@client2.fr', 'sha256$MjhdGuDELhI82lKY$2161be4a68a9f236a27781a7f981a531d11fdc50e4112d912a7754de2dfa0422', 'client2', 'ROLE_client', 1),
        ('Romain', 'romain.meyer.fkpt@gmail.com', 'sha256$fNr1sj4gBPxAlnpI$5b0242df0c3559cb66c1d29ec72bc9ead6f13a32fdd9cac7216761123dbf3e10', 'client3', 'ROLE_client', 1);
        """,

        # États
        """
        INSERT INTO etat (libelle_etat) VALUES
        ('en attente'),
        ('expédié'),
        ('validé'),
        ('confirmé');
        """,

        # Tailles
        """
        INSERT INTO taille (libelle_taille) VALUES
        ('XS'),
        ('S'),
        ('M'),
        ('L'),
        ('XL');
        """,

        # Coupes de jean
        """
        INSERT INTO coupe_jean (libelle) VALUES
        ('Slim'),
        ('Droit'),
        ('Bootcut'),
        ('Skinny'),
        ('Flare');
        """,

        # Couleurs
        """
        INSERT INTO couleur (libelle_couleur, code_couleur) VALUES
        ('Bleu', '001'),
        ('Noir', '002'),
        ('Gris', '003'),
        ('Marron', '004'),
        ('Vert', '005');
        """,

        # Jeans
        """
        INSERT INTO jean (nom, disponible, prix, description, image, id_coupe_jean) VALUES
        ('Slim Fit Blue', 'En stock', 49.99, 'Jean slim en coton bleu', 'jean1.jpg', 1),
        ('Classic Black', 'En stock', 59.99, 'Jean droit en denim noir', 'jean2.jpg', 2),
        ('Flex Grey Bootcut', 'En stock', 69.99, 'Jean bootcut stretch gris', 'jean3.jpg', 3),
        ('Leather Brown Skinny', 'En stock', 79.99, 'Jean skinny en cuir marron', 'jean4.jpg', 4),
        ('Flare Green Canvas', 'En stock', 89.99, 'Jean flare en toile verte', 'jean5.jpg', 5);
        """
    ]

    for query in insert_data_queries:
        mycursor.execute(query)
        get_db().commit()

    return redirect('/')
