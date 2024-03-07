import datetime
import random
import string

# preferences
sample_preferences = [
    "Playing football",
    "Drawing pictures",
    "Reading books",
    "Singing songs",
    "Playing video games",
    "Cycling",
    "Watching cartoons",
    "Playing with toys",
    "Building blocks",
    "Cooking",
    "Dancing",
    "Swimming",
    "Playing musical instruments",
    "Solving puzzles",
    "Playing board games",
    "Painting",
    "Gardening",
    "Hiking",
    "Watching movies",
    "Baking cookies"
]

# disabilities
sample_disabilities = [
    "Autism",
    "Cerebral palsy",
    "Down syndrome",
    "Intellectual disability",
    "Learning disability",
    "Visual impairment",
    "Hearing impairment",
    "Speech impairment",
    "Physical disability",
    "Emotional/behavioral disorder",
    "Developmental delay",
    "ADHD",
    "Dyslexia",
    "Epilepsy",
    "Anxiety disorder",
    "Depression",
    "OCD",
    "Bipolar disorder",
    "Schizophrenia",
    "Tourette syndrome"
]

# skills.py
sample_skills = [
    "First Aid Certification",
    "CPR Certification",
    "Childcare Certification",
    "Cooking",
    "Swimming",
    "Teaching",
    "Music",
    "Arts and Crafts",
    "Sports Coaching",
    "Languages",
    "Driving",
    "Tutoring",
    "Housekeeping",
    "Pet Care",
    "Special Needs Care",
    "Time Management",
    "Problem Solving",
    "Communication",
    "Organization",
    "Patience"
]

# Function to generate random disabilities for a child
def generate_random_disabilities():
    num_disabilities = random.randint(0, 3)
    random.shuffle(sample_disabilities)
    return sample_disabilities[:num_disabilities]

# Function to generate random preferences for a child
def generate_random_preferences():
    num_preferences = random.randint(1, 4)
    random.shuffle(sample_preferences)
    return sample_preferences[:num_preferences]

# Function to generate skill
def generate_random_skills():
    num_skills = random.randint(1, 3)
    random.shuffle(sample_skills)
    return sample_skills[:num_skills]


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

def random_createdAt_date():
    start_date = datetime.datetime(2022, 1, 1)
    end_date = datetime.datetime(2023, 12, 31)
    return random_date(start_date, end_date)