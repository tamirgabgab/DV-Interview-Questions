// Offline reading (review V7): a service worker that keeps the pages a reader opened, so
// they open again without a network (for example on the way to an interview). Network
// first: with a network the reader always gets the current site and the copy is
// refreshed; without one the last copy is served. Only GET requests to this site and to
// the CDNs the pages load scripts from are kept, at most MAX_ENTRIES of them.
// Kill switch: set ENABLED to false and deploy; every reader's worker then deletes its
// copies and unregisters itself on its next update check (at most a day later).
const ENABLED = true;
const CACHE = "dvq-pages-v1";
const MAX_ENTRIES = 400;
const CDNS = ["cdn.jsdelivr.net", "unpkg.com", "cdnjs.cloudflare.com"];

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (event) => {
  event.waitUntil((async () => {
    const names = await caches.keys();
    await Promise.all(names.filter((n) => n.startsWith("dvq-") && (!ENABLED || n !== CACHE)).map((n) => caches.delete(n)));
    if (!ENABLED) { await self.registration.unregister(); return; }
    await self.clients.claim();
  })());
});

const keep = (url) => url.origin === self.location.origin || CDNS.includes(url.hostname);

// trim the oldest entries once the cache grows past MAX_ENTRIES
const trim = async (cache) => {
  const keys = await cache.keys();
  for (let i = 0; i < keys.length - MAX_ENTRIES; i++) await cache.delete(keys[i]);
};

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (!ENABLED || req.method !== "GET") return;
  const url = new URL(req.url);
  if (!keep(url)) return;
  event.respondWith((async () => {
    const cache = await caches.open(CACHE);
    try {
      const res = await fetch(req);
      if (res.ok || res.type === "opaque") {
        cache.put(req, res.clone()).then(() => trim(cache)).catch(() => {});
      }
      return res;
    } catch (err) {
      const hit = await cache.match(req, { ignoreVary: true });
      if (hit) return hit;
      if (req.mode === "navigate") {
        return new Response("<!doctype html><meta charset=\"utf-8\"><title>אין חיבור</title>" +
          "<body dir=\"rtl\" style=\"font-family:sans-serif;padding:2rem\"><h1>אין חיבור לרשת</h1>" +
          "<p>העמוד הזה עוד לא נשמר במכשיר. עמודים שכבר פתחתם נפתחים גם בלי רשת.</p></body>",
          { status: 503, headers: { "Content-Type": "text/html; charset=utf-8" } });
      }
      throw err;
    }
  })());
});
