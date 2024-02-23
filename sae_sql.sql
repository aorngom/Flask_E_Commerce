DROP TABLE IF EXISTS ligne_panier, ligne_commande, jean, couleur, coupe_jean, taille, commande, etat, utilisateur;

# Creation tables
CREATE TABLE utilisateur(
    id_utilisateur INT AUTO_INCREMENT,
    login VARCHAR(255),
    email VARCHAR(255),
    nom VARCHAR(255),
    password VARCHAR(255),
    role VARCHAR(255),
    est_actif tinyint(1), #boolean
    PRIMARY KEY (id_utilisateur)
) ENGINE = InnoDB DEFAULT CHARSET utf8mb4;

CREATE TABLE etat(
    id_etat INT AUTO_INCREMENT,
    libelle_etat VARCHAR(255),
    PRIMARY KEY (id_etat)
);


CREATE TABLE commande(
    id_commande INT AUTO_INCREMENT,
    date_achat DATE,
    utilisateur_id INT,
    etat_id INT,
    PRIMARY KEY (id_commande),
    CONSTRAINT fk_utilisateur_commande FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
    CONSTRAINT fk_etat FOREIGN KEY  (etat_id) REFERENCES etat(id_etat)
);



CREATE TABLE taille(
    id_taille INT AUTO_INCREMENT,
    libelle_taille VARCHAR(255),
    PRIMARY KEY (id_taille)
);


CREATE TABLE coupe_jean(
   id_coupe_jean INT,
   libelle VARCHAR(50) NOT NULL,
   PRIMARY KEY(id_coupe_jean)
);


CREATE TABLE couleur(
    id_couleur INT AUTO_INCREMENT,
    libelle_couleur VARCHAR(255),
    code_couleur VARCHAR(50),
    PRIMARY KEY (id_couleur)
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

CREATE TABLE ligne_commande(
   id_jean INT,
   id_commande INT,
   quantite DECIMAL(15,2) NOT NULL,
   prix DECIMAL(15,2) NOT NULL,
   PRIMARY KEY(id_jean, id_commande),
   FOREIGN KEY(id_jean) REFERENCES jean(id_jean),
   FOREIGN KEY(id_commande) REFERENCES commande(id_commande)
);


CREATE TABLE ligne_panier(
   id_jean INT,
   id_utilisateur INT,
   quantite DECIMAL(15,2) NOT NULL,
   date_ajout DATE NOT NULL,
   PRIMARY KEY(id_jean, id_utilisateur),
   FOREIGN KEY(id_jean) REFERENCES jean(id_jean),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);



-- Ajoutez ici vos commandes INSERT comme précédemment fournies

-- INSERT COMMANDS FOR USERS
INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom,est_actif) VALUES
(1,'admin','admin@admin.fr',
    'sha256$dPL3oH9ug1wjJqva$2b341da75a4257607c841eb0dbbacb76e780f4015f0499bb1a164de2a893fdbf',
    'ROLE_admin','admin','1'),
(2,'client','client@client.fr',
    'sha256$1GAmexw1DkXqlTKK$31d359e9adeea1154f24491edaa55000ee248f290b49b7420ced542c1bf4cf7d',
    'ROLE_client','client','1'),
(3,'client2','client2@client2.fr',
    'sha256$MjhdGuDELhI82lKY$2161be4a68a9f236a27781a7f981a531d11fdc50e4112d912a7754de2dfa0422',
    'ROLE_client','client2','1'),
(4, 'Romain', 'romain.meyer.fkpt@gmail.com',
    'sha256$fNr1sj4gBPxAlnpI$5b0242df0c3559cb66c1d29ec72bc9ead6f13a32fdd9cac7216761123dbf3e10',
    'ROLE_client', 'client3', '1');


INSERT INTO etat(id_etat, libelle_etat) VALUES
(1,'en attente'),
(2,'expédié'),
(3,'validé'),
(4,'confirmé');


INSERT INTO commande(id_commande, date_achat, utilisateur_id, etat_id) VALUES
(1,'2023-01-07', 1, 3),
(2,'2023-01-19', 1, 1),
(3,'2023-01-07', 2, 2),
(4,'2023-01-19', 2, 1),
(5,'2023-01-07', 3, 4);


-- INSERT COMMANDS FOR SIZES
INSERT INTO taille (id_taille, libelle, code_taille) VALUES
(1, 'XS', 001),
(2, 'S', 002),
(3, 'M', 003),
(4, 'L', 004),
(5, 'XL', 005);

-- INSERT COMMANDS FOR JEAN CUTS
INSERT INTO coupe_jean (id_coupe_jean, libelle) VALUES
(1, 'Slim'),
(2, 'Droit'),
(3, 'Bootcut'),
(4, 'Skinny'),
(5, 'Flare');

-- INSERT COMMANDS FOR COLORS
INSERT INTO couleur (id_couleur, libelle, code_couleur) VALUES
(1, 'Bleu', 001),
(2, 'Noir', 002),
(3, 'Gris', 003),
(4, 'Marron', 004),
(5, 'Vert', 005);

-- INSERT COMMANDS FOR JEANS
INSERT INTO jean (id_jean, nom, disponible, prix, description, image, id_coupe_jean) VALUES
(1, 'Slim Fit Blue', 'En stock', 49.99, 'Jean slim en coton bleu', 'jean1.jpg', 1),
(2, 'Classic Black', 'En stock', 59.99, 'Jean droit en denim noir', 'jean2.jpg', 2),
(3, 'Flex Grey Bootcut', 'En stock', 69.99, 'Jean bootcut stretch gris', 'jean3.jpg', 3),
(4, 'Leather Brown Skinny', 'En stock', 79.99, 'Jean skinny en cuir marron', 'jean4.jpg', 4),
(5, 'Flare Green Canvas', 'En stock', 89.99, 'Jean flare en toile verte', 'jean5.jpg', 5);

INSERT INTO ligne_commande(commande_id, vetement_id, prix, quantite) VALUES
(1, 11, 5400, 2),
(2, 15, 179.94, 6),
(3, 9, 12500, 1),
(4, 11, 5400, 2),
(5, 6, 300, 6);


INSERT INTO ligne_panier(utilisateur_id, vetement_id, quantite, prix, date_ajout) VALUES
(1, 13, 2, 39.9, '2023-01-19'),
(1, 2, 2, 150, '2023-01-19'),
(2, 8, 1, 59.99, '2023-01-20'),
(2, 4, 4, 720, '2023-01-19'),
(3, 7, 3, 89.97, '2023-01-19');

# Verif table

DESCRIBE utilisateur;
DESCRIBE etat;
DESCRIBE commande;
DESCRIBE taille;
DESCRIBE type_vetement;
DESCRIBE couleur;
DESCRIBE vetement;
DESCRIBE ligne_commande;
DESCRIBE ligne_panier;

# Verif contenus table

SELECT * FROM utilisateur;
SELECT * FROM etat;
SELECT * FROM commande;
SELECT * FROM taille;
SELECT * FROM coupe_jean;
SELECT * FROM couleur;
SELECT * FROM jean;
SELECT * FROM ligne_commande;
SELECT * FROM ligne_panier;

