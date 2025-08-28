import './App.css';
import { BrowserRouter, Route, Routes, Link } from 'react-router-dom';
import PamphletPage from './PamphletPage';
import DashboardPage from './DashboardPage';
import InputPage from './InputPage';
function App() {
  return (
    <div className="container">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/input" element={<InputPage />} />
          <Route path="/pamphlet" element={<PamphletPage />} />
          <Route path="*" element={<h1>Not Found Page</h1>} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
