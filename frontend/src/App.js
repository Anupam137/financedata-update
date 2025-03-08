import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

// Import components
import Header from './components/Header';
import SearchPage from './pages/SearchPage';
import ComparisonPage from './pages/ComparisonPage';
import AboutPage from './pages/AboutPage';

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <main className="container">
          <Routes>
            <Route path="/" element={<SearchPage />} />
            <Route path="/compare" element={<ComparisonPage />} />
            <Route path="/about" element={<AboutPage />} />
          </Routes>
        </main>
        <footer className="footer">
          <div className="container">
            <p>&copy; {new Date().getFullYear()} Financial Search Engine. All rights reserved.</p>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;
