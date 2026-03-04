"""
Production-ready Claude API Chatbot (v3)
Features: Conversation history, token management, streaming, personas, retries
"""
import os
import time
from datetime import datetime
from dotenv import load_dotenv
import anthropic

load_dotenv()  # Load environment variables from .env

class ChatBot:
    """Claude chatbot with advanced features"""

    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment. Check .env file.")
        self.client = anthropic.Anthropic(api_key=api_key)
        self.conversation_history = []
        self.model = "claude-haiku-4-5-20251001"  
        self.system_prompt = "You are a helpful AI assistant."

    def count_tokens(self):
        """Estimate tokens used (rough: 1 token ≈ 4 chars)"""
        total_chars = sum(len(msg['content']) for msg in self.conversation_history)
        return total_chars // 4

    def trim_history(self, max_tokens=100000):
        """Trim history if exceeding context window"""
        while self.count_tokens() > max_tokens and len(self.conversation_history) > 2:
            self.conversation_history.pop(0)  # Remove oldest user message
            self.conversation_history.pop(0)  # Remove oldest assistant response
        print("✓ History trimmed to fit context window")

    def chat(self, user_message):
        """Send message (non-streaming)"""
        self.conversation_history.append({"role": "user", "content": user_message})
        self.trim_history()  # Ensure within limits

        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=self.system_prompt,
            messages=self.conversation_history
        )
        response = message.content[0].text
        self.conversation_history.append({"role": "assistant", "content": response})
        return response

    def chat_stream(self, user_message):
        """Stream response word-by-word"""
        self.conversation_history.append({"role": "user", "content": user_message})
        self.trim_history()

        print("Claude: ", end="", flush=True)
        full_response = ""
        with self.client.messages.stream(
            model=self.model,
            max_tokens=1024,
            system=self.system_prompt,
            messages=self.conversation_history
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
                full_response += text
        print()  # Newline
        self.conversation_history.append({"role": "assistant", "content": full_response})
        return full_response

    def chat_with_retry(self, user_message, max_retries=3, stream=False):
        """Chat with retries and optional streaming"""
        for attempt in range(max_retries):
            try:
                if stream:
                    return self.chat_stream(user_message)
                else:
                    return self.chat(user_message)
            except anthropic.APIError as e:
                print(f"API error: {e}. Retrying ({attempt + 1}/{max_retries})...")
                time.sleep(2 ** attempt)  # Exponential backoff
        print(f"Failed after {max_retries} attempts.")
        return None

    def set_persona(self, persona):
        """Set system prompt for different behaviors"""
        personas = {
            "helpful": "You are a helpful AI assistant.",
            "expert": "You are an expert AWS cloud engineer. Provide detailed technical answers.",
            "concise": "You are a concise assistant. Keep answers under 3 sentences.",
            "teacher": "You are a patient teacher. Explain concepts simply with examples."
        }
        self.system_prompt = personas.get(persona.lower(), personas["helpful"])
        print(f"✓ Persona set to: {persona}")

    def clear_history(self):
        """Reset conversation"""
        self.conversation_history = []
        print("✓ Conversation cleared")

    def save_conversation(self, filename=None):
        """Save conversation to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{timestamp}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            for msg in self.conversation_history:
                role = msg['role'].upper()
                content = msg['content']
                f.write(f"{role}: {content}\n\n")
        print(f"✓ Saved to {filename}")

def main():
    print("=" * 70)
    print("Claude Chatbot v3 - With Memory, Streaming, Personas, and More")
    print("=" * 70)
    print("Commands:")
    print("  /clear     - Clear conversation history")
    print("  /save      - Save conversation to file")
    print("  /persona [name] - Set persona (helpful, expert, concise, teacher)")
    print("  /stream    - Toggle streaming responses (default: on)")
    print("  /quit      - Exit")
    print("=" * 70)
    print()

    bot = ChatBot()
    use_stream = True  # Default to streaming

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue

        # Handle commands
        if user_input.lower() == '/quit':
            print("Goodbye!")
            break
        elif user_input.lower() == '/clear':
            bot.clear_history()
            continue
        elif user_input.lower() == '/save':
            bot.save_conversation()
            continue
        elif user_input.lower().startswith('/persona '):
            persona = user_input.split(maxsplit=1)[1].strip()
            bot.set_persona(persona)
            continue
        elif user_input.lower() == '/stream':
            use_stream = not use_stream
            print(f"✓ Streaming {'enabled' if use_stream else 'disabled'}")
            continue

        # Get response with retry
        response = bot.chat_with_retry(user_input, stream=use_stream)
        if response:
            print()  # Extra newline for readability if not streaming

if __name__ == "__main__":
    main()
