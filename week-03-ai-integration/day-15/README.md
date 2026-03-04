# Claude API Chatbot - Intelligent CLI Assistant

A progressive CLI chatbot built with Anthropic's Claude API, evolving from basic single-message responses to advanced features like conversation memory, streaming, personas, and error handling.

This project demonstrates API integration, state management, and prompt engineering — a portfolio piece showcasing AI automation skills for Upwork gigs or cloud engineering roles.

---

## Features

- 🗣️ **Natural Conversation:** Multi-turn chats with full history/memory
- 📡 **Streaming Responses:** Real-time word-by-word output for better UX
- 🎭 **Personas:** Switch behaviors (e.g., "expert" for technical advice, "concise" for short answers)
- 🔄 **Retries & Error Handling:** Automatic retries for API issues with exponential backoff
- 💾 **Save/Load:** Export conversations to timestamped TXT files
- 📊 **Token Management:** Auto-trims history to fit context limits
- 🔒 **Secure:** Uses .env for API keys (never hardcoded)
- 💰 **Cost-Effective:** Optimized for Claude Haiku (cheapest model) — ~$0.001 per conversation

---

## Versions

This repo includes three progressive versions to show evolution:

| Version | Features | File | Use Case |
|---------|----------|------|----------|
| **v1** | Single-message responses, no memory | `chatbot_v1.py` | Learning, simple questions |
| **v2** | Conversation history for context-aware chats | `chatbot_v2.py` | Multi-turn conversations |
| **v3** | Full production-ready with streaming, personas, retries, saving, token trimming | `chatbot_v3.py` | **Recommended for production** |

---

## Tech Stack

- **Python 3.12**
- **Anthropic SDK** (latest: 0.18.0+) — For Claude API calls
- **python-dotenv** — Secure environment variables
- **Models:** Defaults to "claude-haiku-4-5-20251001" (cheap/fast); configurable for Sonnet/Opus

---

## Installation

### Prerequisites

- Python 3.12+ installed
- Anthropic API key (sign up at [console.anthropic.com](https://console.anthropic.com), add $5 credits)

### Setup

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# OR activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

---

## Usage

### Run v3 (Recommended)

```bash
python chatbot_v3.py
```

### Commands (in v3)

| Command | Action |
|---------|--------|
| `/clear` | Reset conversation history |
| `/save` | Export chat to timestamped TXT file |
| `/persona [name]` | Switch persona (helpful, expert, concise, teacher) |
| `/stream` | Toggle real-time streaming (default: on) |
| `/quit` | Exit |

### Example Chat

```
You: What's 3+3?
Claude: 3+3 equals 6.

You: What about 4+4?  # Remembers context
Claude: Following the pattern, 4+4 equals 8.
```

---

## Project Structure

```
day-15/
├── chatbot_v1.py        # Basic version (no memory)
├── chatbot_v2.py        # With memory
├── chatbot_v3.py        # Advanced production-ready
├── .env.example         # Template for API key
├── requirements.txt     # Dependencies
├── .gitignore           # Excludes venv, .env, etc.
└── README.md            # This file
```

---

## Cost

Using Haiku:
- **Per query:** ~$0.00025 (input: $0.25/M tokens, output: $1.25/M)
- **Full conversation (10 turns):** <$0.001

**Optimize:** Use short prompts; trim history regularly.

---

## Limitations

- CLI-only (no GUI yet — extend to Streamlit if needed)
- Internet required for API calls
- Token limits: Auto-trims history at ~100K tokens

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| API Key Error | Check .env file and reload venv |
| Model Not Found | Use "claude-haiku-4-5-20251001" (update if new versions release) |
| Rate Limits | Built-in retries; wait 60s if persistent |

---

## License

MIT License — see LICENSE file.

---

## Author

Built by **Juno-50** ⭐

Star this repo if it helped! Contributions welcome.
