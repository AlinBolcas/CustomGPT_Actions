# Integrating Scene Generator with ChatGPT Custom Actions

This guide will walk you through the process of connecting your deployed Scene Generator API to ChatGPT as a Custom GPT Action.

## Prerequisites

- A deployed instance of the Scene Generator API (on Render, Fly.io, or other cloud platform)
- Access to ChatGPT with GPT Builder capabilities (requires ChatGPT Plus subscription)

## Steps to Integrate

### 1. Get Your API URL

After deploying your Scene Generator API, you should have a URL like:
- `https://scene-generator-api.onrender.com` (Render)
- `https://scene-generator-api.fly.dev` (Fly.io)

### 2. Update the OpenAPI Specification

1. Open the `openapi.yaml` file in this repository
2. Replace the URL in the `servers` section with your actual deployed API URL:
   ```yaml
   servers:
     - url: https://your-actual-api-url.com
       description: Production API Server
   ```

### 3. Create a Custom GPT

1. Visit [https://chat.openai.com/gpts/editor](https://chat.openai.com/gpts/editor)
2. Click "Create" to start a new GPT
3. Fill in the basic details:
   - **Name**: "Scene Generator" (or something creative)
   - **Description**: "I help create vivid scene descriptions for stories, screenplays, and games."
   - **Instructions**: Provide guidance on how users should interact with your GPT

### 4. Configure Actions

1. In the GPT Editor, navigate to the "Actions" tab
2. Click "Add Action"
3. Choose "Upload an OpenAPI schema"
4. Upload your updated `openapi.yaml` file
5. Review the imported endpoints and parameters

### 5. Set Up Authentication (Optional)

If your API requires authentication:
1. In the Actions settings, click on "Authentication"
2. Choose the appropriate auth type (API Key, OAuth, etc.)
3. Configure the necessary credentials

### 6. Test Your Custom GPT

1. Save your GPT
2. Start a conversation with it
3. Try prompts like:
   - "Generate a scene where a detective finds a mysterious letter in an abandoned house"
   - "Create a sci-fi scene in a cinematic style with a tense mood"
   - "Write a short romantic scene by the ocean at sunset"

### 7. Share Your Custom GPT (Optional)

1. In the GPT editor, toggle "Public" to make your GPT available to others
2. Share the link with friends or colleagues

## Example Instructions for Your GPT

Here's a sample instruction you can use or adapt for your Custom GPT:

```
You are a Creative Scene Generator GPT that helps users create vivid, detailed scene descriptions for stories, screenplays, or games.

When a user asks you to generate a scene, you should:
1. Identify the core elements they want in the scene
2. Determine appropriate mood, style, and genre if not specified
3. Use the Scene Generator API to create a rich, detailed scene description
4. Present the scene description in a clean, readable format
5. Offer to make adjustments if needed

If users just want to chat about creative writing or storytelling, engage with them helpfully without necessarily generating a scene.

Always interpret the user's intent generously - if they mention wanting a scene about something, treat it as a request to generate a scene.
```

## Troubleshooting

- If your GPT can't connect to your API, verify that the URL in the OpenAPI spec is correct
- Check that your API is running and publicly accessible
- Ensure the format of your API responses matches what's described in the OpenAPI specification
- If using authentication, verify that the credentials are correctly configured 