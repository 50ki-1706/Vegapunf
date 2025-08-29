import { useRef } from 'react';
import { useLocation, Link } from 'react-router-dom';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import './pamphlet.css';

const PamphletPage = () => {
  const location = useLocation();
  const pamphletData = location.state?.pamphletData;
  const pamphletRef = useRef(null);

  if (!pamphletData) {
    return (
      <div className="pamphlet-page loading">
        <div className="loading-container">
          <div className="spinner"></div>
          <p>パンフレットデータを読み込んでいます...</p>
          <p>
            データが表示されない場合は、
            <Link to="/">入力ページ</Link>
            に戻ってください。
          </p>
        </div>
      </div>
    );
  }

  const data = {
    title: pamphletData.title,
    description: pamphletData.introduction,
    sections: pamphletData.spots.map((spot) => ({
      heading: spot.name,
      text: spot.ai_description,
    })),
  };

  const handleExportPDF = async () => {
    if (!pamphletRef.current) return;
    // PDF出力時にスタイルが適用されるように、一時的にクラスを追加
    pamphletRef.current.classList.add('pdf-export-mode');

    const canvas = await html2canvas(pamphletRef.current, {
      scale: 2,
      useCORS: true,
      windowWidth: pamphletRef.current.scrollWidth,
      windowHeight: pamphletRef.current.scrollHeight,
    });

    pamphletRef.current.classList.remove('pdf-export-mode');

    const imgData = canvas.toDataURL('image/png');
    const pdf = new jsPDF({
      unit: 'pt',
      format: 'a4',
      orientation: 'portrait',
    });

    const pageWidth = pdf.internal.pageSize.getWidth();
    const pageHeight = pdf.internal.pageSize.getHeight();
    const imgProps = pdf.getImageProperties(imgData);
    const imgWidth = pageWidth;
    const imgHeight = (imgProps.height * imgWidth) / imgProps.width;

    let heightLeft = imgHeight;
    let position = 0;

    pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
    heightLeft -= pageHeight;

    while (heightLeft > 0) {
      position = heightLeft - imgHeight;
      pdf.addPage();
      pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
      heightLeft -= pageHeight;
    }

    pdf.save(`${data.title || 'pamphlet'}.pdf`);
  };

  return (
    <div className="pamphlet-page">
      <header className="pamphlet-header">
        <h1>パンフレットプレビュー</h1>
        <button className="btn-export" onClick={handleExportPDF}>
          PDFをダウンロード
        </button>
      </header>

      <main className="pamphlet-main">
        <div className="pamphlet-container" ref={pamphletRef}>
          <div className="pamphlet-cover">
            <h2 className="pamphlet-title">{data.title}</h2>
          </div>

          {data.description && (
            <section className="pamphlet-section description-section">
              <p>{data.description}</p>
            </section>
          )}
          <div className="pamphlet-grid">
            {data.sections.map((sec, idx) => (
              <section className="pamphlet-section spot-card" key={idx}>
                <div className="spot-card-header">
                  <h3 className="spot-title">{sec.heading}</h3>
                </div>
                <div className="spot-card-body">
                  <p>{sec.text}</p>
                </div>
              </section>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
};

export default PamphletPage;
