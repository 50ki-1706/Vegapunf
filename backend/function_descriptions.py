function_descriptions = [
    {
        "type": "function",
        "function": {
            "name": "call_tavily_search",
            "description": (
                "Tavily のWeb検索APIで外部情報を取得する。"
                "最新情報・公式情報・比較記事などが必要なときに使用。"
                "検索クエリは日本語でよい。結果(JSON)には要約(answer)・検索結果(results)が含まれる場合がある。"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "検索したい自然文クエリ（例: '国内の生成AIの最新動向 2025 上半期'）",
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "call_nearby_search",
            "description": "指定された緯度経度とキーワードで周辺の場所を検索する。",
            "parameters": {
                "type": "object",
                "properties": {
                    "lat": {"type": "number", "description": "緯度"},
                    "lng": {"type": "number", "description": "経度"},
                    "keyword": {
                        "type": "string",
                        "description": "検索キーワード（例: 'カフェ', '神社'）",
                    },
                    "radius": {
                        "type": "integer",
                        "description": "検索半径（メートル）",
                        "default": 2000,
                    },
                },
                "required": ["lat", "lng", "keyword"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "submit_pamphlet",
            "description": "最終的なパンフレットのコンテンツを提出する。全ての情報収集とコンテンツ生成が終わったら、最後にこの関数を呼び出す。",
            "parameters": {
                "type": "object",
                "properties": {
                    "request_location": {
                        "type": "string",
                        "description": "ユーザーが最初に入力した場所の名前",
                    },
                    "title": {
                        "type": "string",
                        "description": "AIによって生成されたパンフレット全体のタイトル",
                    },
                    "introduction": {
                        "type": "string",
                        "description": "AIによって生成されたパンフレット全体の導入文",
                    },
                    "spots": {
                        "type": "array",
                        "description": "パンフレットに掲載するスポットのリスト",
                        "items": {
                            "type": "object",
                            "properties": {
                                "place_id": {"type": "string"},
                                "name": {"type": "string"},
                                "vicinity": {"type": "string"},
                                "rating": {"type": "number"},
                                "photo_reference": {"type": "string"},
                                "ai_description": {
                                    "type": "string",
                                    "description": "AIによって生成された、その場所の魅力的な紹介文",
                                },
                            },
                            "required": [
                                "place_id",
                                "name",
                                "vicinity",
                                "ai_description",
                            ],
                        },
                    },
                },
                "required": ["request_location", "title", "introduction", "spots"],
            },
        },
    },
]