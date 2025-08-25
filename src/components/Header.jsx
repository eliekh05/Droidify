import React from 'react';
import './Header.css';

const Header = () => {
  return (
    <header>
      <div className="container header-container">
        <div className="logo" role="banner">
          <i className="fas fa-mobile-alt" aria-hidden="true"></i>
          <span>AndroidCustomizer</span>
        </div>

        <nav role="navigation" aria-label="Primary Navigation">
          <ul>
            <li><a href="https://anroot.netlify.app/">Home</a></li>
            <li><a href="https://anroot.netlify.app/Features">Features</a></li>
            <li><a href="https://anroot.netlify.app/Devices">Devices</a></li>
            <li><a href="https://anroot.netlify.app/Guides">Guides</a></li>
            <li><a href="https://anroot.netlify.app/Community">Community</a></li>
            <li><a href="https://anroot.netlify.app/Contact">Contact</a></li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;
