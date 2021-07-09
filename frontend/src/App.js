import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios'

function App() {
  const [lastNews, setLastNews] = useState(0);

  useEffect(()=>{
  axios.get('http://localhost:5000/index').then(response => {
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
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      <p>{lastNews}</p>
      </header>
    </div>
  );
}

export default App;
