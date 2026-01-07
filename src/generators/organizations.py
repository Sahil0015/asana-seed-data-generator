"""
Organization generator module.
Creates the top-level organization entity.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import gen_id
from config import COMPANY_NAME, COMPANY_DOMAIN


def generate_organization(cursor):
    """
    Generate the organization (top-level container).
    
    Returns:
        org_id: The generated organization ID
    """
    org_id = gen_id()
    
    cursor.execute("""
        INSERT INTO organizations (org_id, name, domain, created_at)
        VALUES (?, ?, ?, ?)
    """, (org_id, COMPANY_NAME, COMPANY_DOMAIN, "2018-03-15 00:00:00"))
    
    print(f"Created organization: {COMPANY_NAME}")
    return org_id
