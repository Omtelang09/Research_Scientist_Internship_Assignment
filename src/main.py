import argparse
import sqlite3
import os
from dotenv import load_dotenv

# [cite_start]Import the modular generator functions [cite: 74, 76]
from generators.users import generate_users
from generators.teams_projects import generate_organization
from generators.tasks import generate_tasks
from generators.metadata import generate_metadata

# [cite_start]Define directory structure according to assignment requirements [cite: 61, 84]
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_schema(conn, schema_path):
    [cite_start]"""Executes the DDL script to initialize the SQLite database[cite: 71, 92]."""
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())

def main():
    # [cite_start]Setup argument parser for external configuration of database size [cite: 96]
    parser = argparse.ArgumentParser(description="Asana RL Seed Data Generator")
    parser.add_argument('--users', type=int, default=5000, 
                        [cite_start]help='Number of users to generate (target: 5000-10000) [cite: 24]')
    parser.add_argument('--db', type=str, 
                        default=os.path.join(OUTPUT_DIR, 'asana_simulation.sqlite'),
                        [cite_start]help='Path to the final SQLite database [cite: 88]')
    args = parser.parse_args()

    # [cite_start]Load environment variables for LLM API keys [cite: 96]
    load_dotenv()

    # Initialize fresh database to ensure a clean simulation run
    db_path = args.db
    if os.path.exists(db_path):
        os.remove(db_path)

    # [cite_start]Establish connection and enforce referential integrity [cite: 31, 57]
    conn = sqlite3.connect(db_path)
    conn.execute('PRAGMA foreign_keys = ON;')

    # [cite_start]Load the relational schema [cite: 28, 29]
    schema_path = os.path.join(BASE_DIR, 'schema.sql')
    if not os.path.exists(schema_path):
        print(f"Error: schema.sql not found at {schema_path}")
        return
    load_schema(conn, schema_path)

    print(f"Starting simulation for {args.users} users...")

    # [cite_start]Phase 1: Core Organization Structure [cite: 21, 32]
    # Creates Organizations, Teams, Projects, and Users
    org_context = generate_organization(conn, num_users=args.users)

    # [cite_start]Phase 2: Metadata Generation [cite: 21, 32]
    # Generates Tags and Custom Field Definitions (Priority, Status, etc.)
    org_context = generate_metadata(conn, org_context)

    # [cite_start]Phase 3: Task & Artifact Generation [cite: 21, 32, 40]
    # Generates Tasks, Subtasks, Comments, Attachments, and Custom Field Values
    # [cite_start]Maintains temporal and relational consistency [cite: 54, 57]
    generate_tasks(conn, org_context, density=1.0)

    # [cite_start]Commit changes and finalize the .sqlite file [cite: 97, 98]
    conn.commit()
    conn.close()
    
    print(f"Successfully wrote enterprise-grade dataset to: {db_path}")

if __name__ == '__main__':
    main()