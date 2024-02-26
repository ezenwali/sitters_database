import random
import string
import mysql.connector
from faker import Faker
import datetime

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Desinho20@",
    port="3306",
    database="Sitters_nannies"
)

# Create cursor
cursor = db.cursor()

# Function to generate random date within a range
def random_date(start, end):
    return start + datetime.timedelta(
        seconds=random.randint(0, int((end - start).total_seconds()))
    )

# Function to generate random mobile number
def random_mobile_number():
    return ''.join(random.choices(string.digits, k=10))

# Generate 50 users
fake = Faker()
for _ in range(50):
    email = fake.email()
    address = fake.address()
    fullname = fake.name()
    birthdate = fake.date_of_birth(minimum_age=18, maximum_age=70)
    mobile_number = random_mobile_number()
    
    # Insert user into User table
    insert_user_query = "INSERT INTO User (email, address, fullname, birthdate, mobile_number) VALUES (%s, %s, %s, %s, %s)"
    user_data = (email, address, fullname, birthdate, mobile_number)
    cursor.execute(insert_user_query, user_data)
    db.commit()

    # Retrieve the userID of the last inserted user
    user_id = cursor.lastrowid
    
    # Determine if the user is a family representative or a nanny
    is_family_rep = random.choice([True, False])
    
    if is_family_rep:
        occupation = fake.job()
        marital_status = random.choice(["Single", "Married", "Divorced", "Widowed"])
        
        # Insert family representative into Family_rep table
        insert_family_rep_query = "INSERT INTO Family_rep (userID, occupation, marital_status) VALUES (%s, %s, %s)"
        family_rep_data = (user_id, occupation, marital_status)
        cursor.execute(insert_family_rep_query, family_rep_data)
        db.commit()
        
        # Generate random number of children (1-4)
        num_children = random.randint(1, 4)
        for _ in range(num_children):
            child_name = fake.first_name()
            gender = random.choice(["Male", "Female"])
            child_birthdate = fake.date_of_birth(minimum_age=0, maximum_age=18)
            
            # Insert child into Child table
            insert_child_query = "INSERT INTO Child (userID, birth_date, child_name, gender) VALUES (%s, %s, %s, %s)"
            child_data = (user_id, child_birthdate, child_name, gender)
            cursor.execute(insert_child_query, child_data)
            db.commit()
            
            # Retrieve the child_key of the last inserted child
            child_key = cursor.lastrowid
            
            # Generate random number of preferences (1-4)
            num_preferences = random.randint(1, 4)
            for _ in range(num_preferences):
                preference = fake.text(max_nb_chars=100)
                # Insert child's preference into Child_Preferences table
                insert_preference_query = "INSERT INTO Child_Preferences (child_key, userID, preference) VALUES (%s, %s, %s)"
                preference_data = (child_key, user_id, preference)
                cursor.execute(insert_preference_query, preference_data)
                db.commit()
            
            # Generate random number of disabilities (1-4)
            num_disabilities = random.randint(1, 4)
            for _ in range(num_disabilities):
                disability = fake.text(max_nb_chars=100)
                # Insert child's disability into Child_Disability table
                insert_disability_query = "INSERT INTO Child_Disability (child_key, userID, disability) VALUES (%s, %s, %s)"
                disability_data = (child_key, user_id, disability)
                cursor.execute(insert_disability_query, disability_data)
                db.commit()
                
                
    else:
        ssn = fake.ssn()
        highest_edu = random.choice(["High School", "Bachelor's Degree", "Master's Degree", "PhD"])
        gender = random.choice(["Male", "Female"])
        availability = fake.text(max_nb_chars=100)
        
        # Insert nanny into Nanny table
        insert_nanny_query = "INSERT INTO Nanny (userID, ssn, highest_edu, gender, availability) VALUES (%s, %s, %s, %s, %s)"
        nanny_data = (user_id, ssn, highest_edu, gender, availability)
        cursor.execute(insert_nanny_query, nanny_data)
        db.commit()
        
        # Generate random skills for nannies (1-3 skills)
        num_skills = random.randint(1, 3)
        for _ in range(num_skills):
            skill = fake.job()
            # Insert nanny's skill into Nanny_skill table
            insert_skill_query = "INSERT INTO Nanny_skill (userID, skill) VALUES (%s, %s)"
            skill_data = (user_id, skill)
            cursor.execute(insert_skill_query, skill_data)
            db.commit()




cursor.execute("""
    SELECT fr.userID, c.child_key
    FROM Family_rep fr
    JOIN Child c ON fr.userID = c.userID
""")
family_representatives = cursor.fetchall()

contracts_to_generate = random.randint(50, 100)
family_representatives_for_contracts = random.sample(family_representatives, contracts_to_generate)


for fr_id, child_key in family_representatives_for_contracts:
    start_date = datetime.datetime(2022, 1, 1)  # Start date range
    end_date = datetime.datetime(2024, 2, 25)  # End date range
    contract_start_date = random_date(start_date, end_date)
    contract_end_date = random_date(contract_start_date, end_date)
    pay_per_hour = round(random.uniform(10, 50), 2)  # Random pay per hour between $10 and $50
    
    # Insert contract into Contract table
    insert_contract_query = "INSERT INTO Contract (start_date, end_date, pay_per_hour) VALUES (%s, %s, %s)"
    contract_data = (contract_start_date.date(), contract_end_date.date(), pay_per_hour)
    cursor.execute(insert_contract_query, contract_data)
    db.commit()
    
    # Retrieve the contractID of the last inserted contract
    contract_id = cursor.lastrowid
    
    # Insert contract into Family_rep_sign_contract table
    insert_fr_contract_query = "INSERT INTO Family_rep_sign_contract (child_key, userID, contractID) VALUES (%s, %s, %s)"
    fr_contract_data = (child_key, fr_id, contract_id)
    cursor.execute(insert_fr_contract_query, fr_contract_data)
    db.commit()
    
    
# Close cursor and database connection
cursor.close()
db.close()