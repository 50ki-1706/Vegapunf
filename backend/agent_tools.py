import requests
import settings


def call_tavily_search(query, depth="basic", max_results=3, include_answer=False):
    api_key = settings.TAVILY_API_KEY
    if not api_key:
        raise RuntimeError("TAVILY_API_KEY 未設定")

    url = "https://api.tavily.com/search"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "query": query,
        "search_depth": depth,  # "basic" or "advanced"
        "max_results": int(max_results),
        "include_answer": bool(include_answer),
        "include_images": False,
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()


def call_nearby_search(
    lat: float, lng: float, radius: int = 1500, tag: list[str] = ["自然"]
):
    """
    Google Maps Places API の Nearby Search を呼び出してJSONを返す
    """
    api_key = settings.GOOGLE_MAPS_API_KEY
    if not api_key:
        return {"error": "API key not found."}

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": 1500,  # 取得する範囲の半径（メートル単位）
        "type": "restaurant",
        "key": api_key,
    }

    response = requests.get(url, params=params)
    return response.json()
