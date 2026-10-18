'use strict';
const PREFIX='rrb-practice:'+self.registration.scope+':';
const CACHE=PREFIX+'1d47a79e8830bd23';
const SCOPE=self.registration.scope;
const FILES=["index.html", "style.css", "core.js", "app.js", "storage.js", "backup.js", "platform.js", "bank.json", "manifest.webmanifest", "icon-192.png", "icon-512.png", "downloads/RRB-IT-Practice-Lite.apk", "scope.json"];
const urls=FILES.map(file=>new URL(file,SCOPE).href);
self.addEventListener('install',event=>{event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(urls)));});
self.addEventListener('activate',event=>{event.waitUntil((async()=>{
 // Scope-specific metadata prevents this project from deleting another Pages app's cache.
 for(const key of await caches.keys())if(key.startsWith(PREFIX)&&key!==CACHE){const cache=await caches.open(key);if(await cache.match(new URL('scope.json',SCOPE).href))await caches.delete(key);}
 await self.clients.claim();
})());});
self.addEventListener('message',event=>{if(event.data&&event.data.type==='ACTIVATE_UPDATE')self.skipWaiting();});
self.addEventListener('fetch',event=>{
 if(event.request.method!=='GET')return;
 const url=new URL(event.request.url);if(!url.href.startsWith(SCOPE))return;
 if(event.request.mode==='navigate'){event.respondWith(caches.open(CACHE).then(async cache=>(await cache.match(new URL('index.html',SCOPE).href))||fetch(event.request)));return;}
 if(urls.includes(url.href))event.respondWith(caches.open(CACHE).then(async cache=>(await cache.match(event.request))||fetch(event.request)));
});
