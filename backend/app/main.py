from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routes.api_key import router1 as api_key_router
from app.routes.auth import router2 as auth_router
from app.db.base import Base
from app.db.session import engine
from contextlib import asynccontextmanager
from fastapi import Request
from app.core.exceptions import AuthError

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown logic (if any) goes here

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(AuthError)
async def auth_error_handler(request: Request, exc: AuthError):
    return JSONResponse(
        status_code=401,
        content={"detail": str(exc)},
    )

app.include_router(api_key_router,prefix="/api_f/v1")
app.include_router(auth_router,prefix="/auth_f/v1")


@app.get("/")
def home_p():
    return {"Shit you have 0 coding language"}

@app.get("/healthz")
def health():
    return {"status": "ok"}