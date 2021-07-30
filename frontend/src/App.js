import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios'

function App() {
  const [lastNews, setLastNews] = useState(0);

  useEffect(()=>{
  axios.get('http://localhost:5000/news').then(response => {
      setLastNews(response.data)    
    }).catch(error => {
      console.log(error)
    })
  }, [])
  // useEffect(() => {
  //   fetch('/time').then(res => res.json()).then(data => {
  //     setCurrentTime(data.time);
  //   });
  // }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>
          Welcome to Brazil Covid Analysis.
        </h1>

        <h2 className="News">{lastNews}</h2>

        <a
          className="App-link"
          href="https://github.com/luantorrex/brazil-covid-analysis"
          target="_blank"
          rel="noopener noreferrer"
        >
          Our Repository
        </a>
      </header>
    </div>
  );
}

export default App;
