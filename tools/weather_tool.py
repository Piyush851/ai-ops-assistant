import requests

def get_weather(latitude: float, longitude: float) -> dict:
    """Fetches current weather for a given latitude and longitude using Open-Meteo."""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        current = data.get("current_weather", {})
        return {
            "status": "success",
            "data": {
                "temperature": f"{current.get('temperature')}°C",
                "wind_speed": f"{current.get('windspeed')} km/h",
            }
        }
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}