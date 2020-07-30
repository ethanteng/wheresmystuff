CREATE TABLE users (
  id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  firstname VARCHAR(30) NOT NULL,
  lastname VARCHAR(30) NOT NULL,
  email VARCHAR(30) UNIQUE NOT NULL,
  phone VARCHAR(30)
);



CREATE TABLE packages (
  id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  user_id INT(6) UNSIGNED NOT NULL,
  tracking_code VARCHAR(100) NOT NULL,
  carrier VARCHAR(30),
  description VARCHAR(50)
);



CREATE TABLE trackers (
  id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  package_id INT(6) UNSIGNED NOT NULL,
  tracker_id VARCHAR(100) UNIQUE,
  status VARCHAR(100),
  est_delivery_date DATETIME,
  current_city VARCHAR(50),
  current_state VARCHAR(50),
  current_country VARCHAR(50),
  updated_at DATETIME
);



CREATE TABLE amazon_delivery (
  id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  package_id INT(6) UNSIGNED NOT NULL,
  tracking_url VARCHAR(500) UNIQUE,
  status VARCHAR(200),
  updated_at DATETIME
);