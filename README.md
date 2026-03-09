# InsureSmart AI - Next-Gen Insurance Portal

InsureSmart AI is a full-stack insurance portal with a React frontend, a Python Flask backend, and a MySQL database. The project is documented in SDLC phases to demonstrate production engineering practices expected by UK software teams.

Live repository: `https://github.com/nishant2-1/InsureSmart-AI`

## Why This Project

The goal is to solve a clear business problem: users struggle to choose the right insurance plan, and they need AI-assisted guidance with a transparent user dashboard.

This repository is intentionally structured to show a senior engineering mindset:
- Requirement-first development
- Architecture and API design before scaling features
- Secure implementation patterns
- Test-driven quality checks
- Deployment planning for Azure

## Core Features

- 🛡️ Chat-to-Insight Advisor for policy recommendations
- 🔐 Secure login with JWT and bcrypt password hashing
- 📊 Policy management dashboard with active coverage tracking
- 🗂️ Conversation history persistence for AI consultations
- ⚡ Defensive fallback mode when AI provider is unavailable

## Quick Start (Visual)

- 🚀 Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```

- 💻 Frontend Setup

```bash
cd frontend
npm install
npm start
```

- 🌱 Seed Demo Data

```bash
cd backend
python seed.py
```

## UI Preview

Add a screenshot after running the app and save it as `docs/images/dashboard.png`:

```markdown
![InsureSmart Dashboard](docs/images/dashboard.png)
```

## Three-Tier Architecture Data Flow

1. Frontend (Presentation): React captures user needs, such as travel or health insurance requests.
2. Backend (Logic): Flask validates JWT authentication and processes the AI advisor request.
3. Database (Storage): MySQL stores users, policies, claims, and AI chat history records.

## SDLC Phase 1: Requirements Gathering

### Problem Statement

Users need a faster and more accurate way to discover insurance plans that match their profile and financial goals.

### Functional Requirements

- The system shall allow a user to register, log in, and log out securely.
- The system shall allow authenticated users to view active policies.
- The system shall allow authenticated users to create and view claims history.
- The system shall provide an AI policy advisor endpoint.
- The system shall store user, policy, and claim data in a relational database.
- The system shall expose REST APIs for frontend consumption.

### Non-Functional Requirements

- API responses for core routes should return within 2 seconds under normal development load.
- Passwords must be hashed and never stored in plain text.
- Secrets must be loaded from environment variables and never committed to source control.
- The frontend must support responsive layout for desktop and mobile widths.
- The backend must include baseline unit tests for critical routes.

## SDLC Phase 2: System Design

### High-Level Design (HLD)

1. React frontend sends HTTP requests via Axios.
2. Flask backend handles authentication, policy, claims, and AI routes.
3. SQLAlchemy maps backend models to MySQL tables.
4. JWT secures protected endpoints.

See full architecture notes in `docs/ARCHITECTURE.md`.

### Low-Level Design (LLD)

Core database tables:
- `users`
- `policies`
- `claims`
- `chat_history`

Core API endpoints:
- `GET /api/hello`
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`
- `GET /api/policies`
- `POST /api/policies`
- `GET /api/policies/{id}`
- `GET /api/policies/{id}/claims`
- `POST /api/policies/{id}/claims`
- `POST /api/ai/policy-advisor`
- `GET /api/ai/history`

## SDLC Phase 3: Implementation Standards

### Version Control Strategy

- Commit after each small feature is completed.
- Use Conventional Commits: `feat:`, `fix:`, `test:`, `docs:`, `refactor:`.
- Push frequently to show visible development progress.

Suggested feature commit flow:
1. `feat: add login form validation`
2. `feat: add policy list filtering`
3. `test: add auth route regression tests`
4. `docs: update architecture decisions`

### Clean Code Rules

- Use descriptive names (`registration_date`, not `d`).
- Keep route handlers small and explicit.
- Validate request payloads before business logic.

### Environment and Secrets

- Keep secrets in `backend/.env`.
- Track only `backend/.env.example`.
- Never commit API keys to GitHub.

## SDLC Phase 4: Testing and QA

### Unit Testing

Backend test command:

```bash
cd backend
pytest --cov=app tests/
```

Frontend test command:

```bash
cd frontend
npm test
```

### Manual Testing Bug Report Process

For each bug found during manual testing, capture this template in GitHub Issues:

- Expected behavior
- Actual behavior
- Steps to reproduce
- Root cause
- Fix applied
- Verification result

The repository includes an issue template at `.github/ISSUE_TEMPLATE/bug_report.yml`.

## SDLC Phase 5: Deployment and Documentation

- Target deployment: Azure Static Web Apps.
- Deployment checklist: `docs/DEPLOYMENT.md`.
- Architecture and HLD/LLD notes: `docs/ARCHITECTURE.md`.
- Sprint implementation playbook: `docs/SDLC_SPRINT_PLAYBOOK.md`.

## Tech Stack

- Frontend: React 18, React Router, Tailwind CSS, Axios
- Backend: Flask, SQLAlchemy, Flask-JWT-Extended, Repository Pattern
- Database: MySQL
- AI: OpenAI API integration path via backend route
- Testing: Pytest and React Testing Library
- Deployment: Azure Static Web Apps, Azure App Service

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js 16+
- MySQL 8+

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```

Backend URL: `http://localhost:5000`

### Frontend

```bash
cd frontend
npm install
npm start
```

Frontend URL: `http://localhost:3000`

### Hello World Connection Check

Run both apps, then confirm:
- Browser home page shows `API Connection: Hello from InsureSmart AI backend`
- Direct API check: `GET http://localhost:5000/api/hello`

## Project Structure

```text
InsureSmart AI/
├── backend/
├── frontend/
├── docs/
└── .github/
```

## Future Roadmap

- Add PDF generation for insurance certificates.
- Add CI/CD quality gates with test and lint checks.
- Add role-based access for admin and support operations.

## Copilot Prompt Sequence Used

Use these in order while developing new features:

1. "I am building an Insurance AI portal. Help me write a Software Requirement Specification list for the core features."
2. "Help me design a MySQL database schema for a user-based insurance portal with AI history."
3. "Help me write the boilerplate for a Flask API that connects to MySQL."
4. "Write 3 unit tests for my login route using Pytest."

## Support

- Issues: `https://github.com/nishant2-1/InsureSmart-AI/issues`
- Discussions: `https://github.com/nishant2-1/InsureSmart-AI/discussions`
