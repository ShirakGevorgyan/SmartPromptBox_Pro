"""Minimal FastAPI app for health checks and simple diagnostics.

This service can be used as:
- a container health probe (e.g., `/healthz`),
- a very small public surface to verify the deployment is running,
- a placeholder API if you decide to add HTTP endpoints later.

The Telegram bot runs separately; this HTTP app is intentionally lightweight.
"""

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


# App config
app = FastAPI(
    title="SmartPromptBox Pro 🤖",
    description="Receive YouTube links, return lyrics with AI",
    version="1.0.0",
)


# Root path
@app.get("/")
def root():
    """Simple greeting to verify the API is reachable."""
    return {"message": "Welcome to SmartPromptBox Pro API 🎤"}


# Health check
@app.get("/healthz")
def health():
    """Kubernetes/Compose health probe endpoint."""
    return {"status": "ok"}


# Exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Normalize Starlette HTTP errors into JSON payloads."""
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Return validation errors with a 422 status and structured details."""
    return JSONResponse(status_code=422, content={"error": exc.errors()})
