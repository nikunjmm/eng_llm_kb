import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", ""))

def get_equipment_details(equipment_id: str) -> str:
    """Finds manufacturing equipment details from the knowledge base by ID."""
    return f"Details for {equipment_id}"

model = genai.GenerativeModel("gemini-2.5-flash", tools=[get_equipment_details])
chat = model.start_chat()
response = chat.send_message("What are PUMP-101 details?")

print("RESPONSE TYPE:", type(response))
print("DIR RESPONSE:", dir(response))

# print parts
try:
    for part in response.parts:
        print("PART FUNCTION CALL:", part.function_call)
        if part.function_call:
            print("FN NAME:", part.function_call.name)
            print("FN ARGS:", part.function_call.args)
except Exception as e:
    print("FAILED on parts:", e)
