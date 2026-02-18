self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  return self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  // Empty fetch handler is enough to trigger the Install button
  event.respondWith(fetch(event.request));
});

