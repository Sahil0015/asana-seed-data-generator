"""
Project generator module.
Creates projects with various types and statuses.
"""
import sys
import os
import random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from faker import Faker
from utils.helpers import gen_id
from utils.dates import random_date, parse_datetime, add_days, to_date_only
from config import NUM_PROJECTS

fake = Faker()
Faker.seed(42)
random.seed(42)

PROJECT_TYPES = ["sprint", "kanban", "campaign", "operations"]
PROJECT_STATUSES = ["active", "active", "active", "completed", "on_hold"]  # Weighted towards active


def generate_projects(cursor, teams):
    """
    Generate projects assigned to teams.
    
    Methodology:
    - Projects distributed across teams
    - Project types: sprint (30%), kanban (25%), campaign (25%), operations (20%)
    - Status: 60% active, 20% completed, 20% on_hold
    
    Returns:
        list: List of project dictionaries
    """
    print(f"Creating {NUM_PROJECTS} projects...")
    
    projects = []
    
    for i in range(NUM_PROJECTS):
        team = random.choice(teams)
        project_id = gen_id()
        project_type = random.choice(PROJECT_TYPES)
        
        # Get a team member as owner
        cursor.execute("SELECT user_id FROM team_memberships WHERE team_id = ? LIMIT 1", 
                      (team["team_id"],))
        row = cursor.fetchone()
        owner_id = row[0] if row else None
        
        name = f"{team['department']} - {fake.bs().title()}"[:50]
        created_at = random_date(180, 10)
        due_date = to_date_only(add_days(created_at, random.randint(30, 90)))
        
        cursor.execute("""
            INSERT INTO projects (project_id, team_id, owner_id, name, project_type, status, created_at, due_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (project_id, team["team_id"], owner_id, name, project_type,
              random.choice(PROJECT_STATUSES), created_at, due_date))
        
        projects.append({
            "project_id": project_id,
            "team_id": team["team_id"],
            "department": team["department"],
            "project_type": project_type,
            "created_at": created_at
        })
    
    print(f"  Created {len(projects)} projects")
    return projects
