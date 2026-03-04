"""
Chatbot with conversation memory
"""
import os
import time
from datetime import datetime
from dotenv import load_dotenv
import anthropic

load_dotenv()

class ChatBot:
    """Chatbot with memory"""

    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key: 
           raise ValueError("❌ ANTHROPIC_API_KEY not found in environment. Check .env file.")
        self.client = anthropic.Anthropic(api_key=api_key)
        self.history = []  # Store conversation
        self.model = "claude-haiku-4-5-20251001"
    
    def chat(self, user_message):
        """Send message and remember conversation"""
        # Add user message to history
        self.history.append({
            "role": "user",
            "content": user_message
        })
        
        # Send ALL history to Claude
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=self.history  # Full conversation!
        )
        
        # Get Claude's response
        assistant_message = response.content[0].text
        
        # Add Claude's response to history
        self.history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message
    
    def clear(self):
        """Reset conversation"""
        self.history = []
        print("✓ Conversation cleared")

def main():
    print("=== Claude Chat v2 (With Memory) ===")
    print("Commands: /clear, /quit\n")
    
    # Initialize chatbot
    bot = ChatBot()
    
    while True:
        user_input = input("You: ")
        
        # Handle commands
        if user_input == "/quit":
            break
        elif user_input == "/clear":
            bot.clear()
            continue
        
        # Get response
        response = bot.chat(user_input)
        print(f"Claude: {response}\n")

if __name__ == "__main__":
    main()
