self.addEventListener('install', e => e.waitUntil(
  caches.open('chambeapr-v1').then(c => c.addAll(['/','  /subscribe','/terms','/privacy','/dashboard']))
));
self.addEventListener('fetch', e => e.respondWith(
  caches.match(e.request).then(r => r || fetch(e.request))
));