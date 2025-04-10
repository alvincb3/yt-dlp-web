import { useState } from 'react';
import axios from 'axios';

function App() {
  const [url, setUrl] = useState('');
  const [filename, setFilename] = useState('');
  const [error, setError] = useState('');

  const handleDownload = async () => {
    try {
      const res = await axios.post('/api/download', { url });
      setFilename(res.data.filename);
      setError('');
    } catch (err) {
      setError(err.response?.data?.error || 'Error occurred');
      setFilename('');
    }
  };

  return (
    <div className="p-6 max-w-md mx-auto">
      <h1 className="text-2xl mb-4">yt-dlp Web</h1>
      <input
        type="text"
        value={url}
        onChange={e => setUrl(e.target.value)}
        className="border p-2 w-full mb-4"
        placeholder="Enter video URL"
      />
      <button
        onClick={handleDownload}
        className="bg-blue-500 text-white px-4 py-2 rounded"
      >
        Download
      </button>
      {filename && (
        <p className="mt-4">
          Download ready: <a href={`/api/downloads/${filename}`} className="text-blue-600 underline">Click here</a>
        </p>
      )}
      {error && <p className="text-red-600 mt-4">{error}</p>}
    </div>
  );
}

export default App;
