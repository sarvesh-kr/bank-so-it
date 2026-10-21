'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs');
const C=require('../app/src/main/assets/core.js');
const bank=JSON.parse(fs.readFileSync(__dirname+'/../app/src/main/assets/bank.json','utf8'));
const state={progress:{},bookmarks:{}};
test('Reviewed bank keeps references, excludes retired IDs and preserves legacy pack compatibility',()=>{
 const validated=C.validatePack(bank),ids=new Set(validated.questions.map(q=>q.id));
 assert.equal(validated.questions.length,1037);assert.equal(validated.subjects.length,11);
 assert.equal(validated.retiredQuestionIds.length,1105);
 assert(validated.retiredQuestionIds.every(id=>!ids.has(id)));
 assert(validated.questions.every(q=>q.references.length>0));
 const old={schemaVersion:1,subjects:[bank.subjects[0]],questions:[{...bank.questions[0]}]};delete old.questions[0].references;
 assert.deepEqual(C.validatePack(old).questions[0].references,[]);
});
test('Legacy imports cannot restore retired items or overwrite reviewed built-ins; explicit personal edits work',()=>{
 const q=bank.questions[0],retired={...q,id:bank.retiredQuestionIds[0]},stale={...q,question:'Stale stock wording'};
 const merged=C.mergePack(bank,{subjects:bank.subjects,questions:[stale,retired],retiredQuestionIds:[q.id]});
 assert.equal(merged.questions.length,1037);assert.equal(merged.questions[0].question,q.question);
 assert(!merged.questions.some(x=>x.id===retired.id));
 assert.equal(C.mergePack(bank,{questions:[{...stale,kind:'custom'}]}).questions[0].question,stale.question);
});
test('Reference imports reject executable URLs and preserve valid source links',()=>{
 const pack={schemaVersion:1,subjects:[bank.subjects[0]],questions:[{...bank.questions[0]}]};
 assert(C.validatePack(pack).questions[0].references[0].url.startsWith('https://'));
 for(const url of ['javascript:alert(1)','data:text/html,test','https://user:password@example.com']){
  const copy=JSON.parse(JSON.stringify(pack));copy.questions[0].references=[{title:'Source',url}];assert.throws(()=>C.validatePack(copy));
 }
});
test('Bank has reviewed coverage counts and structurally valid answer keys',()=>{const b=C.validatePack(bank);assert.equal(b.questions.length,1037);assert.equal(new Set(b.questions.map(q=>q.question)).size,1037);for(const [s,n] of Object.entries({network:231,dbms:200,os:100,dsa:150,linux:75,dw_dm:50,cloud_ai_ml:50,se_bank_it:68,programming:60,architecture:33,web:20}))assert.equal(b.questions.filter(q=>q.subject===s).length,n);});
test('Sampling covers every subject, avoids duplicates, preserves shuffled correct text',()=>{const original=new Map(bank.questions.map(q=>[q.id,q]));for(const n of [1,20,40,50,1037]){const picked=C.sample(bank.questions,n);assert.equal(picked.length,n);assert.equal(new Set(picked.map(q=>q.id)).size,n);for(const q of picked)assert.equal(q.options[q.answer],original.get(q.id).options[original.get(q.id).answer]);if(n>=20)assert.equal(new Set(picked.map(q=>q.subject)).size,11);}const picked=C.sample(bank.questions,40);for(const s of bank.subjects)assert([3,4].includes(picked.filter(q=>q.subject===s.id).length));});
test('Sampling invalid counts fails promptly',()=>{for(const n of [0,-1,1.5,1038,NaN])assert.throws(()=>C.sample(bank.questions,n));});
test('Scoring includes option A, negative marks and blanks correctly',()=>{const q=C.sample(bank.questions,4),session={questions:q,answers:{0:q[0].answer,1:(q[1].answer+1)%5,2:q[2].answer},penalty:.25};const r=C.score(session);assert.equal(r.correct,2);assert.equal(r.wrong,1);assert.equal(r.unanswered,1);assert.equal(r.marks,1.75);assert.equal(r.accuracy,67);session.penalty=0;assert.equal(C.score(session).marks,2);assert.equal(C.score({questions:q,answers:{0:(q[0].answer+1)%5},penalty:.25}).marks,-.25);assert.equal(C.score({questions:q,answers:{},penalty:.25}).accuracy,0);});
test('Filters honor subject, topic, level, unseen, latest wrong and bookmarks',()=>{const q=bank.questions[0];const s={progress:{[q.id]:{last:'wrong'}},bookmarks:{[q.id]:true}};const cfg={subjects:[q.subject],topic:q.topic,difficulty:q.difficulty,pool:'wrong'};assert.deepEqual(C.eligible(bank,cfg,s).map(q=>q.id),[q.id]);cfg.pool='bookmarked';assert.deepEqual(C.eligible(bank,cfg,s).map(q=>q.id),[q.id]);cfg.pool='unseen';assert(!C.eligible(bank,cfg,s).some(x=>x.id===q.id));});
test('Imports reject malformed or ambiguous answer keys and duplicate IDs',()=>{const p={schemaVersion:1,subjects:[bank.subjects[0]],questions:[{...bank.questions[0],options:[...bank.questions[0].options]}]};C.validatePack(p);for(const mutate of [p=>p.schemaVersion=2,p=>p.questions[0].answer=5,p=>p.questions[0].answer='0',p=>p.questions[0].options[1]=p.questions[0].options[0],p=>p.questions.push(p.questions[0]),p=>p.questions[0].subject='missing',p=>p.questions[0].explanation='',p=>p.questions[0].id='__proto__']){const copy=JSON.parse(JSON.stringify(p));mutate(copy);assert.throws(()=>C.validatePack(copy));}});
test('Import updates by ID and retains unrelated questions',()=>{const q={...bank.questions[0],question:'A revised question?',kind:'custom'};const merged=C.mergePack(bank,{subjects:[{...bank.subjects[0],name:'Renamed'}],questions:[q]});assert.equal(merged.questions.length,1037);assert.equal(merged.questions[0].question,q.question);assert.equal(merged.subjects[0].name,'Renamed');assert.equal(merged.questions[1].question,bank.questions[1].question);assert.notEqual(bank.questions[0].question,q.question);});

test('Coverage includes the previously missing degree-level areas',()=>{
 const requirements={programming:['OOP','C basics','C++ basics','Java basics','Python basics','Python output'],architecture:['CPU organisation','Digital logic','Memory hierarchy','I/O organisation'],web:['HTML','CSS','HTTP','Browser security','Data formats'],dbms:['Normalization & dependencies','Transactions & recovery','SQL clauses & query logic','SQL output & command practice','ER modelling & Chen notation','Relational algebra','Indexes & B/B+ trees','Backup & RAID'],network:['Subnetting','TLS, cryptography & encoding','Common attacks'],os:['CPU scheduling','Memory allocation & addressing','Deadlocks','Processes & states','OS roles & architecture','Synchronization','Virtual memory & replacement','Files, storage & I/O','Threads & IPC']};
 for(const [subject,topics] of Object.entries(requirements))for(const topic of topics)assert(bank.questions.some(q=>q.subject===subject&&q.topic===topic),subject+': '+topic);
});

test('Network covers requested protocols, API and blockchain basics with ten subnet calculations',()=>{
 const qs=bank.questions.filter(q=>q.subject==='network');
 assert.equal(qs.length,231);assert(qs.every(q=>q.id.startsWith('network-r2-')));
 const drills=qs.filter(q=>q.kind==='worked-drill');assert.equal(drills.length,10);assert(drills.every(q=>q.topic==='Subnetting'));
 for(const topic of ['OSI & TCP/IP models','Network devices & media','Frames, packets & headers','IP addressing & NAT','Services & ports','Malware & virus types','CIA & general security'])assert(qs.some(q=>q.topic===topic));
 for(let n=1;n<=257;n++)assert(bank.retiredQuestionIds.includes('network-'+String(n).padStart(3,'0')));
});

test('DBMS revision has 200 fresh IDs and separates executable exercises from concise concepts',()=>{
 const qs=bank.questions.filter(q=>q.subject==='dbms');
 assert.equal(qs.length,200);assert(qs.every(q=>/^dbms-r2-\d{3}$/.test(q.id)));
 for(const [kind,count] of Object.entries({'checked-sql':32,'checked-algebra':6,'worked-dbms':10,concept:152}))assert.equal(qs.filter(q=>q.kind===kind).length,count);
 for(let n=1;n<=257;n++)assert(bank.retiredQuestionIds.includes('dbms-'+String(n).padStart(3,'0')));
 const all={subjects:['dbms'],topic:'',difficulty:'',pool:'all'};
 assert.equal(C.eligible(bank,all,state).length,200);
 for(const [topic,count] of Object.entries({'Normalization & dependencies':16,'Relational algebra':14,'SQL output & command practice':32,'Backup & RAID':12}))assert.equal(C.eligible(bank,{...all,topic},state).length,count);
});

test('OS revision has 100 fresh questions, ten short worked cases and the requested subtopics',()=>{
 const qs=bank.questions.filter(q=>q.subject==='os');assert.equal(qs.length,100);
 assert(qs.every(q=>/^os-r2-\d{3}$/.test(q.id)));assert.equal(qs.filter(q=>q.kind==='worked-os').length,10);
 assert.equal(qs.filter(q=>q.kind==='concept').length,90);
 for(let n=1;n<=103;n++)assert(bank.retiredQuestionIds.includes('os-'+String(n).padStart(3,'0')));
 const all={subjects:['os'],topic:'',difficulty:'',pool:'all'};assert.equal(C.eligible(bank,all,state).length,100);
 for(const [topic,count] of Object.entries({'Processes & states':14,'CPU scheduling':14,'Deadlocks':12,'Virtual memory & replacement':10}))assert.equal(C.eligible(bank,{...all,topic},state).length,count);
});

test('DSA revision has 150 fresh questions, 25 short worked cases and core structure coverage',()=>{
 const qs=bank.questions.filter(q=>q.subject==='dsa');assert.equal(qs.length,150);
 assert(qs.every(q=>/^dsa-r2-\d{3}$/.test(q.id)));assert.equal(qs.filter(q=>q.kind==='worked-dsa').length,25);
 assert.equal(qs.filter(q=>q.kind==='concept').length,125);
 for(let n=1;n<=250;n++)assert(bank.retiredQuestionIds.includes('dsa-'+String(n).padStart(3,'0')));
 const all={subjects:['dsa'],topic:'',difficulty:'',pool:'all'};assert.equal(C.eligible(bank,all,state).length,150);
 for(const [topic,count] of Object.entries({'Sorting':26,'Searching':12,'Arrays & strings':12,'Linked lists':12,'Stacks':10,'Queues':10,'Binary trees & traversals':14,'Binary search trees':12,'Heaps & priority queues':10,'Hashing':8,'Graphs & algorithm approaches':12,'Complexity & algorithm basics':12}))assert.equal(C.eligible(bank,{...all,topic},state).length,count);
});

test('Linux revision has 75 fresh questions and 17 executed command, permission and Bash examples',()=>{
 const qs=bank.questions.filter(q=>q.subject==='linux');assert.equal(qs.length,75);
 assert(qs.every(q=>/^linux-r2-\d{3}$/.test(q.id)));assert.equal(qs.filter(q=>q.kind==='checked-linux').length,17);
 assert.equal(qs.filter(q=>q.kind==='concept').length,58);
 for(let n=1;n<=100;n++)assert(bank.retiredQuestionIds.includes('linux-'+String(n).padStart(3,'0')));
 const all={subjects:['linux'],topic:'',difficulty:'',pool:'all'};assert.equal(C.eligible(bank,all,state).length,75);
 for(const [topic,count] of Object.entries({'Linux foundations & navigation':10,'Files, text & search':16,'Users, groups & permissions':14,'Processes, storage & services':10,'Shell operators & expansion':10,'Bash programming basics':15}))assert.equal(C.eligible(bank,{...all,topic},state).length,count);
});
