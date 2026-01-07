"""
Asana Seed Data Generator - Main Entry Point
=============================================

Generates realistic seed data for an Asana-like project management simulation.
Simulates a B2B SaaS company with ~7500 employees.

Usage: python src/main.py
"""
import sqlite3
import os
import sys
import random

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import DB_PATH, SCHEMA_PATH
from generators.organizations import generate_organization
from generators.users import generate_users
from generators.teams import generate_teams, generate_team_memberships
from generators.projects import generate_projects
from generators.sections import generate_sections
from generators.tasks import generate_tasks

# Set seeds for reproducibility
random.seed(42)


def main():
    """
    Main orchestration function.
    Generates all data in dependency order to maintain referential integrity.
    """
    print("=" * 50)
    print("Asana Seed Data Generator")
    print("=" * 50)
    print()
    
    # Create output directory
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    # Remove existing database
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Removed existing database: {DB_PATH}")
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Load and execute schema
    schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), SCHEMA_PATH)
    with open(schema_path, 'r') as f:
        conn.executescript(f.read())
    print(f"Created database schema from {SCHEMA_PATH}")
    print()
    
    # ============================================
    # GENERATION PIPELINE
    # ============================================
    
    # 1. Organization (top-level container)
    org_id = generate_organization(cursor)
    conn.commit()
    
    # 2. Users
    users, users_by_dept = generate_users(cursor, org_id)
    conn.commit()
    
    # 3. Teams
    teams = generate_teams(cursor, org_id, users_by_dept)
    generate_team_memberships(cursor, teams, users_by_dept)
    conn.commit()
    
    # 4. Projects
    projects = generate_projects(cursor, teams)
    conn.commit()
    
    # 5. Sections
    project_sections = generate_sections(cursor, projects)
    conn.commit()
    
    # 6. Tasks (includes subtasks and comments)
    total_tasks, total_subtasks = generate_tasks(cursor, projects, project_sections)
    conn.commit()
    
    # ============================================
    # SUMMARY
    # ============================================
    print()
    print("=" * 50)
    print("Generation Complete!")
    print("=" * 50)
    print(f"Database: {DB_PATH}")
    print()
    
    # Verify counts
    cursor.execute("SELECT COUNT(*) FROM organizations")
    print(f"Organizations: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM users")
    print(f"Users: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM teams")
    print(f"Teams: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM projects")
    print(f"Projects: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE parent_task_id IS NULL")
    print(f"Tasks: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE parent_task_id IS NOT NULL")
    print(f"Subtasks: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM comments")
    print(f"Comments: {cursor.fetchone()[0]}")
    
    conn.close()
    print()
    print("Done!")


if __name__ == "__main__":
    main()
