import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const InputPage = () => {
  const navigate = useNavigate();

  // フォームのステート
  const [location, setLocation] = useState("");
  const [selectedGenres, setSelectedGenres] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // ジャンルの候補
  const genres = ["自然", "歴史文化", "グルメ", "アクティビティ", "温泉", "イベント", "美術館", "ショッピング"];

  // ジャンルボタンクリック時のトグル処理
  const handleGenreClick = (genre) => {
    setSelectedGenres((prev) =>
      prev.includes(genre)
        ? prev.filter((g) => g !== genre)
        : [...prev, genre]
    );
  };

  // 送信ボタン押下時
  const handleSubmit = async () => {
    if (!location) {
      alert("観光地名を入力してください");
      return;
    }
    if (selectedGenres.length === 0) {
      alert("少なくとも1つのジャンルを選択してください");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const res = await axios.post("http://localhost:8000/create-pamphlet", {
        location: location,
        genres: selectedGenres,
      });

      // APIレスポンスを受け取ったらパンフレットページへ遷移
      navigate("/pamphlet", {
        state: {
          pamphletData: res.data,
        },
      });
    } catch (err) {
      console.error(err);
      setError("パンフレットの作成に失敗しました。再度お試しください。");
    } finally {
      setLoading(false);
    }
  };

  // ローディング中はメッセージ表示のみ
  if (loading) {
    return (
      <div style={{ textAlign: "center", marginTop: "2rem" }}>
        <p>パンフレット作成中...</p>
        {/* ここにスピナーなどを入れてもOK */}
      </div>
    );
  }

  return (
    <div style={{ maxWidth: "600px", margin: "2rem auto", padding: "1rem" }}>
      <h2>パンフレット作成フォーム</h2>

      {/* 観光地入力 */}
      <div style={{ marginBottom: "1rem" }}>
        <label>
          観光地名：
          <input
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="例：京都"
            style={{ marginLeft: "0.5rem", padding: "0.5rem", width: "70%" }}
          />
        </label>
      </div>

      {/* ジャンル選択 */}
      <div style={{ marginBottom: "1rem" }}>
        <p>ジャンルを選択：</p>
        <div style={{ display: "flex", flexWrap: "wrap", gap: "0.5rem" }}>
          {genres.map((g) => {
            const isSelected = selectedGenres.includes(g);
            return (
              <button
                key={g}
                type="button"
                onClick={() => handleGenreClick(g)}
                style={{
                  padding: "0.5rem 1rem",
                  border: "1px solid #333",
                  borderRadius: "4px",
                  backgroundColor: isSelected ? "#4caf50" : "#f0f0f0",
                  color: isSelected ? "#fff" : "#000",
                  cursor: "pointer",
                }}
              >
                {g}
              </button>
            );
          })}
        </div>
      </div>

      {/* エラー表示 */}
      {error && (
        <div style={{ color: "red", marginBottom: "1rem" }}>{error}</div>
      )}

      {/* 送信ボタン */}
      <div>
        <button
          type="button"
          onClick={handleSubmit}
          style={{
            padding: "0.75rem 1.5rem",
            fontSize: "1rem",
            backgroundColor: "#007bff",
            color: "#fff",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
          }}
        >
          パンフレットを作成
        </button>
      </div>
    </div>
  );
};

export default InputPage;