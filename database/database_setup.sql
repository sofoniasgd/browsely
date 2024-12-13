-- Create the database
CREATE DATABASE IF NOT EXISTS browsely_db;

-- Use the database
USE browsely_db;

-- Create the table
CREATE TABLE IF NOT EXISTS files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    location VARCHAR(50) NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    root_directory VARCHAR(255) NOT NULL,
    UNIQUE (id)
);

-- Create the users
CREATE USER IF NOT EXISTS 'browsely_sys'@'localhost' IDENTIFIED BY 'browsely_sys_pwd';
CREATE USER IF NOT EXISTS 'browsely_admin'@'localhost' IDENTIFIED BY 'browsely_admin_pwd';

-- Grant privileges to the users
GRANT ALL PRIVILEGES ON browsely_db.* TO 'browsely_sys'@'localhost';
GRANT ALL PRIVILEGES ON browsely_db.* TO 'browsely_admin'@'localhost';

-- Apply the changes
FLUSH PRIVILEGES;