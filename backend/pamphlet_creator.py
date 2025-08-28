import json

import agent_tools
import gpt
from function_descriptions import function_descriptions


def run_pamphlet_agent(
    location_name: str, genres: list[str], coordinates: dict
) -> dict:
    """
    Tool Callingを利用して、対話形式でパンフレットを生成するAIエージェントを実行する。

    Args:
        location_name: ユーザーが指定した観光地の名前
        genres: ユーザーが選択したジャンルのリスト
        coordinates: 中心となる場所の緯度経度

    Returns:
        AIによって生成され、提出されたパンフレットのデータ(辞書形式)
    """

    print("Tool Callingエージェントを開始します...")

    # AIが利用可能な関数と、実際のPython関数をマッピング

    available_tools = {
        "call_nearby_search": agent_tools.call_nearby_search,
        "call_tavily_search": agent_tools.call_tavily_search,
    }

    # AIへの最初の指示

    initial_prompt = """「{}」周辺の観光パンフレットを作成してください。
    興味のあるジャンルは {} です。

    手順:
    1. まず、興味のあるジャンルに基づいて、どのようなキーワードで周辺情報を検索すべきか計画を立ててください。
    2. `call_nearby_search` ツールを複数回使用して、計画に沿った情報収集を行ってください。
    3. 収集した情報が十分だと判断したら、それらの情報を基に魅力的なパンフレットコンテンツ（タイトル、導入文、スポットごとの紹介文）を作成してください。
    4. 最後に、完成したパンフレットの全データを `submit_pamphlet` 関数を呼び出して提出してください。""".format(
        location_name, ", ".join(genres)
    )

    messages = [
        {"role": "user", "content": initial_prompt},
    ]

    # 最大5回の対話ループで、無限ループを防ぐ
    for _ in range(5):
        print(f"\n--- Agent Turn {_ + 1} ---")
        # 1. AIに関数定義を渡して、次の行動を決めさせる
        response = gpt.call_chat_completions(
            messages, tools=function_descriptions, tool_choice="auto"
        )
        response_message = response["choices"][0]["message"]
        messages.append(response_message)  # AIの応答を履歴に追加

        # 2. AIがツールの使用を要求したかチェック
        if not response_message.get("tool_calls"):
            print("AIがツールの使用を要求しませんでした。処理を終了します。")
            break

        tool_calls = response_message["tool_calls"]

        # 3. 要求されたツールを順番に実行
        for tool_call in tool_calls:
            function_name = tool_call["function"]["name"]
            function_args = json.loads(tool_call["function"]["arguments"])

            print(
                f"AIがツール '{function_name}' の使用を要求しました。引数: {function_args}"
            )

            # AIが最終成果物を提出してきた場合
            if function_name == "submit_pamphlet":
                print(
                    "AIが最終的なパンフレットを提出しました。エージェントの処理を完了します。"
                )
                return function_args  # これが最終的な成果物

            # 実際にツール（Python関数）を実行
            function_to_call = available_tools.get(function_name)
            if not function_to_call:
                raise ValueError(f"不明な関数です: {function_name}")

            try:
                function_response = function_to_call(**function_args)
            except Exception as e:
                print(f"ツール '{function_name}' の実行中にエラー: {e}")
                function_response = {"error": str(e)}

            # 4. ツールの実行結果を履歴に追加して、次のループへ
            messages.append(
                {
                    "tool_call_id": tool_call["id"],
                    "role": "tool",
                    "name": function_name,
                    "content": json.dumps(function_response, ensure_ascii=False),
                }
            )

    raise RuntimeError("AIエージェントが規定のターン数内に処理を完了できませんでした。")
