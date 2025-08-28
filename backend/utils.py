import requests
import settings


def placeToPosition(place_name: str) -> dict:
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

    if data["status"] != "OK":
        return {"status": data["status"]}

    location = data["results"][0]["geometry"]["location"]
    return {"lat": location["lat"], "lng": location["lng"]}
