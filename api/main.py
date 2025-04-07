from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from datetime import datetime

# Import our replicate router
from api.replicate_router import router as replicate_router

app = FastAPI(
    title="Media Generation API",
    description="Generate images and 3D models using AI",
    version="1.0.0"
)

# Add CORS middleware to allow ChatGPT to display images and load 3D models
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Include the replicate router
app.include_router(replicate_router)

@app.get("/")
def read_root():
    """Root endpoint with API info"""
    import platform
    import sys
    
    return {
        "status": "running",
        "service": "Media Generation API",
        "version": "1.1.0",
        "documentation": "Use /docs for OpenAPI documentation",
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "replicate_configured": bool(os.environ.get("REPLICATE_API_TOKEN"))
        }
    }

if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment variable for Render deployment
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True) 