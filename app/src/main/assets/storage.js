/* Browser storage is scoped to this Pages project path; Android uses AtomicFile. */
(function(){
'use strict';
if(window.Android)return;
const scope=new URL('./',location.href).pathname;
const name='rrb-it-practice:'+scope;
let dbPromise;
function database(){if(!dbPromise)dbPromise=new Promise((resolve,reject)=>{const req=indexedDB.open(name,1);req.onupgradeneeded=()=>req.result.createObjectStore('state');req.onsuccess=()=>resolve(req.result);req.onerror=()=>reject(req.error);});return dbPromise;}
window.AppStore={
 async load(){const db=await database();const raw=await new Promise((resolve,reject)=>{const req=db.transaction('state','readonly').objectStore('state').get('current');req.onsuccess=()=>resolve(req.result||'');req.onerror=()=>reject(req.error);});if(raw)return raw;const legacy=localStorage.getItem('rrb-it-state-v1');if(legacy){await this.save(legacy);return legacy;}return '';},
 async save(raw){const db=await database();return new Promise((resolve,reject)=>{const tx=db.transaction('state','readwrite');tx.objectStore('state').put(raw,'current');tx.oncomplete=()=>resolve();tx.onerror=()=>reject(tx.error);tx.onabort=()=>reject(tx.error||Error('Storage transaction aborted'));});}
};
})();
