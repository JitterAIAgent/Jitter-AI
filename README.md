# Light-AI

Light-AI is a modular framework for building conversational AI agents with RAG (Retrieval-Augmented Generation) and multi-provider support (Google Gemini, OpenRouter, etc.).

## Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the following example to a new file named `.env` in your project root, then add your own values 

### 3. Create/Edit `being.json`

This file defines your agent's character, system instructions, and knowledge base. Example:

```json
{
  "modelProvider": "google",
  "contextId": "kim-kardashian",
  "system": "you must always respond in the character of Kim Kardashian...",
  "character": {
    "name": "Kim Kardashian",
    "bio": "Kim Kardashian is a media personality...",
    "personality": "Kim is known for her glamorous lifestyle..."
  },
  "tools": [],
  "knowledge": [
    "john is 27 years old",
    "john is a software engineer"
  ],
  "exampleResponses": [
    "Hi, I'm Kim! How can I help you today?",
    "Of course, darling! Let me tell you more."
  ]
}
```

- Change `modelProvider` to `google` or `openRouter` as needed.
- Add facts to `knowledge` for RAG.
- Add style examples to `exampleResponses`.

### 4. Start the Backend Server

```bash
python server.py
```

- The server will start at `http://localhost:8000`.
- You can interact with the API via `/message` and `/being` endpoints.

### 5. Frontend (Client)

If you have a `client` folder (e.g., React, Vue, etc.), open a new terminal and run:

```bash
cd client
npm install
npm start
```

- The frontend will connect to the backend API at `http://localhost:8000`.

## How to Create Your Own Agent

To create your own agent, you need to define a `being.json` file in the project root. This file controls the character, personality, system instructions, and knowledge base for your agent. You can use any persona, style, or knowledge you want.

### Example: Creating a Custom `being.json`

Below is a template you can use and modify. You do NOT need to copy the Kim Kardashian example—just fill in your own details:

```json
{
  "modelProvider": "openRouter", // or "google"
  "model": "moonshotai/kimi-k2:free", // required for openRouter, ignored for google
  "contextId": "my-unique-agent-id",
  "system": "You are a friendly assistant who loves science fiction and always answers with optimism.",
  "character": {
    "name": "Alex Star",
    "bio": "Alex is a space explorer and AI expert, known for their curiosity and helpfulness.",
    "personality": "Alex is upbeat, curious, and always tries to make learning fun."
  },
  "tools": ["calculator", "weather"],
  "knowledge": [
    "Mars is the fourth planet from the Sun.",
    "The speed of light is approximately 299,792 kilometers per second.",
    "Alex's favorite book is 'Dune' by Frank Herbert."
  ],
  "exampleResponses": [
    "Hi! I'm Alex. Ready to explore the universe with you!",
    "Absolutely! The speed of light is about 299,792 km/s.",
    "Mars is a fascinating planet—did you know it has the largest volcano in the solar system?"
  ]
}
```

**Key Fields:**
- `modelProvider`: Choose `google` for Gemini or `openRouter` for OpenRouter. This controls which backend is used.
- `model`: (OpenRouter only) Specify the model string, e.g. `moonshotai/kimi-k2:free` or any supported model from OpenRouter.
- `contextId`: Any unique string to identify your agent's context/memory.
- `system`: Instructions for the agent's behavior, style, or rules.
- `character`: Define the agent's name, bio, and personality.
- `tools`: List any tools your agent can use (optional).
- `knowledge`: Add facts, background info, or context for RAG (retrieval-augmented generation).
- `exampleResponses`: Add sample responses to guide the agent's style and tone (optional).

**Tips:**
- Be creative! You can make your agent a celebrity, a fictional character, a helpful assistant, or anything you want.
- The more detailed your `bio`, `personality`, and `knowledge`, the more realistic and useful your agent will be.
- For OpenRouter, make sure to set the `model` field to a valid model string.
- For Gemini, the `model` field is ignored; use `GOOGLE_MODEL_ID` in your `.env` file instead.

Once your `being.json` is ready, set your API keys in `.env`, and start the server and frontend as described above.

## Troubleshooting
- Ensure your API keys are set and valid.
- Check the logs for errors if the server does not start.
- Make sure your `being.json` is correctly formatted and includes all required fields.

## License
MIT