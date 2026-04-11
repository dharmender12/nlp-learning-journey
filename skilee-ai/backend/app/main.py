import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth, contracts, applications, users

app = FastAPI(title="Skilee-AI API", version="1.0.0")

frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(contracts.router)
app.include_router(applications.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "Skilee-AI backend running"}
