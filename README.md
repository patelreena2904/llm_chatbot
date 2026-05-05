# AI Engineering Tutor Chatbot

## What it does
A CLI chatbot powered by Claude that acts as a 
specialized AI engineering tutor. Features multi-turn
memory, streaming responses, and full error handling.

## Features
- Multi-turn conversation with memory
- Streaming responses token by token
- Specialized system prompt for AI tutoring
- Error handling for rate limits and connection errors
- Commands: clear history, view history, quit

## How to run
```bash
pip install -r requirements.txt
```

Add your API key to a `.env` file:
ANTHROPIC_API_KEY=your-key-here

Then run:
```bash
python chatbot.py
```

## Tech used
Python, Anthropic Claude API, python-dotenv

## What I learned
- How to call LLM APIs with streaming
- How to manage multi-turn conversation history
- How system prompts control model behavior
- How to handle API errors gracefully

## What I just build
- ✅ Real API call to Claude
- ✅ System prompt — specialized behavior
- ✅ Multi-turn memory — conversation history
- ✅ Streaming — token by token output
- ✅ Error handling — rate limit, connection, auth
- ✅ Special commands — clear, history, quit
- ✅ Pushed to GitHub
