# Examples for ChatGPT: Media API Response Handling

When our Media Generation API returns an image or 3D model, here are examples of how to properly use those in your responses:

## For Images

When you receive a response from the `/media/generate-image` endpoint, you'll get an object like:

```json
{
  "image_url": "https://replicate.delivery/xezq/EseCYd9pJjy4Py6mdxIhysjtdOArOw7TXMJv5FfiBrPwZOgUA/out-0.jpg",
  "direct_url": "https://replicate.delivery/xezq/EseCYd9pJjy4Py6mdxIhysjtdOArOw7TXMJv5FfiBrPwZOgUA/out-0.jpg",
  "description": "AI-generated image created from prompt: 'A cyberpunk character'",
  "download_instructions": "Right-click the image and select 'Save Image As...' to download"
}
```

**DO**:
- Use the `image_url` directly to display the image
- Example response: "Here's the generated image: ![Generated Image](https://replicate.delivery/xezq/EseCYd9pJjy4Py6mdxIhysjtdOArOw7TXMJv5FfiBrPwZOgUA/out-0.jpg)"
- Alternative response: "Here's your image: [View Image](https://replicate.delivery/xezq/EseCYd9pJjy4Py6mdxIhysjtdOArOw7TXMJv5FfiBrPwZOgUA/out-0.jpg)"

**DON'T**:
- Don't construct your own URL
- Don't modify the domain or path

## For 3D Models

When you receive a response from the `/media/generate-3d` endpoint, you'll get an object like:

```json
{
  "model_url": "https://replicate.delivery/pbxt/AEgGU9rW3PF3AwVd4La5W3zG5MsM6LHwv3GoYofjJ0lSP52cA/model.glb",
  "download_url": "https://replicate.delivery/pbxt/AEgGU9rW3PF3AwVd4La5W3zG5MsM6LHwv3GoYofjJ0lSP52cA/model.glb",
  "description": "3D model generated from image using trellis",
  "download_instructions": "Click to download the GLB 3D model file"
}
```

**DO**:
- Provide a direct link to the 3D model using `model_url` or `download_url`
- Example response: "Your 3D model is ready! [Download 3D Model](https://replicate.delivery/pbxt/AEgGU9rW3PF3AwVd4La5W3zG5MsM6LHwv3GoYofjJ0lSP52cA/model.glb)"

**DON'T**:
- Don't build your own URL
- Don't attempt to embed the 3D model directly

## General Tips

1. Always use the complete URL returned by the API
2. For images, prefer using `image_url` field for display
3. For 3D models, provide a direct download link using `model_url` or `download_url`
4. Include helpful download instructions from the `download_instructions` field 