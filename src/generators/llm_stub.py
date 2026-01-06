from faker import Faker
import random

fake = Faker()

def generate_task_title():
    # Mimics professional task naming conventions
    prefixes = ['Update', 'Implement', 'Fix', 'Refactor', 'Research']
    subjects = ['API', 'UI Module', 'Database Schema', 'Auth Flow', 'Documentation']
    
    template = random.choice([
        f"{random.choice(prefixes)} {fake.word().capitalize()} {random.choice(subjects)}",
        f"{random.choice(subjects)}: {fake.catch_phrase()}",
        f"[{fake.word().upper()}] - {fake.bs().capitalize()}"
    ])
    return template

def generate_task_body():
    # Generates tiered complexity for task descriptions
    chance = random.random()
    
    if chance < 0.15:
        return ""  # Empty description
    
    if chance < 0.50:
        return fake.paragraph(nb_sentences=3)
    
    # Detailed technical description with checklist
    overview = fake.paragraph(nb_sentences=2)
    checklist = "\n".join([f"- [ ] {fake.sentence(nb_words=5)}" for _ in range(3)])
    return f"{overview}\n\nKey Tasks:\n{checklist}"