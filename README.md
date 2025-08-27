# 最初の環境構築

## ターミナルでリポジトリをクローン

```bash
git clone このリポジトリのurl
```

## backend フォルダに移動して以下のコマンドを実行

```bash
cd backend/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## frontend フォルダに移動して以下のコマンドを実行

```bash
cd frontend/
npm install
```

# ローカルでの開発手順

## バックエンド

### backend フォルダに移動

```bash
cd backend/
```

### 仮想環境を起動

```bash
source venv/bin/activate
```

### FastAPI サーバーを起動

```bash
uvicorn main:app --reload
```

次にターミナルをもう一つ開く

## フロントエンド

### frontend フォルダに移動

```bash
cd frontend/
```

### ローカルサーバーを起動

```bash
npm run dev
```
