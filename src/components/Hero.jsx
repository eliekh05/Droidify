import React, { useState } from 'react';
import './Hero.css';

const Hero = () => {
  const [searchInput, setSearchInput] = useState('');
  const [loader, setLoader] = useState(false);

  const handleSearch = async () => {
    setLoader(true);
    if (searchInput.trim()) {
      try {
        const data = await handleSubmit();
        setLoader(false);
        console.log(data);
      } catch (error) {
        setLoader(false);
        console.error('Error:', error);
      }
    } else {
      alert('Please enter a device model to search');
      setLoader(false);
    }
  };

  const handleSubmit = async () => {
    const response = await fetch(`/api/search/${searchInput}`);
    const data = await response.json();
    return data;
  };

  return (
    <section className="hero" id="home">
      <div className="container">
        <h1>All Android Custom ROMs in One Place</h1>
        <p>
          Stop wasting days searching for custom firmware files. Our platform provides all the resources, tools, and guides you need for any Android device - ready to use in minutes, not days.
        </p>
        <div className="search-bar">
          <input
            type="text"
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
            placeholder="Enter your device model"
          />
          <button onClick={handleSearch} disabled={loader}>
            <i className="fas fa-search"></i> 
            {loader ? ' Loading...' : ' Find Resources'}
          </button>
        </div>
      </div>
    </section>
  );
};

export default Hero;
