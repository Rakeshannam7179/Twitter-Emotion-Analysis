import React, { useState } from 'react';
import axios from 'axios';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title } from 'chart.js';
import { Pie, Bar } from 'react-chartjs-2';
import { Activity, Image as ImageIcon, Hash, Link as LinkIcon, AlertCircle } from 'lucide-react';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title);

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

function App() {
  return (
    <div className="app-container">
      <header className="header">
        <h1>Tweet Emotion Matrix</h1>
        <p>Advanced AI Emotion Analysis Dashboard</p>
      </header>

      <div className="dashboard-grid">
        <TextAnalysis />
        <ImageAnalysis />
        <HashtagAnalysis />
        <UrlAnalysis />
      </div>
    </div>
  );
}

function TextAnalysis() {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    if (!text) return;
    setLoading(true);
    setError('');
    
    try {
      const formData = new FormData();
      formData.append('text', text);
      const res = await axios.post(`${API_BASE}/analyze_text`, formData);
      setResult(res.data);
    } catch (err) {
      setError('Failed to analyze text. Ensure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-card">
      <div className="card-title">
        <Activity size={24} color="var(--primary)" />
        <h2>Text Emotion</h2>
      </div>
      <div className="input-group">
        <input 
          type="text" 
          placeholder="Enter text to analyze..." 
          value={text} 
          onChange={(e) => setText(e.target.value)} 
        />
        <button className="btn" onClick={handleAnalyze} disabled={loading || !text}>
          {loading ? <Activity className="loading-spinner" /> : 'Analyze'}
        </button>
      </div>

      {error && <div className="error-message"><AlertCircle size={16} />{error}</div>}
      
      {result && (
        <div className="result-container">
          <div className="emotion-label">Dominant: {result.label} ({(result.score * 100).toFixed(1)}%)</div>
          <div className="chart-wrapper">
            <Pie 
              data={{
                labels: Object.keys(result.all_scores || {}),
                datasets: [{
                  data: Object.values(result.all_scores || {}).map(s => s * 100),
                  backgroundColor: [
                    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#C9CBCF'
                  ]
                }]
              }}
              options={{ maintainAspectRatio: false, plugins: { legend: { position: 'right' } } }}
            />
          </div>
        </div>
      )}
    </div>
  );
}

function ImageAnalysis() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    if (!file) return;
    setLoading(true);
    setError('');
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      const res = await axios.post(`${API_BASE}/analyze_image`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResult(res.data);
    } catch (err) {
      setError('Failed to analyze image. It might not contain a detectable face.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-card">
      <div className="card-title">
        <ImageIcon size={24} color="var(--primary)" />
        <h2>Image Emotion</h2>
      </div>
      <div className="input-group">
        <input 
          type="file" 
          accept="image/*"
          onChange={(e) => setFile(e.target.files[0])} 
        />
        <button className="btn" onClick={handleAnalyze} disabled={loading || !file}>
          {loading ? <Activity className="loading-spinner" /> : 'Analyze'}
        </button>
      </div>

      {error && <div className="error-message"><AlertCircle size={16} />{error}</div>}
      
      {result && (
        <div className="result-container">
          <div className="emotion-label">Dominant: {result.emotion}</div>
          <div className="chart-wrapper">
            <Pie 
              data={{
                labels: Object.keys(result.scores),
                datasets: [{
                  data: Object.values(result.scores),
                  backgroundColor: [
                    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#C9CBCF'
                  ]
                }]
              }}
              options={{ maintainAspectRatio: false, plugins: { legend: { position: 'right' } } }}
            />
          </div>
        </div>
      )}
    </div>
  );
}

function HashtagAnalysis() {
  const [hashtag, setHashtag] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    if (!hashtag) return;
    setLoading(true);
    setError('');
    
    try {
      const cleanHash = hashtag.replace('#', '');
      const res = await axios.get(`${API_BASE}/analyze_hashtag?hashtag=${cleanHash}`);
      if (res.data.message) {
        setError(res.data.message);
        setResult(null);
      } else {
        setResult(res.data);
      }
    } catch (err) {
      setError('Failed to fetch hashtag data.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-card">
      <div className="card-title">
        <Hash size={24} color="var(--primary)" />
        <h2>Hashtag Aggregation</h2>
      </div>
      <div className="input-group">
        <input 
          type="text" 
          placeholder="Enter hashtag (e.g. tech)" 
          value={hashtag} 
          onChange={(e) => setHashtag(e.target.value)} 
        />
        <button className="btn" onClick={handleAnalyze} disabled={loading || !hashtag}>
          {loading ? <Activity className="loading-spinner" /> : 'Analyze'}
        </button>
      </div>

      {error && <div className="error-message"><AlertCircle size={16} />{error}</div>}
      
      {result && (
        <div className="result-container">
          <div style={{textAlign: 'center', marginBottom: '1rem'}}>
            Tweets Analyzed: <strong>{result.tweets_analyzed}</strong>
          </div>
          <div className="chart-wrapper">
            <Pie 
              data={{
                labels: Object.keys(result.emotion_distribution),
                datasets: [{
                  data: Object.values(result.emotion_distribution),
                  backgroundColor: [
                    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#C9CBCF'
                  ]
                }]
              }}
              options={{ maintainAspectRatio: false, plugins: { legend: { position: 'right' } } }}
            />
          </div>
        </div>
      )}
    </div>
  );
}


function UrlAnalysis() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    if (!url) return;
    setLoading(true);
    setError('');
    
    try {
      const res = await axios.post(`${API_BASE}/analyze_url?url=${encodeURIComponent(url)}`);
      if (res.data.error) {
        setError(res.data.error);
        setResult(null);
      } else {
        setResult(res.data);
      }
    } catch (err) {
      setError('Failed to fetch URL analysis.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-card">
      <div className="card-title">
        <LinkIcon size={24} color="var(--primary)" />
        <h2>URL Analysis</h2>
      </div>
      <div className="input-group">
        <input 
          type="text" 
          placeholder="Enter tweet URL..." 
          value={url} 
          onChange={(e) => setUrl(e.target.value)} 
        />
        <button className="btn" onClick={handleAnalyze} disabled={loading || !url}>
          {loading ? <Activity className="loading-spinner" /> : 'Analyze'}
        </button>
      </div>

      {error && <div className="error-message"><AlertCircle size={16} />{error}</div>}
      
      {result && (
        <div className="result-container">
          <div className="emotion-label">Dominant: {result.label} ({(result.score * 100).toFixed(1)}%)</div>
          <div className="chart-wrapper">
            <Pie 
              data={{
                labels: Object.keys(result.all_scores || {}),
                datasets: [{
                  data: Object.values(result.all_scores || {}).map(s => s * 100),
                  backgroundColor: [
                    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#C9CBCF'
                  ]
                }]
              }}
              options={{ maintainAspectRatio: false, plugins: { legend: { position: 'right' } } }}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
