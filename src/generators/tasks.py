"""
Task generator module.
Creates tasks and subtasks with realistic names and distributions.
"""
import sys
import os
import random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import gen_id
from utils.dates import random_date, add_days, add_hours, to_date_only
from utils.llm import generate_task_names_with_llm
from config import TASKS_PER_PROJECT, SUBTASK_CHANCE, COMMENT_CHANCE, COMPLETION_RATE, UNASSIGNED_RATE, USE_LLM

random.seed(42)

# ============================================
# TASK NAME TEMPLATES (Fallback when no LLM)
# ============================================
TASK_TEMPLATES = {
    "Engineering": [
        "Implement {feature} API endpoint",
        "Fix bug in {component}",
        "Refactor {module} for performance",
        "Add unit tests for {feature}",
        "Update {library} to latest version",
        "Review PR for {feature}",
        "Set up CI/CD for {service}",
        "Optimize database queries in {module}",
        "Document {feature} architecture",
        "Deploy {service} to staging"
    ],
    "Marketing": [
        "Create blog post about {topic}",
        "Design email campaign for {campaign}",
        "Update landing page copy",
        "Analyze campaign metrics",
        "Schedule social media posts",
        "Create product demo video",
        "Review competitor messaging",
        "Plan webinar content",
        "Update brand guidelines",
        "Write case study draft"
    ],
    "Sales": [
        "Follow up with {company}",
        "Prepare demo for {prospect}",
        "Update CRM records",
        "Send proposal to {client}",
        "Schedule discovery call",
        "Complete quarterly forecast",
        "Update sales deck",
        "Review contract terms",
        "Onboard new account",
        "Research target accounts"
    ],
    "Product": [
        "Write PRD for {feature}",
        "Analyze user feedback",
        "Prioritize backlog items",
        "Create wireframes for {feature}",
        "Plan sprint goals",
        "Review analytics dashboard",
        "Define success metrics",
        "Conduct user interviews",
        "Update product roadmap",
        "Sync with engineering team"
    ],
    "default": [
        "Complete {item} review",
        "Update documentation",
        "Prepare status report",
        "Schedule team meeting",
        "Review project timeline",
        "Send weekly update",
        "Organize project files",
        "Follow up on action items",
        "Update project tracker",
        "Plan next quarter goals"
    ]
}

PLACEHOLDERS = {
    "feature": ["user auth", "dashboard", "notifications", "search", "payments", "analytics", "reports"],
    "component": ["login flow", "checkout", "data pipeline", "API gateway", "cache layer"],
    "module": ["auth service", "billing module", "notification system", "user service"],
    "library": ["React", "Node.js", "Python SDK", "database driver"],
    "service": ["web app", "backend API", "worker service"],
    "topic": ["product updates", "industry trends", "customer success stories"],
    "campaign": ["Q1 launch", "product release", "holiday promo"],
    "company": ["Acme Corp", "TechStart Inc", "Global Systems"],
    "prospect": ["enterprise client", "new lead", "warm prospect"],
    "client": ["existing customer", "renewal account"],
    "item": ["weekly", "monthly", "quarterly"]
}

COMMENT_TEMPLATES = [
    "Looking good, let's move forward.",
    "Can you provide more details on this?",
    "Updated the status - ready for review.",
    "Blocked on dependencies, need input.",
    "Great progress on this task!",
    "Let's discuss in our next sync.",
    "Added more context to the description.",
    "This is now complete."
]


def generate_task_name(department):
    """Generate a realistic task name using templates."""
    templates = TASK_TEMPLATES.get(department, TASK_TEMPLATES["default"])
    template = random.choice(templates)
    
    for key, values in PLACEHOLDERS.items():
        if "{" + key + "}" in template:
            template = template.replace("{" + key + "}", random.choice(values))
    
    return template


def generate_tasks(cursor, projects, project_sections):
    """
    Generate tasks for each project.
    
    Methodology:
    - Task count: 30-100 per project
    - Completion rate: 60% of tasks completed
    - Unassigned rate: 15% of tasks have no assignee
    - Subtask rate: 20% of tasks have subtasks
    - Comment rate: 30% of tasks have comments
    
    Returns:
        tuple: (total_tasks, total_subtasks)
    """
    print("Creating tasks (this may take a moment)...")
    
    total_tasks = 0
    total_subtasks = 0
    llm_cache = {}
    
    for project in projects:
        dept = project["department"]
        project_id = project["project_id"]
        section_ids = project_sections.get(project_id, [])
        
        if not section_ids:
            continue
        
        # Get team members for assignment
        cursor.execute("SELECT user_id FROM team_memberships WHERE team_id = ?", 
                      (project["team_id"],))
        team_members = [row[0] for row in cursor.fetchall()]
        
        # Number of tasks for this project
        num_tasks = random.randint(*TASKS_PER_PROJECT)
        
        # Try LLM for task names (cached per department)
        llm_names = None
        if USE_LLM and dept not in llm_cache:
            llm_names = generate_task_names_with_llm(dept, project["project_type"], 5)
            if llm_names:
                llm_cache[dept] = llm_names
        
        if dept in llm_cache:
            llm_names = llm_cache[dept]
        
        for _ in range(num_tasks):
            task_id = gen_id()
            
            # Task name
            task_name = random.choice(llm_names) if llm_names else generate_task_name(dept)
            
            # Completion status
            completed = random.random() < COMPLETION_RATE
            
            # Section based on completion
            if completed:
                section_id = section_ids[-1]  # Done section
            else:
                section_id = random.choice(section_ids[:-1]) if len(section_ids) > 1 else section_ids[0]
            
            # Assignee
            assignee_id = random.choice(team_members) if team_members and random.random() > UNASSIGNED_RATE else None
            
            # Timestamps
            created_at = random_date(150, 5)
            completed_at = add_days(created_at, random.randint(1, 30)) if completed else None
            due_date = to_date_only(add_days(created_at, random.randint(7, 60)))
            
            cursor.execute("""
                INSERT INTO tasks (task_id, project_id, section_id, assignee_id, name, completed,
                                   priority, due_date, created_at, completed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (task_id, project_id, section_id, assignee_id, task_name, completed,
                  random.choice(["high", "medium", "low", None]), due_date, created_at, completed_at))
            
            total_tasks += 1
            
            # Subtasks
            if random.random() < SUBTASK_CHANCE:
                for j in range(random.randint(1, 4)):
                    subtask_id = gen_id()
                    cursor.execute("""
                        INSERT INTO tasks (task_id, project_id, section_id, parent_task_id,
                                           assignee_id, name, completed, created_at, completed_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (subtask_id, project_id, section_id, task_id, assignee_id,
                          f"Subtask {j+1}: {task_name[:30]}", completed, created_at, completed_at))
                    total_subtasks += 1
            
            # Comments
            if random.random() < COMMENT_CHANCE and team_members:
                cursor.execute("""
                    INSERT INTO comments (comment_id, task_id, author_id, content, created_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (gen_id(), task_id, random.choice(team_members),
                      random.choice(COMMENT_TEMPLATES), add_hours(created_at, random.randint(1, 72))))
        
        if (projects.index(project) + 1) % 100 == 0:
            print(f"  Processed {projects.index(project) + 1} projects...")
    
    print(f"  Created {total_tasks} tasks + {total_subtasks} subtasks")
    return total_tasks, total_subtasks
