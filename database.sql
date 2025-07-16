CREATE DATABASE IF NOT EXISTS sentiment_db;
USE sentiment_db;

CREATE TABLE IF NOT EXISTS emails (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender VARCHAR(255),
    subject TEXT,
    body TEXT,
    sentiment VARCHAR(50),
    highlighted_body TEXT,
    timestamp DATETIME
);
ALTER TABLE emails ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY;

