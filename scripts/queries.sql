USE Sitters_nannies;

-- 1. List all users with their userID,name, email addresses, age and addresses that are more than 30 years old.
SELECT userID,fullname,email,address,birthdate,(YEAR(NOW()) - YEAR(birthdate)) AS Age
FROM User
HAVING Age > 30;

-- Q2. List all users with their userID, name and userType. Since userType is a new column

SELECT userID,fullname, CASE 
        WHEN userID IN (SELECT userID FROM Nanny) THEN 'Nanny'
        ELSE 'Family Representative'
    END AS userType
FROM User;

-- Q3. Find the name and age of the oldest child.

SELECT child_name, (YEAR(NOW()) - YEAR(birth_date)) AS Age
FROM Child
HAVING Age = (SELECT  Max((YEAR(NOW()) - YEAR(birth_date)))
FROM Child);

-- Q4. Show the details of users who have a family representative role.

SELECT U.*, Fam.occupation,Fam.marital_status
FROM Family_rep Fam LEFT JOIN User U ON (Fam.userID = U.userID);

-- Q5. List all contracts along with their start dates and end dates.

SELECT start_date, end_date
FROM CONTRACT;

-- Q6. Retrieve the names of users who have signed contracts as family representatives.
SELECT *
FROM Family_rep_sign_contract C INNER JOIN User U ON (C.userID = U.userID);

-- A left join on Family_rep_sign_contract against User can work too

SELECT *
FROM Family_rep_sign_contract C LEFT JOIN User U ON (C.userID = U.userID);

-- Q7. Find the distinct skills that nannies possess.

SELECT DISTINCT(skill)
FROM Nanny_skill;

-- Q8. Show the details of users who have preferences for children.

SELECT *
FROM Child_Preferences C LEFT JOIN User U ON (U.userID = C.userID);

-- Q9. Find the count of nannies for each gender.

SELECT gender, count(gender) AS 'No. of nanny by gender'
FROM Nanny
GROUP BY gender;

-- Q10. List the names and preferences (With or without) of children with their 
-- family rep name who have disabilities or no disabilities.

SELECT C.child_name,CP.preference,CD.disability,U.fullname
FROM ((Child C LEFT JOIN Child_Preferences CP ON (C.child_key =CP.child_key AND C.userID = CP.userID))
	LEFT JOIN Child_Disability CD ON (C.child_key =CD.child_key AND C.userID = CD.userID)) LEFT JOIN 
    User U ON (C.userID = U.userID);


-- Q11. Find the number of children for each family representative.

SELECT fullname,COUNT(fullname) AS 'No. children'
FROM Child C LEFT JOIN User U ON (U.userID = C.userID)
GROUP BY U.fullname,U.UserID;

-- Q12. List all users who are parents (have children).

-- Left join childern table with the parent table

SELECT DISTINCT F.fullname AS 'Parent'
FROM Child C 
LEFT JOIN User F ON (F.userID = C.userID);

-- Q13. Find all nannies who have specific skills. 'Child Care', 'First Aid'

SELECT DISTINCT U.fullname AS 'Nannies with specific skill'
FROM User U 
JOIN Nanny N on (U.userID = N.userID)
LEFT JOIN Nanny_skill NS on (NS.userID = N.userID)
WHERE NS.skill IN ('Child Care', 'First Aid');

-- Q14. Find all contracts where a child has preferences.

SELECT distinct F.contractID
FROM Family_rep_sign_contract F
JOIN Child_Preferences C ON (F.child_key = C.child_key AND F.userID = C.userID);

-- Q15. Find the average age of parents.

-- Creating view for parent_details

CREATE VIEW parent_details AS
SELECT U.*,F.occupation,F.marital_status,YEAR(NOW()) - YEAR(birthdate) AS Age
FROM Family_rep F
JOIN User U ON F.userID = U.userID;

-- finding Average age

SELECT round(avg(Age))
FROM parent_details;

-- Q16. Find the most common preference among children. 

With preference_occurrances as (
	SELECT preference,COUNT(preference) AS occurrances
	FROM Child_Preferences
	GROUP BY preference
)SELECT *
	FROM preference_occurrances
	WHERE occurrances = (SELECT Max(occurrances) FROM preference_occurrances);

-- Q17. Find the total pay for each schedule.

With Pay_schedule AS(
SELECT *,hour_worked * pay_per_hour as pay_schedule
	FROM (SELECT C.contractID,TIMESTAMPDIFF(HOUR,CS.start_date_time,CS.end_date_time) as hour_worked,C.pay_per_hour
		FROM Contract C
		JOIN Contract_schedule CS ON C.contractID = CS.contractID) 
        AS hour_worked_query
) SELECT *
FROM Pay_schedule P;

-- Q18. Find the total pay for each contract.

SELECT contractID,SUM(pay_schedule) contract_pay
FROM Pay_schedule
GROUP BY contractID;


-- Q19. The highest paid Nanny per hour.
SELECT highest_pay.*,U.fullname
FROM (
	SELECT NC.contractID,NC.userID,MAX(pay_per_hour)  Pay
	FROM Contract C 
	JOIN Nanny_sign_contract NC
	ON NC.contractID = C.contractID
	GROUP BY NC.contractID,NC.userID) AS highest_pay 
LEFT JOIN User U
ON U.userID = highest_pay.userID;

-- Q20. Find all single parent with full details.

SELECT *
FROM User U
JOIN (SELECT *
	FROM Family_rep F
	WHERE F.marital_status = "single") AS single_fam
ON U.userID = single_fam.userID



Select u.userID,address,fullname,birthdate,occupation,marital_status,highest_edu,gender,availability,   CASE 
        WHEN f.userID IS NOT NULL THEN 'family_rep'
        WHEN n.userID IS NOT NULL THEN 'nanny'
    END AS role
From User u
Left Join Family_rep f
On u.userID = f.userID
Left join Nanny n
On n.userID = u.userID



Select c.contractID,start_date,end_date,pay_per_hour,f.userID as family_rep_id,n.userID as nanny_id
From Contract c
Join Family_rep_sign_contract f
On c.contractID = f.contractID
Join Nanny_sign_contract n
On c.contractID = n.contractID
    