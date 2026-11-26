import fs from 'node:fs';
import path from 'node:path';
const root='source/cloud/staging-preview';
const file=path.join(root,'sw.js');
let sw=fs.readFileSync(file,'utf8');
sw=sw.replace('if(req.method!=="GET" || new URL(req.url).origin!==location.origin)return;', 'if(req.method!=="GET" || new URL(req.url).origin!==location.origin || !new URL(req.url).pathname.startsWith(new URL(self.registration.scope).pathname))return;');
sw=sw.replace('if(new URL(client.url).origin===new URL(url).origin){','if(client.url.startsWith(self.registration.scope)){');
fs.writeFileSync(file,sw);
const files=JSON.parse(sw.match(/const ASSETS=(\[.*?\]);/s)[1]);
for(const a of files)if(!fs.existsSync(path.join(root,a)))throw Error('Missing PWA asset '+a);
const manifest=JSON.parse(fs.readFileSync(path.join(root,'manifest.webmanifest'),'utf8'));
if(!manifest.name.includes('RHTFLOW')||!manifest.name.includes('TEST'))throw Error('Brand missing');
for(const icon of manifest.icons){const b=fs.readFileSync(path.join(root,icon.src));const [w,h]=icon.sizes.split('x').map(Number);if(b.readUInt32BE(16)!==w||b.readUInt32BE(20)!==h)throw Error('Icon dimensions '+icon.src);}
console.log('Verified '+files.length+' PWA resources; separate TEST scope');
