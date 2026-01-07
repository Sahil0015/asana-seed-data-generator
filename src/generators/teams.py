"""
Team generator module.
Creates teams and team memberships.
"""
import sys
import os
import random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import gen_id
from utils.dates import random_date
from config import TEAM_NAMES

random.seed(42)


def generate_teams(cursor, org_id, users_by_dept):
    """
    Generate teams organized by department.
    
    Methodology:
    - Teams created based on department structure
    - Team names follow common organizational patterns
    
    Returns:
        list: List of team dictionaries
    """
    print(f"Creating teams...")
    
    teams = []
    
    for dept, names in TEAM_NAMES.items():
        for name in names:
            team_id = gen_id()
            cursor.execute("""
                INSERT INTO teams (team_id, org_id, name, department, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (team_id, org_id, f"{dept} - {name}", dept, random_date(300, 100)))
            teams.append({"team_id": team_id, "department": dept})
    
    print(f"  Created {len(teams)} teams")
    return teams


def generate_team_memberships(cursor, teams, users_by_dept):
    """
    Assign users to teams based on their department.
    
    Methodology:
    - Users assigned to teams within their department
    - Each team gets 20-100 members (varies by availability)
    """
    print("Assigning users to teams...")
    
    for team in teams:
        dept = team["department"]
        dept_users = users_by_dept.get(dept, [])
        
        if dept_users:
            num_members = min(random.randint(20, 100), len(dept_users))
            members = random.sample(dept_users, num_members)
            
            for user_id in members:
                cursor.execute("""
                    INSERT OR IGNORE INTO team_memberships (id, team_id, user_id, role, joined_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (gen_id(), team["team_id"], user_id, "member", random_date(200, 50)))
