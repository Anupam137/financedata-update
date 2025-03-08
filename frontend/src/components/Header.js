import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

const Header = () => {
  return (
    <header className="header">
      <div className="container">
        <div className="header-content">
          <div className="logo">
            <Link to="/">
              <h1>FinSearch</h1>
              <span className="tagline">Powered by AI</span>
            </Link>
          </div>
          <nav className="main-nav">
            <ul>
              <li>
                <Link to="/">Search</Link>
              </li>
              <li>
                <Link to="/compare">Compare Companies</Link>
              </li>
              <li>
                <Link to="/about">About</Link>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header; 