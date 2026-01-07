"""
Configuration settings for the Asana seed data generator.
Adjust these values to change the size and characteristics of generated data.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ============================================
# DATABASE CONFIGURATION
# ============================================
DB_PATH = "output/asana_simulation.sqlite"
SCHEMA_PATH = "schema.sql"

# ============================================
# COMPANY CONFIGURATION
# ============================================
COMPANY_NAME = "TechFlow Solutions"
COMPANY_DOMAIN = "techflow.io"

# ============================================
# SCALE CONFIGURATION
# ============================================
NUM_USERS = 7500          # Target: 5000-10000 employees
NUM_TEAMS = 78            # Number of teams
NUM_PROJECTS = 500        # Number of projects
TASKS_PER_PROJECT = (30, 100)  # Min/max tasks per project

# ============================================
# DATA GENERATION SETTINGS
# ============================================
SUBTASK_CHANCE = 0.2      # 20% of tasks have subtasks
COMMENT_CHANCE = 0.3      # 30% of tasks have comments
COMPLETION_RATE = 0.6     # 60% of tasks are completed
UNASSIGNED_RATE = 0.15    # 15% of tasks are unassigned

# ============================================
# DEPARTMENT DISTRIBUTION (Typical SaaS Company)
# ============================================
DEPARTMENTS = {
    "Engineering": 0.35,
    "Sales": 0.20,
    "Marketing": 0.10,
    "Product": 0.08,
    "Customer Success": 0.08,
    "Design": 0.05,
    "Operations": 0.05,
    "HR": 0.04,
    "Finance": 0.03,
    "Legal": 0.02
}

# ============================================
# ROLE DISTRIBUTION
# ============================================
ROLES = ["Executive", "Director", "Manager", "Senior IC", "IC", "Intern"]
ROLE_WEIGHTS = [0.01, 0.02, 0.08, 0.25, 0.54, 0.10]

# ============================================
# TEAM NAMES BY DEPARTMENT
# ============================================
TEAM_NAMES = {
    "Engineering": ["Platform", "Backend", "Frontend", "Mobile", "DevOps", "QA", "Security", "Data"],
    "Sales": ["Enterprise", "SMB", "SDR", "Solutions", "Partnerships"],
    "Marketing": ["Content", "Demand Gen", "Brand", "Product Marketing", "Events"],
    "Product": ["Core Product", "Growth", "Platform", "Analytics"],
    "Customer Success": ["Support Tier 1", "Support Tier 2", "Success", "Onboarding"],
    "Design": ["Product Design", "Brand Design", "UX Research"],
    "Operations": ["IT", "Rev Ops", "Data Ops"],
    "HR": ["Recruiting", "People Ops", "L&D"],
    "Finance": ["FP&A", "Accounting", "Procurement"],
    "Legal": ["Legal", "Compliance"]
}

# ============================================
# SECTION TEMPLATES BY PROJECT TYPE
# ============================================
SECTION_TEMPLATES = {
    "sprint": ["Backlog", "To Do", "In Progress", "Review", "Done"],
    "kanban": ["To Do", "In Progress", "Done"],
    "campaign": ["Planning", "In Progress", "Review", "Launched"],
    "default": ["To Do", "In Progress", "Done"]
}

# ============================================
# LLM CONFIGURATION (Optional)
# ============================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
USE_LLM = os.getenv("USE_LLM", "false").lower() == "true"
