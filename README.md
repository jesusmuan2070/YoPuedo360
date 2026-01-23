# YoPuedo360 - Language Learning Platform

A personalized language learning platform with AI-powered instruction, gamification, and adaptive learning paths.

## 🏗️ Architecture

```
YoPuedo360/
├── backend/          # Django REST API
├── frontend/         # React + Vite
├── docs/             # Documentation
└── configs/          # Configuration files
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (or SQLite for development)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

## 🔐 Admin Panel

Access the Django admin panel to manage users, learning profiles, and content:

```
URL: http://localhost:8000/admin/
```

You need a superuser account:
```bash
python manage.py createsuperuser
```

### Admin Features

| Model | Description |
|-------|-------------|
| **Users** | User accounts with OAuth connections |
| **Learning Profiles** | CEFR levels, XP, streaks, learning preferences |
| **Daily Activities** | Study time tracking (read-only) |
| **Scenarios** | Learning scenarios organized by category |
| **Milestones** | Learning milestones within scenarios |
| **Vocabulary** | Words and phrases with SRS tracking |
| **Grammar** | Grammar units with contextual examples |

## 📡 API Endpoints

### Users API (`/api/v1/users/`)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/me/` | GET, PATCH, DELETE | User profile management |
| `/me/dashboard/` | GET | Aggregated stats for home screen |
| `/me/record-session/` | POST | Record study session time |
| `/me/activity/` | GET | Activity history (calendar/heatmap) |
| `/me/streaks/` | GET | Streak details with at-risk detection |
| `/me/xp-history/` | GET | XP progress and level info |
| `/me/settings/` | GET, PATCH | User preferences |

### Learning Path API (`/api/v1/learning-path/`)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/scenarios/` | GET | List available scenarios |
| `/milestones/` | GET | List milestones |
| `/recommendations/` | GET | Personalized recommendations |

## 🎮 Gamification System

### XP System

- **CEFR Multipliers**: Higher levels = more XP
  - A1: 1.0x, A2: 1.2x, B1: 1.5x, B2: 2.0x, C1: 2.5x, C2: 3.0x
- **Activities**: Exercises, milestones, vocabulary, grammar
- **Bonuses**: Daily goal completion, streak milestones

### Streak System

- Minimum 5 minutes of study per day to maintain streak
- Streak bonus XP at milestones (7, 30, 100, 365 days)

### Inactivity Penalties

- Grace period on first inactive day
- Progressive penalties: 5 → 10 → 15 → 20 XP max per day
- Level protection: XP never drops below 0

## 🧪 Testing

```bash
cd backend

# Run all tests
python -m pytest

# Run specific app tests
python -m pytest apps/users/tests.py -v

# Run with coverage
python -m pytest --cov=apps
```

## 📝 Management Commands

```bash
# Apply inactivity penalties (run daily via cron)
python manage.py apply_inactivity_penalties

# Update daily streaks (run daily via cron)
python manage.py update_daily_streaks

# Dry run (see what would happen without making changes)
python manage.py apply_inactivity_penalties --dry-run
```

## 🔧 Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Django
SECRET_KEY=your-secret-key
DEBUG=True

# Database
DATABASE_URL=postgres://user:pass@localhost:5432/yopuedo360

# AI Providers
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

## 📚 Documentation

- [Git Workflow](GIT_WORKFLOW.md)
- [Design System](DESIGN_SYSTEM.md)
- [Architecture Details](architecture_detailed.py)

## 🤝 Contributing

1. Create a feature branch from `develop`
2. Make your changes with tests
3. Submit a pull request

## 📄 License

Proprietary - All rights reserved
