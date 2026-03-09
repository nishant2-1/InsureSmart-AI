# InsureSmart AI - System Architecture

## System Overview

InsureSmart AI is a full-stack intelligent insurance portal built with modern technologies. This document outlines the system architecture and component interactions.

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

## API Endpoints

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
- `POST /api/ai/policy-advisor` - Get policy recommendations from AI

## Data Flow

1. User registers/logs in via the frontend
2. Backend validates credentials and issues JWT token
3. Frontend stores token in localStorage
4. Subsequent requests include JWT in Authorization header
5. Backend validates token before processing protected routes
6. Data is persisted in MySQL database
7. AI advisor processes natural language input and returns recommendations

## Security Measures

- Password hashing with Werkzeug
- JWT token-based authentication
- Protected routes with JWT middleware
- CORS configuration for frontend-backend communication
- SQL injection prevention via SQLAlchemy ORM
