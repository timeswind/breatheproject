import React from 'react';
import logo from './logo.svg';
import './App.css';
import { PythonShell } from 'python-shell';

function App() {

  function test() {
    PythonShell.run('../hello.py', null, function (err, results) {
      if (err) throw err;
      console.log('hello.py finished.');
      console.log('results', results);
    });
  }

  return (
    <div className="App">
      <header className="App-header">
        {/* <img src={logo} className="App-logo" alt="logo" />
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
        </a> */}

        <div>
          Start Date:
    <input type="date" name="start_date" />
          End Date:
    <input type="date" name="end_date" />
        </div>
        <button onClick={test}></button>
      </header>
    </div>
  );
}

export default App;
