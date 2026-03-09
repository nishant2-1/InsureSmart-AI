# SDLC Sprint Playbook

This file captures the implementation flow used to build InsureSmart AI like a real company sprint.

## Phase 1: Database and Environment Setup

Goal: Build the memory layer and secure configuration.

Tasks:
- Create `users`, `policies`, and `chat_history` schema.
- Store secrets in environment variables.
- Keep `.env` out of version control.

Copilot prompt:
"Create a MySQL schema for 'InsureSmart'. I need a 'Users' table with hashed passwords, a 'Policies' table (Health, Life, Auto), and a 'ChatHistory' table to store AI recommendations."

## Phase 2: AI Integration

Goal: Turn the advisor into a reliable assistant with guardrails.

Tasks:
- Add a system-role prompt for consistent insurance recommendations.
- Return a polite explanation if no policy is a fit.
- Save each consultation to `chat_history`.

Copilot prompt:
"Write a Python function that uses the OpenAI API. The system prompt should be: 'You are a professional insurance advisor. Use the following JSON list of policies to recommend the best one to the user based on their needs. If no policy fits, explain why politely.'"

## Phase 3: Frontend Dashboard

Goal: Build a fintech-style operations panel.

Tasks:
- Sidebar navigation for policy operations.
- Cards for active policy overview.
- Chat window for AI consultation.

Copilot prompt:
"Create a React dashboard component using Tailwind. It should have a sidebar for navigation, a main area showing 'My Active Policies' as cards, and a 'Consult AI' chat window."

## Phase 4: QA and Testing

Goal: Prove reliability and defect tracking discipline.

Tasks:
- Add unit tests for login failure and advisor output.
- Validate advisor history persistence.
- Log manual bugs through GitHub issue templates.

Copilot prompt:
"Write 3 Unit Tests using PyTest to ensure that the AI Advisor returns a valid recommendation and the Login API handles wrong passwords correctly."

## Phase 5: Deployment and Reporting

Goal: Publish and document production readiness.

Tasks:
- Deploy to Azure Static Web Apps.
- Add setup and architecture instructions to README.
- Track release increments through small, frequent commits.
