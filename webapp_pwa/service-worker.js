const CACHE_NAME = 'omb-pwa-v8.2';
const ASSETS = [
    './',
    './index.html',
    './css/style.css',
    './js/app.js',
    './manifest.json',
    './assets/openmotorbridge_logo.svg',
    './assets/openmotormesh_logo.svg',
    './assets/openmotorbridge_logo.jpg',
    './assets/openmotormesh_logo.jpg'
];

self.addEventListener('install', (e) => {
    e.waitUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
    );
});

self.addEventListener('fetch', (e) => {
    e.respondWith(
        caches.match(e.request).then((res) => res || fetch(e.request))
    );
});