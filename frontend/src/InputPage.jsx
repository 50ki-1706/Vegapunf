import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './InputPage.css';

// 選択可能なジャンルを定義
const AVAILABLE_GENRES = ["自然", "歴史文化", "食事", "エンタメ", "ショッピング"];

const InputPage = () => {
  const [location, setLocation] = useState('');
  const [selectedGenres, setSelectedGenres] = useState(new Set());
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  // ジャンル選択のハンドラ
  const handleGenreChange = (genre) => {
    const newGenres = new Set(selectedGenres);
    if (newGenres.has(genre)) {
      newGenres.delete(genre);
    } else {
      newGenres.add(genre);
    }
    setSelectedGenres(newGenres);
  };

  // フォーム送信のハンドラ
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!location) {
      setError('観光地の名称を入力してください。');
      return;
    }
    if (selectedGenres.size === 0) {
      setError('ジャンルを1つ以上選択してください。');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const requestBody = {
        location: location,
        genres: Array.from(selectedGenres),
      };

      console.log('APIにリクエストを送信します:', requestBody);

      // バックエンドのAPIを呼び出す
      const response = await axios.post(
        'http://127.0.0.1:8000/make-pamphlet',
        requestBody
      );

      console.log('APIからレスポンスを受信しました:', response.data);

      // 成功したら、結果を持ってパンフレットページに遷移
      navigate('/pamphlet', { state: { pamphletData: response.data } });

    } catch (err) {
      console.error('API呼び出し中にエラーが発生しました:', err);
      const errorMessage = err.response?.data?.detail || 'パンフレットの作成に失敗しました。サーバーのログを確認してください。';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="input-page">
      <h1>旅のパンフレットを自動作成</h1>
      <p>好きな観光地と興味のあるジャンルを選ぶだけで、<br/>AIがあなただけのオリジナルパンフレットを作成します。</p>
      
      <form onSubmit={handleSubmit} className="pamphlet-form">
        <div className="form-group">
          <label htmlFor="location">観光地の名称</label>
          <input
            id="location"
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="例: 沖縄 美ら海水族館"
            disabled={isLoading}
          />
        </div>

        <div className="form-group">
          <label>興味のあるジャンル（複数選択可）</label>
          <div className="genre-tags">
            {AVAILABLE_GENRES.map((genre) => (
              <button
                type="button"
                key={genre}
                className={`genre-tag ${selectedGenres.has(genre) ? 'selected' : ''}`}
                onClick={() => handleGenreChange(genre)}
                disabled={isLoading}
              >
                {genre}
              </button>
            ))}
          </div>
        </div>

        {error && <p className="error-message">{error}</p>}

        <button type="submit" className="submit-btn" disabled={isLoading}>
          {isLoading ? 'AIが作成中...' : 'パンフレットを作成'}
        </button>
      </form>
    </div>
  );
};

export default InputPage;