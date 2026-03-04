"""
Basic chatbot - single message (no memory)
"""
import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

def send_message(user_input):
    """Send a single message to Claude"""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment. Check .env file.")
    
    client = anthropic.Anthropic(api_key=api_key)
    
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": user_input}
        ]
    )
    
    return response.content[0].text

def main():
    print("=== Basic Claude Chat (v1) ===")
    print("Type 'quit' to exit\n")
    
    while True:
        user_msg = input("You: ")
        
        if user_msg.lower() in ['quit', 'exit']:
            break
        
        claude_response = send_message(user_msg)
        print(f"Claude: {claude_response}\n")

if __name__ == "__main__":
    main()
