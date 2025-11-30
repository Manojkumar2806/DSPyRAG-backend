
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


try:
    import dspy_config 
except Exception:
    dspy_config = None

from routes.chat import router as chat_router
from routes.system import router as system_router
from routes.medical import router as medical_router

app = FastAPI(title="MedSage API — Memory-First Medical Reasoning")

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


import importlib, sys, types

try:
    openai = importlib.import_module("openai")
except Exception:
    openai = types.ModuleType("openai")
    sys.modules["openai"] = openai

# ensure expected exception symbols exist
if not hasattr(openai, "AuthenticationError"):
    class AuthenticationError(Exception):
        """Compatibility shim for packages expecting openai.AuthenticationError"""
        pass
    openai.AuthenticationError = AuthenticationError

if not hasattr(openai, "OpenAIError"):
    openai.OpenAIError = getattr(openai, "OpenAIError", Exception)



@app.get("/")
def root():
    return {"message": "MedSage API Running", "status": "ok"}

@app.get("/health")
def health():
    return {"status": "ok"}
