import requests

def search_github_repos(query: str, limit: int = 3) -> dict:
    """Searches GitHub for repositories based on a query."""
    url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page={limit}"
    
    try:
        # Added timeout to prevent hanging requests
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        repos = []
        for item in data.get("items", []):
            repos.append({
                "name": item.get("full_name"),
                "stars": item.get("stargazers_count"),
                "description": item.get("description")
            })
        return {"status": "success", "data": repos}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}