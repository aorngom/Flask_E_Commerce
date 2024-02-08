-- Suppression des tables si elles existent
DROP TABLE IF EXISTS jean;
DROP TABLE IF EXISTS coupe_jean;
DROP TABLE IF EXISTS taille;
DROP TABLE IF EXISTS utilisateur;

-- Création de la table taille
CREATE TABLE taille (
   id_taille INT PRIMARY KEY AUTO_INCREMENT,
   nom_taille VARCHAR(50)
);

-- Création de la table coupe_jean
CREATE TABLE coupe_jean (
   id_coupe_jean INT PRIMARY KEY AUTO_INCREMENT,
   nom_coupe VARCHAR(50)
);

-- Création de la table jean avec les clés étrangères
CREATE TABLE jean (
   id_jean INT PRIMARY KEY AUTO_INCREMENT,
   matiere VARCHAR(50),
   couleur VARCHAR(50),
   description VARCHAR(50),
   marque VARCHAR(50),
   nom_jean VARCHAR(50),
   prix_jean DECIMAL(15,2),
   id_coupe_jean INT NOT NULL,
   id_taille INT NOT NULL,
   image VARCHAR(255), -- Changer la longueur en fonction de vos besoins
   stock INT,
   FOREIGN KEY(id_coupe_jean) REFERENCES coupe_jean(id_coupe_jean),
   FOREIGN KEY(id_taille) REFERENCES taille(id_taille)
);
-- Insertion de données dans la table coupe_jean
INSERT INTO coupe_jean (nom_coupe) VALUES
('Slim Fit'),
('Straight Fit'),
('Skinny Fit'),
('Bootcut'),
('Relaxed Fit');

-- Insertion de données dans la table taille
INSERT INTO taille (nom_taille) VALUES
('Small'),
('Medium'),
('Large'),
('X-Large'),
('XX-Large');

INSERT INTO jean (matiere, couleur, description, marque, nom_jean, prix_jean, id_coupe_jean, id_taille, image, stock)
VALUES
('Denim', 'Blue', 'Slim Fit', 'Brand1', 'Jean1', 59.99, 1, 1, 'jean1.jpg', 50),
('Cotton', 'Black', 'Straight Fit', 'Brand2', 'Jean2', 49.99, 2, 2, 'jean2.jpg', 30),
('Stretch', 'Gray', 'Skinny Fit', 'Brand3', 'Jean3', 69.99, 3, 3, 'jean3.jpg', 20),
('Denim', 'Blue', 'Bootcut', 'Brand1', 'Jean4', 54.99, 4, 1, 'jean4.jpg', 10),
('Cotton', 'Brown', 'Relaxed Fit', 'Brand2', 'Jean5', 44.99, 5, 2, 'jean5.jpg', 15),
('Stretch', 'White', 'Slim Fit', 'Brand3', 'Jean6', 64.99, 1, 3, 'jean6.jpg', 25),
-- Ajoutez 24 inserts supplémentaires en suivant le même modèle avec des numéros d'image différents
('Denim', 'Black', 'Skinny Fit', 'Brand1', 'Jean7', 59.99, 2, 1, 'jean7.jpg', 18),
('Cotton', 'Blue', 'Straight Fit', 'Brand2', 'Jean8', 49.99, 3, 2, 'jean8.jpg', 22),
('Stretch', 'Gray', 'Bootcut', 'Brand3', 'Jean9', 69.99, 4, 3, 'jean9.jpg', 30),
('Denim', 'Brown', 'Relaxed Fit', 'Brand1', 'Jean10', 54.99, 5, 1, 'jean10.jpg', 12),
('Cotton', 'White', 'Slim Fit', 'Brand2', 'Jean11', 44.99, 1, 2, 'jean11.jpg', 40),
('Stretch', 'Black', 'Skinny Fit', 'Brand3', 'Jean12', 64.99, 2, 3, 'jean12.jpg', 25),
('Denim', 'Blue', 'Straight Fit', 'Brand1', 'Jean13', 59.99, 3, 1, 'jean13.jpg', 30),
('Cotton', 'Gray', 'Bootcut', 'Brand2', 'Jean14', 49.99, 4, 2, 'jean14.jpg', 20),
('Stretch', 'Brown', 'Relaxed Fit', 'Brand3', 'Jean15', 69.99, 5, 3, 'jean15.jpg', 15);
-- Ajoutez 15 inserts supplémentaires en suivant le même modèle avec des numéros d'image différents

-- Suppression de la table utilisateur si elle existe
DROP TABLE IF EXISTS utilisateur;

-- Création de la table utilisateur
CREATE TABLE utilisateur (
    id_utilisateur INT PRIMARY KEY AUTO_INCREMENT,
    login VARCHAR(50),
    password VARCHAR(150),
    role VARCHAR(100),
    est_actif TINYINT,
    nom VARCHAR(50),
    email VARCHAR(50)
);

-- Insertion de données dans la table utilisateur
INSERT INTO utilisateur (id_utilisateur, login, email, password, role, nom, est_actif) VALUES
(1, 'admin', 'admin@admin.fr', 'sha256$dPL3oH9ug1wjJqva$2b341da75a4257607c841eb0dbbacb76e780f4015f0499bb1a164de2a893fdbf', 'ROLE_admin', 'admin', 1),
(2, 'client', 'client@client.fr', 'sha256$1GAmexw1DkXqlTKK$31d359e9adeea1154f24491edaa55000ee248f290b49b7420ced542c1bf4cf7d', 'ROLE_client', 'client', 1),
(3, 'client2', 'client2@client2.fr', 'sha256$MjhdGuDELhI82lKY$2161be4a68a9f236a27781a7f981a531d11fdc50e4112d912a7754de2dfa0422', 'ROLE_client', 'client2', 1);
