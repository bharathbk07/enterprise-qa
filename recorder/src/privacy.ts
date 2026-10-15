export type Policy = 'mask' | 'plaintext';
export class Privacy {
  readonly values = new Set<string>();
  constructor(readonly policy: Policy) {}
  remember(value: string) { if (value.length >= 3) this.values.add(value); }
  text(value: string): string {
    if (this.policy === 'plaintext') return value;
    let result = value;
    for (const secret of [...this.values].sort((a,b) => b.length-a.length)) result = result.split(secret).join('[REDACTED]');
    return result.replace(/(bearer\s+)[\w.\-]+/gi, '$1[REDACTED]');
  }
  url(value: string): string {
    if (this.policy === 'plaintext') return value;
    try { const u = new URL(value); u.username = ''; u.password = '';
      for (const key of [...u.searchParams.keys()]) u.searchParams.set(key, '[REDACTED]');
      if (u.hash) u.hash = '[REDACTED]'; return this.text(u.toString());
    } catch { return '[INVALID URL]'; }
  }
  headers(value: Record<string,string>): Record<string,string> {
    if (this.policy === 'plaintext') return value;
    const safe = new Set(['content-type','content-length','accept','cache-control']);
    return Object.fromEntries(Object.entries(value).map(([k,v])=>[k,safe.has(k.toLowerCase()) ? this.text(v) : '[REDACTED]']));
  }
  body(buffer: Buffer, contentType: string): Buffer | undefined {
    if (this.policy === 'plaintext') return buffer;
    if (!contentType.includes('json')) return undefined;
    try {
      const scrub = (v: unknown): unknown => {
        if (Array.isArray(v)) return v.map(scrub);
        if (v !== null && typeof v === 'object') return Object.fromEntries(Object.entries(v).map(([k,x])=>[this.text(k),scrub(x)]));
        return v === null ? null : '[REDACTED]';
      };
      return Buffer.from(JSON.stringify(scrub(JSON.parse(buffer.toString('utf8')))));
    } catch { return undefined; }
  }
}
