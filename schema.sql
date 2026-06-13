-- ============================================================
--  EduGenie Database Setup Script
--  Run this in MySQL Workbench or via: mysql -u root -p < schema.sql
-- ============================================================

CREATE DATABASE IF NOT EXISTS edugenie_db;
USE edugenie_db;

-- Users Table
CREATE TABLE IF NOT EXISTS Users (
    user_id        INT AUTO_INCREMENT PRIMARY KEY,
    username       VARCHAR(50)  NOT NULL,
    email          VARCHAR(100) NOT NULL UNIQUE,
    password_hash  VARCHAR(255) NOT NULL,
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Documents Table
CREATE TABLE IF NOT EXISTS Documents (
    doc_id           INT AUTO_INCREMENT PRIMARY KEY,
    user_id          INT NOT NULL,
    file_name        VARCHAR(200) NOT NULL,
    extracted_text   LONGTEXT,
    upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Summaries Table
CREATE TABLE IF NOT EXISTS Summaries (
    summary_id   INT AUTO_INCREMENT PRIMARY KEY,
    doc_id       INT NOT NULL,
    summary_text LONGTEXT,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (doc_id) REFERENCES Documents(doc_id) ON DELETE CASCADE
);

-- Quizzes Table (stores each quiz attempt)
CREATE TABLE IF NOT EXISTS Quizzes (
    quiz_id         INT AUTO_INCREMENT PRIMARY KEY,
    doc_id          INT NOT NULL,
    score           INT NOT NULL DEFAULT 0,
    total_questions INT NOT NULL DEFAULT 5,
    taken_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (doc_id) REFERENCES Documents(doc_id) ON DELETE CASCADE
);
