import json

import requests
import settings


def call_chat_completions(messages: list[dict]):
    """
    OpenAIのChat Completions APIを呼び出す関数

    Args:
        messages (list[dict]): OpenAI APIに送信するメッセージのリスト

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
