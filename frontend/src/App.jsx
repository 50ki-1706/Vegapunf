import { useState, useEffect } from 'react';
import axios from 'axios'; // axiosをインポート
import './App.css';

function App() {
  // バックエンドからのメッセージを保存するstate
  const [message, setMessage] = useState('');

  // コンポーネントが最初に表示された時に実行する処理
  useEffect(() => {
    // FastAPIのエンドポイントにGETリクエストを送る
    axios
      .get('http://127.0.0.1:8000/')
      .then((response) => {
        // 成功したら、レスポンスのデータをmessageにセット
        setMessage(response.data.message);
      })
      .catch((error) => {
        console.error('APIの呼び出し中にエラーが発生しました', error);
        setMessage('APIの読み込みに失敗しました。');
      });
  }, []); // 第2引数の配列が空なので、初回レンダリング時のみ実行される

  return (
    <>
      <h1>Vite + React + FastAPI</h1>
      <div className="card">
        <p>バックエンドからのメッセージ:</p>
        <h2>{message || '読み込み中...'}</h2>
      </div>
    </>
  );
}

export default App;
