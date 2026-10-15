import { realpath, mkdir } from 'node:fs/promises';
import { dirname, relative, isAbsolute } from 'node:path';
export function contained(root:string,path:string){const r=relative(root,path);return r!== '..'&&!r.startsWith('..'+(process.platform==='win32'?'\\':'/'))&&!isAbsolute(r);}
/** Validate nearest existing ancestor before creating directories through possible symlinks. */
export async function ensureOutputDirectory(workspace:string,path:string){
 const root=await realpath(workspace);let candidate=path;
 for(;;){try{const existing=await realpath(candidate);if(!contained(root,existing))throw Error('Output path escapes workspace.');break;}
 catch(e){if((e as NodeJS.ErrnoException).code!=='ENOENT')throw e;const parent=dirname(candidate);if(parent===candidate)throw e;candidate=parent;}}
 await mkdir(path,{recursive:true,mode:0o700});const result=await realpath(path);if(!contained(root,result))throw Error('Output path escapes workspace.');return result;
}
