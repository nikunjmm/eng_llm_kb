import os
from tempfile import NamedTemporaryFile
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

def main():
    client = genai.Client()
    
    # Test dictionary-based history
    history = [
        types.Content(role="user", parts=[types.Part.from_text(text="Hi there")]),
        types.Content(role="model", parts=[types.Part.from_text(text="Hello! How can I help?")])
    ]
    
    chat = client.chats.create(
        model="gemini-2.5-flash",
        history=history
    )
    
    print("Sending message...")
    response = chat.send_message("What did I just say?")
    print("Response:", response.text)

if __name__ == "__main__":
    main()
