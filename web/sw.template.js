'use strict';
const PREFIX='bank-so-it:'+self.registration.scope+':';
const LEGACY_PREFIX='rrb-practice:'+self.registration.scope+':';
const CACHE=PREFIX+'__BUILD_HASH__';
const SCOPE=self.registration.scope;
const FILES=__PRECACHE__;
const urls=FILES.map(file=>new URL(file,SCOPE).href);
self.addEventListener('install',event=>{event.waitUntil((async()=>{
 // Revalidate every release asset, even if the browser's HTTP cache is fresh.
 await (await caches.open(CACHE)).addAll(urls.map(url=>new Request(url,{cache:'reload'})));
 // Also activates updates for older clients that only offered a manual button.
 await self.skipWaiting();
})());});
self.addEventListener('activate',event=>{event.waitUntil((async()=>{
 // Scope-specific metadata prevents this project from deleting another Pages app's cache.
 for(const key of await caches.keys())if((key.startsWith(PREFIX)||key.startsWith(LEGACY_PREFIX))&&key!==CACHE){const cache=await caches.open(key);if(await cache.match(new URL('scope.json',SCOPE).href))await caches.delete(key);}
 await self.clients.claim();
})());});
self.addEventListener('message',event=>{if(event.data&&event.data.type==='ACTIVATE_UPDATE')self.skipWaiting();});
// Downloads are assets even when a browser sends them as a navigation.
const DOWNLOADS={
 [new URL('downloads/Bank-SO-IT.apk',SCOPE).href]:{name:'Bank-SO-IT.apk',type:'application/vnd.android.package-archive'},
 [new URL('bank.json',SCOPE).href]:{name:'bank-so-it-question-bank.json',type:'application/json'}
};
async function asset(request,href,navigation){
 const cache=await caches.open(CACHE);
 const response=(await cache.match(href))||await fetch(request);
 const download=DOWNLOADS[href];
 if(!download||!response.ok)return response;
 // Content-Disposition covers browsers that navigate instead of honoring download.
 // Preserve JSON fetch semantics; attachment is only needed for document navigation.
 if(!navigation)return response;
 const headers=new Headers(response.headers);
 // Fetch exposes decoded bytes; copied transport headers would describe gzip bytes.
 headers.delete('Content-Encoding');headers.delete('Content-Length');
 headers.set('Content-Type',download.type);
 headers.set('Content-Disposition','attachment; filename="'+download.name+'"');
 return new Response(response.body,{status:response.status,statusText:response.statusText,headers});
}
self.addEventListener('fetch',event=>{
 if(event.request.method!=='GET')return;
 const url=new URL(event.request.url);if(!url.href.startsWith(SCOPE))return;
 // Query strings do not turn a known static file into an app route.
 url.search='';url.hash='';
 const href=url.href;
 if(urls.includes(href)){
  event.respondWith(asset(event.request,href,event.request.mode==='navigate'));return;
 }
 // This app uses in-page screens, so only its root URL needs a shell fallback.
 // Unknown paths must retain real network errors/404s, including missing downloads.
 if(event.request.mode==='navigate'&&href===SCOPE){
  event.respondWith(asset(event.request,new URL('index.html',SCOPE).href,false));
 }
});
