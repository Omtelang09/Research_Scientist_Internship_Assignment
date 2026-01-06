import sqlite3
import uuid
import random
from faker import Faker
from datetime import datetime, timedelta
from itertools import cycle
from .users import generate_users

fake = Faker()

def _uid():
    """Generates a UUIDv4 string for primary keys."""
    return str(uuid.uuid4())

def generate_organization(conn: sqlite3.Connection, num_users: int = 5000):
    """
    Orchestrates the creation of the top-level organization, teams, users, 
    memberships, and projects.
    """
    cur = conn.cursor()
    
    # 1. Create Organization
    org_id = _uid()
    org_name = fake.company() + ' Inc.'
    # Generate a clean domain for professional email addresses
    domain = org_name.split()[0].lower().replace(',', '') + ".com"
    
    cur.execute('''
        INSERT INTO organizations(org_id, name, domain) 
        VALUES (?,?,?)
    ''', (org_id, org_name, domain))

    # 2. Generate Teams (Scaling logic: ~10 users per team)
    avg_team_size = 10
    num_teams = max(3, num_users // avg_team_size)
    teams = []
    
    for _ in range(num_teams):
        team_id = _uid()
        # Use business jargon to create realistic team names
        team_name = fake.bs().title()[:40]
        cur.execute('''
            INSERT INTO teams(team_id, org_id, name) 
            VALUES (?,?,?)
        ''', (team_id, org_id, team_name))
        teams.append({'team_id': team_id, 'name': team_name})

    # 3. Generate Users (Calls the users.py generator)
    # Passes the generated domain to ensure consistent email addresses
    users = generate_users(conn, org_id, num_users, domain)

    # 4. Create Team Memberships (Round-robin assignment)
    team_cycle = cycle(teams)
    for u in users:
        t = next(team_cycle)
        # Handles Many-to-Many relationship
        cur.execute('''
            INSERT INTO team_memberships(team_id, user_id) 
            VALUES (?,?)
        ''', (t['team_id'], u['user_id']))

    # 5. Generate Projects & Sections
    # Benchmark: 1-3 projects per team to simulate various workstreams
    projects = []
    start_date = datetime.utcnow() - timedelta(days=180)
    
    for t in teams:
        for _ in range(random.randint(1, 3)):
            project_id = _uid()
            project_name = fake.catch_phrase()[:80]
            desc = fake.sentence(nb_words=12)
            
            # Temporal consistency: Project creation date
            created_at = start_date + timedelta(days=random.randint(0, 30))
            
            cur.execute('''
                INSERT INTO projects(project_id, team_id, name, description, created_at) 
                VALUES (?,?,?,?,?)
            ''', (project_id, t['team_id'], project_name, desc, created_at.isoformat()))

            # Standard Section Set per Project requirement
            for sname in ['To Do', 'In Progress', 'Review', 'Done']:
                section_id = _uid()
                cur.execute('''
                    INSERT INTO sections(section_id, project_id, name) 
                    VALUES (?,?,?)
                ''', (section_id, project_id, sname))
                
            projects.append({
                'project_id': project_id, 
                'team_id': t['team_id'],
                'created_at': created_at
            })

    conn.commit()
    return {
        'org_id': org_id, 
        'domain': domain, 
        'teams': teams, 
        'projects': projects, 
        'users': users
    }