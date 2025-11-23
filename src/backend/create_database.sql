CREATE DATABASE IF NOT EXISTS recruit_AI;
USE recruit_AI;

CREATE TABLE files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filepath VARCHAR(255) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE conversations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE conversation_text (
    id INT AUTO_INCREMENT PRIMARY KEY,
    conversation_id INT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sent_by_AI BOOLEAN NOT NULL,
    text TEXT NOT NULL,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);

CREATE TABLE files_in_text (
    text_id INT NOT NULL,
    file_id INT NOT NULL,
    FOREIGN KEY (text_id) REFERENCES conversation_text(id)
    FOREIGN KEY (file_id) REFERENCES files(id)
);