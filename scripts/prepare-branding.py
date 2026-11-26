from PIL import Image
from pathlib import Path
import hashlib
root=Path('source/cloud/public/icons')
original=Path('branding/original.png')
preview=Path('branding/preview.webp')
if original.exists():
    im=Image.open(original).convert('RGBA')
    assert min(im.size)>=512,'Original artwork must be at least 512 pixels'
    assert im.getchannel('A').getextrema()[0]==0,'Original artwork needs a transparent background'
    print(f'TEST: original transparent artwork {im.width}x{im.height}')
else:
    assert hashlib.sha256(preview.read_bytes()).hexdigest()=='761781915996e229ba816af5b392ef3e6b13f7fb5590bab043d4229e451d6cfc', 'Preview artwork corrupted'
    im=Image.open(preview).convert('RGBA')
    print('TEST: existing preview remains until branding/original.png is uploaded')
def fit(size):
    out=Image.new('RGBA',(size,size))
    img=im.copy()
    img.thumbnail((size,size),Image.Resampling.LANCZOS)
    out.alpha_composite(img,((size-img.width)//2,(size-img.height)//2))
    return out
# No white background or forced downsampling of the full logo.
im.save(root/'logo-full.webp',quality=96,method=6,exact=True)
for name,size in [('icon-192.png',192),('icon-512.png',512)]:
    fit(size).save(root/name)
apple=Image.new('RGBA',(180,180),'#171529')
apple.alpha_composite(fit(180))
apple.convert('RGB').save(root/'apple-touch-icon.png')
mask=Image.new('RGBA',(512,512),'#171529')
mask.alpha_composite(fit(288),(112,112))
mask.convert('RGB').save(root/'icon-maskable-512.png')
# Override old white frame only in TEST builds.
css=root.parent/'vice-city-theme.css'
css.write_text(css.read_text(encoding='utf8')+'\n.vice-city-theme .brand,.vice-city-theme .auth-logo{background:transparent;border:0;padding:0;border-radius:0;box-shadow:none;object-fit:contain}\n.vice-city-theme .brand{width:100%;max-width:210px;height:auto;max-height:210px}\n',encoding='utf8')
# Every actual artwork change invalidates only this PWA's own cached assets.
sw=root.parent/'sw.js'
source=sw.read_text(encoding='utf8')
digest=hashlib.sha256((root/'logo-full.webp').read_bytes()).hexdigest()[:12]
import re
source,n=re.subn(r'(const CACHE=CACHE_PREFIX\+"[^"]+)(")',lambda m:m[1]+'-branding.'+digest+m[2],source,count=1)
assert n==1,'Missing scoped cache version'
sw.write_text(source,encoding='utf8')
