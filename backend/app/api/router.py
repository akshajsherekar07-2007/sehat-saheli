"""
API router aggregator.
Registers all versioned API routers under a single prefix.
Add new feature routers here as the app grows.
"""

from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.chat import router as chat_router
from app.api.v1.quiz import router as quiz_router
from app.api.v1.flashcards import router as flashcard_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.learn import router as learn_router

# ── Create the versioned API router ──────────────────────────────
api_router = APIRouter()

# ── Register feature routers ─────────────────────────────────────
api_router.include_router(auth_router)
api_router.include_router(chat_router)
api_router.include_router(quiz_router)
api_router.include_router(flashcard_router)
api_router.include_router(dashboard_router)
api_router.include_router(learn_router)
