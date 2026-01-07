# Asana Seed Data Generator

A Python project that generates realistic seed data for an Asana-like project management simulation. Creates a SQLite database simulating a B2B SaaS company with ~7,500 employees.

## Overview

This project creates seed data for a reinforcement learning environment simulating Asana. The data includes:

- **1 Organization** - The company container
- **7,500 Users** - Employees distributed across departments
- **78 Teams** - Organized by department  
- **500 Projects** - Various project types (sprints, kanban, campaigns)
- **30,000+ Tasks** - With subtasks, comments, and realistic names

## Project Structure

```
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── schema.sql                   # Complete DDL for SQLite
├── .env.example                 # Environment variable template
├── src/
│   ├── main.py                  # Entry point / orchestration
│   ├── config.py                # Configuration settings
│   ├── export_data.py           # CSV export utility
│   ├── generators/              # Data generation logic
│   │   ├── organizations.py
│   │   ├── users.py
│   │   ├── teams.py
│   │   ├── projects.py
│   │   ├── sections.py
│   │   └── tasks.py
│   ├── utils/                   # Helper modules
│   │   ├── helpers.py           # ID generation, utilities
│   │   ├── dates.py             # Date/time utilities
│   │   └── llm.py               # LLM integration (optional)
│   ├── models/                  # Data models (placeholder)
│   └── scrapers/                # External data scrapers (placeholder)
├── prompts/                     # LLM prompts
│   └── task_generation.md
└── output/
    └── asana_simulation.sqlite  # Generated database
```

## Quick Start

### Prerequisites
- Python 3.10+
- pip

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment (optional for LLM):
```bash
cp .env.example .env
# LLM is OFF by default. To enable, set USE_LLM=true and provide OPENAI_API_KEY
```

### Run

```bash
python src/main.py
```

Output: `output/asana_simulation.sqlite`

### LLM Task Names (optional)
- Default: LLM is **disabled** (`USE_LLM=false`). Task names use templates.
- Enable: set `USE_LLM=true` and add `OPENAI_API_KEY` to `.env` (model via `LLM_MODEL`, default `gpt-4o-mini`).
- Disable: set `USE_LLM=false` or remove `OPENAI_API_KEY`.
- Efficiency: the generator now requests a small batch (20 names per department) to keep calls fast and cached.

#### Export to CSV

```bash
python src/export_data.py
```

Writes all tables to the `output/` folder as CSV files.

## Configuration

Edit `src/config.py` to adjust:

```python
NUM_USERS = 7500          # Number of employees
NUM_TEAMS = 78            # Number of teams
NUM_PROJECTS = 500        # Number of projects
TASKS_PER_PROJECT = (30, 100)  # Task range per project
```

## Data Generation Approach

### User Distribution
Users are distributed across departments based on typical SaaS company ratios:
- Engineering: 35%
- Sales: 20%  
- Marketing: 10%
- Product: 8%
- Customer Success: 8%
- Others: 19%

### Task Names
Tasks are generated using either:
1. **LLM (if configured)** - GPT-4o-mini generates realistic task names
2. **Template fallback** - Department-specific templates with placeholders

### Realistic Distributions
- **Completion rate**: ~60% of tasks marked complete
- **Assignment**: 85% of tasks assigned, 15% unassigned
- **Subtasks**: 20% of tasks have 1-4 subtasks
- **Comments**: 30% of tasks have comments

## Database Schema

| Table | Description |
|-------|-------------|
| `organizations` | Company info |
| `users` | Employee records |
| `teams` | Team definitions |
| `team_memberships` | User-team associations |
| `projects` | Project containers |
| `sections` | Project sections (To Do, In Progress, Done) |
| `tasks` | Tasks and subtasks (via parent_task_id) |
| `comments` | Task comments |

## Sample Queries

```sql
-- Count tasks by department
SELECT u.department, COUNT(*) as task_count
FROM tasks t
JOIN users u ON t.assignee_id = u.user_id
GROUP BY u.department;

-- Completion rate by project type
SELECT p.project_type, 
       ROUND(100.0 * SUM(t.completed) / COUNT(*), 1) as completion_rate
FROM tasks t
JOIN projects p ON t.project_id = p.project_id
GROUP BY p.project_type;
```
