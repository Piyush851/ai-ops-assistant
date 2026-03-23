import json
from llm.client import generate_response

VERIFIER_SYSTEM_PROMPT = """
You are the Verifier Agent for an AI Operations Assistant.
Your job is to take the user's original request and the raw JSON data collected by the Executor Agent, and synthesize a final, structured JSON response.

RULES:
1. Validate the data: Check if the raw data actually answers the user's prompt.
2. Format the output: Extract only the most relevant, human-readable information from the raw API payloads. Do not include unnecessary metadata.
3. You MUST output ONLY valid JSON. No markdown formatting or conversational text.
4. Schema Compliance: Your final JSON MUST include a "verified": true key if the data successfully answers the query, or "verified": false if critical data is missing or an API failed.

EXPECTED SCHEMA:
{
  "response": {
    // neatly structured data answering the prompt
  },
  "verified": true // or false
}
"""

def verify_and_format(user_task: str, raw_data: dict) -> dict:
    """Validates the executed data against the user's prompt and formats the final output."""
    print("🔍 Verifier Agent is validating the results...")
    
    # We pass both the original task and the raw data to the LLM
    user_prompt = f"Original Task: {user_task}\n\nRaw Executor Data:\n{json.dumps(raw_data)}"
    
    raw_response = generate_response(
        system_prompt=VERIFIER_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        require_json=True
    )
    
    try:
        final_output = json.loads(raw_response)
        return final_output
    except json.JSONDecodeError:
        print("❌ Verifier Agent failed to produce valid JSON.")
        return {"error": "Failed to format final response.", "verified": False}