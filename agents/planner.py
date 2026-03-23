import json
from llm.client import generate_response

PLANNER_SYSTEM_PROMPT = """
You are the Planner Agent for an AI Operations Assistant. Your job is to decompose a user's natural language request into a strict, step-by-step execution plan.

You have access to exactly TWO tools:
1. "GitHubTool": Searches for GitHub repositories.
   - Required arguments: "query" (str), "limit" (int, default 3)
2. "WeatherTool": Gets the current weather for a location.
   - Required arguments: "latitude" (float), "longitude" (float)
   Note: If the user provides a city name, you must estimate the rough latitude and longitude for that city to pass to the WeatherTool.

RULES:
- You MUST output ONLY valid JSON.
- No conversational filler, no markdown formatting outside of the JSON object.
- The JSON must follow this exact schema:
{
  "steps": [
    {
      "step": 1,
      "tool": "ToolName",
      "args": {"arg_name": "arg_value"}
    }
  ]
}
"""

def generate_plan(user_task: str) -> dict:
    """Takes the user task and returns a parsed JSON dictionary representing the plan."""
    print("🧠 Planner Agent is analyzing the task...")
    
    raw_response = generate_response(
        system_prompt=PLANNER_SYSTEM_PROMPT,
        user_prompt=f"Task: {user_task}",
        require_json=True
    )
    
    try:
        plan_dict = json.loads(raw_response)
        return plan_dict
    except json.JSONDecodeError:
        print("❌ Planner Agent failed to produce valid JSON.")
        return {"steps": []}