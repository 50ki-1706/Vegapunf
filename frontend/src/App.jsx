import React, { useState, useEffect } from 'react';
import { Routes, Route } from 'react-router-dom';
import axios from 'axios';
import InputPage from './pages/InputPage';
import PamphletPage from './pages/PamphletPage';
import './App.css';

const App = () => {
  // バックエンドからのメッセージを保存する state
  const [message, setMessage] = useState('');

  // マウント時に FastAPI へ GET
  useEffect(() => {
    axios
      .get('http://127.0.0.1:8000/')
      .then((response) => {
        setMessage(response.data.message);
      })
      .catch((error) => {
        console.error('APIの呼び出し中にエラーが発生しました', error);
        setMessage('APIの読み込みに失敗しました。');
      });
  }, []);

  return (
    <>
      <h1>Vite + React + FastAPI</h1>
      <div className="card">
        <p>バックエンドからのメッセージ:</p>
        <h2>{message || '読み込み中...'}</h2>
      </div>

      {/* ルーティングの定義 */}
      <Routes>
        <Route path="/" element={<InputPage />} />
        <Route path="/pamphlet" element={<PamphletPage />} />
      </Routes>
    </>
  );
};

export default App;