# InsureSmart AI - System Architecture

## System Overview

InsureSmart AI is a full-stack insurance platform with clear HLD and LLD documentation so engineering decisions are traceable.

## HLD (High-Level Design)

System context:
- React frontend provides user-facing workflows.
- Flask backend provides authentication, policy, claims, and AI endpoints.
- MySQL stores persistent relational data.
- JWT secures protected requests.

Three-tier flow:
1. Presentation tier: React captures insurance intent from authenticated users.
2. Logic tier: Flask validates identity and generates advisor output from OpenAI with a fallback engine.
3. Storage tier: MySQL persists user profiles, selected policies, and AI consultation history.

## Tech Stack

- Frontend: React
- Backend: Flask
- Database: MySQL
- AI Logic: OpenAI API

## Design Pattern

- RESTful API Architecture for client-server communication.
- Repository Pattern for database interactions via `backend/app/repositories.py`.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     Frontend Layer (React)                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ HomePage │ LoginPage │ RegisterPage │ DashboardPage    │  │
│  │ (Public)  │ (Public)  │ (Public)     │ (Protected)     │  │
│  └──────────────────────────────────────────────────────────┘  │
│              │                                    │              │
│              └────────────────────────────────────┘              │
│                    React Router Handling                         │
│              Tailwind CSS Styling (Responsive)                  │
│              JWT Authentication via localStorage                │
└─────────────────────────────────────────────────────────────────┘
                           │
                    HTTP (Axios API Calls)
                           │
┌─────────────────────────────────────────────────────────────────┐
│                     Backend Layer (Flask)                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Auth Routes: /auth/register, /auth/login, /auth/me      │  │
│  │ Policy Routes: GET/POST /policies, GET /policies/{id}   │  │
│  │ Claims Routes: GET/POST /policies/{id}/claims            │  │
│  │ AI Routes: POST /ai/policy-advisor                       │  │
│  └──────────────────────────────────────────────────────────┘  │
│              │                                    │              │
│              │    JWT Middleware Validation       │              │
│              └────────────────────────────────────┘              │
│                 SQLAlchemy ORM Data Layer                        │
└─────────────────────────────────────────────────────────────────┘
                           │
                      SQL Queries
                           │
┌─────────────────────────────────────────────────────────────────┐
│                     Database Layer (MySQL)                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Table: users      │ Table: policies │ Table: claims     │  │
│  │ - id              │ - id            │ - id              │  │
│  │ - email           │ - user_id       │ - user_id         │  │
│  │ - password_hash   │ - policy_type   │ - policy_id       │  │
│  │ - full_name       │ - coverage_amt  │ - claim_amount    │  │
│  │ - created_at      │ - premium       │ - status          │  │
│  │                   │ - status        │ - created_at      │  │
│  │                   │ - start_date    │                   │  │
│  │                   │ - end_date      │                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

## Key Technologies

- **Frontend**: React 18, React Router 6, Tailwind CSS
- **Backend**: Flask, SQLAlchemy ORM, PyJWT
- **Database**: MySQL 8.0
- **AI**: OpenAI API (for policy recommendations)
- **Testing**: Pytest, Jest
- **Deployment**: Azure Static Web Apps

## LLD (Low-Level Design)

### Database Entities

- `users`: account identity and credentials
- `policies`: user policy ownership and lifecycle data
- `claims`: claim records tied to user and policy
- `chat_history`: advisor prompt, summary, recommended policy, and timestamp

### API Contract

Public endpoints:
- `GET /api/hello`
- `POST /api/auth/register`
- `POST /api/auth/login`

Protected endpoints:
- `GET /api/auth/me`
- `GET /api/policies`
- `POST /api/policies`
- `GET /api/policies/{id}`
- `GET /api/policies/{id}/claims`
- `POST /api/policies/{id}/claims`
- `POST /api/ai/policy-advisor`
- `GET /api/ai/history`

### Security Controls

- Password hashing via bcrypt
- Token-based auth via JWT
- ORM usage via SQLAlchemy to reduce SQL injection risk
- Environment variable-based secrets handling

## Endpoint Reference

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user (Protected)

### Policies
- `GET /api/policies` - Get user's policies (Protected)
- `POST /api/policies` - Create new policy (Protected)
- `GET /api/policies/{id}` - Get specific policy (Protected)

### Claims
- `GET /api/policies/{id}/claims` - Get claims for a policy (Protected)
- `POST /api/policies/{id}/claims` - Submit new claim (Protected)

### AI Advisor
- `POST /api/ai/policy-advisor` - Get policy recommendations from AI (Protected)
- `GET /api/ai/history` - Get last advisor conversations (Protected)

## Data Flow

1. Client authenticates using `/api/auth/login`.
2. Backend returns JWT token.
3. Client sends token in `Authorization: Bearer <token>`.
4. Backend verifies token and executes protected route logic.
5. SQLAlchemy persists and retrieves data from MySQL.
