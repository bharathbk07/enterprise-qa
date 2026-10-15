import type { Policy } from './privacy.js';
const kinds=new Set(['click','field-entry','upload','upload-resource','toggle','key','submit']);
const targets=['tag','id','role','testId','name','label','text'];
const object=(v:unknown):v is Record<string,unknown>=>v!==null&&typeof v==='object'&&!Array.isArray(v);
/** Page bindings are untrusted. Never spread arbitrary page-controlled fields into evidence. */
export function parseBrowserEvent(raw:unknown,policy:Policy,remaining:number):Record<string,unknown>{
 if(!object(raw)||typeof raw.kind!=='string'||!kinds.has(raw.kind))throw Error('Unsupported browser event.');
 const event:Record<string,unknown>={kind:raw.kind};
 for(const key of ['at','frameUrl'])if(typeof raw[key]==='string')event[key]=raw[key].slice(0,4096);
 if(object(raw.target))event.target=Object.fromEntries(targets.filter(k=>typeof (raw.target as Record<string,unknown>)[k]==='string').map(k=>[k,String((raw.target as Record<string,unknown>)[k]).slice(0,256)]));
 if(raw.kind==='field-entry'&&typeof raw.value==='string')event.value=raw.value.slice(0,65536);
 if(raw.kind==='key'&&typeof raw.key==='string'&&['Enter','Escape','Tab','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(raw.key))event.key=raw.key;
 if(raw.kind==='toggle'&&typeof raw.checked==='boolean')event.checked=raw.checked;
 const metadata=(v:Record<string,unknown>)=>({name:typeof v.name==='string'?v.name.slice(0,1024):'',size:typeof v.size==='number'&&Number.isSafeInteger(v.size)&&v.size>=0?v.size:null,type:typeof v.type==='string'?v.type.slice(0,128):''});
 if(raw.kind==='upload'&&Array.isArray(raw.files))event.files=raw.files.slice(0,100).filter(object).map(metadata);
 if(raw.kind==='upload-resource'){
  Object.assign(event,metadata(raw));
  if(policy==='mask')Object.assign(event,{captured:false,reason:'raw-file-omitted-in-masked-mode'});
  else if(typeof raw.base64==='string'){
   if(raw.base64.length>Math.ceil(remaining/3)*4||!/^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/.test(raw.base64))Object.assign(event,{captured:false,reason:'oversized-or-invalid-upload'});
   else event.base64=raw.base64;
  }else Object.assign(event,{captured:false,reason:'resource-not-supplied'});
 }
 return event;
}
