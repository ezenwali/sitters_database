-- DROPPING the database
DROP DATABASE IF EXISTS Sitters_nannies; 


-- Create the database
CREATE DATABASE Sitters_nannies;

-- Activating Sitters
USE Sitters_nannies;

-- Create the User table
CREATE TABLE User (
    userID INT AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    address VARCHAR(255) NOT NULL,
    fullname VARCHAR(255) NOT NULL,
    birthdate DATE NOT NULL,
    mobile_number VARCHAR(15) NOT NULL,
    createdAt DATE NOT NULL,
    
    PRIMARY KEY(userID)
);

-- Create the Family_rep table
CREATE TABLE Family_rep (
    userID INT NOT NULL,
    occupation VARCHAR(255) NOT NULL,
    marital_status VARCHAR(20) NOT NULL,
    
    PRIMARY KEY(userID),
	FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE
);

-- Create the Nanny table
CREATE TABLE Nanny (
    userID INT PRIMARY KEY,
    ssn VARCHAR(11) NOT NULL,
    highest_edu VARCHAR(255),
    gender VARCHAR(10) NOT NULL,
    availability VARCHAR(255) NOT NULL,
    
    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE
);

-- Create the Nanny_skill table
CREATE TABLE Nanny_skill (
    userID INT,
    skill VARCHAR(255),
    
    PRIMARY KEY (userID, skill),
    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE
);

-- Create the Contract table
CREATE TABLE Contract (
    contractID INT AUTO_INCREMENT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    pay_per_hour DECIMAL(10, 2) NOT NULL,
    
    PRIMARY KEY(contractID)
);

-- Create the Contract_schedule table
CREATE TABLE Contract_schedule (
    contractID INT,
    start_date_time DATETIME,
    end_date_time DATETIME NOT NULL,
    description VARCHAR(255),
    
    PRIMARY KEY (contractID, start_date_time),
    FOREIGN KEY (contractID) REFERENCES Contract(contractID) ON DELETE CASCADE
);

-- Create the Child table
CREATE TABLE Child (
    child_key INT AUTO_INCREMENT,
    userID INT,
    birth_date DATE NOT NULL,
    child_name VARCHAR(255) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    
	PRIMARY KEY (child_key, userID),
    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE
);

-- Create the Child_Preferences table
CREATE TABLE Child_Preferences (
    child_key INT,
    userID INT,
    preference VARCHAR(255) NOT NULL,
    
    PRIMARY KEY (child_key, userID, preference),
	-- change to the one from MYsql
    FOREIGN KEY (child_key, userID) REFERENCES Child(child_key, userID) ON DELETE CASCADE
);

-- Create the Child_Disability table
CREATE TABLE Child_Disability (
    child_key INT,
    userID INT,
    disability VARCHAR(255),
    
    PRIMARY KEY (child_key, userID, disability),
	-- change to the one from MYsql
    FOREIGN KEY (child_key,userID) REFERENCES Child(child_key,userID) ON DELETE CASCADE
);

-- Create the Family_rep_sign_contract table
CREATE TABLE Family_rep_sign_contract (
    child_key INT,
    userID INT,
    contractID INT,
    
    PRIMARY KEY (contractID),
    FOREIGN KEY (child_key) REFERENCES Child(child_key) ON DELETE CASCADE,
    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE,
    FOREIGN KEY (contractID) REFERENCES Contract(contractID) ON DELETE CASCADE
);

-- Create the Nanny_sign_contract table
CREATE TABLE Nanny_sign_contract (
    userID INT,
    contractID INT,
    
    PRIMARY KEY (contractID),
    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE,
    FOREIGN KEY (contractID) REFERENCES Contract(contractID) ON DELETE CASCADE
);
