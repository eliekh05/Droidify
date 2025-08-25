import React from 'react';
import './PopularDevices.css';

const PopularDevices = () => {
  const devices = [
    {
      image: 'https://via.placeholder.com/150',
      name: 'Samsung Galaxy S21',
      codename: 'o1s',
      romsCount: 21,
    },
    {
      image: 'https://via.placeholder.com/150',
      name: 'Google Pixel 6',
      codename: 'oriole',
      romsCount: 18,
    },
    {
      image: 'https://via.placeholder.com/150',
      name: 'OnePlus 9 Pro',
      codename: 'lemonadep',
      romsCount: 24,
    },
    {
      image: 'https://via.placeholder.com/150',
      name: 'Xiaomi Mi 11',
      codename: 'venus',
      romsCount: 29,
    },
  ];

  return (
    <section className="popular-devices" id="devices">
      <div className="container">
        <div className="section-title">
          <h2>Popular Devices</h2>
          <p>Explore some of our most frequently customized Android devices</p>
        </div>
        <div className="devices-grid">
          {devices.map((device, index) => (
            <div key={index} className="device-card">
              <div className="device-image">
                <img src={device.image} alt={device.name} />
              </div>
              <div className="device-info">
                <h3>{device.name}</h3>
                <p>Codename: {device.codename}</p>
                <p>{device.romsCount} ROMs available</p>
                <button type="button" className="btn">View Resources</button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default PopularDevices;
