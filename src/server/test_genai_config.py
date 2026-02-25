import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

def main():
    print(dir(types.GenerateContentConfig))
    print(help(types.GenerateContentConfig))

if __name__ == "__main__":
    main()
