/* reveal.js — AOS handles animations via data-aos attributes.
   This file provides the _reObserve noop for backward compatibility. */
window._reObserve = function() { if (window.AOS) AOS.refresh(); };
