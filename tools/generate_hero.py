"""Gera o GIF original do perfil. Requer Python 3 e Pillow: pip install Pillow."""
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
W, H = 1200, 590
BG = '#0c1017'
FG = '#eee9df'
BLUE = '#6daaff'
MUTED = '#91a0b5'
GREEN = '#86d8b0'
FONT_DIR = Path('/usr/share/fonts/truetype/dejavu')

def font(size, bold=False, mono=False):
    name = 'DejaVuSansMono' if mono else 'DejaVuSans'
    if bold: name += '-Bold'
    for p in [FONT_DIR / (name + '.ttf'), Path(name + '.ttf')]:
        try: return ImageFont.truetype(str(p), size)
        except OSError: pass
    raise RuntimeError('Instale as fontes DejaVu Sans / DejaVu Sans Mono ou ajuste FONT_DIR.')

f12, f14, f16 = font(12, mono=True), font(14, mono=True), font(16)
f19, f24, f48 = font(19, True), font(24, True), font(48, True)

# Caminhos desenhados como uma integração; representam a stack, não telemetria real.
paths = [
    ([(254,337),(335,337),(385,395),(461,395)], BLUE),
    ([(254,465),(335,465),(385,413),(461,413)], '#b3a0f0'),
    ([(739,395),(811,395),(857,337),(941,337)], GREEN),
    ([(739,413),(811,413),(857,465),(941,465)], '#e8c17a'),
]

def along(points, ratio):
    lens = [math.dist(a,b) for a,b in zip(points,points[1:])]
    target = max(0,min(1,ratio))*sum(lens)
    for a,b,l in zip(points,points[1:],lens):
        if target <= l:
            q=target/l
            return (a[0]+(b[0]-a[0])*q,a[1]+(b[1]-a[1])*q)
        target -= l
    return points[-1]

def partial(d, points, amount, color, width=4):
    lens = [math.dist(a,b) for a,b in zip(points,points[1:])]
    remain=max(0,min(1,amount))*sum(lens)
    for a,b,l in zip(points,points[1:],lens):
        if remain <= 0: break
        q=min(1,remain/l)
        end=(a[0]+(b[0]-a[0])*q,a[1]+(b[1]-a[1])*q)
        d.line([a,end],fill=color,width=width)
        remain-=l

def label(d, xy, text, ft, color=FG):
    d.text(xy,text,font=ft,fill=color)

def centered(d, x,y,text,ft,color=FG):
    box=d.textbbox((0,0),text,font=ft)
    label(d,(x-(box[2]-box[0])/2,y),text,ft,color)

def card(d, box, kicker, title, subtitle, color, active):
    d.rounded_rectangle(box,14,fill='#121b29',outline=color if active else '#293547',width=2)
    x,y,_,_=box
    label(d,(x+18,y+12),kicker,f12,color)
    label(d,(x+18,y+32),title,f19)
    label(d,(x+18,y+59),subtitle,f12,MUTED)

frames=[]
for i in range(110):
    t=i/109
    img=Image.new('RGB',(W,H),BG)
    d=ImageDraw.Draw(img)
    d.rounded_rectangle((1,1,W-2,H-2),22,outline='#2a3545',width=2)
    # Pontos discretos no fundo.
    for x in range(30,W-20,24):
        for y in range(88,H-20,24):
            d.ellipse((x,y,x+1,y+1),fill='#1a2331')
    d.line((1,52,W-2,52),fill='#283344',width=1)
    for x,c in [(28,'#ec737a'),(49,'#e8c17a'),(70,GREEN)]:
        d.ellipse((x,21,x+10,31),fill=c)
    label(d,(99,17),'ca10v1ana / construindo conexões',f14,MUTED)
    label(d,(1025,17),'PROFILE.md',f12,MUTED)
    label(d,(52,91),'OLÁ, EU SOU',f14,BLUE)
    label(d,(48,118),'Caio Viana',f48)
    label(d,(52,185),'Transformando ideias em soluções digitais.',f24)
    label(d,(52,230),'Desenvolvimento Full Stack  /  Fortaleza, CE',f16,MUTED)
    d.line((52,276,1148,276),fill='#253045',width=1)
    for idx,(points,c) in enumerate(paths):
        d.line(points,fill='#283447',width=4)
        progress=min(1,max(0,(t-0.10-idx*0.065)/0.28))
        partial(d,points,progress,c)
        if progress>=1:
            pos=along(points,((t-0.35)*2+idx*0.23)%1)
            x,y=pos
            d.ellipse((x-8,y-8,x+8,y+8),fill='#22334b')
            d.ellipse((x-4,y-4,x+4,y+4),fill=c)
    card(d,(52,293,254,381),'01 / INTERFACE','Angular + React','TypeScript',BLUE,t>.08)
    card(d,(52,421,254,509),'02 / AMBIENTE','Docker','Git + GitHub','#b3a0f0',t>.15)
    card(d,(941,293,1148,381),'03 / DADOS','PostgreSQL','Modelagem de dados',GREEN,t>.22)
    card(d,(941,421,1148,509),'04 / PROJETOS','Ideias reais','Soluções para negócios','#e8c17a',t>.29)
    d.rounded_rectangle((461,327,739,477),18,fill='#162338',outline=BLUE if t>.35 else '#34445b',width=2)
    centered(d,600,336,'< DV />',f24,BLUE)
    centered(d,600,371,'DEV VIANA',f19)
    centered(d,600,404,'Java + Spring Boot',f14)
    centered(d,600,442,'DESENVOLVENDO SOLUÇÕES',f12,MUTED)
    # Terminal: linhas surgem uma a uma e seguram a cena final.
    status=[('> estruturando a interface',BLUE),('> conectando a API e os dados',BLUE),('> transformando ideias em soluções',GREEN)]
    idx=0 if t<.23 else 1 if t<.52 else 2
    line,col=status[idx]
    d.rounded_rectangle((52,538,1148,573),8,fill='#121b29')
    label(d,(66,546),line + (' _' if i//5%2==0 else ''),f14,col)
    label(d,(1017,548),'DEV VIANA',f12,MUTED)
    frames.append(img)

out=ROOT/'assets'/'hero-integracao.gif'
out.parent.mkdir(parents=True,exist_ok=True)
# Paleta única mantém as cores estáveis entre os quadros.
palette=frames[-1].quantize(colors=128)
indexed=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
indexed[0].save(out,save_all=True,append_images=indexed[1:],duration=90,loop=0,optimize=True,disposal=1)
frames[-1].save(ROOT/'assets'/'hero-integracao.png')
print(f'GIF: {out.stat().st_size:,} bytes | {len(frames)} quadros | 9,9 segundos | loop infinito')
