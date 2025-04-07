from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import random
import json
import os
from datetime import datetime

# Import our new router
from api.replicate_router import router as replicate_router

app = FastAPI(
    title="Creative Scene Generator API",
    description="Generate creative scene descriptions and media for stories, screenplays, or games",
    version="1.0.0"
)

# Include the replicate router
app.include_router(replicate_router)

class SceneRequest(BaseModel):
    prompt: str
    mood: Optional[str] = "neutral"
    style: Optional[str] = "descriptive"
    genre: Optional[str] = "fantasy"
    length: Optional[str] = "medium"

class SceneResponse(BaseModel):
    scene_description: str
    created_at: str
    id: str
    metadata: Dict

# In-memory storage of generated scenes
scenes_db = []

@app.get("/")
def read_root():
    return {"status": "running", "service": "Scene Generator and Media Generation API"}

@app.post("/generate-scene", response_model=SceneResponse)
def generate_scene(req: SceneRequest):
    # Log the request (in a real app, you'd use proper logging)
    print(f"Received request: {req}")
    
    # Generate a unique ID
    scene_id = f"scene_{len(scenes_db) + 1}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Map length to approximate word count
    length_map = {
        "short": (50, 100),
        "medium": (150, 250),
        "long": (300, 500)
    }
    target_length = length_map.get(req.length.lower(), (150, 250))
    
    # Advanced scene generation logic
    # In a real application, this might call an LLM API or use more sophisticated algorithms
    scene = generate_creative_scene(
        req.prompt, 
        req.mood, 
        req.style, 
        req.genre,
        target_length
    )
    
    # Create response
    response = SceneResponse(
        scene_description=scene,
        created_at=datetime.now().isoformat(),
        id=scene_id,
        metadata={
            "mood": req.mood,
            "style": req.style,
            "genre": req.genre,
            "length": req.length,
            "word_count": len(scene.split())
        }
    )
    
    # Store in our "database"
    scenes_db.append(response)
    
    return response

@app.get("/scenes/{scene_id}")
def get_scene(scene_id: str):
    for scene in scenes_db:
        if scene.id == scene_id:
            return scene
    raise HTTPException(status_code=404, detail="Scene not found")

# Creative scene generation function
def generate_creative_scene(prompt, mood, style, genre, target_length):
    # This is a simplified version that would be replaced with LLM integration
    # but demonstrates the concept for our prototype
    
    # Scene templates based on genre
    genre_intros = {
        "fantasy": [
            "A magical glow emanated from the ancient stones as",
            "Mist swirled around the twisted trees while",
            "The dragon's scales glittered in the moonlight as",
        ],
        "sci-fi": [
            "The spacecraft's engines hummed softly as",
            "Holographic displays flickered with strange symbols while",
            "The alien landscape stretched endlessly beneath",
        ],
        "horror": [
            "A chill ran down their spine when",
            "Shadows seemed to move of their own accord as",
            "The decrepit mansion creaked and moaned while",
        ],
        "romance": [
            "Their eyes met across the crowded room as",
            "The sunset painted the sky in brilliant hues while",
            "Rose petals scattered across the path where",
        ],
        "mystery": [
            "The detective narrowed his eyes, noticing",
            "Fog obscured the crime scene, but revealed",
            "A single clue remained, pointing to",
        ]
    }
    
    # Mood modifiers
    mood_phrases = {
        "joyful": ["delightful", "exuberant", "gleeful", "vibrant", "cheerful"],
        "melancholy": ["somber", "wistful", "forlorn", "gloomy", "mournful"],
        "tense": ["apprehensive", "uneasy", "anxious", "fraught", "electric"],
        "peaceful": ["serene", "tranquil", "calm", "gentle", "harmonious"],
        "mysterious": ["enigmatic", "cryptic", "puzzling", "arcane", "veiled"],
        "romantic": ["passionate", "tender", "intimate", "affectionate", "amorous"],
        "neutral": ["balanced", "measured", "moderate", "tempered", "composed"]
    }
    
    # Style adjustments
    style_patterns = {
        "descriptive": lambda s: s,  # No change for descriptive
        "poetic": lambda s: s.replace(".", ".\n") + "\n",  # Add line breaks for poetic
        "cinematic": lambda s: s + " The camera pans to reveal more of the scene.",
        "minimalist": lambda s: " ".join([w for w in s.split() if len(w) > 3 or random.random() > 0.3]),
        "stream-of-consciousness": lambda s: s.replace(".", "...") + "..."
    }
    
    # Select a random genre intro or use default
    selected_genre = genre.lower() if genre.lower() in genre_intros else "fantasy"
    intro = random.choice(genre_intros[selected_genre])
    
    # Select mood modifiers
    selected_mood = mood.lower() if mood.lower() in mood_phrases else "neutral"
    mood_words = mood_phrases[selected_mood]
    
    # Build the scene based on the prompt
    scene_parts = [
        intro,
        prompt,
        f"The atmosphere was {random.choice(mood_words)}.",
        f"Everything seemed to {random.choice(['whisper', 'shout', 'suggest', 'reveal', 'hint at'])} a sense of {random.choice(mood_words)} {random.choice(['potential', 'danger', 'mystery', 'wonder', 'beauty'])}."
    ]
    
    # Add detail based on target length
    words_needed = target_length[0] - sum(len(part.split()) for part in scene_parts)
    
    if words_needed > 0:
        # Add descriptive details
        details = [
            f"The {random.choice(['light', 'colors', 'sounds', 'air', 'feeling'])} {random.choice(['evoked', 'suggested', 'created', 'inspired'])} a {random.choice(mood_words)} sentiment.",
            f"One could {random.choice(['sense', 'feel', 'see', 'hear', 'taste'])} the {random.choice(mood_words)} {random.choice(['emotion', 'energy', 'essence', 'spirit', 'ambiance'])} in the {random.choice(['air', 'surroundings', 'atmosphere', 'environment', 'space'])}.",
            f"This place seemed {random.choice(mood_words)} in a way that {random.choice(['touched', 'moved', 'affected', 'stirred', 'resonated with'])} something deep within.",
        ]
        
        # Add details until we reach minimum target length
        while sum(len(part.split()) for part in scene_parts) < target_length[0] and details:
            scene_parts.append(details.pop(0))
    
    # Combine all parts
    raw_scene = " ".join(scene_parts)
    
    # Apply style
    selected_style = style.lower() if style.lower() in style_patterns else "descriptive"
    final_scene = style_patterns[selected_style](raw_scene)
    
    return final_scene

if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment variable for Render deployment
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True) 