DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  mode BIT 
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

-- Create fake data to populate the database
-- User password == 123
INSERT INTO user (username, password, mode) 
VALUES 
  ('Travis', 'pbkdf2:sha256:600000$vpikcbo6ftzgAA2a$d3afea41f2afa195aa5b09c78406f4865c7eb9efec09cda6f4c04eef9e662a64', 0),
  ('Kyle', 'pbkdf2:sha256:600000$vpikcbo6ftzgAA2a$d3afea41f2afa195aa5b09c78406f4865c7eb9efec09cda6f4c04eef9e662a64', 1);

INSERT INTO post (title, body, author_id) 
VALUES 
  ('Test Title', 'Test Body', 1),
  ('Test Title', 'Test Body', 2);