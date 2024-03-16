import React, { useState } from 'react';
import './App.css';
import logo from './logo.png';
import avatarRita from './assets/rita.png';
import avatarMark from './assets/mark.png';
import avatarMary from './assets/mary.png';

function App() {
  const [activeAgent, setActiveAgent] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);  // Add this line to define audioUrl and setAudioUrl
  const [audioStream, setAudioStream] = useState(null);  // Add this line to define audioStream and setAudioStream
  const [stockSymbol, setStockSymbol] = useState('');
   
  const handleAgentClick = (agent) => {
    setActiveAgent(agent);
  };

  const handleCommand = async (command) => {
   if (command === 'TALK') {
            let endpoint = '';
            let bodyData = {};
            if (activeAgent === 'rita') {
              endpoint = '/talk-to-rita';
              bodyData = { text: "Good Morning to everyone" };// Add any specific data or parameters for RITA if required
            } else if (activeAgent === 'mark') {
              endpoint = '/talk-to-mark';
              // Add any specific data or parameters for MARK if required
            } else if (activeAgent === 'mary' && stockSymbol) {
              endpoint = '/talk-to-mary';
              bodyData = { symbol: stockSymbol };
            } else {
              console.error('Agent not selected or stock symbol not provided');
              return;
            }
      
            try {
              const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}${endpoint}`, {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify(bodyData),// Add body data if needed for the specific agent
              });
              const data = await response.json();        
  
        if (response.ok) {
          const audioContent = base64ToArrayBuffer(data.audioContent); // Convert base64 to ArrayBuffer
          const blob = new Blob([audioContent], { type: 'audio/mp3' });
          const url = URL.createObjectURL(blob);
          setAudioUrl(url);  // Update state
          setAudioStream(url);
        } else {
          console.error('Response error:', data);
        }
      } catch (error) {
        console.error('Error:', error);
      }
    }
  };
    // Function to convert base64 to ArrayBuffer
    function base64ToArrayBuffer(base64) {
      const binaryString = window.atob(base64);
      const len = binaryString.length;
      const bytes = new Uint8Array(len);
      for (let i = 0; i < len; i++) {
        bytes[i] = binaryString.charCodeAt(i);
      }
      return bytes.buffer;
    }


  return (
    <div className="App">
      <header className="navbar">
        <span>DATE: {new Date().toLocaleDateString()}</span>
        <span>   </span>
      </header>
      <h1>Welcome to MultiChat!</h1>
      <h2>Choose an agent to start the conversation</h2>
      <h3>Select Rita for Weather, Mark for Headlines and Mary for Stocks</h3>
      <img src={logo} className="logo" alt="logo" />
      <div className="avatar-container">
        <div className={`avatar ${activeAgent === 'rita' ? 'active' : ''}`} onClick={() => handleAgentClick('rita')}>
          <img src={avatarRita} alt="Rita" />
          <p>RITA</p>
        </div>
        <div className={`avatar ${activeAgent === 'mark' ? 'active' : ''}`} onClick={() => handleAgentClick('mark')}>
          <img src={avatarMark} alt="Mark" />
          <p>MARK</p>
        </div>
        <div className={`avatar ${activeAgent === 'mary' ? 'active' : ''}`} onClick={() => handleAgentClick('mary')}>
          <img src={avatarMary} alt="Mary" />
          <p>MARY</p>
        </div>
      </div>
      <div>
        {activeAgent === 'mary' && (
          <input 
            type="text" 
            placeholder="Enter Stock Symbol" 
            value={stockSymbol} 
            onChange={(e) => setStockSymbol(e.target.value)}
            className="stock-input"
          />
        )}
      </div>      
      <div className="controls">
        <button onClick={() => handleCommand('TALK')}>TALK</button>
      </div>
      <div className="audio-container">
        {audioStream && <audio src={audioStream} controls autoPlay />}
        {audioUrl && (
          <a href={audioUrl} download="speech.mp3" className="download-link">
            Download MP3
          </a>
        )}
      </div>
    </div>
  );
}

export default App;
