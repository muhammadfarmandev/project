-- NSOS Database Schema
-- Police Station Management System
-- Created for 2nd Semester Project

-- Create database if it doesn't exist
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'NSOS')
BEGIN
    CREATE DATABASE NSOS;
END
GO

-- Use the NSOS database
USE NSOS;
GO

-- Drop tables if they exist (for testing)
IF OBJECT_ID('AuditLog', 'U') IS NOT NULL DROP TABLE AuditLog;
IF OBJECT_ID('Evidence', 'U') IS NOT NULL DROP TABLE Evidence;
IF OBJECT_ID('CaseUpdate', 'U') IS NOT NULL DROP TABLE CaseUpdate;
IF OBJECT_ID('Duty', 'U') IS NOT NULL DROP TABLE Duty;
IF OBJECT_ID('Case', 'U') IS NOT NULL DROP TABLE Case;
IF OBJECT_ID('Criminal', 'U') IS NOT NULL DROP TABLE Criminal;
IF OBJECT_ID('Officer', 'U') IS NOT NULL DROP TABLE Officer;
IF OBJECT_ID('Unit', 'U') IS NOT NULL DROP TABLE Unit;
IF OBJECT_ID('Admin', 'U') IS NOT NULL DROP TABLE Admin;

-- Unit table for police units
CREATE TABLE Unit (
    unit_id INT PRIMARY KEY IDENTITY(1,1),
    unit_name NVARCHAR(50) NOT NULL UNIQUE
);

-- Admin table for login
CREATE TABLE Admin (
    admin_id INT PRIMARY KEY IDENTITY(1,1),
    username NVARCHAR(50) NOT NULL UNIQUE,
    password_hash NVARCHAR(255) NOT NULL
);

-- Officer table
CREATE TABLE Officer (
    officer_id INT PRIMARY KEY IDENTITY(1,1),
    name NVARCHAR(100) NOT NULL,
    address NVARCHAR(200),
    badge_no NVARCHAR(20) NOT NULL UNIQUE,
    rank NVARCHAR(50),
    contact NVARCHAR(20),
    unit_id INT,
    FOREIGN KEY (unit_id) REFERENCES Unit(unit_id)
);

-- Criminal table
CREATE TABLE Criminal (
    criminal_id INT PRIMARY KEY IDENTITY(1,1),
    name NVARCHAR(100) NOT NULL,
    address NVARCHAR(200),
    cnic NVARCHAR(20) NOT NULL UNIQUE,
    notes NVARCHAR(500)
);

-- Case (FIR) table
CREATE TABLE Case (
    case_id INT PRIMARY KEY IDENTITY(1,1),
    case_number NVARCHAR(50) NOT NULL UNIQUE,
    title NVARCHAR(200) NOT NULL,
    description NVARCHAR(1000),
    filed_date DATE NOT NULL,
    filed_by INT NOT NULL,
    suspect_id INT,
    status NVARCHAR(20) NOT NULL DEFAULT 'Open',
    FOREIGN KEY (filed_by) REFERENCES Officer(officer_id),
    FOREIGN KEY (suspect_id) REFERENCES Criminal(criminal_id)
);

-- CaseUpdate table for progress notes
CREATE TABLE CaseUpdate (
    update_id INT PRIMARY KEY IDENTITY(1,1),
    case_id INT NOT NULL,
    update_text NVARCHAR(1000) NOT NULL,
    update_date DATETIME NOT NULL DEFAULT GETDATE(),
    updated_by INT NOT NULL,
    FOREIGN KEY (case_id) REFERENCES Case(case_id),
    FOREIGN KEY (updated_by) REFERENCES Officer(officer_id)
);

-- Evidence table
CREATE TABLE Evidence (
    evidence_id INT PRIMARY KEY IDENTITY(1,1),
    case_id INT NOT NULL,
    file_name NVARCHAR(255) NOT NULL,
    description NVARCHAR(500),
    upload_date DATETIME NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (case_id) REFERENCES Case(case_id)
);

-- Duty table for duty assignments
CREATE TABLE Duty (
    duty_id INT PRIMARY KEY IDENTITY(1,1),
    officer_id INT NOT NULL,
    duty_date DATE NOT NULL,
    duty_time TIME NOT NULL,
    location NVARCHAR(200) NOT NULL,
    FOREIGN KEY (officer_id) REFERENCES Officer(officer_id)
);

-- AuditLog table for tracking actions
CREATE TABLE AuditLog (
    log_id INT PRIMARY KEY IDENTITY(1,1),
    action NVARCHAR(20) NOT NULL,
    table_name NVARCHAR(50) NOT NULL,
    record_id INT NOT NULL,
    action_date DATETIME NOT NULL DEFAULT GETDATE()
);

-- Insert sample data

-- Units
INSERT INTO Unit (unit_name) VALUES ('Investigation');
INSERT INTO Unit (unit_name) VALUES ('Patrol');
INSERT INTO Unit (unit_name) VALUES ('Admin');

-- Admin (password: admin123)
-- NOTE: Run setup_admin.py to generate the proper password hash
-- Then update the password_hash value below with the generated hash
-- For now, using a placeholder - you MUST update this before first login
INSERT INTO Admin (username, password_hash) VALUES ('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYq5q5q5q5q');

-- Officers
INSERT INTO Officer (name, address, badge_no, rank, contact, unit_id) 
VALUES ('John Smith', '123 Main St, City', 'BADGE001', 'Inspector', '0300-1234567', 1);

INSERT INTO Officer (name, address, badge_no, rank, contact, unit_id) 
VALUES ('Sarah Khan', '456 Park Ave, City', 'BADGE002', 'Sub-Inspector', '0300-2345678', 2);

INSERT INTO Officer (name, address, badge_no, rank, contact, unit_id) 
VALUES ('Ahmed Ali', '789 Station Rd, City', 'BADGE003', 'Constable', '0300-3456789', 1);

-- Criminals
INSERT INTO Criminal (name, address, cnic, notes) 
VALUES ('Ali Hassan', '100 Crime St, City', '12345-1234567-1', 'Previous theft cases');

INSERT INTO Criminal (name, address, cnic, notes) 
VALUES ('Bilal Ahmed', '200 Illegal Ave, City', '23456-2345678-2', 'Suspected in multiple robberies');

-- Cases
INSERT INTO Case (case_number, title, description, filed_date, filed_by, suspect_id, status) 
VALUES ('FIR-2025-001', 'Theft at Market', 'Reported theft of goods from local market', '2025-01-01', 1, 1, 'Open');

INSERT INTO Case (case_number, title, description, filed_date, filed_by, suspect_id, status) 
VALUES ('FIR-2025-002', 'Robbery Case', 'Armed robbery at bank', '2025-01-02', 2, 2, 'Open');

-- Case Updates
INSERT INTO CaseUpdate (case_id, update_text, update_date, updated_by) 
VALUES (1, 'Initial investigation started. Evidence collected from scene.', '2025-01-01 10:00:00', 1);

INSERT INTO CaseUpdate (case_id, update_text, update_date, updated_by) 
VALUES (1, 'Suspect questioned. Awaiting further evidence.', '2025-01-02 14:30:00', 1);

-- Duties
INSERT INTO Duty (officer_id, duty_date, duty_time, location) 
VALUES (1, '2025-01-10', '08:00:00', 'Main Station');

INSERT INTO Duty (officer_id, duty_date, duty_time, location) 
VALUES (2, '2025-01-10', '14:00:00', 'City Patrol');

