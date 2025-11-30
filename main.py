# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Optional DSPy config (non-fatal)
try:
    import dspy_config  # optional
except Exception:
    dspy_config = None

# Use relative imports so package mode works
from routes.chat import router as chat_router
from routes.system import router as system_router
from routes.medical import router as medical_router

app = FastAPI(title="MedSage API — Memory-First Medical Reasoning")

# CORS for local dev (tighten for prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers under /api
app.include_router(chat_router, prefix="/api/chat", tags=["chat"])
app.include_router(system_router, prefix="/api/system", tags=["system"])
app.include_router(medical_router, prefix="/api/medical", tags=["medical"])

# compatibility shim — put at top of main.py before other imports
try:
    import openai  # noqa: E401
    from openai import AuthenticationError  # try direct import
except Exception:
    try:
        import openai as _openai
        import openai.error as _oe
        # ensure openai.AuthenticationError exists for legacy imports
        setattr(_openai, "AuthenticationError", getattr(_oe, "AuthenticationError", Exception))
    except Exception:
        pass


@app.get("/")
def root():
    return {"message": "MedSage API Running", "status": "ok"}

@app.get("/health")
def health():
    return {"status": "ok"}
