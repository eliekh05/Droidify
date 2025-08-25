import React from 'react';
import './Footer.css';

const Footer = () => {
  const footerColumns = [
    {
      title: 'Resources',
      links: [
        { text: 'Custom Rom', url: 'https://anroot.netlify.app/Custom_Rom' },
        { text: 'Recovery Images', url: 'https://anroot.netlify.app/Recovery_Images' },
        { text: 'Kernels', url: 'https://anroot.netlify.app/Kernels' },
        { text: 'Root Tools', url: 'https://anroot.netlify.app/Root_Tools' },
        { text: 'Mods & Tweaks', url: 'https://anroot.netlify.app/Mods_and_Tweaks' }
      ],
    },
    {
      title: 'Guides',
      links: [
        { text: 'Rooting Guide', url: 'https://anroot.netlify.app/Rooting_Guide' },
        { text: 'Custom ROM Installation', url: 'https://anroot.netlify.app/Custom_ROM_Installation' },
        { text: 'Backup & Restore', url: 'https://anroot.netlify.app/Backup_and_Restore' },
        { text: 'Troubleshooting', url: 'https://anroot.netlify.app/Troubleshooting' },
        { text: 'FAQ', url: 'https://anroot.netlify.app/FAQ' }
      ],
    },
    {
      title: 'Company',
      links: [
        { text: 'About Us', url: 'https://anroot.netlify.app/About_Us' },
        { text: 'Our Team', url: 'https://anroot.netlify.app/Our_Team' },
        { text: 'Privacy Policy', url: 'https://anroot.netlify.app/Privacy_Policy' },
        { text: 'Terms of Service', url: 'https://anroot.netlify.app/Terms_of_Service' },
        { text: 'Contact Us', url: 'https://anroot.netlify.app/Contact_Us' }
      ],
    },
  ];

  const socialLinks = [
    { icon: 'fab fa-facebook-f', url: 'https://www.facebook.com/eliekh05', label: 'Facebook' },
    { icon: 'fab fa-x-twitter', url: 'https://x.com/eliekh05', label: 'Twitter' },
    { icon: 'fab fa-github', url: 'https://github.com/eliekh05/droidify', label: 'GitHub' },
    { icon: 'fab fa-telegram', url: 'https://t.me/eliekh05', label: 'Telegram' },
    { icon: 'fab fa-whatsapp', url: 'https://wa.me/+96179140038', label: 'WhatsApp' }
  ];

  return (
    <footer id="contact" role="contentinfo" aria-label="Footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-column">
            <h3 id="footer-brand">AndroidCustomizer</h3>
            <p>
              Making Android customization accessible to everyone by
              eliminating the confusion and wasted time.
            </p>
            <div className="social-links">
              {socialLinks.map((social, index) => (
                <a
                  key={index}
                  href={social.url}
                  aria-label={social.label}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="social-link"
                >
                  <i className={social.icon} aria-hidden="true"></i>
                </a>
              ))}
            </div>
          </div>

          {footerColumns.map((column, index) => (
            <div
              key={index}
              className="footer-column"
              role="region"
              aria-labelledby={`footer-${column.title.toLowerCase().replace(/\\s+/g, '-')}`}
            >
              <h3 id={`footer-${column.title.toLowerCase().replace(/\\s+/g, '-')}`}>{column.title}</h3>
              <ul>
                {column.links.map((link, linkIndex) => (
                  <li key={linkIndex}>
                    <a href={link.url} className="footer-link" target="_blank" rel="noopener noreferrer">
                      {link.text}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="footer-bottom">
          <p>&copy; {new Date().getFullYear()} AndroidCustomizer. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
