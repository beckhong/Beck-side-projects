-- Setting low password policy
SET global validate_password_policy=0;

-- Create database for project1 user
CREATE DATABASE IF NOT EXISTS project1_user;

USE project1_user;

-- Create table
CREATE TABLE IF NOT EXISTS users (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, username TEXT, password TEXT);