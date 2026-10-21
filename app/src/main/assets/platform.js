(function(){
'use strict';
if(window.Android){window.platformCard=()=>'';return;}
let registration=null,installPrompt=null,ready=false;
const refresh=()=>{if(typeof state!=='undefined'&&state&&screen==='library'&&typeof render==='function')render();};
window.platformCard=()=>'<div class="card"><h3>Use it like an app</h3><p class="small muted gap-sm">'+(ready?'Ready for offline practice on this browser.':'Open online once to prepare offline practice.')+' Progress is saved in this browser. Open or reload online to load the latest release. Updates do not restart a page you are already using.</p><p class="small muted gap-sm">Install from your browser menu or Add to Home Screen on iPhone/iPad.</p>'+(installPrompt?'<div class="actions"><button data-action="install-web" class="primary">Install web app</button></div>':'')+'<p class="small muted gap-sm">The Android APK includes the same curated questions and quick revision. Progress can be moved using a progress backup.</p><a href="downloads/Bank-SO-IT.apk" class="download-link" download="Bank-SO-IT.apk" data-download="apk">Download Android APK</a><br><a href="bank.json" class="download-link" download="bank-so-it-question-bank.json" data-download="bank">Download latest question pack</a><p class="small muted gap-sm">Export a progress backup before reinstalling. The current APK can update an installation signed with the Android 1.2 release key.</p></div>';
// Fetch through the offline worker, then save a local Blob. WebKit's native URL
// download path can bypass its offline cache even when normal fetch succeeds.
const downloads={apk:{path:'downloads/Bank-SO-IT.apk',name:'Bank-SO-IT.apk',type:'application/vnd.android.package-archive'},bank:{path:'bank.json',name:'bank-so-it-question-bank.json',type:'application/json'}};
const pendingDownloads=new Set();
document.addEventListener('click',async event=>{
 const link=event.target.closest('[data-download]');if(!link||event.button>0||event.ctrlKey||event.metaKey||event.shiftKey||event.altKey)return;
 const key=link.dataset.download,item=downloads[key];if(!item)return;event.preventDefault();if(pendingDownloads.has(key))return;
 pendingDownloads.add(key);link.setAttribute('aria-busy','true');
 try{
  const response=await fetch(item.path,{cache:'no-store'});if(!response.ok)throw Error();const bytes=await response.arrayBuffer();
  if(key==='apk'){const magic=new Uint8Array(bytes,0,Math.min(bytes.byteLength,4));if(magic.length!==4||magic[0]!==80||magic[1]!==75||magic[2]!==3||magic[3]!==4)throw Error();}
  else QuizCore.validatePack(JSON.parse(new TextDecoder().decode(bytes)));
  const url=URL.createObjectURL(new Blob([bytes],{type:item.type})),save=document.createElement('a');save.href=url;save.download=item.name;document.body.appendChild(save);save.click();save.remove();setTimeout(()=>URL.revokeObjectURL(url),60000);
 }catch(error){if(typeof toast==='function')toast((key==='apk'?'The APK':'The question pack')+' could not be downloaded. Reload online and try again.');}
 finally{pendingDownloads.delete(key);link.removeAttribute('aria-busy');}
});
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
