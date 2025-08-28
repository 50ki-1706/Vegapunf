import React, { useState } from 'react';
function InputPage() {
  // ① 入力された観光地名を管理
  const [spotName, setSpotName] = useState('')
  // ② 選択可能なジャンル配列
  const genres = ['自然', '歴史文化', 'グルメ', 'アクティビティ', '温泉']
  // ③ 選択中のジャンルを管理
  const [selectedGenres, setSelectedGenres] = useState([])
  // ジャンルボタンクリック時のトグル処理
  const handleGenreToggle = (genre) => {
    setSelectedGenres(prev => {
      if (prev.includes(genre)) {
        // すでに選択済なら外す
        return prev.filter(g => g !== genre)
      } else {
        // 未選択なら追加
        return [...prev, genre]
      }
    })
  }
  // 送信ボタン押下時の処理
  const handleSubmit = async () => {
    // 簡易バリデーション
    if (!spotName.trim()) {
      alert('観光地名を入力してください')
      return
    }
    if (selectedGenres.length === 0) {
      alert('ジャンルを 1 つ以上選択してください')
      return
    }
    const payload = {
      spotName,
      genres: selectedGenres,
    }
    try {
      const response = await fetch('/api/submitSpot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })
      if (!response.ok) throw new Error('ネットワークエラー')
      const data = await response.json()
      console.log('送信成功:', data)
      // 必要ならリセット／画面遷移など
      setSpotName('')
      setSelectedGenres([])
    } catch (err) {
      console.error(err)
      alert('送信に失敗しました')
    }
  }
  return (
    <div style={{ maxWidth: 400, margin: '0 auto', padding: 20 }}>
      {/* 観光地入力フォーム */}
      <label>
        観光地名：
        <input
          type="text"
          value={spotName}
          onChange={e => setSpotName(e.target.value)}
          placeholder="例：京都の清水寺"
          style={{ width: '100%', padding: 8, marginTop: 4, marginBottom: 12 }}
        />
      </label>
      {/* ジャンル選択タグ */}
      <div style={{ marginBottom: 20 }}>
        <p>ジャンルを選択（複数可）:</p>
        {genres.map(genre => {
          const isSelected = selectedGenres.includes(genre)
          return (
            <button
              key={genre}
              onClick={() => handleGenreToggle(genre)}
              style={{
                margin: 4,
                padding: '6px 12px',
                border: 'none',
                borderRadius: 4,
                cursor: 'pointer',
                backgroundColor: isSelected ? '#007bff' : '#eee',
                color: isSelected ? '#fff' : '#333',
              }}
            >
              {genre}
            </button>
          )
        })}
      </div>
      {/* データ送信ボタン */}
      <button
        onClick={handleSubmit}
        style={{
          width: '100%',
          padding: 10,
          fontSize: 16,
          backgroundColor: '#28a745',
          color: '#fff',
          border: 'none',
          borderRadius: 4,
          cursor: 'pointer',
        }}
      >
        送信する
      </button>
    </div>
  )
}
export default InputPage