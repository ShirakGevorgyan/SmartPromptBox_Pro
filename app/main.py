from fastapi import FastAPI
from app.routers import youtube_generate, generate
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


# App config
app = FastAPI(
    title="SmartPromptBox Pro 🤖",
    description="Receive YouTube links, return lyrics with AI",
    version="1.0.0"
)

# Routers
app.include_router(youtube_generate.router, prefix="/api/youtube", tags=["YouTube Lyrics"])
app.include_router(generate.router, prefix="/api/generate", tags=["Prompt-based Generation"])

# Root path
@app.get("/")
def root():
    return {"message": "Welcome to SmartPromptBox Pro API 🎤"}

# Health check
@app.get("/healthz")
def health():
    return {"status": "ok"}

# Exception handlers

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"error": exc.errors()})
