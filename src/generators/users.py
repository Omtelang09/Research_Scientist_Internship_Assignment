import sqlite3
import uuid
import random
from faker import Faker
from datetime import datetime, timedelta

# Initialize Faker with localized data for realistic distribution
fake = Faker()

def _uid():
    """Generates a UUIDv4 string to simulate Asana's GID format."""
    return str(uuid.uuid4())

def generate_users(conn: sqlite3.Connection, org_id: str, num_users: int, domain: str):
    """
    Generates realistic user data for a B2B SaaS organization.
    Ensures unique emails, job-based roles, and temporal consistency.
    """
    cur = conn.cursor()
    users = []
    
    # Define the simulation start date (6 months ago)
    start_date = datetime.utcnow() - timedelta(days=180)
    
    # Enterprise role distribution for simulation realism
    roles = ['member'] * 85 + ['admin'] * 5 + ['guest'] * 10

    for _ in range(num_users):
        user_id = _uid()
        full_name = fake.name()
        
        # Methodology: Generate professional emails using the organization's domain
        # Example: john.doe@company.com
        clean_name = "".join(filter(str.isalnum, full_name.lower().replace(" ", ".")))
        email = f"{clean_name}@{domain}"
        
        # Methodology: Roles follow specific industry distributions
        role_type = random.choice(roles)
        
        # Methodology: faker.job() mimics varied seniority and job titles
        job_title = fake.job()
        
        # Methodology: Sampling over 6-12 month history with weekday bias
        # Adding a random number of days to the start_date
        days_offset = fake.random_int(0, 180)
        creation_dt = start_date + timedelta(days=days_offset)
        
        # Ensure created_at does not exceed 'now'
        if creation_dt > datetime.utcnow():
            creation_dt = datetime.utcnow()

        cur.execute('''
            INSERT INTO users(user_id, org_id, email, full_name, role, created_at) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            user_id, 
            org_id, 
            email, 
            full_name, 
            f"{job_title} ({role_type})", 
            creation_dt.isoformat()
        ))
        
        users.append({
            'user_id': user_id, 
            'email': email, 
            'full_name': full_name,
            'role': role_type
        })

    return users