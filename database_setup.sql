-- Database Setup Script for Hostel Management System
-- Run this script to initialize the database structure

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS mydb;
USE mydb;

-- Create users table for authentication
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') DEFAULT 'user',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email)
);

-- Create/Update hostel table with enhanced schema
CREATE TABLE IF NOT EXISTS hostel (
    BedNo INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    StudentID VARCHAR(50),
    Contact VARCHAR(20),
    Email VARCHAR(100),
    CheckInDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    PaymentStatus ENUM('Paid', 'Pending') DEFAULT 'Pending',
    INDEX idx_name (Name),
    INDEX idx_student_id (StudentID),
    INDEX idx_payment (PaymentStatus)
);

-- If hostel table already exists with old schema, migrate it
-- This will preserve existing data
ALTER TABLE hostel 
    MODIFY COLUMN Name VARCHAR(100) NOT NULL,
    ADD COLUMN IF NOT EXISTS StudentID VARCHAR(50) AFTER Name,
    ADD COLUMN IF NOT EXISTS Contact VARCHAR(20) AFTER StudentID,
    ADD COLUMN IF NOT EXISTS Email VARCHAR(100) AFTER Contact,
    ADD COLUMN IF NOT EXISTS CheckInDate DATETIME DEFAULT CURRENT_TIMESTAMP AFTER Email,
    ADD COLUMN IF NOT EXISTS PaymentStatus ENUM('Paid', 'Pending') DEFAULT 'Pending' AFTER CheckInDate;

-- Create index on CheckInDate for better query performance
CREATE INDEX IF NOT EXISTS idx_checkin ON hostel(CheckInDate);

