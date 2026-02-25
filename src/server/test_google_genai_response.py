import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

def get_equipment_details(equipment_id: str) -> str:
    """Finds manufacturing equipment details from the knowledge base by ID."""
    return f"Details for {equipment_id}"

def main():
    client = genai.Client()
    
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            tools=[get_equipment_details],
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
        )
    )
    
    response = chat.send_message("What are PUMP-101 details?")
    if response.function_calls:
        fc = response.function_calls[0]
        print("Sending function response for", fc.name)
        
        # New syntax usually involves a types.Part.from_function_response
        try:
            tool_response = types.Part.from_function_response(
                name=fc.name,
                response={"result": "Operating pressure is 150 PSI"}
            )
            
            final_response = chat.send_message(tool_response)
            print("Final Text:", final_response.text)
        except Exception as e:
            print("ERROR", e)

if __name__ == "__main__":
    main()
