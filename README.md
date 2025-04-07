# Scene Generator API for ChatGPT Custom Actions

This project provides a creative scene generation API that can be integrated with ChatGPT Custom Actions.

## Features

- Generate vivid scene descriptions for stories, screenplays, or games
- Customize mood, style, genre, and length
- RESTful API built with FastAPI
- Available 24/7 through cloud deployment

## Local Development

### Prerequisites

- Python 3.10+
- Docker (optional)

### Setup

1. Create a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the API locally:
   ```bash
   uvicorn api.main:app --reload
   ```

4. Access the API at http://localhost:8000
   - API docs available at http://localhost:8000/docs

## Cloud Deployment (Recommended)

### Deploy to Render

1. Fork/clone this repository to your GitHub account
2. Go to [Render.com](https://render.com) and create an account
3. Click "New +" and select "Blueprint"
4. Connect your GitHub repository
5. Render will automatically use the `render.yaml` configuration
6. Once deployed, copy the URL provided by Render (e.g., `https://scene-generator-api.onrender.com`)

### Deploy to Fly.io (Alternative)

1. Install the Fly CLI:
   ```
   brew install flyctl
   ```

2. Log in to Fly:
   ```
   fly auth login
   ```

3. Launch the app:
   ```
   fly launch
   ```

4. Deploy:
   ```
   fly deploy
   ```

5. Get your URL:
   ```
   fly open
   ```

## Integrating with ChatGPT Custom Actions

1. After deployment, update the URL in `openapi.yaml` to your cloud service URL
2. Go to https://chat.openai.com/gpts/editor
3. In the "Actions" section, upload your `openapi.yaml` file
4. Configure the GPT's instructions to use your Scene Generator
5. Save your GPT

## Usage Examples

Once integrated with ChatGPT, users can try prompts like:

- "Generate a scene where a detective finds a mysterious letter in an abandoned house"
- "Create a sci-fi scene in a cinematic style with a tense mood"
- "Write a short romantic scene by the ocean at sunset"

## API Reference

### POST /generate-scene

Generates a creative scene description.

**Request body:**

```json
{
  "prompt": "A character discovers an ancient artifact",
  "mood": "mysterious",
  "style": "cinematic",
  "genre": "fantasy",
  "length": "medium"
}
```

**Response:**

```json
{
  "scene_description": "Mist swirled around the twisted trees while a character discovers an ancient artifact. The atmosphere was enigmatic. Everything seemed to whisper a sense of cryptic wonder...",
  "created_at": "2023-04-06T12:34:56.789012",
  "id": "scene_1_20230406123456",
  "metadata": {
    "mood": "mysterious",
    "style": "cinematic",
    "genre": "fantasy",
    "length": "medium",
    "word_count": 178
  }
}
``` 