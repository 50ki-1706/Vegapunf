from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # CORSを扱うために必要

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
    return {"message": "これはFastAPIからのメッセージです！"}
