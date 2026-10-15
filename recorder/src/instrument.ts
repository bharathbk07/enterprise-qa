// Serialized by Playwright into every page/frame. Keep browser dependencies inside this function.
export function instrument() {
  const w = window as unknown as {__qaEmit:(x:unknown)=>Promise<void>;__qaBudget:()=>Promise<number>;__qaPolicy:'mask'|'plaintext';__qaSensitive?:string[]};
  const pending = new Map<Element,ReturnType<typeof setTimeout>>();
  const latest = new WeakMap<Element,string>();
  w.__qaSensitive=[];
  const target = (el:Element) => ({tag:el.tagName.toLowerCase(),id:el.id,role:el.getAttribute('role'),testId:el.getAttribute('data-testid'),name:el.getAttribute('name'),label:el.getAttribute('aria-label'),text:(el.textContent||'').trim().slice(0,120)});
  const emit = (kind:string, el:Element, extra:Record<string,unknown>={}) => {
    void w.__qaEmit({kind,target:target(el),frameUrl:location.href,at:new Date().toISOString(),...extra}).catch(()=>{});
  };
  const field = (el:Element) => {
    const timer=pending.get(el); if(timer) clearTimeout(timer); pending.delete(el);
    const v=el instanceof HTMLInputElement || el instanceof HTMLTextAreaElement || el instanceof HTMLSelectElement ? el.value : el.textContent||'';
    if(latest.get(el)===v) return; latest.set(el,v);
    if(v.length>=3 && !w.__qaSensitive!.includes(v)) w.__qaSensitive!.push(v);
    emit('field-entry',el,{value:v});
  };
  document.addEventListener('input',event=>{
    const el=event.composedPath()[0]; if(!(el instanceof Element))return;
    const old=pending.get(el); if(old)clearTimeout(old);
    pending.set(el,setTimeout(()=>field(el),700));
  },true);
  document.addEventListener('focusout',event=>{const el=event.composedPath()[0];if(el instanceof Element && pending.has(el))field(el);},true);
  document.addEventListener('change',event=>{
    const el=event.composedPath()[0];if(!(el instanceof Element))return;
    if(el instanceof HTMLInputElement && el.type==='file') {
      const files=Array.from(el.files||[]);
      emit('upload',el,{files:files.map(f=>({name:f.name,size:f.size,type:f.type}))});
      void (async()=>{for(const file of files){
        if(w.__qaPolicy==='mask') { emit('upload-resource',el,{name:file.name,size:file.size,captured:false,reason:'raw-file-omitted-in-masked-mode'});continue; }
        const remaining=await w.__qaBudget();
        if(file.size>remaining){emit('upload-resource',el,{name:file.name,size:file.size,captured:false,reason:'session-resource-budget-exceeded'});continue;}
        const data=await new Promise<string>((resolve,reject)=>{const r=new FileReader();r.onload=()=>resolve(String(r.result).split(',')[1]||'');r.onerror=()=>reject(r.error);r.readAsDataURL(file);});
        emit('upload-resource',el,{name:file.name,size:file.size,type:file.type,base64:data});
      }})().catch(()=>emit('upload-resource',el,{captured:false,reason:'file-read-failed'}));
    } else if(el instanceof HTMLInputElement && ['checkbox','radio'].includes(el.type)) emit('toggle',el,{checked:el.checked});
    else field(el);
  },true);
  document.addEventListener('click',event=>{const el=event.composedPath()[0];if(el instanceof Element){for(const f of [...pending.keys()])field(f);emit('click',el);}},true);
  document.addEventListener('submit',event=>{for(const f of [...pending.keys()])field(f);if(event.target instanceof Element)emit('submit',event.target);},true);
  document.addEventListener('keydown',event=>{if(['Enter','Escape','Tab','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(event.key) && event.target instanceof Element)emit('key',event.target,{key:event.key});},true);
  window.addEventListener('beforeunload',()=>{for(const f of [...pending.keys()])field(f);});
}
