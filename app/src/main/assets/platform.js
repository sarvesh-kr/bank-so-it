(function(){
'use strict';
if(window.Android){window.platformCard=()=>'';return;}
let registration=null,installPrompt=null,ready=false;
const refresh=()=>{if(typeof screen!=='undefined'&&screen==='library'&&typeof render==='function')render();};
window.platformCard=()=>'<div class="card"><h3>Use it like an app</h3><p class="small muted gap-sm">'+(ready?'Ready for offline practice on this browser.':'Open online once to prepare offline practice.')+' Progress is saved in this browser. Install from your browser menu or Add to Home Screen on iPhone/iPad.</p><div class="actions">'+(installPrompt?'<button data-action="install-web" class="primary">Install web app</button>':'')+(registration&&registration.waiting?'<button data-action="update-web">Apply available update</button>':'')+'</div><p class="small muted gap-sm">The Android APK includes all 1,150 questions and focused revision. Progress can be moved using a progress backup.</p><a href="downloads/RRB-IT-Practice-Lite.apk" class="download-link" download>Download Android APK</a><br><a href="bank.json" class="download-link" download="rrb-it-question-bank.json">Download latest question pack</a><p class="small muted gap-sm">Version 1.2 uses a new signing key. If you installed the old APK, export your progress first, uninstall it, install this version, then restore your backup.</p></div>';
window.addEventListener('beforeinstallprompt',event=>{event.preventDefault();installPrompt=event;refresh();});
window.addEventListener('appinstalled',()=>{installPrompt=null;refresh();});
document.addEventListener('click',async event=>{const b=event.target.closest('[data-action]');if(!b)return;if(b.dataset.action==='install-web'&&installPrompt){installPrompt.prompt();await installPrompt.userChoice;installPrompt=null;refresh();}if(b.dataset.action==='update-web'&&registration&&registration.waiting){if(typeof state!=='undefined'&&state.active){toast('Finish your unfinished session before applying this update.');return;}registration.waiting.postMessage({type:'ACTIVATE_UPDATE'});}});
if('serviceWorker' in navigator&&isSecureContext){
 let reloading=false,hadController=!!navigator.serviceWorker.controller;
 navigator.serviceWorker.addEventListener('controllerchange',()=>{if(hadController&&!reloading){reloading=true;location.reload();}hadController=true;});
 window.addEventListener('load',async()=>{try{registration=await navigator.serviceWorker.register('./sw.js',{scope:'./',updateViaCache:'none'});navigator.serviceWorker.ready.then(()=>{ready=true;refresh();});registration.addEventListener('updatefound',()=>{const worker=registration.installing;if(worker)worker.addEventListener('statechange',()=>{if(worker.state==='installed')refresh();});});refresh();}catch(e){console.warn('Offline cache was not installed:',e.message);}});
}
})();
