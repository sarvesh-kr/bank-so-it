'use strict';
const {chromium}=require('playwright'),http=require('node:http'),fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../_site');
const types={'.html':'text/html','.js':'application/javascript','.json':'application/json','.webmanifest':'application/manifest+json','.css':'text/css','.png':'image/png','.apk':'application/vnd.android.package-archive'};
const server=http.createServer((req,res)=>{const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);const prefix=['/rrb-it-practice/','/another-practice/','/'].find(x=>pathname.startsWith(x));if(!prefix){res.writeHead(404).end();return;}let file=path.resolve(root,pathname.slice(prefix.length)||'index.html');if(!file.startsWith(root+path.sep)||!fs.existsSync(file)||!fs.statSync(file).isFile()){res.writeHead(404).end();return;}res.writeHead(200,{'Content-Type':types[path.extname(file)]||'application/octet-stream','Cache-Control':'no-cache'});fs.createReadStream(file).pipe(res);});
(async()=>{await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));const origin='http://127.0.0.1:'+server.address().port,url=origin+'/rrb-it-practice/';const browser=await chromium.launch({headless:true,executablePath:process.env.CHROME_PATH,args:['--no-sandbox']});let context;
try{
 context=await browser.newContext({viewport:{width:390,height:844},acceptDownloads:true});const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));const action=a=>page.locator('[data-action="'+a+'"]').first();
 await page.goto(url);await page.waitForSelector('.subjects');assert.match(await page.locator('.stats').innerText(),/1150/);
 for(const id of ['dw_dm','cloud_ai_ml','se_bank_it']){
  await page.locator('[data-action="subject"][data-id="'+id+'"]').click();
  const focused=await page.evaluate(()=>getPool().length);
  await page.locator('#studyScope').selectOption('all');
  assert((await page.evaluate(()=>getPool().length))>focused);
  await page.locator('#count').fill('1');await action('begin').click();
  const answer=await page.evaluate(()=>state.active.questions[0].answer);
  await page.locator('[data-action="answer"][data-index="'+answer+'"]').click();
  await action('check').click();assert.match(await page.locator('.feedback').innerText(),/Correct/);
  await action('submit').click();await action('finish').click();
  await page.locator('#nav [data-screen="home"]').click();
 }
 // Keep the existing persistence assertions independent of these new-subject sessions.
 await page.evaluate(()=>{state.progress={};state.history=[];state.totalSessions=0;persist();});
 await page.evaluate(async()=>{await navigator.serviceWorker.ready;if(!navigator.serviceWorker.controller)await new Promise(r=>navigator.serviceWorker.addEventListener('controllerchange',r,{once:true}));});
 const manifest=await page.evaluate(async()=>await(await fetch('manifest.webmanifest')).json());assert.equal(manifest.start_url,'./');assert.equal(manifest.scope,'./');
 await action('subject').click();await page.locator('#count').fill('3');await action('begin').click();await page.waitForSelector('.question');let correct=await page.evaluate(()=>state.active.questions[0].answer);await page.locator('[data-action="answer"][data-index="'+correct+'"]').click();await action('bookmark').click();await action('check').click();assert.match(await page.locator('.feedback').innerText(),/Correct/);await action('next').click();let wrong=await page.evaluate(()=>(state.active.questions[1].answer+1)%5);await page.locator('[data-action="answer"][data-index="'+wrong+'"]').click();await action('save-exit').click();await page.evaluate(async()=>await AppStore.save(JSON.stringify(state)));
 await context.setOffline(true);await page.reload();await page.waitForSelector('.subjects');await action('resume').click();assert.equal(await page.locator('.option.chosen').count(),1);await action('submit').click();await action('finish').click();assert.match(await page.locator('.result-score').innerText(),/0\.75/);await action('review-wrong').click();assert.equal(await page.locator('.option.correct').count(),1);assert.equal(await page.locator('.option.incorrect').count(),1);
 await page.locator('#nav [data-screen="library"]').click();assert.match(await page.locator('#app').innerText(),/Ready for offline/);
 const saved=page.waitForEvent('download');await action('backup-progress').click();const download=await saved;fs.mkdirSync('test-results',{recursive:true});await download.saveAs('test-results/progress-backup.json');const backup=JSON.parse(fs.readFileSync('test-results/progress-backup.json'));assert.equal(backup.state.totalSessions,1);
 // Verify the APK can also be fetched from the offline cache.
 assert.equal(await page.evaluate(async()=>{const r=await fetch('downloads/RRB-IT-Practice-Lite.apk');const a=new Uint8Array(await r.arrayBuffer());return a[0]+','+a[1];}),'80,75');
 await context.setOffline(false);
 const fresh=await browser.newContext();const restore=await fresh.newPage();await restore.goto(url);await restore.waitForSelector('.subjects');await restore.evaluate(p=>receiveImport(JSON.stringify(p)),backup);await restore.locator('[data-action="confirm-restore"]').click();assert.equal(await restore.evaluate(()=>state.totalSessions),1);assert.equal(await restore.evaluate(()=>Object.keys(state.progress).length),2);await restore.evaluate(async()=>await AppStore.save(JSON.stringify(state)));await restore.reload();await restore.waitForSelector('.subjects');assert.equal(await restore.evaluate(()=>Object.keys(state.bookmarks).length),1);
 // Identical app hosted at a second Pages path must get separate browser state.
 const sibling=await fresh.newPage();await sibling.goto(origin+'/another-practice/');await sibling.waitForSelector('.subjects');assert.equal(await sibling.evaluate(()=>state.totalSessions),0);assert.equal(await sibling.evaluate(()=>Object.keys(state.bookmarks).length),0);
 // A custom domain serves the same app at /, with a root-scoped offline cache.
 const domainContext=await browser.newContext();const domainPage=await domainContext.newPage();await domainPage.goto(origin+'/');await domainPage.waitForSelector('.subjects');assert.match(await domainPage.locator('.stats').innerText(),/1150/);
 assert.equal(await domainPage.evaluate(async()=>{const registration=await navigator.serviceWorker.ready;if(!navigator.serviceWorker.controller)await new Promise(r=>navigator.serviceWorker.addEventListener('controllerchange',r,{once:true}));return new URL(registration.scope).pathname;}),'/');
 await domainContext.setOffline(true);await domainPage.reload();await domainPage.waitForSelector('.subjects');assert.match(await domainPage.locator('.stats').innerText(),/1150/);await domainContext.close();
 // Simulated native storage bridge consumes the same backup and UI assets.
 const native=await browser.newContext();await native.addInitScript(({raw})=>{let value=raw;window.Android={readState:()=>value,writeState:v=>{value=v;return '';},importPack:()=>{},exportPack:()=>{}};},{raw:JSON.stringify(backup.state)});const apk=await native.newPage();await apk.goto(url);await apk.waitForSelector('.subjects');assert.equal(await apk.evaluate(()=>state.totalSessions),1);await apk.locator('#nav [data-screen="library"]').click();assert.equal(await apk.locator('[data-action="install-web"]').count(),0);
 for(const width of [320,390,900]){await page.setViewportSize({width,height:844});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));}
 assert.deepEqual(errors,[]);await page.screenshot({path:'test-results/pages-library.png',fullPage:true});
 console.log('PASS: Pages subpath and custom-domain root, shared 1150-question bank, PWA scope, offline reload and quiz, score/review, IndexedDB persistence, backup/restore, path isolation, cached APK, simulated native bridge and responsive layouts.');
 await fresh.close();await native.close();
}finally{await browser.close();server.close();}
})().catch(error=>{console.error(error);server.close();process.exitCode=1;});
