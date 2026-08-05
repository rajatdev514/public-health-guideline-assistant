from fastapi import FastAPI

app = FastAPI(
    title = "Public Health Guideline Assistant",
    description= "Production-grade RAG API for Tuberculosis Guidelines",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message" : "Welcome to the Public Health Guideline Assistant API"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }