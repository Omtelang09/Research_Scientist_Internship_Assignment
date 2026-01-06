# LLM Prompt Templates for Asana Simulation

This file contains the prompt templates used by the task generation engine to produce realistic, non-generic task metadata.

---

## 1. Task Name Generator
**Usage**: Generates concise, action-oriented titles based on project category.

**Prompt**:
> "Generate a realistic task name for a {project_type} project in a B2B SaaS product team. 
> The name should be 3-7 words long. 
> Use professional terminology (e.g., 'Refactor', 'Provision', 'Onboard', 'Validate').
> 
> **Examples**:
> - Engineering: 'Refactor auth middleware for JWT validation'
> - Marketing: 'Coordinate Q3 product launch social assets'
> - Design: 'Create high-fidelity mockups for billing dashboard'
> - HR: 'Update employee handbook for remote work policy'"

---

## 2. Task Description Generator
**Usage**: Creates context-aware descriptions with technical or business depth.

**Prompt**:
> "Write a brief task description (2-4 sentences) for the task '{task_name}' within the context of a '{project_type}' initiative.
> 
> **Requirements**:
> - Tone: Professional and concise.
> - Structure: State the 'Why' and the 'What'.
> - Include a 'Definition of Done' or 'Acceptance Criteria' bulleted list for 30% of responses.
> 
> **Context**: {project_context}"

---

## 3. Comment Generator
**Usage**: Simulates team collaboration and status updates.

**Prompt**:
> "Generate a realistic project management comment for the task '{task_name}'. 
> The comment should reflect one of the following states: 
> 1. A blocker update.
> 2. A request for review.
> 3. A notification of completion.
> 4. A question regarding the description."