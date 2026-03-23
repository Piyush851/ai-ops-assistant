import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def generate_response(system_prompt: str, user_prompt: str, require_json: bool = False) -> str:
    """A helper function to generate responses from the LLM."""
    
    # We'll use llama-3.3-70b-versatile for high reasoning capabilities
    model = "llama-3.3-70b-versatile" 
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    # Groq supports JSON mode, which is crucial for our Planner Agent
    response_format = {"type": "json_object"} if require_json else {"type": "text"}
    
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.1, # Keep it low for deterministic planning
            response_format=response_format
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"LLM Error: {e}")
        return "{}" if require_json else "Error generating response."