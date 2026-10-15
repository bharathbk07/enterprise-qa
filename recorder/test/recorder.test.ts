import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, readFile, readdir, rm, stat } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createServer } from 'node:http';
import { once } from 'node:events';
import { setTimeout as delay } from 'node:timers/promises';
import { ResourceBudget } from '../src/budget.js';
import { Privacy } from '../src/privacy.js';
import { startRecording } from '../src/recorder.js';

test('concurrent resource captures cannot exceed the aggregate limit',async()=>{
 const directory=await mkdtemp(join(tmpdir(),'qa-budget-'));try{
 const b=new ResourceBudget(directory,10);const results=await Promise.all([b.save(Buffer.alloc(6),'a'),b.save(Buffer.alloc(6),'b')]);
 assert.equal(b.used,6);assert.equal(results.filter(x=>x.captured).length,1);
 }finally{await rm(directory,{recursive:true});}
});
test('masking strips URL secrets, auth headers and nested payload values',()=>{
 const p=new Privacy('mask');p.remember('super-secret');
 assert.ok(!p.url('https://example.test/path?token=super-secret#access').includes('super-secret'));
 assert.equal(p.headers({authorization:'Bearer secret'})['authorization'],'[REDACTED]');
 const body=p.body(Buffer.from('{"nested":{"password":"super-secret","age":42}}'),'application/json')!.toString();
 assert.ok(!body.includes('super-secret'));assert.ok(!body.includes('42'));assert.equal(p.body(Buffer.from('secret'),'text/plain'),undefined);
});
async function fixture(){
 const server=createServer((req,res)=>{
  if(req.url?.startsWith('/api')){const data=JSON.stringify({token:'server-secret',ok:true});res.writeHead(200,{'content-type':'application/json','content-length':Buffer.byteLength(data)});res.end(data);return;}
  if(req.url==='/download'){res.writeHead(200,{'content-type':'text/plain','content-disposition':'attachment; filename="test.txt"'});res.end('download-example');return;}
  res.writeHead(200,{'content-type':'text/html'});res.end(`<html><body><label>Password <input id="password" type="password"></label><label>Name <input id="name"></label><input id="file" type="file"><button id="go" onclick="document.querySelector('#output').textContent=document.querySelector('#password').value;fetch('/api?token=secret');console.error('server-secret')">Submit</button><div id="output"></div><a id="popup" target="_blank" href="/child">Child</a><a id="download" href="/download">Download</a><iframe src="/frame"></iframe></body></html>`);
 });server.listen(0,'127.0.0.1');await once(server,'listening');const address=server.address();assert.ok(address&&typeof address!=='string');return {server,url:`http://127.0.0.1:${address.port}`};
}
async function events(dir:string){return (await readFile(join(dir,'events.jsonl'),'utf8')).trim().split('\n').map(x=>JSON.parse(x));}

test('real Chromium captures steps, API evidence, popup and frame actions, then finalizes on last page close',async()=>{
 const workspace=await mkdtemp(join(tmpdir(),'qa-browser-'));const {server,url}=await fixture();let session;
 try{
  session=await startRecording({workspace,application:'demo',url,policy:'mask',persist:false,headless:true});
  const page=session.context.pages()[0]!;await page.locator('#password').fill('typed-super-secret');await page.locator('#name').fill('Alice Example');await page.locator('#go').click();
  const childPromise=session.context.waitForEvent('page');await page.locator('#popup').click();const child=await childPromise;await child.waitForLoadState('domcontentloaded');
  const frame=page.frames().find(f=>f.url().endsWith('/frame'))!;await frame.locator('#name').fill('Frame User');await frame.locator('#go').click();
  await delay(1500);await child.close();assert.equal(session.context.pages().length,1);await page.close();
  const summary=await session.done;assert.equal(summary.stop_reason,'last-window-closed');assert.ok(Number(summary.steps)>5);assert.ok(Number(summary.pages)>=2);assert.ok(Number(summary.resource_bytes)<=25_000_000);
  const rows=await events(session.directory);assert.ok(rows.some(x=>x.kind==='field-entry'));assert.ok(rows.some(x=>x.type==='api'));assert.ok(rows.some(x=>x.type==='console-error'));assert.ok(rows.some(x=>x.frameUrl?.endsWith('/frame')));
  const text=JSON.stringify(rows);assert.ok(!text.includes('typed-super-secret'));assert.ok(!text.includes('Alice Example'));assert.ok(!text.includes('server-secret'));
  const screenshots=await readdir(join(session.directory,'screenshots'));assert.ok(screenshots.length>0);
  const resources=await readdir(join(session.directory,'resources'));for(const file of resources){const bytes=await readFile(join(session.directory,'resources',file));assert.ok(!bytes.toString().includes('server-secret'));}
  const clarify=JSON.parse(await readFile(join(session.directory,'clarification.json'),'utf8'));assert.equal(clarify.completion_answer,null);
 }finally{if(session)await session.context.close().catch(()=>{});server.close();await rm(workspace,{recursive:true});}
});

test('plaintext uploads/downloads share budget and opted-in profile resumes',async()=>{
 const workspace=await mkdtemp(join(tmpdir(),'qa-profile-'));const {server,url}=await fixture();let session,resumed;
 try{
  session=await startRecording({workspace,application:'demo',url,policy:'plaintext',persist:true,headless:true});const page=session.context.pages()[0]!;
  await page.evaluate(()=>localStorage.setItem('qa-fixture','retained'));
  await page.locator('#file').setInputFiles({name:'fixture.txt',mimeType:'text/plain',buffer:Buffer.from('upload-example')});
  await page.locator('#download').click();await delay(800);await session.stop();const summary=await session.done;
  assert.equal(summary.stop_reason,'explicit-stop');
  const rows=await events(session.directory);assert.ok(rows.some(x=>x.kind==='upload-resource'&&x.captured));assert.ok(rows.some(x=>x.type==='download'&&x.captured));assert.ok(Number(summary.resource_bytes)>0);
  const id=String(summary.recording_id);resumed=await startRecording({workspace,application:'demo',url,policy:'mask',persist:true,headless:true,resume:id});assert.equal(await resumed.context.pages()[0]!.evaluate(()=>localStorage.getItem('qa-fixture')),'retained');await resumed.stop();
  const resumedSummary=await resumed.done;assert.equal(resumedSummary.profile_owner_recording,id);
 }finally{if(session)await session.context.close().catch(()=>{});if(resumed)await resumed.context.close().catch(()=>{});server.close();await rm(workspace,{recursive:true});}
});

test('untrusted browser payload cannot override evidence fields or bypass masked file policy',async()=>{
 const {parseBrowserEvent}=await import('../src/events.js');
 const event=parseBrowserEvent({kind:'upload-resource',base64:Buffer.from('secret-file').toString('base64'),name:'customer.txt',size:11,type:'text/plain',screenshot:'evil',step_id:'fake',extra_secret:'secret'},'mask',25_000_000);
 assert.equal(event.captured,false);assert.equal(event.base64,undefined);assert.equal(event.step_id,undefined);assert.equal(event.screenshot,undefined);assert.equal(event.extra_secret,undefined);
 assert.throws(()=>parseBrowserEvent({kind:'unknown'},'mask',1));
 assert.equal(parseBrowserEvent({kind:'upload-resource',base64:'not base64'},'plaintext',1).captured,false);
});
test('output symlink escape is rejected before writing into the outside directory',async()=>{
 const {symlink}=await import('node:fs/promises');const {ensureOutputDirectory}=await import('../src/paths.js');
 const ws=await mkdtemp(join(tmpdir(),'qa-path-')),outside=await mkdtemp(join(tmpdir(),'qa-outside-'));
 try{await symlink(outside,join(ws,'qa'));await assert.rejects(ensureOutputDirectory(ws,join(ws,'qa/demo/recordings')));assert.deepEqual(await readdir(outside),[]);}
 finally{await rm(ws,{recursive:true});await rm(outside,{recursive:true});}
});
