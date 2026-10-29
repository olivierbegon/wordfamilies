// Offline cache for the word family lessons.
// VERSION and FILES are written by build.py. Run it, then push; the iPad picks up the update the next time it opens the app online.
const VERSION = "wf-e68b47a776";
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
  "audio/06b9e1150225.mp3",
  "audio/0836f9d01591.mp3",
  "audio/0d753f40bb4a.mp3",
  "audio/1094c109c98c.mp3",
  "audio/11a32b52cdf2.mp3",
  "audio/154b1396d560.mp3",
  "audio/1a7062113536.mp3",
  "audio/1cb95c425ae1.mp3",
  "audio/21d6ec1b2b28.mp3",
  "audio/238ecdd069ca.mp3",
  "audio/2623a06f5ae1.mp3",
  "audio/282428b09882.mp3",
  "audio/28a5f3d8f6f9.mp3",
  "audio/295cc1bdf348.mp3",
  "audio/36ce249cef61.mp3",
  "audio/3824e497eb6a.mp3",
  "audio/38fc8809dfd9.mp3",
  "audio/3948875f7030.mp3",
  "audio/39d2fe0f5ece.mp3",
  "audio/3b02f8914d01.mp3",
  "audio/3d433f8a1523.mp3",
  "audio/3fadc3603302.mp3",
  "audio/40b437bf40af.mp3",
  "audio/450dbe9a74b4.mp3",
  "audio/491be91c3572.mp3",
  "audio/4d28528c68c7.mp3",
  "audio/4d9171370542.mp3",
  "audio/4fc8b28ec7f0.mp3",
  "audio/5cd803670cc9.mp3",
  "audio/6311a71d4144.mp3",
  "audio/6772293e75ed.mp3",
  "audio/6b507c2d5a62.mp3",
  "audio/6c17f6b69477.mp3",
  "audio/6fa6e479ff23.mp3",
  "audio/77abc6bee277.mp3",
  "audio/7c5bb977fb2a.mp3",
  "audio/814958c88d35.mp3",
  "audio/82fb56be2ba0.mp3",
  "audio/833de08528d2.mp3",
  "audio/84737ec7b162.mp3",
  "audio/8dd20a32d260.mp3",
  "audio/91c5496732e2.mp3",
  "audio/9320bf636e31.mp3",
  "audio/94a634a05cf7.mp3",
  "audio/960b4eaaaad0.mp3",
  "audio/992ed0c46f1b.mp3",
  "audio/9d7b4ab96ef0.mp3",
  "audio/a33ad57c1d66.mp3",
  "audio/a41600d502bd.mp3",
  "audio/a46fde9df686.mp3",
  "audio/a5b9021241f4.mp3",
  "audio/a7b008cb4ffc.mp3",
  "audio/a81baa93d7d7.mp3",
  "audio/b310ebdd99b6.mp3",
  "audio/b5ab1f02911b.mp3",
  "audio/b9233e9c33bc.mp3",
  "audio/bfd85f7f73da.mp3",
  "audio/c24e766087e7.mp3",
  "audio/c3bb9cec41de.mp3",
  "audio/c5c19c62f535.mp3",
  "audio/d174c2b3b1d7.mp3",
  "audio/d38a3166c906.mp3",
  "audio/d453b3829e04.mp3",
  "audio/d79da734ffb8.mp3",
  "audio/d948de17853e.mp3",
  "audio/defab56258a4.mp3",
  "audio/e0af6817b8a9.mp3",
  "audio/e2f0b42eb4c6.mp3",
  "audio/e95e802ea9ed.mp3",
  "audio/ea6be724c445.mp3",
  "audio/ec1fd88b72ec.mp3",
  "audio/ec7dfd3c99a2.mp3",
  "audio/ecaba2bc1573.mp3",
  "audio/f56d56a43767.mp3",
  "audio/f871dae075ec.mp3",
  "audio/fae8fe56c98a.mp3"
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
