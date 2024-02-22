DROP TABLE IF EXISTS liste_envie;
DROP TABLE IF EXISTS historique;
DROP TABLE IF EXISTS commentaire;
DROP TABLE IF EXISTS note;
DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS declinaison_jean;
DROP TABLE IF EXISTS adresse;
DROP TABLE IF EXISTS jean;
DROP TABLE IF EXISTS utilisateur;
DROP TABLE IF EXISTS _date_update_;
DROP TABLE IF EXISTS _date_commentaire_;
DROP TABLE IF EXISTS _date_consultation_;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS coupe_jean;
DROP TABLE IF EXISTS Taille;
DROP TABLE IF EXISTS couleur;

    CREATE TABLE couleur(
       id_couleur INT,
       libelle VARCHAR(50) NOT NULL,
       code_couleur INT NOT NULL,
       PRIMARY KEY(id_couleur)
    );

    CREATE TABLE Taille(
       id_taille INT,
       libelle VARCHAR(50) NOT NULL,
       code_taille INT NOT NULL,
       PRIMARY KEY(id_taille)
    );

    CREATE TABLE coupe_jean(
       id_coupe_jean INT,
       libelle VARCHAR(50) NOT NULL,
       PRIMARY KEY(id_coupe_jean)
    );

    CREATE TABLE etat(
       id_etat INT,
       libelle VARCHAR(50) NOT NULL,
       PRIMARY KEY(id_etat)
    );

    CREATE TABLE utilisateur(
       id_utilisateur INT,
       login VARCHAR(50) NOT NULL,
       email VARCHAR(100) NOT NULL,
       nom VARCHAR(50) NOT NULL,
       password VARCHAR(200) NOT NULL,
       role VARCHAR(50) NOT NULL,
       PRIMARY KEY(id_utilisateur),
       UNIQUE(password),
       est_actif int
    );

    CREATE TABLE jean(
       id_jean INT,
       nom VARCHAR(50) NOT NULL,
       disponible VARCHAR(50) NOT NULL,
       prix DECIMAL(15,2) NOT NULL,
       description VARCHAR(250) NOT NULL,
       image VARCHAR(50) NOT NULL,
       id_coupe_jean INT NOT NULL,
       PRIMARY KEY(id_jean),
       FOREIGN KEY(id_coupe_jean) REFERENCES coupe_jean(id_coupe_jean)
    );

    CREATE TABLE adresse(
       id_adresse INT,
       nom VARCHAR(100) NOT NULL,
       rue VARCHAR(50) NOT NULL,
       code_postal INT NOT NULL,
       ville VARCHAR(50) NOT NULL,
       date_utilisation DATE NOT NULL,
       id_utilisateur INT NOT NULL,
       PRIMARY KEY(id_adresse),
       FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
    );

    CREATE TABLE _date_consultation_(
       date_consultation DATE,
       PRIMARY KEY(date_consultation)
    );

    CREATE TABLE _date_commentaire_(
       date_publication DATE,
       PRIMARY KEY(date_publication)
    );

    CREATE TABLE _date_update_(
       date_update DATE,
       PRIMARY KEY(date_update)
    );

    CREATE TABLE declinaison_jean(
       id_declinaison INT,
       stock VARCHAR(50) NOT NULL,
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

    CREATE TABLE commande(
       id_commande INT,
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

    CREATE TABLE ligne_commande(
       id_declinaison INT,
       id_commande INT,
       quantite DECIMAL(15,2) NOT NULL,
       prix DECIMAL(15,2) NOT NULL,
       PRIMARY KEY(id_declinaison, id_commande),
       FOREIGN KEY(id_declinaison) REFERENCES declinaison_jean(id_declinaison),
       FOREIGN KEY(id_commande) REFERENCES commande(id_commande)
    );

    CREATE TABLE ligne_panier(
       id_declinaison INT,
       id_utilisateur INT,
       quantite DECIMAL(15,2) NOT NULL,
       date_ajout DATE NOT NULL,
       PRIMARY KEY(id_declinaison, id_utilisateur),
       FOREIGN KEY(id_declinaison) REFERENCES declinaison_jean(id_declinaison),
       FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
    );

    CREATE TABLE note(
       id_utilisateur INT,
       id_jean INT,
       note VARCHAR(150) NOT NULL,
       PRIMARY KEY(id_utilisateur, id_jean),
       FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
       FOREIGN KEY(id_jean) REFERENCES jean(id_jean)
    );

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

    CREATE TABLE historique(
       id_utilisateur INT,
       id_jean INT,
       date_consultation DATE,
       PRIMARY KEY(id_utilisateur, id_jean, date_consultation),
       FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
       FOREIGN KEY(id_jean) REFERENCES jean(id_jean),
       FOREIGN KEY(date_consultation) REFERENCES _date_consultation_(date_consultation)
    );

    CREATE TABLE liste_envie(
       id_utilisateur INT,
       id_jean INT,
       date_update DATE,
       PRIMARY KEY(id_utilisateur, id_jean, date_update),
       FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
       FOREIGN KEY(id_jean) REFERENCES jean(id_jean),
       FOREIGN KEY(date_update) REFERENCES _date_update_(date_update)
    );
    INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom,est_actif) VALUES
    (1,'admin','admin@admin.fr',
        'pbkdf2:sha256:600000$IvuDq71lXRGkEPVb$95a0bfa3cb4b8fc27822272940e2be85ef67c25d5ce3d5bcc4567dbc7a692a83','ROLE_admin','admin',1),
    (2,'client','client@client.fr',
        'pbkdf2:sha256:600000$yC12DqGQQJQdl1J2$f5b880027610cb813a8247e0bef6d016282e03743827c62b99e6bd596178665b',
        'ROLE_client','client',1),
    (3,'client2','client2@client2.fr',
        'pbkdf2:sha256:600000$6tsowjXSGSRdodCm$4dc4d8491a7c7e67c1d605db6b6fa42d852ca7215c73ddf891f08a1920726aa7',
        'ROLE_client','client2',1);


           INSERT INTO couleur (id_couleur, libelle, code_couleur) VALUES
    (1, 'Bleu', 001),
    (2, 'Noir', 002),
    (3, 'Gris', 003),
    (4, 'Marron', 004),
    (5, 'Vert', 005);

    INSERT INTO Taille (id_taille, libelle, code_taille) VALUES
    (1, 'XS', 001),
    (2, 'S', 002),
    (3, 'M', 003),
    (4, 'L', 004),
    (5, 'XL', 005);

    INSERT INTO coupe_jean (id_coupe_jean, libelle) VALUES
    (1, 'Slim'),
    (2, 'Droit'),
    (3, 'Bootcut'),
    (4, 'Skinny'),
    (5, 'Flare');

    INSERT INTO etat (id_etat, libelle) VALUES
    (1, 'En cours de traitement'),
    (2, 'Expédiée'),
    (3, 'Livraison en attente'),
    (4, 'Livrée'),
    (5, 'Annulée');

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


    INSERT INTO adresse (id_adresse, nom, rue, code_postal, ville, date_utilisation, id_utilisateur) VALUES
    (1, 'Adresse 1', 'Rue 1', 12345, 'Ville 1', '2024-01-01', 1),
    (2, 'Adresse 2', 'Rue 2', 23456, 'Ville 2', '2024-01-02', 2),
    (3, 'Adresse 3', 'Rue 3', 34567, 'Ville 3', '2024-01-03', 3);

    INSERT INTO _date_consultation_ (date_consultation) VALUES
    ('2024-01-01'),
    ('2024-01-02'),
    ('2024-01-03');

    INSERT INTO _date_commentaire_ (date_publication) VALUES
    ('2024-01-01'),
    ('2024-01-02'),
    ('2024-01-03');

    INSERT INTO _date_update_ (date_update) VALUES
    ('2024-01-01'),
    ('2024-01-02'),
    ('2024-01-03');

    INSERT INTO declinaison_jean (id_declinaison, stock, prix_declinaison, image, id_jean, id_taille, id_couleur) VALUES
    (1, 'En stock', 49.99, 'image1.jpg', 1, 1, 1),
    (2, 'En stock', 59.99, 'image2.jpg', 2, 2, 2),
    (3, 'En stock', 69.99, 'image3.jpg', 3, 3, 3),
    (4, 'En stock', 79.99, 'image4.jpg', 4, 4, 4),
    (5, 'En stock', 89.99, 'image5.jpg', 5, 5, 5);

    INSERT INTO commande (id_commande, date_achat, id_adresse_livraison, id_adresse_facturation, id_utilisateur, id_etat) VALUES
    (1, '2024-01-01', 1, 1, 1, 1),
    (2, '2024-01-02', 2, 2, 2, 2),
    (3, '2024-01-03', 3, 3, 3, 3);

    INSERT INTO ligne_commande (id_declinaison, id_commande, quantite, prix) VALUES
    (1, 1, 1, 49.99),
    (2, 2, 1, 59.99),
    (3, 3, 1, 69.99);

    INSERT INTO ligne_panier (id_declinaison, id_utilisateur, quantite, date_ajout) VALUES
    (1, 1, 1, '2024-01-01'),
    (2, 2, 1, '2024-01-02'),
    (3, 3, 1, '2024-01-03');

    INSERT INTO note (id_utilisateur, id_jean, note) VALUES
    (1, 1, 'Bonne qualité'),
    (2, 2, 'Conforme à la description'),
    (3, 3, 'Livraison rapide');

    INSERT INTO commentaire (id_utilisateur, id_jean, date_publication, commentaire, valider) VALUES
    (1, 1, '2024-01-01', 'Très satisfait', 'Oui'),
    (2, 2, '2024-01-02', 'Super produit', 'Oui'),
    (3, 3, '2024-01-03', 'Excellent service', 'Oui');

    INSERT INTO historique (id_utilisateur, id_jean, date_consultation) VALUES
    (1, 1, '2024-01-01'),
    (2, 2, '2024-01-02'),
    (3, 3, '2024-01-03');

    INSERT INTO liste_envie (id_utilisateur, id_jean, date_update) VALUES
    (1, 1, '2024-01-01'),
    (2, 2, '2024-01-02'),
    (3, 3, '2024-01-03');
