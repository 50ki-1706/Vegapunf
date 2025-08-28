import { useRef } from 'react';
import { useLocation } from 'react-router-dom';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import './pamphlet.css';

const PamphletPage = () => {
  // React Router の location.state からデータを受け取る
  const location = useLocation();
  const data = location.state?.pamphletData || {
    title: 'サンプルタイトル',
    coverImage: 'https://via.placeholder.com/600x400',
    description: 'ここに説明文が入ります。',
    sections: [
      {
        heading: 'セクション1',
        text: 'テキスト本文1...',
        image: 'https://via.placeholder.com/300x200',
      },
      {
        heading: 'セクション2',
        text: 'テキスト本文2...',
        image: 'https://via.placeholder.com/300x200',
      },
    ],
  };

  // PDF に変換する対象の DOM
  const pamphletRef = useRef(null);

  const handleExportPDF = async () => {
    if (!pamphletRef.current) return;
    // html2canvas でキャプチャ
    const canvas = await html2canvas(pamphletRef.current, { scale: 2 });
    const imgData = canvas.toDataURL('image/png');
    // jsPDF で PDF 化
    const pdf = new jsPDF({
      unit: 'pt', // pt = point (1/72 inch)
      format: 'a4', // A4 サイズ
      orientation: 'portrait',
    });
    const pageWidth = pdf.internal.pageSize.getWidth();
    const pageHeight = pdf.internal.pageSize.getHeight();
    // 画像サイズを調整（A4 にフィットさせる）
    const imgProps = pdf.getImageProperties(imgData);
    const imgWidth = pageWidth;
    const imgHeight = (imgProps.height * pageWidth) / imgProps.width;
    pdf.addImage(imgData, 'PNG', 0, 0, imgWidth, imgHeight);
    pdf.save(`${data.title || 'pamphlet'}.pdf`);
  };

  return (
    <div className="pamphlet-page">
      <h1>パンフレットプレビュー</h1>
      <div className="pamphlet-container" ref={pamphletRef}>
        {/* 表紙 */}
        <div className="pamphlet-cover">
          <img src={data.coverImage} alt="cover" />
          <h2 className="pamphlet-title">{data.title}</h2>
        </div>

        {/* 説明文 */}
        <div className="pamphlet-description">
          <p>{data.description}</p>
        </div>

        {/* セクション一覧 */}
        <div className="pamphlet-sections">
          {data.sections.map((sec, idx) => (
            <div className="section-card" key={idx}>
              <div className="section-img">
                <img src={sec.image} alt={`section-${idx}`} />
              </div>
              <div className="section-text">
                <h3>{sec.heading}</h3>
                <p>{sec.text}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      <button className="btn-export" onClick={handleExportPDF}>
        PDFをダウンロード
      </button>
    </div>
  );
};

export default PamphletPage;
