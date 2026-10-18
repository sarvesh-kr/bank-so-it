/* Shared pure quiz logic: used in the APK and automated tests. */
(function(root){
'use strict';
function shuffle(items,random=Math.random){const a=items.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
function sample(pool,n,random=Math.random){
 if(!Number.isInteger(n)||n<1||n>pool.length)throw Error('Choose between 1 and '+pool.length+' questions.');
 // Round-robin subjects, then topic/family groups, so repeated drills cannot dominate short tests.
 const subjects=new Map();
 for(const q of shuffle(pool,random)){if(!subjects.has(q.subject))subjects.set(q.subject,new Map());const groups=subjects.get(q.subject);const f=q.family||q.topic;if(!groups.has(f))groups.set(f,[]);groups.get(f).push(q);}
 const buckets=shuffle([...subjects.values()].map(m=>shuffle([...m.values()],random)),random),out=[];
 let si=0;
 while(out.length<n){const groups=buckets[si%buckets.length];if(groups.length){const group=groups.shift();out.push(group.pop());if(group.length)groups.push(group);}si++;}
 return out.map(q=>{const order=shuffle(q.options.map((_,i)=>i),random);return {...q,options:order.map(i=>q.options[i]),answer:order.indexOf(q.answer)};});
}
function score(session){let correct=0,wrong=0,unanswered=0;const subjects={};session.questions.forEach((q,i)=>{const a=session.answers[i];const outcome=a==null?'unanswered':a===q.answer?'correct':'wrong';if(outcome==='correct')correct++;else if(outcome==='wrong')wrong++;else unanswered++;if(!subjects[q.subject])subjects[q.subject]={correct:0,wrong:0,unanswered:0};subjects[q.subject][outcome]++;});return {correct,wrong,unanswered,attempted:correct+wrong,total:session.questions.length,marks:correct-wrong*session.penalty,accuracy:correct+wrong?Math.round(correct*100/(correct+wrong)):0,subjects};}
const text=(v,n,max)=>{if(typeof v!=='string'||!v.trim()||v.length>max)throw Error(n+' must be nonempty text (maximum '+max+' characters).');return v.trim();};
function validatePack(input){
 if(!input||typeof input!=='object'||Array.isArray(input)||input.schemaVersion!==1)throw Error('Expected a question pack with schemaVersion: 1.');
 if(!Array.isArray(input.subjects)||!Array.isArray(input.questions))throw Error('The pack needs subjects and questions arrays.');
 if(input.subjects.length>100||input.questions.length>10000)throw Error('A pack supports up to 100 subjects and 10,000 questions.');
 const ids=new Set();const subjects=input.subjects.map(s=>{const id=text(s.id,'Subject ID',80);if(!/^[a-zA-Z0-9_-]+$/.test(id)||(id in Object.prototype || id==='prototype')||ids.has(id))throw Error('Subject IDs must be unique and use letters, digits, - or _.');ids.add(id);return {id,name:text(s.name,'Subject name',100)};});
 const qids=new Set();const questions=input.questions.map(q=>{if(!q||typeof q!=='object')throw Error('Invalid question.');const id=text(q.id,'Question ID',100);if(!/^[a-zA-Z0-9_-]+$/.test(id)||(id in Object.prototype || id==='prototype')||qids.has(id))throw Error('Question IDs must be unique and use letters, digits, - or _.');qids.add(id);if(!ids.has(q.subject))throw Error(id+': include its subject in this pack.');if(!Array.isArray(q.options)||q.options.length!==5)throw Error(id+': provide exactly five options.');const options=q.options.map(o=>text(o,'Option',3000));if(new Set(options).size!==5)throw Error(id+': options must be distinct.');if(!Number.isInteger(q.answer)||q.answer<0||q.answer>4)throw Error(id+': answer must be a zero-based index from 0 to 4.');if(!['Easy','Moderate','Hard'].includes(q.difficulty))throw Error(id+': difficulty must be Easy, Moderate or Hard.');return {id,subject:q.subject,topic:text(q.topic,'Topic',120),difficulty:q.difficulty,question:text(q.question,'Question',12000),options,answer:q.answer,explanation:text(q.explanation,'Explanation',12000),kind:typeof q.kind==='string'?q.kind.slice(0,80):'custom',family:typeof q.family==='string'?q.family.slice(0,120):q.topic};});
 return {schemaVersion:1,subjects,questions};
}
function mergePack(base,custom){const sm=new Map(base.subjects.map(s=>[s.id,s]));const qm=new Map(base.questions.map(q=>[q.id,q]));for(const s of custom.subjects||[])sm.set(s.id,s);for(const q of custom.questions||[])qm.set(q.id,q);return {schemaVersion:1,subjects:[...sm.values()],questions:[...qm.values()]};}
function eligible(bank,config,state){return bank.questions.filter(q=>config.subjects.includes(q.subject)&&(!config.topic||q.topic===config.topic)&&(!config.difficulty||q.difficulty===config.difficulty)&&(config.pool==='all'||config.pool==='unseen'&&!state.progress[q.id]||config.pool==='wrong'&&state.progress[q.id]?.last==='wrong'||config.pool==='bookmarked'&&state.bookmarks[q.id]));}
const api={shuffle,sample,score,validatePack,mergePack,eligible};if(typeof module!=='undefined')module.exports=api;else root.QuizCore=api;
})(typeof window!=='undefined'?window:globalThis);
