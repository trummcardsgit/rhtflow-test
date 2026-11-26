import fs from 'node:fs';
import path from 'node:path';
const root='source/cloud/staging-preview';
const file=path.join(root,'sw.js');
const sw=fs.readFileSync(file,'utf8');
if(!sw.includes('CACHE_PREFIX="tp-cache:"+SCOPE.pathname')||!sw.includes('ownRequest(req.url)')||!sw.includes('ownRequest(client.url)'))throw Error('Missing scoped isolation');
const files=JSON.parse(sw.match(/const ASSETS=(\[.*?\]);/s)[1]);
for(const a of files)if(!fs.existsSync(path.join(root,a)))throw Error('Missing PWA asset '+a);
const manifest=JSON.parse(fs.readFileSync(path.join(root,'manifest.webmanifest'),'utf8'));
if(!manifest.name.includes('RHTFLOW')||!manifest.name.includes('TEST'))throw Error('Brand missing');
for(const icon of manifest.icons){const b=fs.readFileSync(path.join(root,icon.src));const [w,h]=icon.sizes.split('x').map(Number);if(b.readUInt32BE(16)!==w||b.readUInt32BE(20)!==h)throw Error('Icon dimensions '+icon.src);}
console.log('Verified '+files.length+' PWA resources; separate TEST scope');
