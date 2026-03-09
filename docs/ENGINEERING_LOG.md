# Engineering Log

This log documents how InsureSmart AI was delivered using SDLC-style sprint execution, with AI assistance and explicit human verification at each phase.

## Phase 1: Database and Environment Setup

Goal: Build the memory layer and secure configuration.

Tasks:
- Create `users`, `policies`, and `chat_history` schema.
- Store secrets in environment variables.
- Keep `.env` out of version control.

Copilot prompt:
"Create a MySQL schema for 'InsureSmart'. I need a 'Users' table with hashed passwords, a 'Policies' table (Health, Life, Auto), and a 'ChatHistory' table to store AI recommendations."

Validation note:
- I manually checked schema relationships (`users -> policies`, `users -> chat_history`) and verified sensitive config values were excluded by `.gitignore`.

## Phase 2: AI Integration

Goal: Turn the advisor into a reliable assistant with guardrails.

Tasks:
- Add a system-role prompt for consistent insurance recommendations.
- Return a polite explanation if no policy is a fit.
- Save each consultation to `chat_history`.

Copilot prompt:
"Write a Python function that uses the OpenAI API. The system prompt should be: 'You are a professional insurance advisor. Use the following JSON list of policies to recommend the best one to the user based on their needs. If no policy fits, explain why politely.'"

Validation note:
- I manually reviewed prompts to minimize hallucination risk and enforced fallback behavior so recommendations map only to known policy records.

## Phase 3: Frontend Dashboard

Goal: Build a fintech-style operations panel.

Tasks:
- Sidebar navigation for policy operations.
- Cards for active policy overview.
- Chat window for AI consultation.

Copilot prompt:
"Create a React dashboard component using Tailwind. It should have a sidebar for navigation, a main area showing 'My Active Policies' as cards, and a 'Consult AI' chat window."

Validation note:
- I manually tested responsive layouts and route behavior to ensure the dashboard components work on both desktop and mobile widths.

## Phase 4: QA and Testing

Goal: Prove reliability and defect tracking discipline.

Tasks:
- Add unit tests for login failure and advisor output.
- Validate advisor history persistence.
- Log manual bugs through GitHub issue templates.
- Conduct AI-assisted code reviews to identify potential security vulnerabilities in the JWT authentication flow.

Copilot prompt:
"Write 3 Unit Tests using PyTest to ensure that the AI Advisor returns a valid recommendation and the Login API handles wrong passwords correctly."

Validation note:
- I reviewed test coverage manually and verified that failing-auth, fallback-advisor, and history persistence paths are explicitly exercised.

## Phase 5: Deployment and Reporting

Goal: Publish and document production readiness.

Tasks:
- Deploy to Azure Static Web Apps.
- Add setup and architecture instructions to README.
- Track release increments through small, frequent commits.

Validation note:
- I verified deployment documentation includes Azure-specific commands and environment variable guidance suitable for team handoff.

## Why This Improves Recruiter Signal

- Process mastery: Demonstrates practical sprint and SDLC execution.
- Transparency: Shows AI-assisted development with clear human quality gates.
- Structure: Separates responsibilities by database, AI logic, UI, QA, and deployment.
