import { parseArgs } from 'node:util';
import { createRequire } from 'node:module';
import { createInterface } from 'node:readline/promises';
import { stdin, stdout } from 'node:process';
import { readFile, readdir, realpath, rm, stat } from 'node:fs/promises';
import { join, relative, isAbsolute } from 'node:path';
import { chromium } from 'playwright';
import { startRecording } from './recorder.js';
import type { Policy } from './privacy.js';
async function main(){
 const command=process.argv[2];
 const {values}=parseArgs({args:process.argv.slice(3),options:{workspace:{type:'string'},app:{type:'string'},url:{type:'string'},privacy:{type:'string'},resume:{type:'string'},'persist-session':{type:'boolean'},'private-selector':{type:'string',multiple:true},headless:{type:'boolean'},recordings:{type:'string'},confirm:{type:'boolean'},help:{type:'boolean'}}});
 if(values.help||!command){console.log('Commands: doctor | record --workspace PATH --app SLUG --url URL [--privacy mask|plaintext] [--persist-session] [--resume REC-ID] [--private-selector CSS] | cleanup --workspace PATH --app SLUG --recordings REC-ID,REC-ID [--confirm]');return;}
 if(command==='doctor'){
  let browser_present=false;try{await stat(chromium.executablePath());browser_present=true;}catch{}
  console.log(JSON.stringify({node:process.version,playwright:(JSON.parse(await readFile(createRequire(import.meta.url).resolve('playwright/package.json'),'utf8'))).version,chromium_executable:chromium.executablePath(),browser_present,headful_display:process.platform!=='linux'||!!process.env.DISPLAY||!!process.env.WAYLAND_DISPLAY,mcp:'Inspect client tools separately; this command does not install or configure MCP.'},null,2));return;
 }
 if(!values.workspace||!values.app||!/^[a-z0-9][a-z0-9-]{0,63}$/.test(values.app))throw Error('Provide --workspace and a valid --app slug.');
 if(command==='cleanup'){
  const ws=await realpath(values.workspace);const root=await realpath(join(ws,'qa',values.app,'recordings'));const rel=relative(ws,root);if(rel.startsWith('..')||isAbsolute(rel))throw Error('Output escapes workspace.');
  const ids=values.recordings?.split(',').map(x=>x.trim()).filter(Boolean)||[];if(!ids.length)throw Error('Select exact --recordings IDs; wildcards are not supported.');
  const paths:string[]=[];
  for(const id of ids){if(!/^REC-[a-zA-Z0-9-]+$/.test(id))throw Error('Invalid recording ID.');const path=await realpath(join(root,id));if(relative(root,path).startsWith('..'))throw Error('Unsafe recording path.');const meta=JSON.parse(await readFile(join(path,'session.json'),'utf8'));if(meta.application_id!==values.app || meta.recording_id!==id)throw Error('Application/recording identity mismatch.');
    if(!meta.ended_at){
      if(!Number.isSafeInteger(meta.process_id)||meta.process_id<=0)throw Error('Recording completion/active status is unknown; inspect before cleanup.');
      let active=true;try{process.kill(meta.process_id,0);}catch(e){active=(e as NodeJS.ErrnoException).code!=='ESRCH';}
      if(active)throw Error('Cannot delete an active recording.');
    }paths.push(path);}
  for(const id of await readdir(root)){if(ids.includes(id)||!id.startsWith('REC-'))continue;try{const meta=JSON.parse(await readFile(join(root,id,'session.json'),'utf8'));if(ids.includes(meta.profile_owner_recording))throw Error(`Recording ${id} references a selected profile; include it in cleanup or retain the profile owner.`);}catch(e){if(String(e).includes('references a selected profile'))throw e;}}
  console.log(JSON.stringify({preview:paths,delete_requested:!!values.confirm,knowledge_and_runs_preserved:true},null,2));
  if(values.confirm)for(const path of paths)await rm(path,{recursive:true});return;
 }
 if(command!=='record')throw Error('Unknown command.');if(!values.url)throw Error('Provide --url.');
 let policy=values.privacy;
 if(!policy){if(!stdin.isTTY)throw Error('Non-interactive use requires explicit --privacy mask|plaintext.');const rl=createInterface({input:stdin,output:stdout});try{policy=(await rl.question('Evidence policy for this session: mask or plaintext? Plaintext retains credentials and API/file contents: ')).trim();}finally{rl.close();}}
 if(policy!=='mask'&&policy!=='plaintext')throw Error('Choose mask or plaintext.');
 const session=await startRecording({workspace:values.workspace,application:values.app,url:values.url,policy:policy as Policy,persist:!!values['persist-session'],resume:values.resume,privateSelectors:values['private-selector'],headless:!!values.headless});
 console.log(`Recording: ${session.directory}\nPerform your flow. Close every browser window to finish. Ctrl+C stops explicitly.`);
 const interrupt=()=>{void session.stop();};process.once('SIGINT',interrupt);process.once('SIGTERM',interrupt);
 const summary=await session.done;process.off('SIGINT',interrupt);process.off('SIGTERM',interrupt);
 console.log(JSON.stringify(summary,null,2));console.log('Next: present one flow review with suggested name, inferred steps, completion status and minor uncertainties; ask only essential follow-ups.');
}
main().catch(e=>{console.error(String(e));process.exitCode=1;});
