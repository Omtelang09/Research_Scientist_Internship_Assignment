"""
Compatibility wrapper exposing project-related generator functions.

Some consumers expect a `generators.projects` module. This file delegates to
`generators.teams_projects` which contains the authoritative implementation.
"""

from .teams_projects import generate_organization

def generate_projects(conn, num_users=5000):
    """
    Creates an organization structure including teams, users, projects, and sections.
    
    Delegates to the centralized generate_organization function to maintain 
    relational integrity across the enterprise simulation.
    
    Args:
        conn: sqlite3.Connection object.
        num_users: Target number of users for the simulation (default 5000).
        
    Returns:
        dict: The generated organization structure containing IDs for teams and projects.
    """
    # Simply calls the authoritative generator from teams_projects.py
    return generate_organization(conn, num_users=num_users)