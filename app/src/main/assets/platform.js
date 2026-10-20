(function(){
'use strict';
if(window.Android){window.platformCard=()=>'';return;}
let registration=null,installPrompt=null,ready=false;
let appReady=false,currentScreen=null,pendingReload=false,reloading=false;
const refresh=()=>{if(appReady&&currentScreen==='library'&&typeof render==='function')render();};
async function reloadWhenSafe(){
 if(!pendingReload||reloading||!appReady||document.hidden||['quiz','editor','setup'].includes(currentScreen)||document.querySelector('#modal[open]'))return;
 reloading=true;
 // Prevent an answer/edit landing between this snapshot and the committed write.
 document.body.inert=true;
 try{
  const raw=JSON.stringify(state);
  if(window.AppStore)await AppStore.save(raw);else localStorage.setItem('rrb-it-state-v1',raw);
  location.reload();
 }catch(error){
  reloading=false;document.body.inert=false;
  if(typeof toast==='function')toast('Update ready, but progress could not be saved. Back up progress and reopen the app.');
 }
}
window.addEventListener('bank-so-it:screen',event=>{appReady=true;currentScreen=event.detail.screen;reloadWhenSafe();});
// Closing a dialog may not navigate to another screen.
const dialog=document.querySelector('#modal');if(dialog)dialog.addEventListener('close',reloadWhenSafe);
window.platformCard=()=>'<div class="card"><h3>Use it like an app</h3><p class="small muted gap-sm">'+(ready?'Ready for offline practice on this browser.':'Open online once to prepare offline practice.')+' Progress is saved in this browser. Updates apply automatically when you open online; a current test or edit finishes before reloading.</p><p class="small muted gap-sm">Install from your browser menu or Add to Home Screen on iPhone/iPad.</p>'+(installPrompt?'<div class="actions"><button data-action="install-web" class="primary">Install web app</button></div>':'')+'<p class="small muted gap-sm">The Android APK includes the same curated questions and quick revision. Progress can be moved using a progress backup.</p><a href="downloads/Bank-SO-IT.apk" class="download-link" download>Download Android APK</a><br><a href="bank.json" class="download-link" download="bank-so-it-question-bank.json">Download latest question pack</a><p class="small muted gap-sm">Export a progress backup before reinstalling. The current APK can update an installation signed with the Android 1.2 release key.</p></div>';
window.addEventListener('beforeinstallprompt',event=>{event.preventDefault();installPrompt=event;refresh();});
window.addEventListener('appinstalled',()=>{installPrompt=null;refresh();});
document.addEventListener('click',async event=>{const b=event.target.closest('[data-action="install-web"]');if(b&&installPrompt){installPrompt.prompt();await installPrompt.userChoice;installPrompt=null;refresh();}});
if('serviceWorker' in navigator&&isSecureContext){
 let hadController=!!navigator.serviceWorker.controller,checking=false;
 navigator.serviceWorker.addEventListener('controllerchange',()=>{
  if(hadController)pendingReload=true;
  hadController=true;reloadWhenSafe();
 });
 async function checkForUpdate(){
  if(!registration||checking||!navigator.onLine)return;
  checking=true;
  try{await registration.update();}catch(error){/* Retain the complete offline release if the network is unavailable. */}
  finally{checking=false;}
 }
 window.addEventListener('load',async()=>{
  try{
   registration=await navigator.serviceWorker.register('./sw.js',{scope:'./',updateViaCache:'none'});
   navigator.serviceWorker.ready.then(()=>{ready=true;refresh();});
   // Recovery for a worker left waiting by a prior release/browser interruption.
   if(registration.waiting)registration.waiting.postMessage({type:'ACTIVATE_UPDATE'});
   await checkForUpdate();
  }catch(error){/* Online practice still works when offline caching is unavailable. */}
 });
 window.addEventListener('online',checkForUpdate);
 document.addEventListener('visibilitychange',()=>{if(!document.hidden){reloadWhenSafe();checkForUpdate();}});
}
})();
