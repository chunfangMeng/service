Alter user 'dbuser'@'%' IDENTIFIED WITH mysql_native_password BY 'password';
GRANT ALL PRIVILEGES ON service_db.* TO 'dbuser'@'%';
FLUSH PRIVILEGES;