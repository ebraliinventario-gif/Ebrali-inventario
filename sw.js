const CACHE_NAME = 'inventario-cache-v3';

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

    const url = new URL(req.url);
    const isSameOrigin = url.origin === self.location.origin;
    const isNavigation = req.mode === 'navigate';
    const isIndex = isSameOrigin && (url.pathname.endsWith('/') || url.pathname.endsWith('/index.html'));

    event.respondWith(
        (async () => {
            // Para o HTML principal (navegação), prioriza a rede para evitar app desatualizado.
            if (isNavigation || isIndex) {
                try {
                    const res = await fetch(req);
                    const copy = res.clone();
                    const cache = await caches.open(CACHE_NAME);
                    await cache.put(req, copy);
                    return res;
                } catch (_) {
                    const cached = await caches.match(req);
                    return cached || caches.match('./index.html');
                }
            }

            // Para assets, usa cache-first.
            const cached = await caches.match(req);
            if (cached) return cached;
            try {
                const res = await fetch(req);
                const copy = res.clone();
                const cache = await caches.open(CACHE_NAME);
                await cache.put(req, copy);
                return res;
            } catch (_) {
                return caches.match('./index.html');
            }
        })()
    );
});
