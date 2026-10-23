from fastapi import FastAPI
from config.settings import settings
from src.api.routes import router as api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root_health_check():
    return {
        "status": "active",
        "project": settings.PROJECT_NAME,
        "engine": "NVIDIA Nemotron via Nebius"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)