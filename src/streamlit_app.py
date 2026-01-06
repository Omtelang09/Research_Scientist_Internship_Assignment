import streamlit as st
import sqlite3
import os
from datetime import datetime
import pandas as pd

# Default path aligns with the assignment's required output directory [cite: 84, 88]
DEFAULT_DB = os.environ.get('DATABASE_PATH', 'output/asana_simulation.sqlite')

def safe_connect(db_path):
    """Establishes a connection to the SQLite database if it exists."""
    if not os.path.exists(db_path):
        return None
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def load_projects_teams(conn):
    """Loads available projects and their associated teams."""
    cur = conn.cursor()
    cur.execute('''
        SELECT p.project_id, p.name as project_name, t.team_id, t.name as team_name 
        FROM projects p 
        JOIN teams t ON p.team_id = t.team_id
    ''')
    return cur.fetchall()

def load_assignees_for_team(conn, team_id):
    """Fetches users belonging to a specific team for filtering[cite: 21]."""
    cur = conn.cursor()
    cur.execute('''
        SELECT u.user_id, u.full_name 
        FROM users u 
        JOIN team_memberships m ON u.user_id = m.user_id 
        WHERE m.team_id = ?
    ''', (team_id,))
    return cur.fetchall()

def query_tasks(conn, project_id=None, team_id=None, assignee_id=None):
    """Queries the tasks table with relational joins for explorer display[cite: 32]."""
    cur = conn.cursor()
    q = '''SELECT tasks.task_id, tasks.name as task_name, tasks.description, 
                  tasks.created_at, tasks.due_date, tasks.completed,
                  projects.project_id, projects.name as project_name,
                  teams.team_id, teams.name as team_name,
                  users.user_id as assignee_id, users.full_name as assignee_name,
                  sections.name as section_name
           FROM tasks
           JOIN projects ON tasks.project_id = projects.project_id
           JOIN teams ON projects.team_id = teams.team_id
           LEFT JOIN users ON tasks.assignee_id = users.user_id
           LEFT JOIN sections ON tasks.section_id = sections.section_id
           WHERE 1=1'''
    params = []
    if project_id and project_id != 'ALL':
        q += ' AND projects.project_id = ?'
        params.append(project_id)
    if team_id and team_id != 'ALL':
        q += ' AND teams.team_id = ?'
        params.append(team_id)
    if assignee_id and assignee_id != 'ALL':
        q += ' AND users.user_id = ?'
        params.append(assignee_id)
    cur.execute(q, params)
    return cur.fetchall()

def compute_status(row):
    """Calculates realistic task status based on due dates and completion[cite: 42]."""
    now = datetime.utcnow()
    if row['completed']:
        return 'Completed'
    due = row['due_date']
    section = row['section_name'] or ''
    try:
        if due:
            due_dt = datetime.fromisoformat(due)
            if due_dt < now:
                return 'Overdue'
    except Exception:
        pass
    if section.lower() == 'in progress':
        return 'In Progress'
    return 'Open'

# --- UI Layout ---
st.set_page_config(page_title='Asana Simulation Explorer', layout='wide')
st.title('Asana Simulation — Read-only Explorer')

db_path = st.sidebar.text_input('SQLite DB path', DEFAULT_DB)
conn = safe_connect(db_path)

if conn is None:
    st.warning(f'Database not found at path: {db_path}. Please run src/main.py first.')
    st.stop()

# --- Filters ---
rows = load_projects_teams(conn)
projects = sorted({(r['project_id'], r['project_name']) for r in rows}, key=lambda x: x[1])
project_options = ['ALL'] + [p[0] for p in projects]
project_display = {p[0]: p[1] for p in projects}

selected_project = st.sidebar.selectbox('Filter by Project', options=project_options, 
                                        format_func=lambda x: 'All projects' if x == 'ALL' else project_display.get(x, x))

# --- Data Table ---
task_rows = query_tasks(conn, project_id=selected_project)
records = []
for r in task_rows:
    records.append({
        'Project': r['project_name'],
        'Team': r['team_name'],
        'Task Name': r['task_name'],
        'Section': r['section_name'],
        'Assignee': r['assignee_name'] or 'Unassigned',
        'Due Date': r['due_date'],
        'Status': compute_status(r)
    })

df = pd.DataFrame(records)
st.subheader('Generated Task Data')
st.dataframe(df, use_container_width=True)

# --- QC Metrics (Assignment Benchmarks) ---
st.markdown('---')
st.subheader('Methodology Validation (QC Metrics)')
cur = conn.cursor()
total_users = cur.execute('SELECT COUNT(1) FROM users').fetchone()[0]
total_tasks = cur.execute('SELECT COUNT(1) FROM tasks').fetchone()[0]
unassigned = cur.execute('SELECT COUNT(1) FROM tasks WHERE assignee_id IS NULL').fetchone()[0]
# Overdue logic based on assignment criteria [cite: 42]
overdue = cur.execute("SELECT COUNT(1) FROM tasks WHERE completed = 0 AND due_date IS NOT NULL AND due_date < ?", 
                      (datetime.utcnow().isoformat(),)).fetchone()[0]

m_cols = st.columns(4)
m_cols[0].metric('Total Users', total_users)
m_cols[1].metric('Total Tasks', total_tasks)
m_cols[2].metric('% Unassigned', f"{(unassigned/total_tasks*100):.1f}%", help="Benchmark: ~15% [cite: 42]")
m_cols[3].metric('% Overdue', f"{(overdue/total_tasks*100):.1f}%", help="Benchmark: ~5% [cite: 42]")

st.caption('This explorer verifies the realism of your seed data. It does not modify the database.')