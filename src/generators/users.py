"""
User generator module.
Creates users with realistic distributions across departments and roles.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from faker import Faker
from utils.helpers import gen_id, pick_weighted
from utils.dates import random_date
from config import NUM_USERS, DEPARTMENTS, ROLES, ROLE_WEIGHTS, COMPANY_DOMAIN

fake = Faker()
Faker.seed(42)


def generate_users(cursor, org_id):
    """
    Generate users with realistic department and role distributions.
    
    Methodology:
    - Names generated via Faker library
    - Departments distributed based on typical SaaS company ratios
    - Roles follow pyramid structure (more ICs than managers)
    
    Returns:
        tuple: (list of user dicts, dict of users by department)
    """
    print(f"Creating {NUM_USERS} users...")
    
    users = []
    users_by_dept = {dept: [] for dept in DEPARTMENTS.keys()}
    dept_list = list(DEPARTMENTS.keys())
    dept_weights = list(DEPARTMENTS.values())
    
    for i in range(NUM_USERS):
        user_id = gen_id()
        name = fake.name()
        dept = pick_weighted(dept_list, dept_weights)
        role = pick_weighted(ROLES, ROLE_WEIGHTS)
        email = f"{name.lower().replace(' ', '.')}_{i}@{COMPANY_DOMAIN}"
        created_at = random_date(365, 30)
        
        cursor.execute("""
            INSERT INTO users (user_id, org_id, full_name, email, department, role, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, org_id, name, email, dept, role, created_at))
        
        user = {"user_id": user_id, "department": dept}
        users.append(user)
        users_by_dept[dept].append(user_id)
        
        if (i + 1) % 1000 == 0:
            print(f"  Created {i + 1} users...")
    
    return users, users_by_dept
