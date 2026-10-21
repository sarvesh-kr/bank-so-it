'use strict';
const {chromium}=require('playwright'),http=require('node:http'),fs=require('node:fs'),path=require('node:path'),os=require('node:os'),assert=require('node:assert/strict'),{execFileSync}=require('node:child_process');
const repo=path.resolve(__dirname,'..'),site=path.join(repo,'_site'),root=fs.mkdtempSync(path.join(os.tmpdir(),'bank-so-it-update-'));
const scope='/bank-so-it/',types={'.html':'text/html','.js':'application/javascript','.json':'application/json','.webmanifest':'application/manifest+json','.css':'text/css','.png':'image/png'};
function publish(){fs.cpSync(site,root,{recursive:true});}
function revision(marker){
 publish();
 const index=path.join(root,'index.html');fs.writeFileSync(index,fs.readFileSync(index,'utf8').replace('<body>','<body data-release-probe="'+marker+'">'));
 const sw=path.join(root,'sw.js');fs.writeFileSync(sw,fs.readFileSync(sw,'utf8').replace(/const CACHE=PREFIX\+'[^']+';/,"const CACHE=PREFIX+'test-"+marker+"';"));
}
// The compatibility fixture is pinned: future commits must keep testing an actual
// pre-auto-update client, rather than silently replacing it with current HEAD.
const oldCommit='693275acdf059ef83e274cfdbb59d5679f8ce4ff';
function oldFile(name){return execFileSync('git',['show',oldCommit+':'+name],{cwd:repo,maxBuffer:8*1024*1024});}
publish();
for(const name of ['index.html','style.css','core.js','app.js','storage.js','backup.js','platform.js','bank.json','manifest.webmanifest'])fs.writeFileSync(path.join(root,name),oldFile('app/src/main/assets/'+name));
fs.copyFileSync(path.join(site,'downloads/Bank-SO-IT.apk'),path.join(root,'downloads/RRB-IT-Practice-Lite.apk'));
const files=fs.readdirSync(root).filter(name=>fs.statSync(path.join(root,name)).isFile()&&!['sw.js','build.json','.nojekyll','CNAME'].includes(name));files.push('downloads/RRB-IT-Practice-Lite.apk');
fs.writeFileSync(path.join(root,'sw.js'),oldFile('web/sw.template.js').toString().replace('__BUILD_HASH__','legacy-update-fixture').replace('__PRECACHE__',JSON.stringify(files)));
const server=http.createServer((req,res)=>{const pathname=new URL(req.url,'http://localhost').pathname;if(!pathname.startsWith(scope)){res.writeHead(404).end();return;}const file=path.resolve(root,pathname.slice(scope.length)||'index.html');if(!file.startsWith(root+path.sep)||!fs.existsSync(file)||!fs.statSync(file).isFile()){res.writeHead(404).end();return;}res.writeHead(200,{'Content-Type':types[path.extname(file)]||'application/octet-stream','Cache-Control':path.basename(file)==='sw.js'?'no-store':'public, max-age=86400'});fs.createReadStream(file).pipe(res);});
(async()=>{
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 const browser=await chromium.launch({headless:true,executablePath:process.env.CHROME_PATH,args:['--no-sandbox']});
 try{
  const context=await browser.newContext(),page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
  const url='http://127.0.0.1:'+server.address().port+scope;
  await page.goto(url);await page.waitForSelector('.subjects');
  assert.equal(await page.evaluate(()=>bank.questions.length),1150);
  await page.evaluate(async()=>{await navigator.serviceWorker.ready;if(!navigator.serviceWorker.controller)await new Promise(resolve=>navigator.serviceWorker.addEventListener('controllerchange',resolve,{once:true}));});
  const snapshot=await page.evaluate(async()=>{
   const q=bank.questions[0];state.progress[q.id]={attempts:1,correct:1,last:'correct',lastAt:Date.now()};state.bookmarks[q.id]=true;
   state.active={id:'legacy-attempt',questions:[q],startedAt:Date.now(),deadline:Date.now()+600000,mode:'test',penalty:.25,index:0,answers:{0:q.answer},flags:{0:true},revealed:{}};
   await AppStore.save(JSON.stringify(state));
   const other='rrb-practice:'+new URL('../another-practice/',location.href).href+':legacy';
   await(await caches.open(other)).put(new URL('../another-practice/scope.json',location.href),new Response('{}'));
   return {question:q,other};
  });
  revision('migration');
  // Merely loading the old cached client must discover and activate the new release.
  await page.reload();
  await page.waitForFunction(()=>document.body.dataset.releaseProbe==='migration'&&typeof bank!=='undefined'&&bank&&bank.questions.length===1034);
  assert.equal(await page.title(),'Bank SO IT');assert.equal(await page.locator('.brand').innerText(),'Bank SO IT');
  assert.equal(await page.evaluate(()=>state.active.id),'legacy-attempt');
  assert.deepEqual(await page.evaluate(()=>state.active.questions[0]),snapshot.question);
  assert.equal(await page.evaluate(()=>state.active.answers[0]),snapshot.question.answer);
  assert.equal(await page.evaluate(()=>Object.keys(state.bookmarks).length),1);
  assert.equal(await page.evaluate(()=>Object.keys(state.progress).length),1);
  const cacheKeys=await page.evaluate(()=>caches.keys());assert(cacheKeys.includes(snapshot.other));assert(!cacheKeys.some(key=>key.includes(scope)&&key.startsWith('rrb-practice:')));
  assert.equal(await page.locator('[data-action="update-web"]').count(),0);
  // Activating a release does not restart the current page or apply on navigation.
  await page.locator('[data-action="resume"]').click();
  const answer=(snapshot.question.answer+1)%5;
  await page.locator('[data-action="answer"][data-index="'+answer+'"]').click();
  revision('during-test');
  await page.evaluate(async()=>{await(await navigator.serviceWorker.getRegistration()).update();});
  await page.waitForFunction(async()=>{const r=await navigator.serviceWorker.getRegistration();return r.active&&r.active.state==='activated'&&!r.installing&&(await caches.keys()).some(key=>key.endsWith('test-during-test'));});
  assert.equal(await page.evaluate(()=>document.body.dataset.releaseProbe),'migration');
  assert.equal(await page.evaluate(()=>screen),'quiz');
  assert.equal(await page.evaluate(()=>state.active.answers[0]),answer);
  await page.locator('[data-action="save-exit"]').click();
  assert.equal(await page.evaluate(()=>document.body.dataset.releaseProbe),'migration');
  await page.locator('[data-action="resume"]').click();
  // Reload directly from a test; no finish/exit action is needed to get the release.
  await page.reload();
  await page.waitForFunction(()=>document.body.dataset.releaseProbe==='during-test'&&typeof state!=='undefined'&&state&&state.active);
  assert.equal(await page.evaluate(()=>state.active.answers[0]),answer);
  await page.locator('#nav [data-screen="library"]').click();await page.locator('[data-action="add-question"]').click();
  await page.locator('#editStem').fill('Unsaved question retained until user reloads');
  revision('during-edit');await page.evaluate(async()=>{await(await navigator.serviceWorker.getRegistration()).update();});
  await page.waitForFunction(async()=>{const r=await navigator.serviceWorker.getRegistration();return r.active&&r.active.state==='activated'&&!r.installing&&(await caches.keys()).some(key=>key.endsWith('test-during-edit'));});
  assert.equal(await page.locator('#editStem').inputValue(),'Unsaved question retained until user reloads');
  assert.equal(await page.evaluate(()=>document.body.dataset.releaseProbe),'during-test');
  // Reload directly from the editor, with no screen-specific waiting policy.
  await page.reload();
  await page.waitForFunction(()=>document.body.dataset.releaseProbe==='during-edit'&&typeof state!=='undefined'&&state&&state.active);
  // A single reload must also discover a release not already prepared in background.
  revision('on-reload');await page.reload();
  await page.waitForFunction(()=>document.body.dataset.releaseProbe==='on-reload'&&typeof state!=='undefined'&&state&&state.active);
  assert.equal(await page.evaluate(()=>state.active.answers[0]),answer);
  await context.setOffline(true);await page.reload();await page.waitForSelector('.subjects');
  assert.equal(await page.evaluate(()=>document.body.dataset.releaseProbe),'on-reload');assert.equal(await page.evaluate(()=>state.active.answers[0]),answer);
  assert.deepEqual(errors,[]);
  console.log('PASS: real legacy-client migration, updates on user reload, saved progress and question snapshots, no forced restart or navigation-triggered reload, offline latest release and cache isolation.');
 }finally{await browser.close();server.close();fs.rmSync(root,{recursive:true,force:true});}
})().catch(error=>{console.error(error);server.close();fs.rmSync(root,{recursive:true,force:true});process.exitCode=1;});
