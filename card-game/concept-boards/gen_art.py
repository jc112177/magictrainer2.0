import random, math
W,H=600,440
def hdr(seed,extra=''):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3" seed="{seed}"/><feColorMatrix type="matrix" values="0 0 0 0 0.5  0 0 0 0 0.5  0 0 0 0 0.5  0 0 0 0.9 0"/></filter>
<filter id="cloud" x="-20%" y="-20%" width="140%" height="140%"><feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves="4" seed="{seed+3}"/><feDisplacementMap in="SourceGraphic" scale="60"/><feGaussianBlur stdDeviation="10"/></filter>
<filter id="b2"><feGaussianBlur stdDeviation="2"/></filter>
<filter id="b4"><feGaussianBlur stdDeviation="4"/></filter>
<filter id="b10" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="10"/></filter>
<filter id="b24" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="24"/></filter>
<radialGradient id="vig" cx="50%" cy="50%" r="72%"><stop offset="55%" stop-color="#000" stop-opacity="0"/><stop offset="100%" stop-color="#000" stop-opacity="0.85"/></radialGradient>
<linearGradient id="fogL" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfd8d0" stop-opacity="0"/><stop offset="1" stop-color="#cfd8d0" stop-opacity="0.22"/></linearGradient>
{extra}
</defs>'''
def tail(grain=0.16):
    return f'<rect width="{W}" height="{H}" fill="url(#vig)"/><rect width="{W}" height="{H}" filter="url(#grain)" opacity="{grain}" style="mix-blend-mode:overlay"/></svg>'
def dust(r,n,col,box=(0,0,W,H),smax=1.8,op=(0.2,0.8)):
    x0,y0,x1,y1=box
    return ''.join(f'<circle cx="{r.uniform(x0,x1):.1f}" cy="{r.uniform(y0,y1):.1f}" r="{r.uniform(0.4,smax):.2f}" fill="{col}" opacity="{r.uniform(*op):.2f}"/>' for _ in range(n))
def stars(r,n,box=(0,0,W,H)):
    out=[]
    x0,y0,x1,y1=box
    for _ in range(n):
        x,y=r.uniform(x0,x1),r.uniform(y0,y1);s=r.random()**3*1.8+0.3;c=r.choice(['#ffffff','#cfe3ff','#ffe9c8','#bcd4ff'])
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{s:.2f}" fill="{c}" opacity="{r.uniform(.4,1):.2f}"/>')
        if s>1.5: out.append(f'<path d="M{x-6:.1f} {y:.1f}H{x+6:.1f}M{x:.1f} {y-6:.1f}V{y+6:.1f}" stroke="{c}" stroke-width=".5" opacity=".6"/>')
    return ''.join(out)
def fog(r,n,col,yr,op=.18):
    return ''.join(f'<ellipse cx="{r.uniform(-50,W+50):.0f}" cy="{r.uniform(*yr):.0f}" rx="{r.uniform(120,260):.0f}" ry="{r.uniform(20,45):.0f}" fill="{col}" opacity="{op*r.uniform(.5,1):.2f}" filter="url(#b24)"/>' for _ in range(n))
def greebles(r,x,y,w,h,n,cols):
    return ''.join(f'<rect x="{r.uniform(x,x+w):.1f}" y="{r.uniform(y,y+h):.1f}" width="{r.uniform(2,14):.1f}" height="{r.uniform(1.5,6):.1f}" fill="{r.choice(cols)}" opacity="{r.uniform(.5,1):.2f}"/>' for _ in range(n))

# ================= HORROR =================
def warden():
    r=random.Random(11)
    ex='''<linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a1411"/><stop offset="1" stop-color="#0b0807"/></linearGradient>
<radialGradient id="bulb" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#fff3c4"/><stop offset=".25" stop-color="#ffcf6a" stop-opacity=".8"/><stop offset="1" stop-color="#ff9a2a" stop-opacity="0"/></radialGradient>
<linearGradient id="beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd98a" stop-opacity=".45"/><stop offset="1" stop-color="#ffd98a" stop-opacity="0"/></linearGradient>
<linearGradient id="door" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff5a3a"/><stop offset="1" stop-color="#7a1208"/></linearGradient>
<radialGradient id="maskG" cx="40%" cy="35%" r="70%"><stop offset="0" stop-color="#fbf6ea"/><stop offset=".7" stop-color="#c9bea6"/><stop offset="1" stop-color="#6e6452"/></radialGradient>'''
    s=hdr(11,ex)+f'<rect width="{W}" height="{H}" fill="url(#wall)"/>'
    # back wall with doors in perspective rows
    for row,(y,h,sc) in enumerate([(120,70,.5),(150,95,.7)]):
        for i in range(9 if row==0 else 7):
            x=40+i*(66 if row==0 else 84)+(row*12)
            lit=r.random()<.45
            s+=f'<rect x="{x}" y="{y}" width="{38*sc*1.6:.0f}" height="{h}" fill="#0a0706" stroke="#2c211b" stroke-width="2"/>'
            if lit: s+=f'<rect x="{x+3}" y="{y+3}" width="{38*sc*1.6-6:.0f}" height="{h-6}" fill="url(#door)" opacity=".75"/><rect x="{x-10}" y="{y-10}" width="{38*sc*1.6+20:.0f}" height="{h+20}" fill="#ff4a2a" opacity=".25" filter="url(#b10)"/>'
    # catwalk
    s+='<path d="M0 300 L600 300 L600 314 L0 314 Z" fill="#17110e"/><path d="M0 300 L600 300" stroke="#5a4636" stroke-width="2"/>'
    s+=''.join(f'<path d="M{x} 300 L{x} 270 " stroke="#3a2c22" stroke-width="3"/>' for x in range(10,600,40))+'<path d="M0 270 L600 270" stroke="#4a3a2c" stroke-width="3"/>'
    # floor perspective
    s+='<path d="M0 314 L600 314 L600 440 L0 440 Z" fill="#0c0908"/>'+''.join(f'<path d="M300 314 L{x} 440" stroke="#1d1612" stroke-width="1.5"/>' for x in range(-600,1300,90))
    # chains
    for x in [70,150,450,530]:
        s+=''.join(f'<ellipse cx="{x}" cy="{yy}" rx="4" ry="7" fill="none" stroke="#4a3e33" stroke-width="2.5"/>' for yy in range(0,int(r.uniform(140,230)),12))
    # light beam
    s+='<polygon points="300,52 160,440 440,440" fill="url(#beam)"/>'
    s+='<line x1="300" y1="0" x2="300" y2="44" stroke="#2a221c" stroke-width="3"/><circle cx="300" cy="52" r="70" fill="url(#bulb)"/><circle cx="300" cy="52" r="7" fill="#fff8e0"/>'
    # figure (long coat, hood, mask) with rim light
    s+='<path d="M244 300 C246 230 262 196 300 192 C338 196 354 230 356 300 Z" fill="#050403"/>'
    s+='<path d="M262 206 C262 160 338 160 338 206 L332 218 L268 218 Z" fill="#070505"/>'
    s+='<path d="M244 300 C246 230 262 196 300 192" fill="none" stroke="#ffcf6a" stroke-width="2" opacity=".55"/><path d="M356 300 C354 230 338 196 300 192" fill="none" stroke="#ffcf6a" stroke-width="2" opacity=".55"/>'
    s+='<ellipse cx="300" cy="206" rx="25" ry="31" fill="url(#maskG)"/><ellipse cx="290" cy="200" rx="6" ry="8" fill="#0a0706"/><ellipse cx="310" cy="200" rx="6" ry="8" fill="#0a0706"/><circle cx="290" cy="201" r="1.4" fill="#ff5a3a"/><circle cx="310" cy="201" r="1.4" fill="#ff5a3a"/>'
    s+='<path d="M288 220 L312 220" stroke="#6a1a12" stroke-width="2"/>'+''.join(f'<path d="M{x} 216 L{x} 224" stroke="#6a1a12" stroke-width="1.2"/>' for x in range(290,312,4))
    s+='<path d="M311 178 L304 196 L308 206" stroke="#7a705e" stroke-width="1" fill="none"/>'
    # hands holding a lever / key ring
    s+='<path d="M268 262 L256 286" stroke="#050403" stroke-width="12" stroke-linecap="round"/><circle cx="252" cy="292" r="10" fill="none" stroke="#b08a4a" stroke-width="2.5"/>'
    s+=''.join(f'<path d="M{252+12*math.cos(a):.1f} {292+12*math.sin(a):.1f} l{6*math.cos(a):.1f} {6*math.sin(a)+6:.1f}" stroke="#c9a25a" stroke-width="2"/>' for a in [0.5,1.4,2.3,3.1])
    s+=fog(r,9,'#c7b8a0',(260,440),.22)+dust(r,140,'#ffe2a0',(150,40,450,440),1.4,(.15,.7))
    return s+tail(.18)
def collar():
    r=random.Random(21)
    ex='''<radialGradient id="spot" cx="50%" cy="40%" r="60%"><stop offset="0" stop-color="#3a2a1e"/><stop offset="1" stop-color="#070504"/></radialGradient>
<linearGradient id="steel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e3dcd0"/><stop offset=".35" stop-color="#8d8577"/><stop offset=".6" stop-color="#4a443b"/><stop offset="1" stop-color="#a59c8b"/></linearGradient>
<linearGradient id="brass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffe2a0"/><stop offset=".5" stop-color="#a87a2a"/><stop offset="1" stop-color="#5a3a10"/></linearGradient>
<radialGradient id="face" cx="45%" cy="40%" r="60%"><stop offset="0" stop-color="#fff8e8"/><stop offset="1" stop-color="#c8bc9e"/></radialGradient>'''
    s=hdr(21,ex)+f'<rect width="{W}" height="{H}" fill="url(#spot)"/>'
    s+='<path d="M0 330 L600 300 L600 440 L0 440 Z" fill="#1c140f"/>'+''.join(f'<path d="M0 {340+i*16} L600 {310+i*16}" stroke="#2a1e16" stroke-width="1"/>' for i in range(8))
    # collar ellipse ring (3/4 view)
    s+='<ellipse cx="300" cy="250" rx="190" ry="82" fill="#0c0807" opacity=".6" filter="url(#b10)" transform="translate(10 50)"/>'
    s+='<ellipse cx="300" cy="230" rx="180" ry="74" fill="none" stroke="url(#steel)" stroke-width="34"/>'
    s+='<ellipse cx="300" cy="230" rx="180" ry="74" fill="none" stroke="#fff" stroke-width="2" opacity=".35" transform="translate(0 -14)"/>'
    for i in range(22):
        a=i/22*2*math.pi;x=300+180*math.cos(a);y=230+74*math.sin(a)
        s+=f'<circle cx="{x:.1f}" cy="{y-8:.1f}" r="3.2" fill="url(#brass)" stroke="#2a1a08" stroke-width=".8"/>'
    # spikes inward
    for i in range(14):
        a=i/14*2*math.pi;x=300+162*math.cos(a);y=230+64*math.sin(a);x2=300+128*math.cos(a);y2=230+48*math.sin(a)
        s+=f'<path d="M{x-5:.1f} {y:.1f} L{x2:.1f} {y2:.1f} L{x+5:.1f} {y:.1f} Z" fill="#b9b0a0" stroke="#3a342c" stroke-width="1"/>'
    # clock mechanism at front
    s+='<circle cx="300" cy="300" r="62" fill="url(#brass)" stroke="#3a2408" stroke-width="3"/><circle cx="300" cy="300" r="50" fill="url(#face)" stroke="#5a3a10" stroke-width="2"/>'
    for i in range(12):
        a=i/12*2*math.pi-math.pi/2
        s+=f'<path d="M{300+42*math.cos(a):.1f} {300+42*math.sin(a):.1f} L{300+47*math.cos(a):.1f} {300+47*math.sin(a):.1f}" stroke="#2a1a08" stroke-width="{2.5 if i%3==0 else 1.2}"/>'
    s+='<path d="M300 300 L300 262" stroke="#2a1a08" stroke-width="3" stroke-linecap="round"/><path d="M300 300 L326 312" stroke="#8a1c14" stroke-width="2.5" stroke-linecap="round"/><circle cx="300" cy="300" r="4" fill="#2a1a08"/>'
    # gears
    def gear(cx,cy,R,n,col):
        pts=[]
        for i in range(n*2):
            a=i/(n*2)*2*math.pi;rr=R if i%2==0 else R*.82
            pts.append(f'{cx+rr*math.cos(a):.1f},{cy+rr*math.sin(a):.1f}')
        return f'<polygon points="{" ".join(pts)}" fill="{col}" stroke="#2a1a08" stroke-width="1.2"/><circle cx="{cx}" cy="{cy}" r="{R*.35:.1f}" fill="#1c140f"/>'
    s+=gear(214,290,26,12,'url(#brass)')+gear(386,288,22,10,'url(#brass)')+gear(250,330,14,8,'#8d6a2a')
    s+='<ellipse cx="270" cy="160" rx="160" ry="20" fill="#fff" opacity=".07" filter="url(#b10)"/>'
    s+=dust(r,60,'#ffd98a',(0,0,600,300),1.2,(.1,.5))
    return s+tail(.2)
def flood():
    r=random.Random(31)
    ex='''<linearGradient id="tile" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a4a44"/><stop offset="1" stop-color="#1a2420"/></linearGradient>
<linearGradient id="water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2f6a66" stop-opacity=".85"/><stop offset="1" stop-color="#06100f"/></linearGradient>
<linearGradient id="shaft" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d9f0e6" stop-opacity=".5"/><stop offset="1" stop-color="#d9f0e6" stop-opacity="0"/></linearGradient>'''
    s=hdr(31,ex)+f'<rect width="{W}" height="{H}" fill="url(#tile)"/>'
    # tiles grid w/ grime
    for y in range(0,300,28):
        for x in range(0,600,28):
            sh=r.uniform(-.06,.06)
            s+=f'<rect x="{x+1}" y="{y+1}" width="26" height="26" fill="#9fb3aa" opacity="{.08+sh:.2f}"/>'
    s+=''.join(f'<path d="M{r.uniform(0,600):.0f} {r.uniform(0,250):.0f} q{r.uniform(-4,4):.1f} {r.uniform(20,60):.0f} {r.uniform(-3,3):.1f} {r.uniform(40,90):.0f}" stroke="#3a2a14" stroke-width="{r.uniform(1,3):.1f}" opacity=".5" fill="none"/>' for _ in range(14))
    # window bars top
    s+='<rect x="250" y="20" width="100" height="56" fill="#cfe9df"/>'+''.join(f'<rect x="{x}" y="20" width="6" height="56" fill="#0b1210"/>' for x in range(256,346,18))
    s+='<polygon points="250,76 350,76 470,300 130,300" fill="url(#shaft)"/>'
    s+='<rect x="230" y="0" width="140" height="100" fill="#cfe9df" opacity=".25" filter="url(#b24)"/>'
    # pipe + valve
    s+='<rect x="60" y="0" width="24" height="230" fill="#4a3a2a"/><rect x="56" y="210" width="32" height="18" fill="#6a5238"/><path d="M72 228 Q74 250 70 300" stroke="#9fd6cf" stroke-width="10" opacity=".55" fill="none"/>'
    s+='<circle cx="72" cy="150" r="22" fill="none" stroke="#8a1c14" stroke-width="6"/><path d="M50 150 L94 150 M72 128 L72 172" stroke="#8a1c14" stroke-width="5"/>'
    # water
    s+='<rect x="0" y="290" width="600" height="150" fill="url(#water)"/>'
    s+=''.join(f'<path d="M{x} {y:.0f} q15 -4 30 0 t30 0" stroke="#bfeee6" stroke-width="1.2" opacity="{r.uniform(.15,.5):.2f}" fill="none"/>' for x in range(-20,600,50) for y in [r.uniform(292,300),r.uniform(310,330),r.uniform(350,380)])
    s+='<polygon points="250,300 350,300 380,440 220,440" fill="#d9f0e6" opacity=".08"/>'
    # submerged hand reaching
    s+='<path d="M430 300 L438 268 L442 270 L440 252 L446 252 L448 266 L452 250 L458 252 L456 268 L462 258 L466 262 L458 284 L456 300 Z" fill="#c7b9a4" stroke="#3a3228" stroke-width="1"/>'
    s+='<path d="M424 300 Q446 292 470 300" stroke="#e6fff9" stroke-width="2" fill="none" opacity=".6"/>'
    s+='<text x="510" y="70" font-family="Georgia,serif" font-size="46" fill="#8a1c14" opacity=".75" transform="rotate(-6 510 70)">13</text>'
    s+=dust(r,80,'#e6fff9',(0,80,600,300),1.2,(.1,.45))
    return s+tail(.16)
def wren():
    r=random.Random(41)
    ex='''<radialGradient id="lamp" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#fff2c0"/><stop offset=".3" stop-color="#ffb84a" stop-opacity=".7"/><stop offset="1" stop-color="#ff7a1a" stop-opacity="0"/></radialGradient>
<linearGradient id="dwood" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2a1a10"/><stop offset=".5" stop-color="#4a2f1c"/><stop offset="1" stop-color="#22150c"/></linearGradient>'''
    s=hdr(41,ex)+f'<rect width="{W}" height="{H}" fill="#0b0a0c"/>'
    # massive door with many locks on right
    s+='<rect x="330" y="20" width="230" height="420" fill="url(#dwood)" stroke="#120a06" stroke-width="6"/>'
    s+=''.join(f'<path d="M{x} 20 L{x} 440" stroke="#1a100a" stroke-width="2" opacity=".7"/>' for x in range(350,560,30))
    for i,(y) in enumerate([70,120,170,220,270,320,370]):
        x=360+(i%3)*58
        s+=f'<rect x="{x}" y="{y}" width="40" height="30" rx="3" fill="#8a7244" stroke="#2a1a08" stroke-width="2"/><circle cx="{x+20}" cy="{y+12}" r="4" fill="#1a1006"/><rect x="{x+18}" y="{y+12}" width="4" height="10" fill="#1a1006"/>'
    s+=''.join(f'<path d="M330 {y} L560 {y+r.uniform(-4,4):.0f}" stroke="#5a5048" stroke-width="5" opacity=".9"/>' for y in [100,250,400])
    # lantern glow left-center
    s+='<circle cx="270" cy="250" r="190" fill="url(#lamp)" opacity=".85"/>'
    # figure silhouette kneeling at lock, rim lit
    s+='<path d="M150 440 L160 330 C164 290 190 270 220 270 C250 270 266 290 268 320 L280 440 Z" fill="#070608"/>'
    s+='<circle cx="214" cy="236" r="30" fill="#070608"/><path d="M188 226 C194 196 238 192 246 222 C250 236 244 250 240 256 C236 230 196 228 188 244 Z" fill="#1a1012"/>'
    s+='<path d="M244 236 C246 252 240 266 230 270" stroke="#ffc46a" stroke-width="3" fill="none" opacity=".9"/><path d="M262 300 C268 330 276 380 280 440" stroke="#ffc46a" stroke-width="2.5" fill="none" opacity=".7"/>'
    # arm with picks reaching to lock
    s+='<path d="M250 300 C290 290 320 270 352 258" stroke="#070608" stroke-width="16" stroke-linecap="round" fill="none"/><path d="M352 258 L384 252 M352 262 L382 266" stroke="#d9d0c0" stroke-width="2.2"/>'
    s+='<path d="M255 292 C290 282 320 264 350 252" stroke="#ffc46a" stroke-width="2" fill="none" opacity=".6"/>'
    # lantern
    s+='<rect x="258" y="330" width="26" height="36" rx="4" fill="#ffdc8a" stroke="#3a2a14" stroke-width="3"/><path d="M262 330 L280 330 L271 318 Z" fill="#3a2a14"/><circle cx="271" cy="348" r="40" fill="#ffd27a" opacity=".35" filter="url(#b10)"/>'
    s+=dust(r,120,'#ffd9a0',(120,120,420,440),1.3,(.12,.6))
    return s+tail(.18)
def choice():
    r=random.Random(51)
    ex='''<radialGradient id="redL" cx="0%" cy="50%" r="80%"><stop offset="0" stop-color="#ff2a1a" stop-opacity=".55"/><stop offset="1" stop-color="#ff2a1a" stop-opacity="0"/></radialGradient>
<radialGradient id="grnL" cx="100%" cy="50%" r="80%"><stop offset="0" stop-color="#3affb0" stop-opacity=".45"/><stop offset="1" stop-color="#3affb0" stop-opacity="0"/></radialGradient>
<linearGradient id="tbl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a2a1e"/><stop offset="1" stop-color="#120c08"/></linearGradient>
<linearGradient id="tape" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a5650"/><stop offset="1" stop-color="#1e1c1a"/></linearGradient>'''
    s=hdr(51,ex)+f'<rect width="{W}" height="{H}" fill="#08070a"/><rect width="300" height="{H}" fill="url(#redL)"/><rect x="300" width="300" height="{H}" fill="url(#grnL)"/>'
    # two doors
    s+='<rect x="40" y="40" width="150" height="250" fill="#120606" stroke="#ff4a3a" stroke-width="3"/><rect x="410" y="40" width="150" height="250" fill="#06120c" stroke="#3affb0" stroke-width="3"/>'
    s+='<rect x="30" y="30" width="170" height="270" fill="#ff2a1a" opacity=".3" filter="url(#b24)"/><rect x="400" y="30" width="170" height="270" fill="#3affb0" opacity=".25" filter="url(#b24)"/>'
    s+='<text x="115" y="150" text-anchor="middle" font-family="Georgia,serif" font-size="64" fill="#ff6a5a" opacity=".85">I</text><text x="485" y="150" text-anchor="middle" font-family="Georgia,serif" font-size="64" fill="#7affc8" opacity=".85">II</text>'
    # table with tape recorder + two keys
    s+='<path d="M0 320 L600 320 L600 440 L0 440 Z" fill="url(#tbl)"/><path d="M0 320 L600 320" stroke="#6a4a30" stroke-width="2"/>'
    s+='<rect x="220" y="270" width="160" height="80" rx="8" fill="url(#tape)" stroke="#0a0908" stroke-width="2"/><circle cx="262" cy="306" r="20" fill="#0a0908" stroke="#8a847a" stroke-width="2"/><circle cx="338" cy="306" r="20" fill="#0a0908" stroke="#8a847a" stroke-width="2"/>'
    s+='<circle cx="262" cy="306" r="6" fill="#8a847a"/><circle cx="338" cy="306" r="6" fill="#8a847a"/><rect x="238" y="334" width="124" height="8" fill="#2a2724"/><circle cx="370" cy="282" r="4" fill="#ff2a1a"/><circle cx="370" cy="282" r="10" fill="#ff2a1a" opacity=".5" filter="url(#b4)"/>'
    for x,col in [(150,'#ff6a5a'),(450,'#7affc8')]:
        s+=f'<circle cx="{x}" cy="372" r="12" fill="none" stroke="#c9a25a" stroke-width="5"/><rect x="{x+10}" y="368" width="46" height="8" fill="#c9a25a"/><rect x="{x+44}" y="376" width="6" height="10" fill="#c9a25a"/><rect x="{x+34}" y="376" width="5" height="7" fill="#c9a25a"/><circle cx="{x}" cy="372" r="30" fill="{col}" opacity=".18" filter="url(#b10)"/>'
    s+=dust(r,90,'#ffffff',(0,0,600,320),1.1,(.08,.35))
    return s+tail(.18)
def orderly():
    r=random.Random(61)
    ex='''<linearGradient id="cor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1e2422"/><stop offset="1" stop-color="#0a0c0b"/></linearGradient>
<radialGradient id="lan" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#fff0c0"/><stop offset=".35" stop-color="#ffb64a" stop-opacity=".6"/><stop offset="1" stop-color="#ff8a1a" stop-opacity="0"/></radialGradient>
<radialGradient id="pm" cx="40%" cy="35%" r="70%"><stop offset="0" stop-color="#e9e2d2"/><stop offset="1" stop-color="#7a705e"/></radialGradient>'''
    s=hdr(61,ex)+f'<rect width="{W}" height="{H}" fill="url(#cor)"/>'
    # corridor perspective
    s+='<polygon points="0,0 230,150 230,300 0,440" fill="#141917"/><polygon points="600,0 370,150 370,300 600,440" fill="#111513"/><rect x="230" y="150" width="140" height="150" fill="#070908"/>'
    s+='<rect x="276" y="190" width="48" height="90" fill="#ffd98a" opacity=".2"/>'
    for i in range(6):
        t=i/6;x=230*t;s+=f'<path d="M{x:.0f} {150*t:.0f} L{x:.0f} {440-140*t:.0f}" stroke="#222a27" stroke-width="2"/><path d="M{600-x:.0f} {150*t:.0f} L{600-x:.0f} {440-140*t:.0f}" stroke="#222a27" stroke-width="2"/>'
    s+=''.join(f'<rect x="{230*t-14:.0f}" y="{150*t+30:.0f}" width="{30*(1-t)+6:.0f}" height="{80*(1-t)+16:.0f}" fill="#2e3a36" opacity=".6"/>' for t in [.15,.45,.75])
    # flickering lights ceiling
    s+=''.join(f'<rect x="{300-60*(1-t):.0f}" y="{150*t-6:.0f}" width="{120*(1-t):.0f}" height="{6*(1-t)+2:.1f}" fill="#d9f0e6" opacity="{.7 if i!=1 else .15}"/>' for i,t in enumerate([.3,.6,.85]))
    # figure close: shoulders, masked head, lantern raised
    s+='<path d="M120 440 C130 360 190 320 300 314 C410 320 470 360 480 440 Z" fill="#070807"/>'
    s+='<ellipse cx="300" cy="250" rx="58" ry="70" fill="url(#pm)"/><path d="M262 238 L290 236 L288 252 L264 252 Z M338 238 L310 236 L312 252 L336 252 Z" fill="#0a0b0a"/>'
    s+='<path d="M276 288 L324 288" stroke="#3a3228" stroke-width="3"/>'+''.join(f'<circle cx="{x}" cy="{y}" r="1.6" fill="#3a3228"/>' for x in range(270,332,8) for y in [276,300])
    s+='<path d="M246 200 C250 170 350 170 354 200 C360 214 360 226 356 236 C340 200 260 200 244 236 C240 226 240 212 246 200 Z" fill="#141615"/>'
    s+='<path d="M420 360 L440 230" stroke="#070807" stroke-width="22" stroke-linecap="round"/><circle cx="446" cy="214" r="70" fill="url(#lan)"/><rect x="434" y="196" width="24" height="34" rx="4" fill="#ffdf96" stroke="#2a1e10" stroke-width="3"/>'
    s+='<path d="M354 256 C360 280 352 300 340 310" stroke="#ffc46a" stroke-width="3" fill="none" opacity=".75"/>'
    s+=fog(r,7,'#b9c7c0',(300,440),.2)+dust(r,70,'#ffe2a0',(340,140,560,320),1.2,(.15,.6))
    return s+tail(.18)

# ================= SPACE =================
def space_bg(r,seed,neb=('#3a1a6a','#0a3a6a','#6a1a3a')):
    s=f'<rect width="{W}" height="{H}" fill="#04050c"/>'
    for i,c in enumerate(neb):
        s+=f'<ellipse cx="{r.uniform(80,520):.0f}" cy="{r.uniform(60,300):.0f}" rx="{r.uniform(160,300):.0f}" ry="{r.uniform(70,140):.0f}" fill="{c}" opacity=".55" filter="url(#cloud)" transform="rotate({r.uniform(-25,25):.0f} 300 220)"/>'
    s+=stars(r,420)
    return s
def leviathan():
    r=random.Random(71)
    ex='''<linearGradient id="hullT" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c8d2e0"/><stop offset=".5" stop-color="#6c7a8e"/><stop offset="1" stop-color="#2a3240"/></linearGradient>
<linearGradient id="hullS" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a5668"/><stop offset="1" stop-color="#151a24"/></linearGradient>
<radialGradient id="eng" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#ffffff"/><stop offset=".3" stop-color="#7ad8ff"/><stop offset="1" stop-color="#1a6aff" stop-opacity="0"/></radialGradient>
<radialGradient id="planet" cx="35%" cy="30%" r="75%"><stop offset="0" stop-color="#e09a5a"/><stop offset=".55" stop-color="#7a3a1e"/><stop offset="1" stop-color="#1a0806"/></radialGradient>
<linearGradient id="trail" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#7ad8ff" stop-opacity=".9"/><stop offset="1" stop-color="#1a6aff" stop-opacity="0"/></linearGradient>'''
    s=hdr(71,ex)+space_bg(r,71)
    s+='<circle cx="520" cy="520" r="260" fill="url(#planet)"/><circle cx="520" cy="520" r="262" fill="none" stroke="#ffb27a" stroke-width="6" opacity=".55" filter="url(#b4)"/><circle cx="520" cy="520" r="272" fill="none" stroke="#ff8a4a" stroke-width="14" opacity=".2" filter="url(#b10)"/>'
    # ship: long wedge from right-back to left-front
    top='M560 150 L240 168 L60 214 L240 236 L560 214 Z'
    s+=f'<path d="M560 214 L240 236 L60 214 L70 232 L250 262 L560 236 Z" fill="url(#hullS)"/><path d="{top}" fill="url(#hullT)"/>'
    s+='<path d="M560 182 L250 200 L80 214" stroke="#2a3240" stroke-width="2" fill="none"/>'
    for i in range(16):
        t=i/16;x1=560-500*t;s+=f'<path d="M{x1:.0f} {150+64*t*0.28:.0f} L{x1-10:.0f} {214+22*t:.0f}" stroke="#3a4454" stroke-width=".9" opacity=".8"/>'
    s+=greebles(r,260,168,280,40,140,['#2a3240','#8a96a8','#1a202a','#a8b4c4'])
    s+=greebles(r,120,196,140,20,50,['#2a3240','#8a96a8','#1a202a'])
    # bridge tower
    s+='<path d="M430 160 L440 118 L480 116 L488 158 Z" fill="url(#hullT)"/><path d="M436 132 L484 130" stroke="#7ad8ff" stroke-width="2"/>'+''.join(f'<rect x="{x}" y="138" width="3" height="2" fill="#ffe08a"/>' for x in range(444,480,6))
    # turrets
    for x,y in [(330,186),(380,182),(280,192)]:
        s+=f'<ellipse cx="{x}" cy="{y}" rx="13" ry="5" fill="#9aa6b8" stroke="#2a3240"/><path d="M{x} {y-2} L{x-30} {y-8} M{x} {y} L{x-30} {y-4}" stroke="#c8d2e0" stroke-width="2.4"/>'
    # window lights along side
    s+=''.join(f'<rect x="{x:.0f}" y="{y:.0f}" width="2.2" height="1.6" fill="#ffd98a" opacity=".9"/>' for x,y in [(r.uniform(120,550),0) for _ in range(90)] for y in [r.uniform(218,240)+ (560-x)*0.0])
    # engines + trails
    for y in [172,192,212]:
        s+=f'<rect x="560" y="{y-7}" width="40" height="14" fill="url(#trail)" opacity=".7"/><circle cx="562" cy="{y}" r="16" fill="url(#eng)"/>'
    s+='<path d="M60 214 L240 168 L240 236 Z" fill="#fff" opacity=".05"/>'
    # escort ships
    for x,y,sc in [(150,110,.25),(200,300,.2),(470,300,.18)]:
        s+=f'<g transform="translate({x} {y}) scale({sc})"><path d="M200 0 L-40 20 L200 40 Z" fill="url(#hullT)"/><circle cx="200" cy="20" r="14" fill="url(#eng)"/></g>'
    # laser volley
    s+='<path d="M300 180 L0 120" stroke="#ff5a3a" stroke-width="2" opacity=".9"/><path d="M300 180 L0 120" stroke="#ff5a3a" stroke-width="7" opacity=".3" filter="url(#b4)"/>'
    return s+tail(.1)
def talon():
    r=random.Random(81)
    ex='''<linearGradient id="hang" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a2230"/><stop offset="1" stop-color="#07090e"/></linearGradient>
<linearGradient id="armor" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e8eef6"/><stop offset=".5" stop-color="#8a96aa"/><stop offset="1" stop-color="#2a3242"/></linearGradient>
<linearGradient id="armorO" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffc07a"/><stop offset="1" stop-color="#a84a14"/></linearGradient>
<linearGradient id="flood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfe6ff" stop-opacity=".45"/><stop offset="1" stop-color="#cfe6ff" stop-opacity="0"/></linearGradient>
<pattern id="haz" width="24" height="24" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="12" height="24" fill="#ffc21a"/><rect x="12" width="12" height="24" fill="#111"/></pattern>'''
    s=hdr(81,ex)+f'<rect width="{W}" height="{H}" fill="url(#hang)"/>'
    s+=''.join(f'<path d="M{x} 0 L{300+(x-300)*.45:.0f} 120" stroke="#2a3446" stroke-width="3"/>' for x in range(-100,800,60))+'<path d="M0 120 L600 120" stroke="#3a4a60" stroke-width="3"/>'
    s+='<polygon points="120,0 200,0 340,440 -40,440" fill="url(#flood)"/><polygon points="420,0 500,0 660,440 280,440" fill="url(#flood)"/>'
    s+='<rect x="0" y="380" width="600" height="60" fill="#0c1018"/><rect x="0" y="380" width="600" height="10" fill="url(#haz)"/>'
    # gantry
    s+='<rect x="40" y="130" width="14" height="250" fill="#2a3446"/><rect x="546" y="130" width="14" height="250" fill="#2a3446"/><rect x="40" y="200" width="520" height="10" fill="#2a3446"/>'
    # mech
    s+='<path d="M250 140 L350 140 L370 230 L230 230 Z" fill="url(#armor)" stroke="#1a2230" stroke-width="2"/>'
    s+='<path d="M262 150 L338 150 L330 190 L270 190 Z" fill="#1a2230"/><path d="M276 166 L324 166" stroke="#ff7a2a" stroke-width="5"/><path d="M276 166 L324 166" stroke="#ff7a2a" stroke-width="14" opacity=".35" filter="url(#b4)"/>'
    s+='<path d="M200 140 L250 132 L256 176 L208 186 Z" fill="url(#armorO)" stroke="#1a2230" stroke-width="2"/><path d="M400 140 L350 132 L344 176 L392 186 Z" fill="url(#armorO)" stroke="#1a2230" stroke-width="2"/>'
    s+='<path d="M206 186 L190 290 L218 296 L240 200 Z" fill="url(#armor)" stroke="#1a2230" stroke-width="2"/><path d="M394 186 L410 290 L382 296 L360 200 Z" fill="url(#armor)" stroke="#1a2230" stroke-width="2"/>'
    s+='<rect x="404" y="270" width="18" height="70" fill="#3a4454" stroke="#1a2230"/><rect x="408" y="330" width="10" height="30" fill="#8a96aa"/>'
    s+='<path d="M248 230 L232 380 L270 380 L290 236 Z M352 230 L368 380 L330 380 L310 236 Z" fill="url(#armor)" stroke="#1a2230" stroke-width="2"/>'
    s+='<path d="M286 110 L314 110 L320 140 L280 140 Z" fill="url(#armor)" stroke="#1a2230" stroke-width="2"/><path d="M290 122 L310 122" stroke="#7ad8ff" stroke-width="4"/>'
    s+=greebles(r,236,196,128,34,40,['#1a2230','#5a6680','#ffc07a'])
    s+=''.join(f'<path d="M{x:.0f} {y:.0f} l{r.uniform(-14,14):.0f} {r.uniform(4,22):.0f}" stroke="#ffd27a" stroke-width="1.4" opacity=".9"/>' for x,y in [(r.uniform(330,350),r.uniform(200,214)) for _ in range(14)])
    s+='<circle cx="340" cy="206" r="16" fill="#ffd27a" opacity=".55" filter="url(#b4)"/>'
    s+=dust(r,60,'#cfe6ff',(0,0,600,380),1,(.1,.4))
    return s+tail(.12)
def ilsa():
    r=random.Random(91)
    ex='''<radialGradient id="ck" cx="50%" cy="60%" r="70%"><stop offset="0" stop-color="#0a2a3a"/><stop offset="1" stop-color="#020509"/></radialGradient>
<linearGradient id="helm" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f2f5fa"/><stop offset=".55" stop-color="#9aa6ba"/><stop offset="1" stop-color="#2a3242"/></linearGradient>
<linearGradient id="visor" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffb46a"/><stop offset=".4" stop-color="#a03a6a"/><stop offset="1" stop-color="#0a1a3a"/></linearGradient>'''
    s=hdr(91,ex)+f'<rect width="{W}" height="{H}" fill="url(#ck)"/>'
    # canopy frame + HUD
    s+='<path d="M0 60 Q300 -20 600 60" stroke="#1a2a3a" stroke-width="16" fill="none"/>'+stars(r,120,(0,0,600,170))
    s+=''.join(f'<path d="M{40+i*9} 360 L{40+i*9} {360-r.uniform(10,60):.0f}" stroke="#3affd0" stroke-width="4" opacity=".6"/>' for i in range(10))
    s+='<circle cx="520" cy="320" r="44" fill="none" stroke="#3affd0" stroke-width="2" opacity=".6"/><circle cx="520" cy="320" r="28" fill="none" stroke="#3affd0" stroke-width="1" opacity=".5" stroke-dasharray="4 4"/><path d="M520 320 L552 300" stroke="#3affd0" stroke-width="2" opacity=".7"/>'
    s+='<rect x="0" y="380" width="600" height="60" fill="#05090f"/>'+''.join(f'<rect x="{x}" y="396" width="16" height="10" rx="2" fill="{r.choice(["#ff5a3a","#3affd0","#ffc21a","#1a2a3a"])}" opacity=".85"/>' for x in range(60,560,26))
    # pilot shoulders & helmet
    s+='<path d="M140 440 C150 350 220 320 300 316 C380 320 450 350 460 440 Z" fill="#1c2230"/><path d="M160 440 C170 370 220 340 260 336 L270 440 Z" fill="#c25a1e" opacity=".8"/>'
    s+='<circle cx="300" cy="228" r="96" fill="url(#helm)" stroke="#1a2230" stroke-width="3"/>'
    s+='<path d="M222 222 C226 174 374 174 378 222 C380 262 352 292 300 294 C248 292 220 262 222 222 Z" fill="url(#visor)"/>'
    s+='<path d="M240 206 C270 184 330 184 360 206" stroke="#fff" stroke-width="5" opacity=".5" fill="none"/><path d="M250 260 L350 250" stroke="#3affd0" stroke-width="1.4" opacity=".7"/>'
    s+='<path d="M262 236 L284 236 L280 248 Z" fill="#ffd98a" opacity=".7"/>'+stars(r,30,(232,200,368,284))
    s+='<rect x="206" y="210" width="14" height="40" rx="4" fill="#3a4454"/><rect x="380" y="210" width="14" height="40" rx="4" fill="#3a4454"/>'
    s+='<text x="300" y="150" text-anchor="middle" font-family="Arial,sans-serif" font-weight="bold" font-size="14" fill="#c25a1e" letter-spacing="3">VARRO</text>'
    return s+tail(.1)
def lance():
    r=random.Random(101)
    ex='''<radialGradient id="earth" cx="50%" cy="0%" r="90%"><stop offset="0" stop-color="#3a7a9a"/><stop offset=".5" stop-color="#1a3a4a"/><stop offset="1" stop-color="#05121a"/></radialGradient>
<linearGradient id="lb" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffffff" stop-opacity="0"/><stop offset=".5" stop-color="#ffffff"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></linearGradient>
<radialGradient id="imp" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#ffffff"/><stop offset=".25" stop-color="#ffd27a"/><stop offset=".6" stop-color="#ff5a1a" stop-opacity=".6"/><stop offset="1" stop-color="#ff3a1a" stop-opacity="0"/></radialGradient>'''
    s=hdr(101,ex)+f'<rect width="{W}" height="{H}" fill="#03050a"/>'+stars(r,160,(0,0,600,170))
    s+=f'<ellipse cx="300" cy="900" rx="900" ry="720" fill="url(#earth)"/>'
    s+=''.join(f'<ellipse cx="{r.uniform(0,600):.0f}" cy="{r.uniform(220,440):.0f}" rx="{r.uniform(60,160):.0f}" ry="{r.uniform(8,22):.0f}" fill="#e6f2f8" opacity=".35" filter="url(#b10)"/>' for _ in range(16))
    s+='<ellipse cx="300" cy="180" rx="900" ry="16" fill="#7ad8ff" opacity=".35" filter="url(#b10)" transform="translate(0 0)"/>'
    # beam
    s+='<path d="M286 0 L314 0 L306 330 L294 330 Z" fill="#7ad8ff" opacity=".35" filter="url(#b10)"/><path d="M292 0 L308 0 L302 330 L298 330 Z" fill="url(#lb)"/><path d="M296 0 L304 0 L301 330 L299 330 Z" fill="#fff"/>'
    s+='<circle cx="300" cy="330" r="120" fill="url(#imp)"/>'
    for i,rr in enumerate([60,100,150,210]):
        s+=f'<ellipse cx="300" cy="334" rx="{rr}" ry="{rr*.22:.0f}" fill="none" stroke="#ffd27a" stroke-width="{3-i*.5}" opacity="{.8-i*.18:.2f}"/>'
    s+=''.join(f'<path d="M300 330 l{r.uniform(-160,160):.0f} {r.uniform(-90,10):.0f}" stroke="#ffb27a" stroke-width="{r.uniform(.6,2):.1f}" opacity=".7"/>' for _ in range(30))
    # orbital platform at top
    s+='<path d="M250 10 L350 10 L330 30 L270 30 Z" fill="#8a96aa" stroke="#1a2230"/><rect x="200" y="14" width="40" height="6" fill="#4a5668"/><rect x="360" y="14" width="40" height="6" fill="#4a5668"/>'
    return s+tail(.1)
def wing():
    r=random.Random(111)
    ex='''<linearGradient id="fh" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#eef3fa"/><stop offset="1" stop-color="#5a667a"/></linearGradient>
<radialGradient id="fe" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#fff"/><stop offset=".35" stop-color="#ff9a4a"/><stop offset="1" stop-color="#ff5a1a" stop-opacity="0"/></radialGradient>
<linearGradient id="ft" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ff9a4a" stop-opacity="0"/><stop offset="1" stop-color="#ffb46a" stop-opacity=".9"/></linearGradient>'''
    s=hdr(111,ex)+space_bg(r,111,('#6a1a4a','#1a2a6a','#0a4a5a'))
    def fighter(x,y,sc,rot):
        return f'''<g transform="translate({x} {y}) rotate({rot}) scale({sc})"><rect x="-220" y="-5" width="200" height="10" fill="url(#ft)"/><circle cx="-18" cy="0" r="14" fill="url(#fe)"/>
<path d="M-20 -6 L60 -2 L90 0 L60 2 L-20 6 Z" fill="url(#fh)" stroke="#1a2230" stroke-width="1"/><path d="M0 -4 L20 -40 L34 -40 L30 -4 Z M0 4 L20 40 L34 40 L30 4 Z" fill="#c25a1e" stroke="#1a2230" stroke-width="1"/>
<path d="M44 -2 L62 -1 L62 1 L44 2 Z" fill="#7ad8ff"/></g>'''
    for x,y,sc,rot in [(380,140,1.0,-12),(250,200,.8,-12),(470,230,.75,-12),(160,120,.55,-12),(320,300,.6,-12)]:
        s+=fighter(x,y,sc,rot)
    s+='<path d="M600 60 L420 110" stroke="#3affd0" stroke-width="2" opacity=".8"/><path d="M600 260 L500 250" stroke="#3affd0" stroke-width="2" opacity=".8"/>'
    s+='<circle cx="80" cy="360" r="22" fill="#ffd27a" opacity=".6" filter="url(#b10)"/><circle cx="80" cy="360" r="6" fill="#fff"/>'
    return s+tail(.08)
def helios():
    r=random.Random(121)
    ex='''<radialGradient id="sun" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#ffffff"/><stop offset=".15" stop-color="#fff2c0"/><stop offset=".45" stop-color="#ffb24a" stop-opacity=".55"/><stop offset="1" stop-color="#ff7a1a" stop-opacity="0"/></radialGradient>
<linearGradient id="ringG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2a3242"/><stop offset=".5" stop-color="#c8d2e0"/><stop offset="1" stop-color="#2a3242"/></linearGradient>
<linearGradient id="pan" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1a3a8a"/><stop offset="1" stop-color="#0a1a4a"/></linearGradient>'''
    s=hdr(121,ex)+space_bg(r,121,('#2a1a5a','#5a2a1a','#0a2a4a'))
    s+='<circle cx="430" cy="150" r="220" fill="url(#sun)"/>'
    for a in range(0,360,30): s+=f'<path d="M430 150 L{430+330*math.cos(math.radians(a)):.0f} {150+330*math.sin(math.radians(a)):.0f}" stroke="#ffe2a0" stroke-width="1" opacity=".18"/>'
    # ring station
    s+='<ellipse cx="270" cy="250" rx="200" ry="70" fill="none" stroke="url(#ringG)" stroke-width="22"/><ellipse cx="270" cy="250" rx="200" ry="70" fill="none" stroke="#ffd98a" stroke-width="1.5" opacity=".6" transform="translate(0 -10)"/>'
    s+=''.join(f'<rect x="{270+200*math.cos(a)-3:.1f}" y="{250+70*math.sin(a)-4:.1f}" width="6" height="3" fill="#ffd98a"/>' for a in [i/40*2*math.pi for i in range(40)])
    s+='<rect x="262" y="150" width="16" height="200" fill="url(#ringG)"/><rect x="236" y="214" width="68" height="72" rx="10" fill="url(#ringG)" stroke="#1a2230" stroke-width="2"/>'
    s+=''.join(f'<rect x="{x}" y="{y}" width="4" height="3" fill="#7ad8ff"/>' for x in range(244,300,10) for y in range(224,280,12))
    for side in [-1,1]:
        for k in range(3):
            x=270+side*(120+k*46);s+=f'<rect x="{x-20}" y="{140-k*6}" width="40" height="26" fill="url(#pan)" stroke="#7a96d8" stroke-width="1"/>'+''.join(f'<path d="M{x-20+j*10} {140-k*6} V{166-k*6}" stroke="#7a96d8" stroke-width=".5"/>' for j in range(1,4))
        s+=f'<path d="M270 153 L{270+side*210} 147" stroke="#8a96aa" stroke-width="2"/>'
    s+='<circle cx="430" cy="150" r="10" fill="#fff"/><circle cx="330" cy="210" r="8" fill="#ffe2a0" opacity=".5"/><circle cx="210" cy="300" r="14" fill="#ffe2a0" opacity=".25"/><circle cx="130" cy="360" r="22" fill="none" stroke="#ffe2a0" stroke-width="2" opacity=".25"/>'
    return s+tail(.08)

ARTS={'tw-warden':warden,'tw-collar':collar,'tw-flood':flood,'tw-wren':wren,'tw-choice':choice,'tw-orderly':orderly,
      'sf-leviathan':leviathan,'sf-talon':talon,'sf-ilsa':ilsa,'sf-lance':lance,'sf-wing':wing,'sf-helios':helios}
for k,f in ARTS.items():
    open(f'/home/claude/cardgame/art/{k}.svg','w').write(f())
print('wrote',len(ARTS))
