import random
import string
import mysql.connector
from faker import Faker
import datetime
from helper import generate_random_preferences,generate_random_disabilities,generate_random_skills

# Connect to MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Desinho20@",
    port="3306",
)

# Create cursor
cursor = db_connection.cursor()

# Read the SQL queries from file
with open('/Users/shedrach/projects/sitters_database/scripts/sitters_ddl.sql', 'r') as file:
    create_tables_queries = file.read()

try:
  # Split SQL queries by semicolon
    queries = create_tables_queries.split(';')
    for query in queries:
        # Skip empty queries
        if not query.strip():
            continue
        # Execute the SQL query to create the table
        cursor.execute(query)
    # Commit changes
    db_connection.commit()
    
    print("Tables created successfully!")
except mysql.connector.Error as err:
    print("Error creating tables:", err)
    print("SQL queries:", create_tables_queries)

db_connection.database = "Sitters_nannies"

# Function to generate random date within a range
def random_date(start, end):
    return start + datetime.timedelta(
        seconds=random.randint(0, int((end - start).total_seconds()))
    )

# Function to generate a random time within a day
def random_time():
    return datetime.time(random.randint(0, 23), random.randint(0, 59))

# Function to generate random mobile number
def random_mobile_number():
    return ''.join(random.choices(string.digits, k=10))

# Generate 250 users
fake = Faker()
for iter in range(200):
    email = str(iter)+fake.email()
    address = fake.address()
    fullname = fake.name()
    birthdate = fake.date_of_birth(minimum_age=18, maximum_age=70)
    mobile_number = random_mobile_number()
    
    # Insert user into User table
    insert_user_query = "INSERT INTO User (email, address, fullname, birthdate, mobile_number) VALUES (%s, %s, %s, %s, %s)"
    user_data = (email, address, fullname, birthdate, mobile_number)
    cursor.execute(insert_user_query, user_data)
    db_connection.commit()

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
        db_connection.commit()
        
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
            db_connection.commit()
            
            # Retrieve the child_key of the last inserted child
            child_key = cursor.lastrowid
            
            # Generate random number of preferences 
            for preference in generate_random_preferences():
                insert_preference_query = "INSERT INTO Child_Preferences (child_key, userID, preference) VALUES (%s, %s, %s)"
                preference_data = (child_key, user_id, preference)
                cursor.execute(insert_preference_query, preference_data)
                db_connection.commit()
            
            # Generate random number of disabilities:
            for disability in generate_random_disabilities():
                insert_disability_query = "INSERT INTO Child_Disability (child_key, userID, disability) VALUES (%s, %s, %s)"
                disability_data = (child_key, user_id, disability)
                cursor.execute(insert_disability_query, disability_data)
                db_connection.commit()
                
                
    else:
        ssn = fake.ssn()
        highest_edu = random.choice(["High School", "Bachelor's Degree", "Master's Degree", "PhD"])
        gender = random.choice(["Male", "Female"])
        availability = fake.text(max_nb_chars=100)
        
        # Insert nanny into Nanny table
        insert_nanny_query = "INSERT INTO Nanny (userID, ssn, highest_edu, gender, availability) VALUES (%s, %s, %s, %s, %s)"
        nanny_data = (user_id, ssn, highest_edu, gender, availability)
        cursor.execute(insert_nanny_query, nanny_data)
        db_connection.commit()
        
        # Generate random skills for nannies 
        for skill in generate_random_skills():
            insert_skill_query = "INSERT INTO Nanny_skill (userID, skill) VALUES (%s, %s)"
            skill_data = (user_id, skill)
            cursor.execute(insert_skill_query, skill_data)
            db_connection.commit()



# Fetch familyRep',childern user IDs
cursor.execute("""
    SELECT fr.userID, c.child_key
    FROM Family_rep fr
    JOIN Child c ON fr.userID = c.userID
""")
family_representatives = cursor.fetchall()

# Fetch nannies' user IDs
cursor.execute("SELECT userID FROM Nanny")
nanny_ids = [row[0] for row in cursor.fetchall()]


contracts_to_generate = random.randint(350, 500)

family_representatives_for_contracts = random.choices(family_representatives, k=contracts_to_generate)
nanny_ids_for_contracts = random.choices(nanny_ids, k=contracts_to_generate)


# Generate contracts
for (fr_id, child_key), nanny_id in zip(family_representatives_for_contracts, nanny_ids_for_contracts):
    start_date = datetime.datetime(2022, 1, 1)  # Start date range
    end_date = datetime.datetime(2023, 12, 31)  # End date range
    contract_start_date = random_date(start_date, end_date)
    contract_end_date = random_date(contract_start_date, end_date)
    pay_per_hour = round(random.uniform(10, 50), 2)  # Random pay per hour between $10 and $50
    
    # Insert contract into Contract table
    insert_contract_query = "INSERT INTO Contract (start_date, end_date, pay_per_hour) VALUES (%s, %s, %s)"
    contract_data = (contract_start_date.date(), contract_end_date.date(), pay_per_hour)
    cursor.execute(insert_contract_query, contract_data)
    db_connection.commit()
    
    # Retrieve the contractID of the last inserted contract
    contract_id = cursor.lastrowid
    
    # Insert contract into Family_rep_sign_contract table
    insert_fr_contract_query = "INSERT INTO Family_rep_sign_contract (userID, child_key, contractID) VALUES (%s, %s, %s)"
    fr_contract_data = (fr_id, child_key, contract_id)
    cursor.execute(insert_fr_contract_query, fr_contract_data)
    db_connection.commit()
    
    # Insert contract into Nanny_sign_contract table
    insert_nanny_contract_query = "INSERT INTO Nanny_sign_contract (userID, contractID) VALUES (%s, %s)"
    nanny_contract_data = (nanny_id, contract_id)
    cursor.execute(insert_nanny_contract_query, nanny_contract_data)
    db_connection.commit()
    
    # Generate 1 to 5 contract schedules
    num_schedules = random.randint(1, 5)
    for _ in range(num_schedules):
        schedule_start_date = random_date(contract_start_date, contract_end_date)
        schedule_start_time = random_time()
        schedule_end_time = random_time()
        schedule_start_datetime = datetime.datetime.combine(schedule_start_date, schedule_start_time)
        schedule_end_datetime = datetime.datetime.combine(schedule_start_date, schedule_end_time)
        description = fake.text(max_nb_chars=50)         
        # Insert schedule into Contract_schedule table
        insert_schedule_query = "INSERT INTO Contract_schedule (contractID, start_date_time, end_date_time, description) VALUES (%s, %s, %s, %s)"
        schedule_data = (contract_id, schedule_start_datetime, schedule_end_datetime, description)
        cursor.execute(insert_schedule_query, schedule_data)
        db_connection.commit()


# Close cursor and database connection
cursor.close()
db_connection.close()