/**
 * Droidify API client — ES5 compatible
 * Same-origin fetch with AbortController timeout
 */
var BASE = '';

function get(path, params, timeoutMs) {
  params    = params    || {};
  timeoutMs = timeoutMs || 8000;

  var pairs = [];
  Object.keys(params).forEach(function (k) {
    if (params[k] != null && params[k] !== '') {
      pairs.push(encodeURIComponent(k) + '=' + encodeURIComponent(params[k]));
    }
  });
  var qs  = pairs.join('&');
  var url = BASE + '/api' + path + (qs ? '?' + qs : '');

  var ctrl  = new AbortController();
  var timer = setTimeout(function () { ctrl.abort(); }, timeoutMs);

  return fetch(url, { signal: ctrl.signal })
    .then(function (res) {
      clearTimeout(timer);
      if (!res.ok) throw new Error('API ' + res.status + ': ' + path);
      return res.json();
    })
    .catch(function (e) {
      clearTimeout(timer);
      if (e.name === 'AbortError') throw new Error('Request timed out: ' + path);
      throw e;
    });
}

var api = {
  health:          function ()           { return get('/health'); },
  devices:         function (p)          { return get('/devices', p); },
  device:          function (code, ms)   { return get('/devices/' + encodeURIComponent(code), {}, ms || 20000); },
  roms:            function (p)          { return get('/roms', p); },
  recoveries:      function (p)          { return get('/recoveries', p); },
  tools:           function ()           { return get('/tools'); },
  androidVersions: function ()           { return get('/android-versions'); },
  guides:          function (codename)   {
    if (!codename) return get('/guides', {});
    return get('/guides/' + encodeURIComponent(codename));
  },
};
