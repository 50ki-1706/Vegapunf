import json

import requests
import settings


def call_chat_completions(
    messages: list[dict],
    tools: list = None,
    tool_choice: str = "auto",
    response_format: str = "text",
):
    """
    OpenAIのChat Completions APIを呼び出す関数

    Args:
        messages (list[dict]): APIに送信するメッセージのリスト
        tools (list, optional): AIが利用可能なツール（関数）のリスト. Defaults to None.
        tool_choice (str, optional): ツールの使用を制御. "auto", "none", or {"type": "function", ...}. Defaults to "auto".
        response_format (str, optional): レスポンス形式 ("text" or "json_object"). Defaults to "text".

    Returns:
        dict: APIからのレスポンス(JSON)
    """
    # 環境変数からAPIキーを取得
    api_key = settings.OPENAI_API_KEY
    if not api_key:
        # APIキーがない場合はエラーを発生させる
        raise ValueError("OPENAI_API_KEYが設定されていません。")

    # APIエンドポイント
    url = "https://api.openai.com/v1/chat/completions"

    # ヘッダー情報
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    # リクエストデータ
    request_data = {
        "model": "gpt-4o-mini",
        "messages": messages,
    }

    # Tool Callingのパラメータを追加
    if tools:
        request_data["tools"] = tools
        request_data["tool_choice"] = tool_choice

    # レスポンス形式を指定
    if response_format == "json_object":
        request_data["response_format"] = {"type": "json_object"}

    # リクエストの送信 (json引数を使うと自動でJSONに変換される)
    response = requests.post(url, headers=headers, json=request_data)

    # HTTPステータスコードが200番台でない場合にエラーを発生させる
    response.raise_for_status()

    # レスポンスのJSONデータを返す
    return response.json()


# このファイルが直接実行された場合にテストコードを実行
if __name__ == "__main__":
    test_messages = [{"role": "user", "content": "Say this is a test!"}]
    try:
        response_data = call_chat_completions(test_messages)
        print(json.dumps(response_data, indent=2, ensure_ascii=False))
    except (ValueError, requests.exceptions.RequestException) as e:
        print(f"エラーが発生しました: {e}")