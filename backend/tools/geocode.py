import requests

def reverse_geocode(location_text: str) -> dict:
    """
    Geocodes a location string using OpenStreetMap Nominatim API.
    
    Args:
        location_text: The address or location description to geocode.
        
    Returns:
        A dictionary containing the geocoded information (lat, lon, display_name) or an error.
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location_text,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "AgentBeforeAmbulance/1.0"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if data:
            result = data[0]
            return {
                "lat": result.get("lat"),
                "lon": result.get("lon"),
                "display_name": result.get("display_name"),
                "osm_id": result.get("osm_id")
            }
        else:
            return {"error": "Location not found"}
            
    except requests.RequestException as e:
        return {"error": f"Geocoding failed: {str(e)}"}
