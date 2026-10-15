import { mkdir, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { createHash } from 'node:crypto';
export class ResourceBudget {
  used = 0;
  private sequence = 0;
  constructor(readonly directory: string, readonly limit = 25_000_000) {}
  get remaining() { return this.limit-this.used; }
  async save(bytes: Buffer, kind: string): Promise<Record<string,unknown>> {
    const size=bytes.length, hash=createHash('sha256').update(bytes).digest('hex');
    if (size > this.remaining) return {captured:false,size,sha256:hash,reason:'session-resource-budget-exceeded'};
    // Reserve synchronously before awaiting: simultaneous resources share one strict budget.
    this.used += size;
    const file=`resource-${++this.sequence}-${kind}.bin`;
    try { await mkdir(this.directory,{recursive:true,mode:0o700}); await writeFile(join(this.directory,file),bytes,{mode:0o600}); }
    catch(error) { this.used -= size; throw error; }
    return {captured:true,size,sha256:hash,path:`resources/${file}`};
  }
}
