from agents.planner import generate_plan
from agents.executor import execute_plan
from agents.verifier import verify_and_format

def run_agentic_pipeline(user_task: str) -> dict:
    """
    The core orchestration engine. Runs the Plan -> Execute -> Verify loop.
    """
    print(f"\n🚀 Starting AI Operations Assistant for task: '{user_task}'\n")
    
    # 1. Plan
    plan = generate_plan(user_task)
    if not plan.get("steps"):
        return {"error": "Planner failed to generate a valid sequence of steps.", "verified": False}
    
    print(f"📋 Generated Plan: {plan}\n")
    
    # 2. Execute
    raw_results = execute_plan(plan)
    if not raw_results:
        return {"error": "Executor failed to retrieve any data.", "verified": False}
        
    print(f"\n📦 Raw Data Collected: {raw_results}\n")
    
    # 3. Verify
    final_result = verify_and_format(user_task, raw_results)
    
    print("✅ Pipeline Complete.")
    return final_result

# --- Quick Test Block (Run this file directly to test your backend) ---
if __name__ == "__main__":
    test_prompt = "Find the top 3 trending Python repositories on GitHub and tell me the current weather in London."
    result = run_agentic_pipeline(test_prompt)
    
    import json
    print("\n🌟 FINAL OUTPUT:")
    print(json.dumps(result, indent=2))