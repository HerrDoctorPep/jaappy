/*
This file has some useful queries 
that come in handy when managing databases and users
*/

/*
Show databases and users
*/

SELECT Db,Host, User FROM mysql.db;
SELECT USER, host from mysql.user;

/* 
Create user
*/
CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';

/*
Check what is in tables
*/
USE houses_db;
SHOW TABLES;
DESCRIBE houses_detail;

SELECT COUNT(*) FROM houses_detail;
SELECT Type, count(DISTINCT ID) FROM houses_detail GROUP BY Type;
