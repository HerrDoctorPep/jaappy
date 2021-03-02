CREATE DATABASE IF NOT EXISTS houses_db;

CREATE TABLE IF NOT EXISTS locations(
    Index_ INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Date_ DATE,
    ID_ VARCHAR(255),
    Address_ VARCHAR(255) NOT NULL,
    Zip_ VARCHAR(255),
    ZipCode_ VARCHAR(255),
    Longitude_ FLOAT(9,8),
    Latitude_ FLOAT(9,7)
);

CREATE TABLE IF NOT EXISTS attributes_num(
    Index_ INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
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
    Index_ INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Date_ DATE,
    ID_ VARCHAR(255),
    Balkon_ VARCHAR(255),
    Bijzonderheden_ VARCHAR(255),
    Energielabel_(geschat)_ VARCHAR(255),
    Energieverbruik_(geschat)_ VARCHAR(255),
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
    Index_ INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Date_ DATE,
    ID_ VARCHAR(255),
    Long_description_ TEXT,
    Short_description_ TEXT
);

CREATE TABLE IF NOT EXISTS salesinfo(
    Index_ INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Date_ DATE,
    ID_ VARCHAR(255),
    Broker_ VARCHAR(255),
    Geplaatst_op_ DATE,
    Huidige_vraagprijs_ VARCHAR(255),
    Oorspronkelijke_vraagprijs_ INT,
    Pricetype_ VARCHAR(255),
    Sold_ VARCHAR(255)
);

GRANT ALL PRIVILEGES ON houses_db.* TO 'xxx'@'localhost' IDENTIFIED BY 'xxxxxx';
FLUSH PRIVILEGES;