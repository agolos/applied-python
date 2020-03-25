CREATE TABLE IF NOT EXISTS users (user_id INT AUTO_INCREMENT PRIMARY KEY,
user_name CHAR(255), 
password CHAR(255),
create_date TIMESTAMP  DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE IF NOT EXISTS blogs (blog_id INT AUTO_INCREMENT PRIMARY KEY,
user_id INT,
FOREIGN KEY (user_id) REFERENCES users(user_id),
available BOOL,
blog_name CHAR(255),
create_date TIMESTAMP  DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE IF NOT EXISTS posts (post_id INT AUTO_INCREMENT PRIMARY KEY,
post_header CHAR(255),
post_text TEXT,
create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE IF NOT EXISTS post_blog(post_id INT,
FOREIGN KEY (post_id) REFERENCES posts(post_id),
blog_id INT,
FOREIGN KEY (blog_id) REFERENCES blogs(blog_id));

CREATE table IF NOT EXISTS comments(comment_id INT AUTO_INCREMENT PRIMARY KEY,
post_id INT,
FOREIGN KEY (post_id) REFERENCES posts(post_id),
comment_text CHAR(255),
create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE IF NOT EXISTS users_comments (
user_id INT,
FOREIGN KEY (user_id) REFERENCES users(user_id),
comment_id INT,
FOREIGN KEY (comment_id) REFERENCES comments(comment_id));

CREATE TABLE IF NOT EXISTS comments_tree (
comment_id_parent INT,
FOREIGN KEY (comment_id_parent) REFERENCES comments(comment_id),
comment_id_chaild INT,
FOREIGN KEY (comment_id_chaild) REFERENCES comments(comment_id));