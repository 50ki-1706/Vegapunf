from typing import List

from pydantic import BaseModel, Field


class PamphletRequest(BaseModel):
    """
    フロントエンドから送信されるリクエストのスキーマ
    """

    location: str = Field(
        ...,  # ... は必須項目であることを示す
        title="観光地の名称",
        description="ユーザーが入力した中心となる観光地の名前（例: 「浅草寺」）",
        example="東京スカイツリー",
    )
    genres: List[str] = Field(
        ...,
        title="観光のジャンルリスト",
        description='ユーザーが選択した観光ジャンルのタグ（例: ["歴史文化", "食べる"]）',
        example=["自然", "食べる"],
    )


"""
フロントからのリクエストをパンフレットの内容に変換するためのスキーマ群
"""


class PlacePhoto(BaseModel):
    """
    場所の写真に関する情報のスキーマ
    """

    photo_reference: str
    width: int
    height: int


class Place(BaseModel):
    """
    Google Maps APIから取得した単一の場所の情報を格納するスキーマ
    """

    place_id: str = Field(
        ..., description="場所を一意に識別するためのID。重複排除に利用。"
    )
    name: str = Field(..., description="場所の名称")
    vicinity: str = Field(None, description="場所の所在地（簡易的な住所）")
    rating: float = Field(None, description="場所の評価（5段階）")
    photo: PlacePhoto = Field(None, description="場所のメイン写真")
    types: List[str] = Field(
        [], description="場所のカテゴリ（例: 'shrine', 'restaurant'）"
    )


class PamphletSpot(BaseModel):
    """
    パンフレットに掲載する個々のスポット情報のスキーマ
    """

    place_id: str
    name: str
    vicinity: str
    rating: float | None = None  # Python 3.10以降の書き方。Noneを許容する
    photo_reference: str | None = None
    ai_description: str = Field(
        ..., description="AIによって生成された、その場所の魅力的な紹介文"
    )


class PamphletResponse(BaseModel):
    """
    最終的にフロントエンドに返すパンフレット全体のスキーマ
    """

    request_location: str = Field(..., description="ユーザーが最初に入力した場所の名前")
    title: str = Field(
        ..., description="AIによって生成されたパンフレット全体のタイトル"
    )
    introduction: str = Field(
        ..., description="AIによって生成されたパンフレット全体の導入文"
    )
    spots: List[PamphletSpot] = Field(
        [], description="パンフレットに掲載するスポットのリスト"
    )
