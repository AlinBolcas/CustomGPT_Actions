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
    url: Optional[str] = None  # Keep this for backward compatibility
    image_url: Optional[str] = None  # ChatGPT-friendly field for images
    model_url: Optional[str] = None  # ChatGPT-friendly field for 3D models
    created_at: str
    id: str
    media_type: str
    prompt: Optional[str] = None
    model: str
    file_type: Optional[str] = None  # For example: jpg, png, glb, obj
    description: Optional[str] = None  # ChatGPT-friendly description field
    download_instructions: Optional[str] = None  # Direct field for download instructions 
    metadata: Optional[Dict] = None  # Additional metadata

# Helper function to extract URL from various types of Replicate outputs
def extract_url(output):
    """Extract URL string from Replicate output regardless of its type."""
    if output is None:
        return None
        
    # If it's already a string URL, return it directly
    if isinstance(output, str):
        return output
        
    # If it has a url attribute (FileOutput object)
    if hasattr(output, 'url'):
        return output.url
        
    # If it's a dictionary with a url key
    if isinstance(output, dict):
        # For Hunyuan3D model which returns {'mesh': FileOutput} structure 
        if 'mesh' in output:
            if hasattr(output['mesh'], 'url'):
                return output['mesh'].url
            elif isinstance(output['mesh'], str):
                return output['mesh']
                
        # For Trellis model which returns {'model_file': FileOutput} structure
        elif 'model_file' in output:
            if hasattr(output['model_file'], 'url'):
                return output['model_file'].url
            elif isinstance(output['model_file'], str):
                return output['model_file']
                
        # Standard dictionary with 'url' key
        elif 'url' in output:
            return output['url']
            
        # Last resort - try to find any value that has a URL attribute
        for key, value in output.items():
            if hasattr(value, 'url'):
                return value.url
        
    # If it's a list and the first item has a url attribute
    if isinstance(output, list) and len(output) > 0:
        if isinstance(output[0], str):
            return output[0]
        elif hasattr(output[0], 'url'):
            return output[0].url
            
    # If we got here, we couldn't extract a URL
    print(f"Could not extract URL from output: {type(output)}, {output}")
    return None

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
        image_output = replicate_api.generate_image(
            prompt=req.prompt,
            model=req.model,
            negative_prompt=req.negative_prompt,
            aspect_ratio=req.aspect_ratio
        )
        
        # Extract URL from output
        image_url = extract_url(image_output)
        
        if not image_url:
            raise HTTPException(
                status_code=500,
                detail="Failed to extract URL from image generation output"
            )
        
        # Generate a unique ID
        media_id = f"img_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Determine file type from URL
        file_type = "jpg"  # Default
        if image_url.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".gif")):
            file_type = image_url.lower().split(".")[-1]
            if file_type == "jpeg":
                file_type = "jpg"
                
        # Create description
        description = f"AI-generated image created from prompt: '{req.prompt}'"
        
        # Create response - use image_url for ChatGPT-friendly display
        response = MediaResponse(
            url=image_url,  # Keep for backward compatibility
            image_url=image_url,  # ChatGPT-friendly field for auto-preview
            created_at=datetime.now().isoformat(),
            id=media_id,
            media_type="image",
            prompt=req.prompt,
            model=req.model,
            file_type=file_type,
            description=description,
            download_instructions="Right-click the image and select 'Save Image As...' to download",
            metadata={
                "negative_prompt": req.negative_prompt,
                "aspect_ratio": req.aspect_ratio,
                "generation_time": datetime.now().isoformat()
            }
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
            
        # Validate image URL
        if not req.image_url or not isinstance(req.image_url, str) or not req.image_url.startswith(('http://', 'https://')):
            raise HTTPException(
                status_code=400,
                detail="Invalid image URL. Must be a valid URL starting with http:// or https://"
            )
        
        # Generate 3D model
        threed_output = replicate_api.generate_threed(
            image_url=req.image_url,
            model=req.model,
            seed=req.seed,
            remove_background=req.remove_background
        )
        
        # Debugging output to help understand what's returned
        print(f"3D model output type: {type(threed_output)}")
        if isinstance(threed_output, dict):
            print(f"3D model output keys: {threed_output.keys()}")
        
        # Extract URL from output
        threed_url = extract_url(threed_output)
        
        if not threed_url:
            raise HTTPException(
                status_code=500,
                detail="Failed to extract URL from 3D model generation output"
            )
        
        # Generate a unique ID
        media_id = f"3d_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Determine file type from URL
        file_type = "glb"  # Default
        if threed_url.lower().endswith((".glb", ".obj", ".fbx", ".usdz", ".stl")):
            file_type = threed_url.lower().split(".")[-1]
        
        # Create description and download instructions
        description = f"3D model generated from image using {req.model}"
        download_instruction = f"Click to download the {file_type.upper()} 3D model file"
        
        # Create response - use model_url for ChatGPT-friendly display
        response = MediaResponse(
            url=threed_url,  # Keep for backward compatibility
            model_url=threed_url,  # ChatGPT-friendly field
            created_at=datetime.now().isoformat(),
            id=media_id,
            media_type="3d_model",
            model=req.model,
            file_type=file_type,
            description=description,
            download_instructions=download_instruction,
            metadata={
                "source_image": req.image_url,
                "seed": req.seed,
                "remove_background": req.remove_background,
                "generation_time": datetime.now().isoformat()
            }
        )
        
        return response
        
    except Exception as e:
        print(f"Error generating 3D model: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating 3D model: {str(e)}"
        )
