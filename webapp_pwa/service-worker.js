const CACHE_NAME = 'omb-pwa-v8.6';
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
    self.skipWaiting();
    e.waitUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
    );
});

self.addEventListener('activate', (e) => {
    e.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(
                keys.map((key) => {
                    if (key !== CACHE_NAME) {
                        return caches.delete(key);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

// Network-First with Cache Fallback (Ensures freshest updates while supporting full offline PWA)
self.addEventListener('fetch', (e) => {
    e.respondWith(
        fetch(e.request).then((networkRes) => {
            if (networkRes && networkRes.status === 200 && e.request.method === 'GET') {
                const resClone = networkRes.clone();
                caches.open(CACHE_NAME).then((cache) => cache.put(e.request, resClone));
            }
            return networkRes;
        }).catch(() => caches.match(e.request))
    );
});