import time
# Importing the tools your teammate is building
from tools.github_tool import search_github_repos
from tools.weather_tool import get_weather

# A dictionary to map the tool names from the Planner's JSON to actual Python functions
TOOL_MAP = {
    "GitHubTool": search_github_repos,
    "WeatherTool": get_weather
}

def execute_plan(plan: dict, max_retries: int = 2) -> dict:
    """
    Iterates through the JSON plan, executes the mapped tools, 
    and collects the results with retry logic.
    """
    print("⚙️ Executor Agent is running the plan...")
    
    steps = plan.get("steps", [])
    collected_results = {}

    if not steps:
        print("⚠️ No valid steps found in the plan.")
        return collected_results

    for step_data in steps:
        step_num = step_data.get("step")
        tool_name = step_data.get("tool")
        args = step_data.get("args", {})
        
        print(f"  -> Executing Step {step_num}: {tool_name} with args {args}")
        
        # Check if the tool actually exists in our system
        if tool_name not in TOOL_MAP:
            collected_results[f"step_{step_num}_{tool_name}"] = {
                "status": "error", 
                "message": f"Tool '{tool_name}' is not recognized by the Executor."
            }
            continue

        target_function = TOOL_MAP[tool_name]
        attempt = 0
        success = False

        # Retry Logic loop
        while attempt <= max_retries and not success:
            try:
                # Unpack the arguments directly into the target function
                result = target_function(**args)
                
                if result.get("status") == "success":
                    collected_results[f"step_{step_num}_{tool_name}"] = result["data"]
                    success = True
                else:
                    raise Exception(result.get("message", "Unknown API Error"))
                    
            except Exception as e:
                attempt += 1
                print(f"  ❌ Attempt {attempt} failed for {tool_name}: {e}")
                if attempt <= max_retries:
                    print("  🔄 Retrying in 2 seconds...")
                    time.sleep(2)
                else:
                    print("  🚨 Max retries reached. Moving to next step.")
                    # Graceful degradation: log the error but don't crash the whole system
                    collected_results[f"step_{step_num}_{tool_name}"] = {
                        "status": "failed",
                        "error": str(e)
                    }

    return collected_results