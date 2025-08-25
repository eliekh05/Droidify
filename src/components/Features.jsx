import React from 'react';
import './Features.css';

const Features = () => {
  const features = [
    {
      icon: 'fas fa-database',
      title: 'Comprehensive Database',
      description: 'All files organized by device model, manufacturer, and codename so you never have to guess which file is right for your device.'
    },
    {
      icon: 'fas fa-book',
      title: 'Step-by-Step Guides',
      description: 'Clear instructions tailored to your specific device model, making the rooting and flashing process straightforward.'
    },
    {
      icon: 'fas fa-download',
      title: 'Fast Downloads',
      description: 'Direct downloads for all firmware files, tools, and utilities from our high-speed servers - no more hunting across forums.'
    },
    {
      icon: 'fas fa-users',
      title: 'Active Community',
      description: 'Get help from our community of Android enthusiasts and experts for any issues you encounter.'
    },
    {
      icon: 'fas fa-tools',
      title: 'Troubleshooting Tools',
      description: 'Built-in tools to diagnose and fix common issues that occur during the customization process.'
    },
    {
      icon: 'fas fa-bell',
      title: 'Update Notifications',
      description: 'Get notified when new ROMs, kernels, or tools become available for your specific device.'
    }
  ];

  return (
    <section className="features" id="features">
      <div className="container">
        <div className="section-title">
          <h2>Why Choose AndroidCustomizer</h2>
          <p>We streamline the Android customization process, saving you days of research and troubleshooting</p>
        </div>
        <div className="features-grid">
          {features.map((feature, index) => (
            <div key={index} className="feature-card">
              <div className="feature-icon">
                <i className={feature.icon}></i>
              </div>
              <h3>{feature.title}</h3>
              <p>{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;
