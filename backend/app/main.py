from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import nutrition

app = FastAPI(
    title="FoodieAI API",
    description="Backend API for FoodieAI nutrition and meal planning",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(nutrition.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to FoodieAI API"}
