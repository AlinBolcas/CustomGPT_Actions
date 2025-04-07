#!/usr/bin/env python3
"""
Debug script for Media Generation API
This script makes a direct request to the deployed API and prints all the response fields for debugging.
"""

import requests
import json
import sys

def debug_api_response(endpoint, data):
    """Make a request to an API endpoint and print the raw response"""
    print(f"\n🔍 DEBUG: Testing {endpoint}")
    print(f"Request data: {json.dumps(data, indent=2)}")
    
    try:
        # Make the API request
        response = requests.post(
            f"https://customgpt-actions.onrender.com{endpoint}",
            json=data
        )
        
        # Print response status
        print(f"\nResponse status: {response.status_code}")
        
        # Try to parse as JSON
        try:
            json_response = response.json()
            print(f"\nJSON Response:")
            print(json.dumps(json_response, indent=2))
            
            # Check specifically for URL fields
            url_fields = [
                "url", "image_url", "preview_url", "direct_url", 
                "model_url", "download_url"
            ]
            
            print("\n🔗 URLs in response:")
            for field in url_fields:
                if field in json_response:
                    print(f"  • {field}: {json_response[field]}")
                    
            # For convenient copying to chat
            if any(field in json_response for field in url_fields):
                print("\n📋 Copy-paste URL for testing:")
                for field in url_fields:
                    if field in json_response and json_response[field]:
                        print(json_response[field])
                        break
            
        except json.JSONDecodeError:
            print("\nNon-JSON Response:")
            print(response.text)
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

def main():
    """Main function to run tests"""
    
    # Test image generation
    image_data = {
        "prompt": "A detailed cyberpunk character design in futuristic tower",
        "model": "flux-schnell",
        "aspect_ratio": "1:1"
    }
    debug_api_response("/media/generate-image", image_data)
    
    # Test 3D model generation if provided an image URL
    if len(sys.argv) > 1:
        image_url = sys.argv[1]
        threed_data = {
            "image_url": image_url,
            "model": "trellis",
            "seed": 1234,
            "remove_background": True
        }
        debug_api_response("/media/generate-3d", threed_data)

if __name__ == "__main__":
    main() 