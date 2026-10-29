from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router

app = FastAPI(title="Vocal Remover API", version="1.0.0")

# Configure CORS for local development and production frontends
origins = [
    "http://localhost:4200",  # Angular local dev
    "https://*.netlify.app",    # Netlify deployments
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust or restrict in strict production environments if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Vocal Remover FastAPI Backend is running."}