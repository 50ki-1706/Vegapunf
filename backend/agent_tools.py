import requests
import settings


def placeToPosition(place_name: str):
    """
    場所の名前（住所やランドマーク名）から緯度経度を取得する
    """
    api_key = settings.GOOGLE_MAPS_API_KEY
    if not api_key:
        raise RuntimeError("GOOGLE_MAPS_API_KEY 未設定")

    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": place_name,
        "key": api_key,
        "language": "ja",  # 結果を日本語で取得
    }

    response = requests.get(url, params=params)
    response.raise_for_status()  # エラーがあれば例外を発生させる
    data = response.json()

    if data["status"] == "OK":
        location = data["results"][0]["geometry"]["location"]
        return {"lat": location["lat"], "lng": location["lng"]}
    else:
        # 場所が見つからなかった場合など
        return None


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


def call_nearby_search(lat: float, lng: float, keyword: str, radius: int = 1500):
    """
    Google Maps Places API の Nearby Search を呼び出してJSONを返す
    """
    api_key = settings.GOOGLE_MAPS_API_KEY
    if not api_key:
        return {"error": "API key not found."}

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "keyword": keyword,  # 検索キーワード
        "language": "ja",
        "key": api_key,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()  # エラーがあれば例外を発生させる
    return response.json()