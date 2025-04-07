from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional, Union
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Import the ReplicateAPI class from the integrations folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from integrations.replicate_API import ReplicateAPI

# Create router
router = APIRouter(
    prefix="/media",
    tags=["media"],
    responses={404: {"description": "Not found"}},
)

# Initialize the Replicate API
replicate_api = ReplicateAPI()

# Request models
class ImageGenerationRequest(BaseModel):
    prompt: str
    model: str = "flux-schnell"  # Limited options: "flux-schnell" or "imagen-3-fast"
    negative_prompt: Optional[str] = None
    aspect_ratio: str = "16:9"
    
class ThreeDGenerationRequest(BaseModel):
    image_url: str
    model: str = "trellis"  # Options: "hunyuan3d" or "trellis"
    seed: int = 1234
    remove_background: bool = True

# Response models
class MediaResponse(BaseModel):
    url: str
    created_at: str
    id: str
    media_type: str
    prompt: Optional[str] = None
    model: str

# Routes
@router.post("/generate-image", response_model=MediaResponse)
def generate_image(req: ImageGenerationRequest):
    """Generate an image using either flux-schnell or imagen-3-fast model."""
    try:
        # Validate model choice
        if req.model not in ["flux-schnell", "imagen-3-fast"]:
            raise HTTPException(
                status_code=400, 
                detail="Model must be either 'flux-schnell' or 'imagen-3-fast'"
            )
        
        # Generate image
        image_url = replicate_api.generate_image(
            prompt=req.prompt,
            model=req.model,
            negative_prompt=req.negative_prompt,
            aspect_ratio=req.aspect_ratio
        )
        
        if not image_url:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate image"
            )
        
        # Generate a unique ID
        media_id = f"img_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Create response
        response = MediaResponse(
            url=image_url,
            created_at=datetime.now().isoformat(),
            id=media_id,
            media_type="image",
            prompt=req.prompt,
            model=req.model
        )
        
        return response
        
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating image: {str(e)}"
        )

@router.post("/generate-3d", response_model=MediaResponse)
def generate_threed(req: ThreeDGenerationRequest):
    """Generate a 3D model from an image using hunyuan3d or trellis model."""
    try:
        # Validate model choice
        if req.model.lower() not in ["hunyuan3d", "trellis"]:
            raise HTTPException(
                status_code=400, 
                detail="Model must be either 'hunyuan3d' or 'trellis'"
            )
        
        # Generate 3D model
        threed_url = replicate_api.generate_threed(
            image_url=req.image_url,
            model=req.model,
            seed=req.seed,
            remove_background=req.remove_background
        )
        
        if not threed_url:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate 3D model"
            )
        
        # Generate a unique ID
        media_id = f"3d_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Create response
        response = MediaResponse(
            url=threed_url,
            created_at=datetime.now().isoformat(),
            id=media_id,
            media_type="3d_model",
            model=req.model
        )
        
        return response
        
    except Exception as e:
        print(f"Error generating 3D model: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating 3D model: {str(e)}"
        )
