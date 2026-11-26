from PIL import Image
from pathlib import Path
import hashlib
root=Path('source/cloud/public/icons')
src=Path('branding')
original=src/'original.png'
preview=src/'preview.webp'
if original.exists():
    im=Image.open(original).convert('RGB')
else:
    assert hashlib.sha256(preview.read_bytes()).hexdigest()=='761781915996e229ba816af5b392ef3e6b13f7fb5590bab043d4229e451d6cfc', 'Preview artwork corrupted'
    im=Image.open(preview).convert('RGB')
    print('TEST: reduced-resolution original artwork; upload branding/original.png for high resolution')
im.resize((512,512),Image.Resampling.LANCZOS).save(root/'logo-full.webp',quality=90)
for name,size in [('icon-192.png',192),('icon-512.png',512),('apple-touch-icon.png',180)]:
    im.resize((size,size),Image.Resampling.LANCZOS).save(root/name)
mask=Image.new('RGB',(512,512),'#160d29')
mask.paste(im.resize((362,362),Image.Resampling.LANCZOS),(75,75))
mask.save(root/'icon-maskable-512.png')
