import { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('http://localhost:8000')
      .then(res => {
        setMessage(res.data.message);
        setLoading(false);
      })
      .catch(err => {
        setMessage('Không kết nối được với Backend');
        setLoading(false);
        console.error(err);
      });
  }, []);

  return (
    <div style={{ 
      minHeight: '100vh', 
      backgroundColor: '#1a1a1a', 
      color: 'white', 
      display: 'flex', 
      alignItems: 'center', 
      justifyContent: 'center',
      fontFamily: 'Arial, sans-serif'
    }}>
      <div style={{ textAlign: 'center' }}>
        <h1 style={{ fontSize: '3rem', marginBottom: '1rem' }}>
           Gym Management System
        </h1>
        
        <p style={{ fontSize: '1.5rem', marginBottom: '2rem' }}>
          Hệ thống quản lý phòng gym 
        </p>

        <div style={{ 
          backgroundColor: '#333', 
          padding: '20px', 
          borderRadius: '10px',
          maxWidth: '600px',
          margin: '0 auto'
        }}>
          <h2>Kiểm tra kết nối Backend</h2>
          {loading ? (
            <p>Đang kết nối...</p>
          ) : (
            <p style={{ color: message.includes('tốt') ? '#4ade80' : '#f87171' }}>
              {message}
            </p>
          )}
        </div>

        <p style={{ marginTop: '2rem', color: '#888' }}>
          Backend đang chạy tại <strong>http://localhost:8000</strong>
        </p>
      </div>
    </div>
  );
}

export default App;