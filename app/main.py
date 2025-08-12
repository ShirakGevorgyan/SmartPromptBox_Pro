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
