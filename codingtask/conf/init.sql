-- create databases
CREATE DATABASE IF NOT EXISTS testdb;


-- create user
CREATE USER 'test'@'%' IDENTIFIED WITH mysql_native_password BY 'test';

-- grant priviliges
GRANT ALL ON testdb.* TO 'test'@'%';

FLUSH PRIVILEGES;
