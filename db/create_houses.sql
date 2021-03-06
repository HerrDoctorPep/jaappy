CREATE DATABASE IF NOT EXISTS houses_db;

USE houses_db;

CREATE TABLE IF NOT EXISTS locations(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Date_ DATE,
    ID_ VARCHAR(255),
    Address_ VARCHAR(255) NOT NULL,
    Zip_ VARCHAR(255),
    ZipCode_ VARCHAR(255),
    Longitude_ FLOAT(9,8),
    Latitude_ FLOAT(9,7)
);

CREATE TABLE IF NOT EXISTS attributes_num(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Date_ DATE,
    ID_ VARCHAR(255),
    Bouwjaar_ INT,
    Inhoud_ INT,
    Kamers_ INT,
    Perceeloppervlakte_ INT,
    Slaapkamers_ INT,
    Woonoppervlakte_ INT
);

CREATE TABLE IF NOT EXISTS attributes_str(
    id_ INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Date_ DATE,
    ID_ VARCHAR(255),
    Balkon_ VARCHAR(255),
    Bijzonderheden_ VARCHAR(255),
    Energielabel_ VARCHAR(255),
    Energieverbruik_ VARCHAR(255),
    Garage_ VARCHAR(255),
    Isolatie_ VARCHAR(255),
    Keuken_ VARCHAR(255),
    Staat_onderhoud_ VARCHAR(255),
    Staat_schilderwerk_ VARCHAR(255),
    Tuin_ VARCHAR(255),
    Type_ VARCHAR(255),
    Uitzicht_ VARCHAR(255),
    Verwarming_ VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS attributes_txt(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Date_ DATE,
    ID_ VARCHAR(255),
    Long_description_ TEXT,
    Short_description_ TEXT
);

CREATE TABLE IF NOT EXISTS salesinfo(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Date_ DATE,
    ID_ VARCHAR(255),
    Broker_ VARCHAR(255),
    Geplaatst_op_ DATE,
    Huidige_vraagprijs_ VARCHAR(255),
    Oorspronkelijke_vraagprijs_ INT,
    Pricetype_ VARCHAR(255),
    Sold_ VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS postcode_geo_roffa (
            id INT NOT NULL AUTO_INCREMENT,
            PostCode VARCHAR(255) NOT NULL,
            Latitude FLOAT(9,7),
            Longitude FLOAT(9,8),
            PRIMARY KEY (id)
);

LOAD DATA INFILE 'postcode_roffa_geo.csv'
INTO TABLE postcode_geo_roffa
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '/n'
IGNORE 1 ROWS;

/*
GRANT ALL PRIVILEGES ON houses_db.* TO 'xxx'@'localhost' IDENTIFIED BY 'xxxxxx';
FLUSH PRIVILEGES;
*/
