CREATE DATABASE IF NOT EXISTS book_shop;
USE book_shop;
CREATE TABLE books 
	(
		book_id INT NOT NULL AUTO_INCREMENT,
		title TEXT,
		author_fname TEXT,
		author_lname TEXT,
		released_year INT,
		stock_quantity INT,
		pages INT,
		price INT,    
		PRIMARY KEY(book_id)
	);

INSERT INTO books (title, author_fname, author_lname, released_year, stock_quantity, pages, price)
VALUES
('The Namesake', 'Jhumpa', 'Lahiri', 2003, 32, 291, 250),
('Norse Mythology', 'Neil', 'Gaiman',2016, 43, 304, 599),
('American Gods', 'Neil', 'Gaiman', 2001, 12, 465, 799),
('Interpreter of Maladies', 'Jhumpa', 'Lahiri', 1996, 97, 198, 1999),
('A Hologram for the King: A Novel', 'Dave', 'Eggers', 2012, 154, 352, 700),
('The Circle', 'Dave', 'Eggers', 2013, 26, 504, 600),
('The Amazing Adventures of Kavalier & Clay', 'Michael', 'Chabon', 2000, 68, 634, 1000),
('Just Kids', 'Patti', 'Smith', 2010, 55, 304, 150),
('A Heartbreaking Work of Staggering Genius', 'Dave', 'Eggers', 2001, 104, 437, 190),
('Coraline', 'Neil', 'Gaiman', 2003, 100, 208, 880),
('What We Talk About When We Talk About Love: Stories', 'Raymond', 'Carver', 1981, 23, 176, 500),
("Where I'm Calling From: Selected Stories", 'Raymond', 'Carver', 1989, 12, 526, 600),
('White Noise', 'Don', 'DeLillo', 1985, 49, 320, 770),
('Cannery Row', 'John', 'Steinbeck', 1945, 95, 181, 10000),
('Oblivion: Stories', 'David', 'Foster Wallace', 2004, 172, 329, 520),
('Consider the Lobster', 'David', 'Foster Wallace', 2005, 92, 343, 330);
