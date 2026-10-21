(function(){
'use strict';
if(window.Android){window.platformCard=()=>'';return;}
let registration=null,installPrompt=null,ready=false;
const refresh=()=>{if(typeof state!=='undefined'&&state&&screen==='library'&&typeof render==='function')render();};
window.platformCard=()=>'<div class="card"><h3>Use it like an app</h3><p class="small muted gap-sm">'+(ready?'Ready for offline practice on this browser.':'Open online once to prepare offline practice.')+' Progress is saved in this browser. Open or reload online to load the latest release. Updates do not restart a page you are already using.</p><p class="small muted gap-sm">Install from your browser menu or Add to Home Screen on iPhone/iPad.</p>'+(installPrompt?'<div class="actions"><button data-action="install-web" class="primary">Install web app</button></div>':'')+'<p class="small muted gap-sm">The Android APK includes the same curated questions and quick revision. Progress can be moved using a progress backup.</p><a href="downloads/Bank-SO-IT.apk" class="download-link" download="Bank-SO-IT.apk">Download Android APK</a><br><a href="bank.json" class="download-link" download="bank-so-it-question-bank.json">Download latest question pack</a><p class="small muted gap-sm">Export a progress backup before reinstalling. The current APK can update an installation signed with the Android 1.2 release key.</p></div>';
window.addEventListener('beforeinstallprompt',event=>{event.preventDefault();installPrompt=event;refresh();});
window.addEventListener('appinstalled',()=>{installPrompt=null;refresh();});
document.addEventListener('click',async event=>{const b=event.target.closest('[data-action="install-web"]');if(b&&installPrompt){installPrompt.prompt();await installPrompt.userChoice;installPrompt=null;refresh();}});
if('serviceWorker' in navigator&&isSecureContext){
 window.AppUpdateReady=(async()=>{
  const initialController=navigator.serviceWorker.controller;
  try{
   registration=await navigator.serviceWorker.register('./sw.js',{scope:'./',updateViaCache:'none'});
   navigator.serviceWorker.ready.then(()=>{ready=true;refresh();});
   // Only opening/reloading the page applies a release to the displayed app.
   // A worker may prepare in the background without restarting an existing page.
   await registration.update();
   const worker=registration.installing||registration.waiting;
   if(registration.waiting)registration.waiting.postMessage({type:'ACTIVATE_UPDATE'});
   if(worker&&!['activated','redundant'].includes(worker.state))await new Promise(resolve=>{
    const changed=()=>{if(['activated','redundant'].includes(worker.state)){worker.removeEventListener('statechange',changed);resolve();}};
    worker.addEventListener('statechange',changed);changed();
   });
   if(initialController&&navigator.serviceWorker.controller!==initialController){
    // Finish this user-requested load with the complete new cached release.
    // There is deliberately no test/editor/route check.
    location.reload();return false;
   }
  }catch(error){/* An offline load keeps the last complete cached release. */}
  return true;
 })();
}
})();
