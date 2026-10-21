'use strict';
const {chromium,webkit}=require('playwright'),http=require('node:http'),fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),zlib=require('node:zlib'),assert=require('node:assert/strict');
const root=path.resolve(process.env.BANK_DOWNLOAD_SITE||path.join(__dirname,'../_site'));
const types={'.html':'text/html','.js':'application/javascript','.json':'application/json','.webmanifest':'application/manifest+json','.css':'text/css','.png':'image/png','.apk':'application/vnd.android.package-archive'};
let invalidAPK=false;
const server=http.createServer((req,res)=>{
 const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname),prefix=pathname.startsWith('/bank-so-it/')?'/bank-so-it/':'/';
 const file=path.resolve(root,pathname.slice(prefix.length)||'index.html');
 if(!file.startsWith(root+path.sep)||!fs.existsSync(file)||!fs.statSync(file).isFile()){res.writeHead(404,{'Content-Type':'text/plain'}).end('Not found');return;}
 if(invalidAPK&&file.endsWith('.apk')){res.writeHead(200,{'Content-Type':'text/html','Cache-Control':'no-store'}).end('<!doctype html><title>Incorrect download response</title>');return;}
 const headers={'Content-Type':types[path.extname(file)]||'application/octet-stream','Cache-Control':'no-cache'};
 if(['.html','.js','.json','.css'].includes(path.extname(file))){const raw=zlib.gzipSync(fs.readFileSync(file));res.writeHead(200,{...headers,'Content-Encoding':'gzip','Content-Length':raw.length}).end(raw);}
 else{res.writeHead(200,headers);fs.createReadStream(file).pipe(res);}
});
const digest=raw=>crypto.createHash('sha256').update(raw).digest('hex');
const files=[{file:'downloads/Bank-SO-IT.apk',name:'Bank-SO-IT.apk',key:'apk'},{file:'bank.json',name:'bank-so-it-question-bank.json',key:'bank'}].map(x=>({...x,hash:digest(fs.readFileSync(path.join(root,x.file)))}));
async function verifyDownload(download,item){assert.equal(await download.failure(),null);assert.equal(download.suggestedFilename(),item.name);assert.equal(digest(fs.readFileSync(await download.path())),item.hash,'Wrong downloaded bytes for '+item.file);}
(async()=>{
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));const origin='http://127.0.0.1:'+server.address().port;
 try{
  for(const engine of (process.env.BANK_DOWNLOAD_BROWSERS||'chromium,webkit').split(',')){
   assert(['chromium','webkit'].includes(engine));const browser=await({chromium,webkit}[engine]).launch({headless:true,...(engine==='chromium'?{executablePath:process.env.CHROME_PATH,args:['--no-sandbox']}:{})});
   try{
    for(const scope of ['/','/bank-so-it/']){
     console.log('Checking downloads',engine,scope);const context=await browser.newContext({acceptDownloads:true}),page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));page.setDefaultTimeout(30000);
     const library=async()=>{await page.goto(origin+scope);await page.waitForSelector('.subjects');await page.locator('#nav [data-screen="library"]').click();};
     try{
      await library();await page.evaluate(async()=>{await navigator.serviceWorker.ready;if(!navigator.serviceWorker.controller)await new Promise(resolve=>navigator.serviceWorker.addEventListener('controllerchange',resolve,{once:true}));});
      for(const offline of [false,true]){
       await context.setOffline(offline);
       for(const noAttribute of [false,true])for(const item of files){
        const link=page.locator('a[data-download="'+item.key+'"]');await link.evaluate((a,{item,noAttribute})=>{if(noAttribute)a.removeAttribute('download');else a.download=item.name;},{item,noAttribute});
        const [download]=await Promise.all([page.waitForEvent('download'),link.click()]);await verifyDownload(download,item);assert.equal(await page.evaluate(()=>screen),'library');
       }
       await library();
      }
      await context.setOffline(false);
      // Raw URL navigation bypasses the app click handler: the original worker
      // returned index.html here. APK navigation must download the real package.
      const apk=files[0],rawLink=page.locator('a.download-link').filter({hasText:'Download Android APK'});await rawLink.evaluate(a=>{a.removeAttribute('data-download');a.removeAttribute('download');a.href+='?document=1';});
      const [rawDownload]=await Promise.all([page.waitForEvent('download'),rawLink.click()]);await verifyDownload(rawDownload,apk);
      const pack=files[1],packLink=page.locator('a.download-link').filter({hasText:'Download latest question pack'});await packLink.evaluate(a=>{a.removeAttribute('data-download');a.removeAttribute('download');a.href+='?document=1';});
      if(engine==='webkit'){
       // WebKit can render a directly opened JSON document despite attachment;
       // the actual My bank download button above must still download a file.
       const waiting=page.waitForResponse(r=>r.url()===origin+scope+'bank.json?document=1'&&r.request().isNavigationRequest());await packLink.click();const response=await waiting;assert.match(response.headers()['content-type'],/application\/json/);assert.equal(digest(await response.body()),pack.hash);await library();
      }else{const [download]=await Promise.all([page.waitForEvent('download'),packLink.click()]);await verifyDownload(download,pack);await library();}
      const tab=await context.newPage();const css=await tab.goto(origin+scope+'style.css');assert.match(css.headers()['content-type'],/text\/css/);assert(!(await css.text()).startsWith('<!doctype'));const missing=await tab.goto(origin+scope+'downloads/missing.apk');assert.equal(missing.status(),404);assert.equal(await missing.text(),'Not found');await tab.close();
      // A bad 200/HTML response must show an error, never save a fake APK.
      await page.evaluate(async()=>{const href=new URL('downloads/Bank-SO-IT.apk',location.href).href;for(const name of await caches.keys())await(await caches.open(name)).delete(href);});
      invalidAPK=true;let unexpected=0;page.on('download',()=>unexpected++);await page.locator('a[data-download="apk"]').click();await page.waitForFunction(()=>document.querySelector('#toast').textContent.includes('APK could not be downloaded'));assert.equal(unexpected,0);invalidAPK=false;
      assert.deepEqual(errors,[]);console.log(`PASS: ${engine} ${scope}: eight actual file downloads online/offline with/without download attribute, raw APK/JSON navigation, compressed exact bytes/names, reload, static/missing files and HTML-as-APK rejection.`);
     }finally{invalidAPK=false;await context.close();}
    }
   }finally{await browser.close();}
  }
 }finally{server.close();}
})().catch(error=>{console.error(error);server.close();process.exitCode=1;});
