# Asana Simulation — Seed Data Generator

This repository contains a data generation engine designed to create high-quality, realistic seed data for Reinforcement Learning (RL) environments simulating Asana. It models a B2B SaaS company with a workforce of 5,000–10,000 employees using Asana for product development, marketing, and operations.

## Quick Start

1. **Install dependencies**:
Ensure you have Python 3.x installed.


```bash
pip install -r requirements.txt

```


2. **Run the generator**:
The script defaults to a smaller subset for quick validation, but supports up to 10,000 users.


```bash
python src/main.py --users 5000

```


3. **Output**:
The final database is generated as `output/asana_simulation.sqlite`.



## Configuration

**`--users`**: Controls the total number of users in the simulation (Target range: 5,000–10,000).


**`--projects`**: Adjustable ratio of projects per team.



**Date Ranges**: Configurable via `.env` to adjust the company's historical growth curve (default 6 months).



## Project Structure

The repository follows a modular design to ensure separation of concerns:


**`schema.sql`**: Complete DDL for SQLite, covering Organizations, Teams, Users, Projects, Sections, Tasks, Subtasks, Comments, Custom Fields, Tags, and Attachments.



**`src/main.py`**: Orchestration entry point for the simulation.



**`src/generators/`**: Logic for individual entities, including `users.py`, `projects.py`, and `tasks.py`.



**`src/scrapers/`**: Modules for fetching external data from Y Combinator and public directories.



**`src/prompts/`**: LLM templates for generating realistic, non-generic task names and descriptions.



## Methodology Highlights


**Data Realism**: Task names follow specific patterns (e.g., "[Component] - [Action] - [Detail]" for engineering) based on analysis of 200+ public GitHub issues.



**Workload Distribution**: 15% of tasks are left unassigned, and completion rates vary by project type (60-85%) per industry benchmarks.



**Temporal Consistency**: Enforces that tasks cannot be completed before they are created.



**Relational Integrity**: Maintains strict hierarchy for subtasks and ensures users only work on projects assigned to their specific teams.


