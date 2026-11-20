"""
paint_cards.py - paints every card's artwork on YOUR PC, free and unlimited, using ComfyUI + an SDXL model.

  1. Start ComfyUI (it must be running at http://127.0.0.1:8188).
  2. From the card-game folder run, for example:
        python tools/paint_cards.py --set TW --limit 5       (test 5 cards)
        python tools/paint_cards.py                          (paint everything still missing)
        python tools/paint_cards.py --only SFA-002 --force   (redo one card)
        python tools/paint_cards.py --manifest-only          (just re-scan art/ after saving Gemini images by hand)

Finished paintings go to art/<SET>/<ID>.png and art/manifest.js is updated, so index.html shows them.
Uses only the Python standard library (no installs). Works with ComfyUI portable's python_embeded too.
"""
import argparse, json, os, random, sys, time, urllib.request, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NEG = ('text, letters, words, watermark, logo, signature, border, frame, card frame, blurry, lowres, jpeg artifacts, '
       'deformed, disfigured, extra limbs, extra fingers, bad anatomy, cartoon, childish, flat colors, clipart, gore, blood splatter')

def load_cards(only_set=None):
    out = []
    for code in ('TW', 'SFA'):
        if only_set and only_set != code: continue
        s = json.load(open(os.path.join(ROOT, 'data', f'cards_{code.lower()}.json'), encoding='utf-8'))
        out += s['cards']
    return out

def write_manifest():
    m = {}
    for code in ('TW', 'SFA'):
        d = os.path.join(ROOT, 'art', code)
        if not os.path.isdir(d): continue
        for f in sorted(os.listdir(d)):
            base, ext = os.path.splitext(f)
            if ext.lower() in ('.png', '.jpg', '.jpeg', '.webp'):
                m[base.upper()] = f'art/{code}/{f}'
    with open(os.path.join(ROOT, 'art', 'manifest.js'), 'w', encoding='utf-8') as fh:
        fh.write('window.ART_MANIFEST=' + json.dumps(m, indent=0) + ';')
    return len(m)

def workflow(prompt, seed, a):
    return {
      "4": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": a.ckpt}},
      "5": {"class_type": "EmptyLatentImage", "inputs": {"width": a.width, "height": a.height, "batch_size": 1}},
      "6": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": ["4", 1]}},
      "7": {"class_type": "CLIPTextEncode", "inputs": {"text": NEG, "clip": ["4", 1]}},
      "3": {"class_type": "KSampler", "inputs": {"seed": seed, "steps": a.steps, "cfg": a.cfg, "sampler_name": "dpmpp_2m",
             "scheduler": "karras", "denoise": 1.0, "model": ["4", 0], "positive": ["6", 0], "negative": ["7", 0], "latent_image": ["5", 0]}},
      "8": {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae": ["4", 2]}},
      "9": {"class_type": "SaveImage", "inputs": {"filename_prefix": "cardart", "images": ["8", 0]}},
    }

def api(a, path, data=None):
    url = a.host.rstrip('/') + path
    req = urllib.request.Request(url, data=json.dumps(data).encode() if data is not None else None,
                                 headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

def paint(card, a):
    seed = random.Random(card['id']).randint(1, 2**31)
    pid = json.loads(api(a, '/prompt', {"prompt": workflow(card['art_prompt'], seed, a)}))['prompt_id']
    t0 = time.time()
    while True:
        time.sleep(2)
        h = json.loads(api(a, f'/history/{pid}'))
        if pid in h and h[pid].get('outputs'):
            img = h[pid]['outputs']['9']['images'][0]
            q = urllib.parse.urlencode({'filename': img['filename'], 'subfolder': img['subfolder'], 'type': img['type']})
            return api(a, f'/view?{q}'), time.time() - t0
        if time.time() - t0 > 1800:
            raise TimeoutError('ComfyUI took over 30 minutes on one image')

def main():
    p = argparse.ArgumentParser(description='Paint card art with local ComfyUI')
    p.add_argument('--set', choices=['TW', 'SFA'])
    p.add_argument('--only', help='comma list of card ids, e.g. TW-001,SFA-002')
    p.add_argument('--rarity', help='only these rarities, e.g. LR')
    p.add_argument('--limit', type=int, default=0)
    p.add_argument('--force', action='store_true', help='repaint even if the file exists')
    p.add_argument('--ckpt', default='sd_xl_base_1.0.safetensors', help='model file name in ComfyUI/models/checkpoints')
    p.add_argument('--steps', type=int, default=28)
    p.add_argument('--cfg', type=float, default=6.0)
    p.add_argument('--width', type=int, default=1152)
    p.add_argument('--height', type=int, default=896)
    p.add_argument('--host', default='http://127.0.0.1:8188')
    p.add_argument('--manifest-only', action='store_true')
    a = p.parse_args()
    if a.manifest_only:
        print('manifest updated:', write_manifest(), 'paintings'); return
    cards = load_cards(a.set)
    if a.only: ids = {x.strip().upper() for x in a.only.split(',')}; cards = [c for c in cards if c['id'] in ids]
    if a.rarity: cards = [c for c in cards if c['r'] in a.rarity.upper()]
    # legendaries and rares first so the best cards look great soonest
    cards.sort(key=lambda c: 'LRUC'.index(c['r']))
    todo = [c for c in cards if a.force or not any(os.path.exists(os.path.join(ROOT, 'art', c['set'], c['id'] + e)) for e in ('.png', '.jpg', '.webp'))]
    if a.limit: todo = todo[:a.limit]
    try: api(a, '/system_stats')
    except Exception:
        sys.exit(f'Could not reach ComfyUI at {a.host}. Start ComfyUI first (run_nvidia_gpu.bat), then run this again.')
    print(f'{len(todo)} paintings to make with {a.ckpt}. Ctrl+C stops safely; run again to resume.')
    for i, c in enumerate(todo, 1):
        os.makedirs(os.path.join(ROOT, 'art', c['set']), exist_ok=True)
        try:
            png, secs = paint(c, a)
        except Exception as e:
            print(f'  ! {c["id"]} failed: {e}'); continue
        open(os.path.join(ROOT, 'art', c['set'], c['id'] + '.png'), 'wb').write(png)
        write_manifest()
        print(f'[{i}/{len(todo)}] {c["id"]} {c["name"]}  ({secs:.0f}s)')
    print('Done. Open index.html to see the cards with their new art.')

if __name__ == '__main__':
    main()
