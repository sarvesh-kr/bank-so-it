(function(root){
'use strict';
const C=typeof module!=='undefined'?require('./core.js'):root.QuizCore;
const record=(v,label)=>{if(!v||typeof v!=='object'||Array.isArray(v))throw Error(label+' must be an object.');return v;};
const safeID=v=>typeof v==='string'&&v.length<=100&&/^[a-zA-Z0-9_-]+$/.test(v)&&!(v in Object.prototype)&&v!=='prototype';
const number=(v,label,min=0)=>{if(!Number.isFinite(v)||v<min)throw Error('Invalid '+label);return v;};
const integer=(v,label,min=0)=>{number(v,label,min);if(!Number.isInteger(v))throw Error('Invalid '+label);return v;};
function validate(input){
 record(input,'Backup');if(!['bank-so-it-backup','rrb-it-practice-backup'].includes(input.format)||input.schemaVersion!==1)throw Error('Unsupported progress backup.');
 const catalog=C.validatePack({schemaVersion:1,subjects:input.subjects,questions:[]}).subjects;
 const s=record(input.state,'Backup state'),custom=C.validatePack(s.custom);
 const progress={},bookmarks={};
 const entries=Object.entries(record(s.progress,'Progress'));if(entries.length>20000)throw Error('Too many progress entries.');
 for(const [id,p] of entries){if(!safeID(id))throw Error('Invalid progress ID');record(p,'Progress entry');integer(p.attempts,'attempt count',1);integer(p.correct,'correct count');if(p.correct>p.attempts||!['correct','wrong'].includes(p.last))throw Error('Invalid progress entry');progress[id]={attempts:p.attempts,correct:p.correct,last:p.last,lastAt:number(p.lastAt,'attempt time')};}
 const marks=Object.entries(record(s.bookmarks,'Bookmarks'));if(marks.length>20000)throw Error('Too many bookmarks.');for(const [id,v] of marks){if(!safeID(id)||typeof v!=='boolean')throw Error('Invalid bookmark');if(v)bookmarks[id]=true;}
 function session(value,complete){
  record(value,'Session');if(!safeID(value.id))throw Error('Invalid session ID');
  const questions=C.validatePack({schemaVersion:1,subjects:catalog,questions:value.questions}).questions;if(!questions.length)throw Error('Empty session');
  if(!['test','practice'].includes(value.mode)||![0,.25].includes(value.penalty))throw Error('Invalid session settings');
  const index=integer(value.index,'question index');if(index>=questions.length)throw Error('Question index outside session');
  const answers={},flags={},revealed={};
  for(const [key,target,kind] of [['answers',answers,'answer'],['flags',flags,'flag'],['revealed',revealed,'flag']]){
   for(const [i,v] of Object.entries(record(value[key],key))){if(!/^(0|[1-9][0-9]*)$/.test(i)||Number(i)>=questions.length)throw Error('Invalid question reference');if(kind==='answer'){if(!Number.isInteger(v)||v<0||v>4)throw Error('Invalid answer');}else if(typeof v!=='boolean')throw Error('Invalid question flag');target[i]=v;}
  }
  const startedAt=number(value.startedAt,'start time');const deadline=value.deadline==null?null:number(value.deadline,'deadline',startedAt);
  const out={id:value.id,questions,mode:value.mode,penalty:value.penalty,index,answers,flags,revealed,startedAt,deadline};
  if(complete){out.finishedAt=number(value.finishedAt,'finish time',startedAt);out.expired=!!value.expired;out.result=C.score(out);}
  return out;
 }
 if(!Array.isArray(s.history)||s.history.length>5)throw Error('A backup may contain at most five full reviews.');
 const history=s.history.map(x=>session(x,true)),active=s.active==null?null:session(s.active,false);
 return {custom,progress,bookmarks,history,active,totalSessions:integer(s.totalSessions,'session count')};
}
const api={validate};if(typeof module!=='undefined')module.exports=api;else root.PracticeBackup=api;
})(typeof window!=='undefined'?window:globalThis);
