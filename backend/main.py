import json

import agent_tools
import gpt
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

# FastAPIのインスタンスを作成
app = FastAPI()

# --- CORS設定 ---
# フロントエンドからのアクセスを許可するための設定
origins = [
    "http://localhost:5173",  # Viteのデフォルトポート
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ----------------


# ルートURL ("/") へのGETリクエストに対する処理
@app.get("/")
def read_root():
    # OpenAI APIに送信するメッセージを作成
    messages = [{"role": "user", "content": "Say this is a test!"}]

    # gpt.pyの関数を呼び出してレスポンスを取得
    response_data = gpt.call_chat_completions(messages)

    # json.dumpsを使用して、指定された形式でJSON文字列に変換
    json_str = json.dumps(response_data, indent=2, ensure_ascii=False)

    # 整形されたJSON文字列をResponseオブジェクトとして返す
    return Response(content=json_str, media_type="application/json")


@app.get("/nearby-search")
def get_nearby_search(lat: float, lng: float):
    """
    指定された緯度経度で周辺検索を実行し、結果を返すエンドポイント
    """
    return agent_tools.all_nearby_search(lat, lng)
