const CACHE_NAME = 'inventario-cache-v1';

const ASSETS = [
    './',
    './index.html',
    './styles.css',
    './config.js',
    './manifest.webmanifest',
    './logo_ebrali-2025.png',
    './dados_ruas.js',
    './dados_ruas_03_06.js',
    './dados_ruas_07_15.js',
    './dados_ruas_09_15.js',
    './dados_ruas_12_15.js',
    './dados_ruas_14_17.js',
    './dados_ruas_18_20.js',
    './dados_ruas_buffer.js',
    './dados_industria_99.js',
    './dados_piso.js'
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS)).then(() => self.skipWaiting())
    );
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keys) =>
            Promise.all(keys.map((key) => (key !== CACHE_NAME ? caches.delete(key) : Promise.resolve())))
        ).then(() => self.clients.claim())
    );
});

self.addEventListener('fetch', (event) => {
    const req = event.request;
    if (req.method !== 'GET') return;

    event.respondWith(
        caches.match(req).then((cached) => {
            if (cached) return cached;
            return fetch(req)
                .then((res) => {
                    const copy = res.clone();
                    caches.open(CACHE_NAME).then((cache) => cache.put(req, copy));
                    return res;
                })
                .catch(() => caches.match('./index.html'));
        })
    );
});
