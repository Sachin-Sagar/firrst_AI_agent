# test_connection.py
import os
from dotenv import load_dotenv
from groq import Groq

print("Attempting minimal connection to Groq...")

try:
    load_dotenv(override=True)
    api_key = os.environ.get("GROQ_API_KEY")
    
    if not api_key:
        print("Error: GROQ_API_KEY not found in .env file.")
    else:
        print("API key found. Initializing client...")
        client = Groq(api_key=api_key)
        
        print(f"Sending 'Hello' to model: llama-3.3-70b-versatile...")
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "Hello"}]
        )
        
        print("\n--- GROQ SUCCESS ---")
        print("Connection successful. Received response:")
        print(response.choices[0].message.content)

except Exception as e:
    print("\n--- GROQ TEST FAILED ---")
    print(f"A connection error occurred: {e}")