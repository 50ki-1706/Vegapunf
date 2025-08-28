import json

import agent_tools
import gpt
import pamphlet_creator
import schemas
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware

# FastAPIのインスタンスを作成
app = FastAPI()

# --- CORS設定 ---
origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ----------------


@app.post("/make-pamphlet", response_model=schemas.PamphletResponse)
def make_pamphlet(request: schemas.PamphletRequest):
    """
    AIエージェントを起動し、パンフレットを生成するエンドポイント（Tool Calling対応版）
    """
    try:
        # ステップ1: 場所の名前を座標に変換（確定的処理）
        print(f"座標の取得中: '{request.location}'")
        coordinates = agent_tools.placeToPosition(request.location)
        if not coordinates:
            raise HTTPException(
                status_code=404,
                detail=f"'{request.location}' の座標が見つかりませんでした。",
            )
        print(f"座標を取得しました: {coordinates}")

        # ステップ2: AIエージェントを起動してパンフレットを生成
        pamphlet_data = pamphlet_creator.run_pamphlet_agent(
            location_name=request.location,
            genres=request.genres,
            coordinates=coordinates,
        )

        # Pydanticモデルに変換して返す（FastAPIが自動でJSONにしてくれる）
        return schemas.PamphletResponse(**pamphlet_data)

    except ValueError as e:
        # creatorで発生したエラーをHTTPエラーとしてクライアントに返す
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # その他の予期せぬエラー
        print(f"予期せぬエラーが発生しました: {e}")
        raise HTTPException(
            status_code=500, detail="サーバー内部でエラーが発生しました。"
        )


# --- 既存のエンドポイント ---


@app.get("/")
def read_root():
    messages = [{"role": "user", "content": "Say this is a test!"}]
    response_data = gpt.call_chat_completions(messages)
    json_str = json.dumps(response_data, indent=2, ensure_ascii=False)
    return Response(content=json_str, media_type="application/json")
