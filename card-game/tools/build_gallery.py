import base64, os, json
B = os.path.join(os.path.dirname(__file__), '..')
t = open(os.path.join(B, 'tools', 'gallery_template.html'), encoding='utf-8').read()
data = open(os.path.join(B, 'data', 'cards.js'), encoding='utf-8').read()
svg = {}
for f in os.listdir(os.path.join(B, 'art', 'concept')):
    if f.endswith('.svg'):
        svg[f[:-4]] = 'data:image/svg+xml;base64,' + base64.b64encode(open(os.path.join(B, 'art', 'concept', f), 'rb').read()).decode()
t = t.replace('/*__DATA__*/', data).replace('/*__SVG__*/', 'window.CARD_SVG=' + json.dumps(svg) + ';')
open(os.path.join(B, 'index.html'), 'w', encoding='utf-8').write(t)
print('index.html', round(len(t) / 1024), 'KB')
