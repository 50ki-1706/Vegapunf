import { useState, useEffect } from 'react';
import axios from 'axios';

const useDashBoard = () => {
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
  }, []);
};

export default useDashBoard;
