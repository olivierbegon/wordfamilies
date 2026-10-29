// Offline cache for the word family lessons.
// VERSION and FILES are written by build.py. Run it, then push; the iPad picks up the update the next time it opens the app online.
const VERSION = "wf-9f77f3883f";
const FILES = [
  "./",
  "index.html",
  "manifest.webmanifest",
  "am.html",
  "ap.html",
  "mix-am-ap.html",
  "icons/icon-180.png",
  "icons/icon-192.png",
  "icons/icon-512.png",
  "fonts/andika-latin-400-normal.woff2",
  "fonts/andika-latin-700-normal.woff2",
  "fonts/sniglet-latin-400-normal.woff2",
  "fonts/sniglet-latin-800-normal.woff2",
  "audio/01a25265835c.mp3",
  "audio/03bdb0c0b5be.mp3",
  "audio/09eca265b06f.mp3",
  "audio/0e4af02779ad.mp3",
  "audio/10e6e7af1268.mp3",
  "audio/11e2e9de9528.mp3",
  "audio/172ec0579011.mp3",
  "audio/174060f29cf9.mp3",
  "audio/17dbbe4dfaed.mp3",
  "audio/1fbf573a4065.mp3",
  "audio/21b17df32943.mp3",
  "audio/25f8b47debda.mp3",
  "audio/2be149c9d48b.mp3",
  "audio/2d9f7005aa51.mp3",
  "audio/36b1e890e83e.mp3",
  "audio/36c0500f8535.mp3",
  "audio/36d82b8cbe67.mp3",
  "audio/370b15f33e85.mp3",
  "audio/3967d4e5054c.mp3",
  "audio/48c1e4e2e6a8.mp3",
  "audio/4992f7a5bd18.mp3",
  "audio/55fbc17bf8e2.mp3",
  "audio/56d02ec9466a.mp3",
  "audio/581f68f21ec2.mp3",
  "audio/5928bd7e7a0f.mp3",
  "audio/5d28f0b03b5e.mp3",
  "audio/5d3794689d95.mp3",
  "audio/5d3a21f2dcdc.mp3",
  "audio/5f4db352a99d.mp3",
  "audio/6aefd76f6301.mp3",
  "audio/6b89ca846f81.mp3",
  "audio/6cd1f410987a.mp3",
  "audio/6e6cafcef8de.mp3",
  "audio/72a916ea689d.mp3",
  "audio/7648de390472.mp3",
  "audio/799a73ca2d8e.mp3",
  "audio/7b84a9be12d2.mp3",
  "audio/7fb1df6bbab4.mp3",
  "audio/803a771b7da9.mp3",
  "audio/897ed6c03abe.mp3",
  "audio/8b1ca8f194e0.mp3",
  "audio/90f8ddaf6b42.mp3",
  "audio/92195f0534f6.mp3",
  "audio/93b2b6103cc1.mp3",
  "audio/93ca0b2941ea.mp3",
  "audio/93d69c47e16f.mp3",
  "audio/9631dae74d3b.mp3",
  "audio/999b115848ed.mp3",
  "audio/99cbde15f449.mp3",
  "audio/9bf4c00cc54e.mp3",
  "audio/a36749d5b0e7.mp3",
  "audio/ac93f4702744.mp3",
  "audio/b00e1bbc048d.mp3",
  "audio/b53eeb3a6573.mp3",
  "audio/b5bd63d1b1ec.mp3",
  "audio/bb82239974b1.mp3",
  "audio/c06ee32fa21f.mp3",
  "audio/c87e61dc4be9.mp3",
  "audio/cd1038c52f36.mp3",
  "audio/cd93d3dd3784.mp3",
  "audio/cf0f8ed4b9f2.mp3",
  "audio/cf27a7def0ce.mp3",
  "audio/d35151c600a5.mp3",
  "audio/da90ddacb638.mp3",
  "audio/dd3013207c4a.mp3",
  "audio/e09247bc3798.mp3",
  "audio/e0fff871a3b6.mp3",
  "audio/e27c0d538b86.mp3",
  "audio/e5093d725f07.mp3",
  "audio/e72063ed8ba5.mp3",
  "audio/e84a88a31e91.mp3",
  "audio/ee9d9d42109a.mp3",
  "audio/f1e949f5a9bb.mp3",
  "audio/f75168cb239d.mp3",
  "audio/f82b7b09e373.mp3",
  "audio/f887a9791dd4.mp3"
];
self.addEventListener("install", e => {
  e.waitUntil(caches.open(VERSION).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== VERSION).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
// Network first for the page (so updates show when online), cache first for everything else.
self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  if (req.mode === "navigate") {
    e.respondWith(
      fetch(req).then(res => { const copy = res.clone(); caches.open(VERSION).then(c => c.put(req, copy)); return res; })
        .catch(() => caches.match(req, { ignoreSearch: true }).then(hit => hit || caches.match("index.html")))
    );
    return;
  }
  e.respondWith(caches.match(req).then(hit => hit || fetch(req)));
});
