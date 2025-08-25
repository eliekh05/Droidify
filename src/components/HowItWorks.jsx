import React from 'react';
import './HowItWorks.css';

const HowItWorks = () => {
  const steps = [
    {
      number: 1,
      title: 'Find Your Device',
      description: 'Enter your device model or select from our comprehensive database of Android devices.'
    },
    {
      number: 2,
      title: 'Choose Your ROM',
      description: 'Browse through verified custom ROMs, kernels, and mods specifically compatible with your device.'
    },
    {
      number: 3,
      title: 'Download Resources',
      description: 'Get all necessary files in one place - ROMs, recovery images, drivers, and tools.'
    },
    {
      number: 4,
      title: 'Follow Guide',
      description: 'Use our detailed step-by-step guide customized for your specific device model.'
    }
  ];

  return (
    <section className="how-it-works" id="guide">
      <div className="container">
        <div className="section-title">
          <h2>How It Works</h2>
          <p>Our platform simplifies the Android customization process down to a few easy steps</p>
        </div>
        <div className="steps">
          {steps.map((step) => (
            <div key={step.number} className="step">
              <div className="step-number">{step.number}</div>
              <h3>{step.title}</h3>
              <p>{step.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;
