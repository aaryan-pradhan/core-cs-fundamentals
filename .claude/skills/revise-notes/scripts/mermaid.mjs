// Usage: node check.mjs file.md [...]  -> parses every ```mermaid block, prints errors.
import { JSDOM } from 'jsdom';
import fs from 'node:fs';
const dom = new JSDOM('<!doctype html><html><body></body></html>');
globalThis.window = dom.window;
globalThis.document = dom.window.document;
Object.defineProperty(globalThis, 'navigator', { value: dom.window.navigator, configurable: true });
for (const k of Object.getOwnPropertyNames(dom.window)) { if (!(k in globalThis)) { try { globalThis[k] = dom.window[k]; } catch {} } }
const { default: mermaid } = await import('mermaid');
mermaid.initialize({ startOnLoad: false });
let bad = 0, total = 0;
for (const f of process.argv.slice(2)) {
  const md = fs.readFileSync(f, 'utf8');
  const re = /```mermaid\n([\s\S]*?)```/g;
  let m;
  while ((m = re.exec(md))) {
    total++;
    const line = md.slice(0, m.index).split('\n').length;
    try { await mermaid.parse(m[1]); }
    catch (e) { bad++; console.log(`${f}:${line}: ${String(e.message || e).split('\n').slice(0, 4).join(' | ')}`); }
  }
}
console.log(`${total - bad}/${total} diagrams OK`);
process.exit(bad ? 1 : 0);
