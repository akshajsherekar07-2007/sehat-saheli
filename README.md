# Sehat Saheli 🌸

> AI-powered multilingual health companion PWA for adolescent girls in low-connectivity rural areas

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 16 (App Router) + TypeScript + TailwindCSS + ShadCN + React Query + Zustand + Framer Motion |
| Backend | FastAPI + SQLAlchemy (Async) + MySQL/PostgreSQL + Alembic + JWT Auth |
| AI | Google Gemini API |
| PWA | Service Workers + IndexedDB (Dexie.js) + Workbox |

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.11+
- MySQL 8.0+

### Backend Setup

```bash
cd backend

# Create virtual environment (optional)
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your database credentials and Gemini API key

# Create database
mysql -u root -e "CREATE DATABASE IF NOT EXISTS sehat_saheli CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start development server
npm run dev
```

### Access
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Architecture

```
sehat-saheli/
├── frontend/          # Next.js PWA
│   ├── src/
│   │   ├── app/       # Pages (App Router)
│   │   ├── components/  # UI components
│   │   ├── hooks/     # Custom React hooks
│   │   ├── lib/       # Utilities, API, stores, i18n
│   │   ├── providers/ # React context providers
│   │   └── types/     # TypeScript definitions
│   └── public/        # Static assets + PWA manifest
│
├── backend/           # FastAPI API
│   ├── app/
│   │   ├── api/       # Route handlers
│   │   ├── core/      # Config, security, middleware
│   │   ├── models/    # SQLAlchemy ORM models
│   │   ├── schemas/   # Pydantic validation
│   │   ├── services/  # Business logic
│   │   └── repositories/  # Data access
│   └── alembic/       # Database migrations
```

## Features

- 🤖 **AI Chatbot** — Culturally-safe health conversations in 8 languages
- 📚 **Visual Education** — Health topics with diagrams and illustrations
- 🧠 **Quiz Engine** — Gamified health knowledge testing
- 🃏 **Flashcards** — Interactive learning cards
- ❤️ **Health Dashboard** — Menstrual cycle tracker with analytics
- 🏥 **Health Camps** — Government health camp alerts
- 📱 **PWA** — Installable, offline-first progressive web app
- 🌐 **Multilingual** — English, Hindi, Marathi, Bengali, Tamil, Telugu, Kannada, Gujarati

## Languages Supported

| Code | Language | Native Name |
|------|----------|-------------|
| en | English | English |
| hi | Hindi | हिन्दी |
| mr | Marathi | मराठी |
| bn | Bengali | বাংলা |
| ta | Tamil | தமிழ் |
| te | Telugu | తెలుగు |
| kn | Kannada | ಕನ್ನಡ |
| gu | Gujarati | ગુજરાતી |

## License

MIT
