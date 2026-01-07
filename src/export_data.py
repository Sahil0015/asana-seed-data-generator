"""Export Asana seed data to CSV files.

Usage:
    python src/export_data.py
"""
import csv
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import DB_PATH, COMPANY_NAME  # type: ignore

OUTPUT_DIR = "output"


def write_csv(path: str, headers: list[str], rows: list) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"Wrote {path}")


def main() -> None:
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database not found at {DB_PATH}. Run 'python src/main.py' first.")

    conn = sqlite3.connect(DB_PATH)
    print(f"Exporting data for {COMPANY_NAME}...\n")

    # Organization
    rows = conn.execute("SELECT org_id, name, domain, created_at FROM organizations").fetchall()
    write_csv(os.path.join(OUTPUT_DIR, "org.csv"), ["org_id", "name", "domain", "created_at"], rows)

    # Users with aggregates
    rows = conn.execute("""
        SELECT u.user_id, u.full_name, u.email, u.department, u.role, u.created_at,
               COALESCE(tm.team_count, 0) AS team_count,
               COALESCE(t.assigned_count, 0) AS tasks_assigned,
               COALESCE(t.completed_count, 0) AS tasks_completed,
               COALESCE(c.comments_count, 0) AS comments_authored
        FROM users u
        LEFT JOIN (SELECT user_id, COUNT(*) AS team_count FROM team_memberships GROUP BY user_id) tm ON tm.user_id = u.user_id
        LEFT JOIN (SELECT assignee_id, COUNT(*) AS assigned_count, SUM(CASE WHEN completed THEN 1 ELSE 0 END) AS completed_count FROM tasks WHERE assignee_id IS NOT NULL GROUP BY assignee_id) t ON t.assignee_id = u.user_id
        LEFT JOIN (SELECT author_id, COUNT(*) AS comments_count FROM comments GROUP BY author_id) c ON c.author_id = u.user_id
        ORDER BY u.department, u.full_name
    """).fetchall()
    write_csv(os.path.join(OUTPUT_DIR, "users.csv"),
              ["user_id", "full_name", "email", "department", "role", "created_at", "team_count", "tasks_assigned", "tasks_completed", "comments_authored"], rows)

    # Teams
    rows = conn.execute("""
        SELECT t.team_id, t.org_id, t.name, t.department, t.created_at,
               COALESCE(tm.member_count, 0) AS member_count
        FROM teams t
        LEFT JOIN (SELECT team_id, COUNT(*) AS member_count FROM team_memberships GROUP BY team_id) tm ON tm.team_id = t.team_id
        ORDER BY t.department, t.name
    """).fetchall()
    write_csv(os.path.join(OUTPUT_DIR, "teams.csv"), ["team_id", "org_id", "name", "department", "created_at", "member_count"], rows)

    # Team memberships
    rows = conn.execute("""
        SELECT tm.id, tm.team_id, tm.user_id, tm.role, tm.joined_at,
               u.full_name AS user_name, t.name AS team_name
        FROM team_memberships tm
        JOIN users u ON u.user_id = tm.user_id
        JOIN teams t ON t.team_id = tm.team_id
        ORDER BY t.name, u.full_name
    """).fetchall()
    write_csv(os.path.join(OUTPUT_DIR, "team_memberships.csv"),
              ["membership_id", "team_id", "user_id", "role", "joined_at", "user_name", "team_name"], rows)

    # Projects
    rows = conn.execute("""
        SELECT p.project_id, p.team_id, p.owner_id, p.name, p.project_type, p.status,
               p.created_at, p.due_date, t.name AS team_name, u.full_name AS owner_name, u.email AS owner_email
        FROM projects p
        JOIN teams t ON t.team_id = p.team_id
        LEFT JOIN users u ON u.user_id = p.owner_id
        ORDER BY p.project_type, p.name
    """).fetchall()
    write_csv(os.path.join(OUTPUT_DIR, "projects.csv"),
              ["project_id", "team_id", "owner_id", "name", "project_type", "status", "created_at", "due_date", "team_name", "owner_name", "owner_email"], rows)

    # Sections
    rows = conn.execute("""
        SELECT s.section_id, s.project_id, s.name, s.order_index, s.created_at, p.name AS project_name
        FROM sections s
        JOIN projects p ON p.project_id = s.project_id
        ORDER BY p.name, s.order_index
    """).fetchall()
    write_csv(os.path.join(OUTPUT_DIR, "sections.csv"), ["section_id", "project_id", "name", "order_index", "created_at", "project_name"], rows)

    # Tasks
    rows = conn.execute("""
        SELECT t.task_id, t.project_id, t.section_id, t.parent_task_id, t.assignee_id,
               t.name, t.description, t.completed, t.priority, t.due_date, t.created_at, t.completed_at,
               p.name AS project_name, s.name AS section_name, u.full_name AS assignee_name, u.email AS assignee_email
        FROM tasks t
        JOIN projects p ON p.project_id = t.project_id
        LEFT JOIN sections s ON s.section_id = t.section_id
        LEFT JOIN users u ON u.user_id = t.assignee_id
        ORDER BY t.created_at
    """).fetchall()
    write_csv(os.path.join(OUTPUT_DIR, "tasks.csv"),
              ["task_id", "project_id", "section_id", "parent_task_id", "assignee_id", "name", "description",
               "completed", "priority", "due_date", "created_at", "completed_at", "project_name", "section_name", "assignee_name", "assignee_email"], rows)

    # Comments
    rows = conn.execute("""
        SELECT c.comment_id, c.task_id, c.author_id, c.content, c.created_at,
               u.full_name AS author_name, t.name AS task_name
        FROM comments c
        JOIN users u ON u.user_id = c.author_id
        JOIN tasks t ON t.task_id = c.task_id
        ORDER BY c.created_at
    """).fetchall()
    write_csv(os.path.join(OUTPUT_DIR, "comments.csv"), ["comment_id", "task_id", "author_id", "content", "created_at", "author_name", "task_name"], rows)

    conn.close()
    print("\nDone. CSVs are in the output/ folder.")


if __name__ == "__main__":
    main()
