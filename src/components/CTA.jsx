import React from 'react';
import './CTA.css';

const CTA = () => {
  return (
    <section className="cta">
      <div className="container">
        <h2>Ready to Transform Your Android Experience?</h2>
        <p>
          Stop wasting days on research and troubleshooting. Get everything
          you need to customize your Android device in one place.
        </p>
        <div className="cta-buttons">
          <button type="button" className="btn btn-primary">Find My Device</button>
          <button type="button" className="btn btn-secondary">Browse Popular ROMs</button>
        </div>
      </div>
    </section>
  );
};

export default CTA;
