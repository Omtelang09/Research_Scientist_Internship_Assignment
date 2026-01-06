import sqlite3
import uuid
import random
from faker import Faker

fake = Faker()

def _uid():
    """Generates a UUIDv4 string for unique primary keys."""
    return str(uuid.uuid4())

def generate_metadata(conn: sqlite3.Connection, org_struct: dict):
    """
    Generates organizational tags and project-level custom field definitions.
    Updates and returns the org_struct with the generated metadata for downstream task generation.
    """
    cur = conn.cursor()
    org_id = org_struct['org_id']
    
    # 1. Create Organization-level Tags
    # Methodology: Standard labels used across projects for cross-functional tracking.
    tags = []
    tag_names = ['bug', 'feature', 'urgent', 'customer-request', 'research', 'low-priority', 'qa-blocked']
    
    for name in tag_names:
        tag_id = _uid()
        # Ensure the schema table name matches your DDL (tags)
        cur.execute('INSERT INTO tags(tag_id, org_id, name) VALUES (?,?,?)', (tag_id, org_id, name))
        tags.append({'tag_id': tag_id, 'name': name})

    # 2. Create Project-specific Custom Field Definitions
    # Design Decision: Implements the EAV model metadata for varying project needs.
    custom_fields = []
    
    # Iterate through projects created in the teams_projects generator
    for proj in org_struct.get('projects', []):
        # Distribution: 0-3 custom fields per project to simulate realistic workspace variety.
        num_defs = random.randint(0, 3)
        
        for _ in range(num_defs):
            field_id = _uid()
            # Generate realistic field names like 'Priority', 'Effort', or 'Sprint'
            field_name = random.choice(['Priority', 'Story Points', 'T-Shirt Size', 'Reviewer', 'Department'])
            # Field types restricted to text, number, or enum as per schema requirements.
            field_type = random.choice(['text', 'number', 'enum'])
            
            cur.execute('''
                INSERT INTO custom_field_defs(field_id, project_id, name, field_type) 
                VALUES (?,?,?,?)
            ''', (field_id, proj['project_id'], field_name, field_type))
            
            custom_fields.append({
                'field_id': field_id, 
                'project_id': proj['project_id'], 
                'name': field_name, 
                'field_type': field_type
            })

    conn.commit()
    
    # Update the data structure to allow the task generator to assign values to these fields
    org_struct['tags'] = tags
    org_struct['custom_fields'] = custom_fields
    
    return org_struct