import requests
import os
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base URL for API
BASE_URL = "https://customgpt-actions.onrender.com"  # Changed from localhost to the deployed render.com URL

def test_image_generation():
    """Test generating an image with both available models."""
    
    # Test parameters
    models = ["flux-schnell", "imagen-3-fast"]
    prompt = "A futuristic city with flying cars and neon lights"
    
    print("\n===== TESTING IMAGE GENERATION =====")
    
    for model in models:
        print(f"\nGenerating image with model: {model}")
        
        # Prepare request data
        data = {
            "prompt": prompt,
            "model": model,
            "aspect_ratio": "16:9"
        }
        
        # Make the API request
        try:
            response = requests.post(f"{BASE_URL}/media/generate-image", json=data)
            response.raise_for_status()  # Raise exception for HTTP errors
            
            result = response.json()
            print(f"Success! Image URL: {result['url']}")
            print(f"Media ID: {result['id']}")
            
            # You could add download functionality here if needed
            
        except Exception as e:
            print(f"Error generating image with {model}: {str(e)}")

def test_3d_generation():
    """Test generating a 3D model from an image."""
    
    # Test parameters - use an image URL from a previous generation or a hosted image
    image_url = input("Enter an image URL to convert to 3D model: ")
    
    if not image_url:
        print("No image URL provided, skipping 3D generation test")
        return
    
    models = ["trellis", "hunyuan3d"]
    
    print("\n===== TESTING 3D MODEL GENERATION =====")
    
    for model in models:
        print(f"\nGenerating 3D model with {model} from image...")
        
        # Prepare request data
        data = {
            "image_url": image_url,
            "model": model,
            "seed": 1234,
            "remove_background": True
        }
        
        # Make the API request
        try:
            response = requests.post(f"{BASE_URL}/media/generate-3d", json=data)
            response.raise_for_status()  # Raise exception for HTTP errors
            
            result = response.json()
            print(f"Success! 3D model URL: {result['url']}")
            print(f"Media ID: {result['id']}")
            
            # You could add download functionality here if needed
            
        except Exception as e:
            print(f"Error generating 3D model with {model}: {str(e)}")

if __name__ == "__main__":
    # Run the tests
    test_image_generation()
    
    # Ask if user wants to test 3D generation (needs an image URL)
    if input("\nDo you want to test 3D model generation? (y/n): ").lower() == 'y':
        test_3d_generation()
