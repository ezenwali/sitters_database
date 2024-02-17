USE Sitters_nannies;

-- Inserting data into the User table
INSERT INTO User (email, address, fullname, birthdate, mobile_number) VALUES 
('user1@example.com', '23 Main St', 'John Wick', '1990-01-15', '123-456-7890'),
('user2@example.com', '123 Main St', 'Mary', '1995-01-15', '123-456-790'),
('user5@example.com', '111 Maple St', 'Sophie Turner', '1993-02-21', '111-222-3333'),
('user6@example.com', '222 Cedar St', 'Michael Johnson', '1986-06-10', '222-333-4444'),
('user7@example.com', '333 Oak St', 'Emma Watson', '1995-04-15', '333-444-5555'),
('user8@example.com', '444 Pine St', 'Ryan Reynolds', '1980-10-23', '444-555-6666'),
('user9@example.com', '555 Elm St', 'Ava Martinez', '1998-08-05', '555-666-7777');

-- Inserting data into the Family_rep table
INSERT INTO Family_rep (userID, occupation, marital_status) VALUES 
(1, 'Engineer', 'Married'),
(3, 'Doctor', 'Single'),
(4, 'Unemployed', 'Single'),
(5, 'Unemployed', 'Single'),
(6, 'Teacher', 'Single');


-- Inserting data into the Nanny table
INSERT INTO Nanny (userID, ssn, highest_edu, gender, availability) VALUES
 (2, '123-45-6789', 'Bachelor of Science', 'Female', 'Full-time'),
 (7, '113-05-6729', 'Bachelor of AArt', 'Male', 'Part-time');

-- Inserting  data into the Nanny_skill table
INSERT INTO Nanny_skill (userID, skill) VALUES
(2, 'Child Care'),
(2, 'First Aid');

-- Insert data into Contract table
INSERT INTO Contract (start_date, end_date, pay_per_hour)
VALUES ('2023-01-01', '2023-12-31', 32.50);

-- Insert sample data into the Contract_schedule table
INSERT INTO Contract_schedule (contractID, start_date_time, end_date_time, description) VALUES 
(1, '2023-01-01 08:00:00', '2023-01-01 17:00:00', 'Monday Schedule please walk john for 1 hour'),
(1, '2023-01-01 19:00:00', '2023-01-01 21:00:00', 'Monday Schedule please take john for dinner');

-- Insert sample data into the Child table
INSERT INTO Child (userID, birth_date, child_name, gender) VALUES
(1, '2010-05-10', 'John Jr', 'Male'),
(1, '2013-08-22', 'Emily', 'Female'),
(3, '2015-02-18', 'Olivia', 'Female'),
(4, '2018-09-30', 'Michael', 'Male'),
(6, '2012-07-14', 'Liam', 'Male');

-- Insert sample data into the Child_Preferences table
INSERT INTO Child_Preferences (child_key, userID, preference) VALUES 
(1, 1, 'Play outdoors'),
(1,1,'Likes watching tv shows'),
(2,1,'Likes watching tv shows');

-- Insert sample data into the Child_Disability table
INSERT INTO Child_Disability (child_key, userID, disability) VALUES
 (1, 1, 'Allergy to peanuts'),
(3, 3, 'Allergy to peanuts');


-- Insert sample data into the Family_rep_sign_contract table
INSERT INTO Family_rep_sign_contract (child_key, userID, contractID)
VALUES (1, 1, 1);

-- Insert sample data into the Nanny_sign_contract table
INSERT INTO Nanny_sign_contract (userID, contractID)
VALUES (2, 1);
