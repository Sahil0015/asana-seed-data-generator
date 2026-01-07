"""
Section generator module.
Creates project sections based on project type.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import gen_id
from config import SECTION_TEMPLATES


def generate_sections(cursor, projects):
    """
    Generate sections for each project based on project type.
    
    Methodology:
    - Sprint projects: Backlog, To Do, In Progress, Review, Done
    - Kanban projects: To Do, In Progress, Done
    - Campaign projects: Planning, In Progress, Review, Launched
    
    Returns:
        dict: Mapping of project_id to list of section_ids
    """
    print("Creating sections...")
    
    project_sections = {}
    
    for project in projects:
        sections = SECTION_TEMPLATES.get(project["project_type"], SECTION_TEMPLATES["default"])
        section_ids = []
        
        for idx, section_name in enumerate(sections):
            section_id = gen_id()
            cursor.execute("""
                INSERT INTO sections (section_id, project_id, name, order_index, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (section_id, project["project_id"], section_name, idx, project["created_at"]))
            section_ids.append(section_id)
        
        project_sections[project["project_id"]] = section_ids
    
    return project_sections
