import { chromium, type BrowserContext, type Page } from 'playwright';
import { mkdir, writeFile, readFile, appendFile, realpath, stat } from 'node:fs/promises';
import { join, resolve, relative, isAbsolute } from 'node:path';
import { randomUUID } from 'node:crypto';
import { instrument } from './instrument.js';
import { parseBrowserEvent } from './events.js';
import { ensureOutputDirectory } from './paths.js';
import { Privacy, type Policy } from './privacy.js';
import { ResourceBudget } from './budget.js';
export interface Options {
  workspace: string; application: string; url: string; policy:Policy;
  persist:boolean; headless?:boolean; resume?:string; privateSelectors?:string[];
}
export interface Session {
  context:BrowserContext; directory:string; done:Promise<Record<string,unknown>>;
  stop:()=>Promise<void>;
}
const slug=(s:string)=>/^[a-z0-9][a-z0-9-]{0,63}$/.test(s);
export async function startRecording(options:Options):Promise<Session> {
  if(!slug(options.application))throw Error('Application ID must be a lowercase slug (1–64 characters).');
  if(!['mask','plaintext'].includes(options.policy))throw Error('Select mask or plaintext before recording.');
  const url=new URL(options.url);if(!['http:','https:'].includes(url.protocol))throw Error('Use an HTTP(S) start URL.');
  const workspace=await realpath(options.workspace);
  const root=join(workspace,'qa',options.application,'recordings');
  const realRoot=await ensureOutputDirectory(workspace,root);
  const id=`REC-${new Date().toISOString().replace(/[:.]/g,'-')}-${randomUUID().slice(0,8)}`;
  const directory=join(realRoot,id);await mkdir(directory,{mode:0o700});await mkdir(join(directory,'screenshots'),{mode:0o700});
  let profile=join(directory,'profile');
  if(options.resume){
    if(!options.persist)throw Error('Resuming a saved profile requires session-storage consent (--persist-session).');
    if(!/^REC-[a-zA-Z0-9-]+$/.test(options.resume))throw Error('Invalid recording ID.');
    const prior=JSON.parse(await readFile(join(realRoot,options.resume,'session.json'),'utf8'));
    if(prior.application_id!==options.application || prior.profile_retained!==true)throw Error('Prior recording has no retained profile for this application.');
    const owner=prior.profile_owner_recording || options.resume;
    if(!/^REC-[a-zA-Z0-9-]+$/.test(owner))throw Error('Invalid profile owner.');
    profile=await realpath(join(realRoot,owner,'profile'));
    if(relative(realRoot,profile).startsWith('..'))throw Error('Profile escapes application recordings.');
  }
  const privacy=new Privacy(options.policy),budget=new ResourceBudget(join(directory,'resources'));
  let context:BrowserContext;
  if(options.persist) context=await chromium.launchPersistentContext(profile,{headless:!!options.headless,acceptDownloads:true});
  else { const browser=await chromium.launch({headless:!!options.headless});context=await browser.newContext({acceptDownloads:true});context.on('close',()=>void browser.close()); }
  const pages=new Map<Page,string>();let pageSeq=0,step=0;let queue:Promise<void>=Promise.resolve();
  const inFlight=new Set<Promise<unknown>>();let finishing=false;let reason='last-window-closed';
  const errors:string[]=[];const lastUrls:Record<string,string>={};
  const schedule=(task:()=>Promise<void>)=>{queue=queue.then(task).catch(e=>{errors.push(privacy.policy==='mask'?'capture-task-failed':String(e));});return queue;};
  const track=(p:Promise<unknown>)=>{inFlight.add(p);void p.catch(e=>errors.push(privacy.policy==='mask'?'resource-task-failed':String(e))).finally(()=>inFlight.delete(p));};
  const log=async(record:Record<string,unknown>)=>{await appendFile(join(directory,'events.jsonl'),JSON.stringify(record)+'\n',{mode:0o600});};
  const screenshot=async(page:Page,n:number):Promise<Record<string,unknown>>=>{
    const path=`screenshots/step-${String(n).padStart(5,'0')}.png`;
    try {
      if(page.isClosed())return {screenshot:null,screenshot_error:'page-closed-before-capture'};
      if(options.policy==='mask'){
        // Collect current values in every accessible frame before masking reflected field values.
        for(const frame of page.frames()){
          try { const vals=await frame.evaluate(()=>Array.from(document.querySelectorAll('input,textarea,select,[contenteditable="true"]')).map(el=>'value' in el ? String((el as HTMLInputElement).value) : el.textContent||''));vals.forEach(v=>privacy.remember(v)); }catch{}
        }
      }
      const masks=options.policy==='mask'? page.frames().flatMap(frame=>[frame.locator('input,textarea,select,[contenteditable="true"],[data-private]'),...(options.privateSelectors||[]).map(s=>frame.locator(s)),...[...privacy.values].map(v=>frame.getByText(v,{exact:false}))]):[];
      await page.screenshot({path:join(directory,path),mask:masks,timeout:3000});return {screenshot:path};
    } catch {return {screenshot:null,screenshot_error:'capture-failed-or-navigation-race'};}
  };
  const action=(page:Page,payload:Record<string,unknown>)=>{
    const observedUrl=privacy.url(page.url()),observedPageId=pages.get(page);
    return schedule(async()=>{
    const n=++step;
    if(typeof payload.value==='string')privacy.remember(payload.value);
    if(typeof payload.base64==='string' && options.policy==='plaintext'){
      const bytes=Buffer.from(payload.base64,'base64');delete payload.base64;
      Object.assign(payload,await budget.save(bytes,'upload'));
    }
    const shot=await screenshot(page,n);
    if(options.policy==='mask'){
      if('value' in payload)payload.value='[REDACTED]';
      if(payload.target && typeof payload.target==='object'){
        // Labels and DOM identifiers can contain sensitive data: omit them in masked recordings.
        payload.target={tag:(payload.target as Record<string,unknown>).tag,role:(payload.target as Record<string,unknown>).role};
      }
      if(payload.files)payload.files=(payload.files as Record<string,unknown>[]).map(f=>({...f,name:'[REDACTED]'}));
      if(payload.name)payload.name='[REDACTED]';
      if(typeof payload.frameUrl==='string')payload.frameUrl=privacy.url(payload.frameUrl);
    }
    await log({type:'step',step_id:`STEP-${n}`,page_id:observedPageId,recorded_at:new Date().toISOString(),url:observedUrl,...payload,...shot});
    });
  };
  await context.exposeBinding('__qaEmit',({page},payload:unknown)=>action(page,parseBrowserEvent(payload,options.policy,budget.remaining)));
  await context.exposeBinding('__qaBudget',()=>budget.remaining);
  await context.addInitScript(({policy})=>{(window as unknown as {__qaPolicy:string}).__qaPolicy=policy;},{policy:options.policy});
  await context.addInitScript(instrument);
  let resolveDone!:(v:Record<string,unknown>)=>void;
  const done=new Promise<Record<string,unknown>>(r=>{resolveDone=r;});
  const metadata={schema_version:'1.0',recording_id:id,application_id:options.application,started_at:new Date().toISOString(),process_id:process.pid,privacy:options.policy,resource_limit_bytes:budget.limit,profile_retained:options.persist,resumed_from:options.resume||null,completion:'awaiting-user-clarification'};
  await writeFile(join(directory,'session.json'),JSON.stringify(metadata,null,2),{mode:0o600});
  const finish=async()=>{
    if(finishing)return;finishing=true;
    // Drain accepted resource handlers and the step writer before finalizing metadata.
    await Promise.allSettled([...inFlight]);await queue;
    const summary={...metadata,ended_at:new Date().toISOString(),stop_reason:reason,steps:step,pages:pageSeq,resource_bytes:budget.used,last_urls:lastUrls,errors,profile_owner_recording:options.persist ? relative(realRoot,profile).split(/[\\/]/)[0] : null};
    await writeFile(join(directory,'session.json'),JSON.stringify(summary,null,2),{mode:0o600});
    await writeFile(join(directory,'clarification.json'),JSON.stringify({completion_answer:null,step_cursor:0,questions:[],resume_choices:['saved-session-if-retained','fresh-session']},null,2),{mode:0o600});
    resolveDone(summary);
  };
  context.on('close',()=>void finish().catch(e=>{resolveDone({...metadata,error:String(e)});}));
  const attach=(page:Page)=>{
    if(pages.has(page))return;const pid=`PAGE-${++pageSeq}`;pages.set(page,pid);
    void action(page,{kind:'page-opened',at:new Date().toISOString()});
    page.on('framenavigated',frame=>{if(frame===page.mainFrame())lastUrls[pid]=privacy.url(frame.url());void action(page,{kind:'navigation',frameUrl:frame.url(),main_frame:frame===page.mainFrame(),at:new Date().toISOString()});});
    page.on('console',msg=>{if(msg.type()==='error')void schedule(()=>log({type:'console-error',page_id:pid,at:new Date().toISOString(),message:options.policy==='mask'?'[REDACTED console text]':msg.text()}));});
    page.on('pageerror',error=>void schedule(()=>log({type:'page-error',page_id:pid,at:new Date().toISOString(),message:options.policy==='mask'?'[REDACTED error text]':error.message})));
    page.on('dialog',dialog=>void schedule(()=>log({type:'dialog',page_id:pid,at:new Date().toISOString(),dialog_type:dialog.type(),message:options.policy==='mask'?'[REDACTED]':dialog.message()})));
    page.on('close',()=>{void schedule(()=>log({type:'page-closed',page_id:pid,at:new Date().toISOString()}));if(context.pages().length===0){if(reason!=='explicit-stop')reason='last-window-closed';void context.close();}});
    page.on('download',download=>track((async()=>{
      const record:Record<string,unknown>={type:'download',page_id:pid,at:new Date().toISOString(),url:privacy.url(download.url()),filename:options.policy==='mask'?'[REDACTED]':download.suggestedFilename()};
      if(options.policy==='mask'){Object.assign(record,{captured:false,reason:'raw-file-omitted-in-masked-mode'});}
      else { const stream=await download.createReadStream();let length=0;const chunks:Buffer[]=[];
        if(stream){for await(const chunk of stream){const b=Buffer.from(chunk);length+=b.length;if(length>budget.remaining){stream.destroy();break;}chunks.push(b);}}
        Object.assign(record,length>budget.remaining?{captured:false,size_at_least:length,reason:'session-resource-budget-exceeded'}:stream?await budget.save(Buffer.concat(chunks),'download'):{captured:false,reason:'download-stream-unavailable'});
      } await schedule(()=>log(record));
    })()));
  };
  context.on('page',attach);context.pages().forEach(attach);
  context.on('response',response=>{
    const request=response.request();if(!['fetch','xhr'].includes(request.resourceType()))return;
    track((async()=>{
      const record:Record<string,unknown>={type:'api',at:new Date().toISOString(),url:privacy.url(request.url()),method:request.method(),status:response.status(),resource_type:request.resourceType()};
      try {record.page_id=pages.get(request.frame().page());}catch{record.page_id=null;}
      record.request_headers=privacy.headers(await request.allHeaders());const headers=await response.allHeaders();record.response_headers=privacy.headers(headers);
      const post=request.postDataBuffer();if(post){const sanitized=privacy.body(post,request.headers()['content-type']||'');record.request_body=sanitized?await budget.save(sanitized,'request'):{captured:false,size:post.length,reason:'unstructured-body-omitted-in-masked-mode'};}
      const length=Number(headers['content-length']);
      if(!headers['content-length']||!Number.isFinite(length)||length<0)record.response_body={captured:false,reason:'unknown-body-size-no-bounded-read'};
      else if(length>budget.remaining)record.response_body={captured:false,size:length,reason:'session-resource-budget-exceeded'};
      else if(headers['content-encoding'] && headers['content-encoding']!=='identity')record.response_body={captured:false,reason:'compressed-size-does-not-bound-decoded-body'};
      else {try{await response.finished();const bytes=await response.body();const sanitized=privacy.body(bytes,headers['content-type']||'');record.response_body=sanitized?await budget.save(sanitized,'response'):{captured:false,size:bytes.length,reason:'unstructured-body-omitted-in-masked-mode'};}catch{record.response_body={captured:false,reason:'body-unavailable'};}}
      await schedule(()=>log(record));
    })());
  });
  context.on('requestfailed',request=>void schedule(()=>log({type:'request-failed',at:new Date().toISOString(),url:privacy.url(request.url()),method:request.method(),error:options.policy==='mask'?'[REDACTED]':request.failure()?.errorText})));
  const initial=context.pages()[0]||await context.newPage();
  try {await initial.goto(options.url,{waitUntil:'domcontentloaded',timeout:30000});}
  catch {await schedule(()=>log({type:'navigation-warning',message:'Initial navigation failed; continue manually or close browser.'}));}
  return {context,directory,done,stop:async()=>{reason='explicit-stop';await context.close();await done;}};
}
