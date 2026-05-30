from urllib.request import urlopen, Request
import re, os

photos = {
    'hero-product-in-use': 'a-person-is-painting-a-wall-with-a-paint-sprayer-2Mp2Xa4nFJU',
    'hero-painter-at-work': 'a-painter-is-painting-a-white-wall-ddzrK5r1N6o',
    'testimonial-man': 'a-man-in-a-suit-8ONRwVxk6h4',
    'testimonial-woman': 'a-young-woman-with-dark-hair-smiles-broadly-WoGLaHIVoVA',
    'testimonial-woman2': 'a-woman-with-blonde-hair-smiles-over-her-shoulder-wdA8Br4V5jE',
}

out = r'C:\Users\Lucas Pietro\Desktop\Projeto\images'

for name, slug in photos.items():
    url = f'https://unsplash.com/photos/{slug}'
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req, timeout=15).read().decode('utf-8', errors='replace')
        m = re.search(r'<meta property="og:image" content="([^"]+)"', html)
        if m:
            img_url = m.group(1)
            base = img_url.split('?')[0]
            ext = base.split('.')[-1] if '.' in base else 'jpg'
            fname = f'{name}.{ext}'
            path = os.path.join(out, fname)
            req2 = Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
            data = urlopen(req2, timeout=30).read()
            with open(path, 'wb') as f:
                f.write(data)
            sz = len(data) // 1024
            print(f'OK  {fname} ({sz}KB)')
        else:
            print(f'ERR no og:image for {slug}')
    except Exception as e:
        print(f'ERR {slug}: {e}')
