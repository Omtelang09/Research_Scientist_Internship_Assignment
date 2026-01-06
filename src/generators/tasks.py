import sqlite3
import uuid
import random
from faker import Faker
from datetime import datetime, timedelta
from .llm_stub import generate_task_name, generate_description

fake = Faker()

def _uid():
    """Generates a UUIDv4 string for unique primary keys."""
    return str(uuid.uuid4())

def _choose_assignee(conn, team_id):
    """Selects a user belonging specifically to the project's team to ensure relational integrity."""
    cur = conn.cursor()
    cur.execute('''
        SELECT u.user_id 
        FROM users u 
        JOIN team_memberships m ON u.user_id = m.user_id 
        WHERE m.team_id = ? 
        LIMIT 200
    ''', (team_id,))
    rows = cur.fetchall()
    if not rows:
        return None
    return random.choice(rows)[0]

def generate_tasks(conn: sqlite3.Connection, org_struct: dict, density=1.0):
    """
    Generates realistic tasks and related artifacts (comments, tags, custom fields).
    Enforces benchmarks: 15% unassigned tasks and temporal consistency.
    """
    cur = conn.cursor()
    projects = org_struct.get('projects', [])
    tags = org_struct.get('tags', [])
    custom_fields = org_struct.get('custom_fields', [])
    now = datetime.utcnow()

    for p in projects:
        # Scale task count based on project density and randomization
        n_tasks = int(20 * density * random.randint(1, 5))
        
        # Ensure tasks belong to actual project sections
        cur.execute('SELECT section_id, name FROM sections WHERE project_id = ?', (p['project_id'],))
        sections = cur.fetchall()

        for _ in range(n_tasks):
            task_id = _uid()
            
            # Methodology: LLM-generated names and descriptions to avoid generic text
            name = generate_task_name()
            desc = generate_description(name)
            
            section = random.choice(sections) if sections else (None, None)
            section_id = section[0]
            
            # Benchmark: 85% assigned probability (15% unassigned per industry norms)
            assignee = _choose_assignee(conn, p['team_id']) if random.randint(1, 100) <= 85 else None
            
            # Temporal Logic: Task creation over a 2-year history
            created = now - timedelta(days=random.randint(0, 720))
            
            # Due Date Heuristics: 90% have due dates, skewed toward the future relative to creation
            due = None
            if random.randint(1, 100) <= 90:
                due = created + timedelta(days=random.randint(1, 90))
            
            # Completion Probability (Benchmark: 60% default completion rate)
            completed = False
            completed_at = None
            if random.randint(1, 100) <= 60:
                completed = True
                # Logical Constraint: completed_at MUST be after created_at
                completed_at = created + timedelta(days=random.randint(0, 60))
                if completed_at > now:
                    completed_at = now - timedelta(minutes=random.randint(1, 60))

            cur.execute('''
                INSERT INTO tasks(
                    task_id, project_id, section_id, parent_task_id, name, 
                    description, assignee_id, due_date, created_at, completed, completed_at
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?)
            ''', (
                task_id, p['project_id'], section_id, None, name, 
                desc, assignee, due.isoformat() if due else None, 
                created.isoformat(), int(completed), 
                completed_at.isoformat() if completed_at else None
            ))

            # Optional: Subtask Generation (20% chance to create a child task)
            if random.randint(1, 100) <= 20:
                subtask_id = _uid()
                cur.execute('''
                    INSERT INTO tasks(task_id, project_id, section_id, parent_task_id, name, created_at)
                    VALUES (?,?,?,?,?,?)
                ''', (subtask_id, p['project_id'], section_id, task_id, f"Subtask: {name}", created.isoformat()))

            # Occasional Collaboration: 40% of tasks have comments
            if random.randint(1, 100) <= 40 and assignee:
                cur.execute('''
                    INSERT INTO comments(comment_id, task_id, user_id, body, created_at) 
                    VALUES (?,?,?,?,?)
                ''', (_uid(), task_id, assignee, fake.sentence(), (created + timedelta(days=1)).isoformat()))

            # Relational Metadata: Assign org-level tags (35% probability)
            if tags and random.randint(1, 100) <= 35:
                t = random.choice(tags)
                cur.execute('INSERT INTO task_tags(id, task_id, tag_id) VALUES (?,?,?)', (_uid(), task_id, t['tag_id']))

            # Custom Field Values: Map field-specific values to tasks
            for cf in [c for c in custom_fields if c['project_id'] == p['project_id']]:
                val = str(random.randint(1, 100)) if cf['field_type'] == 'number' else fake.word()
                cur.execute('INSERT INTO custom_field_values(value_id, field_id, task_id, value) VALUES (?,?,?,?)', 
                            (_uid(), cf['field_id'], task_id, val))

            # Artifacts: 10% of tasks have attachments
            if random.randint(1, 100) <= 10:
                cur.execute('''
                    INSERT INTO attachments(attachment_id, task_id, filename, url, uploaded_by, created_at) 
                    VALUES (?,?,?,?,?,?)
                ''', (_uid(), task_id, fake.file_name(extension='pdf'), "https://files.example/s", assignee, created.isoformat()))

    conn.commit()
    return True