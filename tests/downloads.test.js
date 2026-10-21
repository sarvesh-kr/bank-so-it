'use strict';
const {chromium,webkit}=require('playwright'),http=require('node:http'),fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),zlib=require('node:zlib'),assert=require('node:assert/strict');
const root=path.resolve(process.env.BANK_DOWNLOAD_SITE||path.join(__dirname,'../_site'));
const types={'.html':'text/html','.js':'application/javascript','.json':'application/json','.webmanifest':'application/manifest+json','.css':'text/css','.png':'image/png','.apk':'application/vnd.android.package-archive'};
const server=http.createServer((req,res)=>{
 const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname),prefix=pathname.startsWith('/bank-so-it/')?'/bank-so-it/':'/';
 const file=path.resolve(root,pathname.slice(prefix.length)||'index.html');
 if(!file.startsWith(root+path.sep)||!fs.existsSync(file)||!fs.statSync(file).isFile()){res.writeHead(404,{'Content-Type':'text/plain'}).end('Not found');return;}
 const headers={'Content-Type':types[path.extname(file)]||'application/octet-stream','Cache-Control':'no-cache'};
 // Production serves text with compression; download responses must preserve decoded bytes.
 if(['.html','.js','.json','.css'].includes(path.extname(file))){const raw=zlib.gzipSync(fs.readFileSync(file));res.writeHead(200,{...headers,'Content-Encoding':'gzip','Content-Length':raw.length}).end(raw);}
 else{res.writeHead(200,headers);fs.createReadStream(file).pipe(res);}
});
const digest=raw=>crypto.createHash('sha256').update(raw).digest('hex');
const files=[{file:'downloads/Bank-SO-IT.apk',name:'Bank-SO-IT.apk'},{file:'bank.json',name:'bank-so-it-question-bank.json'}].map(x=>({...x,hash:digest(fs.readFileSync(path.join(root,x.file)))}));
(async()=>{
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));const origin='http://127.0.0.1:'+server.address().port;
 try{
  for(const engine of (process.env.BANK_DOWNLOAD_BROWSERS||'chromium,webkit').split(',')){
   assert(['chromium','webkit'].includes(engine));
   const browser=await({chromium,webkit}[engine]).launch({headless:true,...(engine==='chromium'?{executablePath:process.env.CHROME_PATH,args:['--no-sandbox']}:{})});
   try{
    for(const scope of ['/','/bank-so-it/']){
     const context=await browser.newContext({acceptDownloads:true}),page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));page.setDefaultTimeout(30000);
     try{
      await page.goto(origin+scope);try{await page.waitForSelector('.subjects');}catch(error){console.error('Startup failure',engine,scope,await page.locator('body').innerText(),errors);throw error;}
      await page.evaluate(async()=>{await navigator.serviceWorker.ready;if(!navigator.serviceWorker.controller)await new Promise(resolve=>navigator.serviceWorker.addEventListener('controllerchange',resolve,{once:true}));});
      await page.locator('#nav [data-screen="library"]').click();
      for(const offline of [false,true]){
       await context.setOffline(offline);
       for(const navigation of [false,true])for(const item of files){
        // Exercise the actual My bank link, including browsers that navigate
        // rather than honoring the HTML download attribute.
        const link=page.locator('a.download-link').filter({hasText:item.file.endsWith('.apk')?'Download Android APK':'Download latest question pack'});
        await link.evaluate((a,{item,navigation})=>{a.href=item.file+(navigation?'?download=1':'');if(navigation)a.removeAttribute('download');else a.download=item.name;},{item,navigation});
        console.log('Download',engine,scope,offline,navigation,item.file);
        const waiting=page.waitForEvent('download');await link.click();let download;try{download=await waiting;}catch(error){console.error('Download state',engine,scope,offline,navigation,item.file,page.url(),await page.locator('body').innerText());fs.mkdirSync('test-results',{recursive:true});await page.screenshot({path:'test-results/download-failure.png'});throw error;}
        assert.equal(await download.failure(),null,engine+': download failed');
        const raw=fs.readFileSync(await download.path());assert.equal(download.suggestedFilename(),item.name);
        assert.equal(digest(raw),item.hash,`${engine} ${scope} offline=${offline} navigation=${navigation}: wrong downloaded bytes for ${item.file}`);
        if(item.file.endsWith('.apk'))assert.equal(raw.subarray(0,4).toString('hex'),'504b0304');else assert.equal(JSON.parse(raw).questions.length,JSON.parse(fs.readFileSync(path.join(root,'bank.json'))).questions.length);
        assert.equal(await page.locator('.subjects').count(),0);assert.equal(await page.evaluate(()=>screen),'library');
       }
       // Files opened as documents must also keep their real MIME, not the shell.
       const tab=await context.newPage();const response=await tab.goto(origin+scope+'style.css');assert.match(response.headers()['content-type'],/text\/css/);assert(!(await response.text()).startsWith('<!doctype'));await tab.close();
       const missing=await context.newPage();
       if(!offline){const response=await missing.goto(origin+scope+'downloads/missing.apk');assert.equal(response.status(),404);assert.equal(await response.text(),'Not found');}
       else{let failed=false;try{await missing.goto(origin+scope+'downloads/missing.apk');}catch(error){failed=true;}assert(failed,'Missing offline file must fail rather than return the app HTML');}
       await missing.close();
       await page.reload();await page.waitForSelector('.subjects');await page.locator('#nav [data-screen="library"]').click();
      }
      assert.deepEqual(errors,[]);console.log(`PASS: ${engine} ${scope}: APK/JSON link downloads and navigation downloads, exact bytes/names, online/offline, CSS navigation, real missing-file errors and app reload.`);
     }finally{await context.close();}
    }
   }finally{await browser.close();}
  }
 }finally{server.close();}
})().catch(error=>{console.error(error);server.close();process.exitCode=1;});
