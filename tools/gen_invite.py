"""Genera la página «<DJ> invites you» y la historia 1080x1920 para un DJ.
Uso: python tools/gen_invite.py <slug> "<NOMBRE DJ>" <enlace_rastreable> [@instagram]
Ej.:  python tools/gen_invite.py jhon "JHON BARRERA" https://www.fourvenues.com/l/n89p @jhon_barrera_dj
Crea <slug>/index.html (shemovesfirst.eu/<slug>) y <slug>/story.jpg."""
import sys, os, html
from PIL import Image, ImageDraw, ImageFont, ImageFilter
slug, name, link = sys.argv[1], sys.argv[2], sys.argv[3]
ig = sys.argv[4] if len(sys.argv) > 4 else ''
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = os.path.join(ROOT, slug); os.makedirs(out, exist_ok=True)
N = html.escape(name)

page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{N} invites you · She Moves First · Halloween</title>
<meta name="description" content="{N} invites you to She Moves First · Halloween Edition. Saturday 31 October 2026, Basement Amsterdam, 22:00–04:00.">
<meta property="og:title" content="{N} invites you · She Moves First Halloween">
<meta property="og:description" content="Sat 31.10 · Basement Amsterdam · Latin house, Afrohouse, Tech house, Reggaeton">
<meta property="og:image" content="https://shemovesfirst.eu/{slug}/story.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&family=Instrument+Sans:wght@400..700&display=swap" rel="stylesheet">
<style>
:root{{--black:#08070A;--paper:#0F0D13;--line:#272232;--muted:#948FA0;--pink:#E0122F;--white:#fff;--display:"Archivo","Arial Narrow",Impact,sans-serif;--sans:"Instrument Sans","Helvetica Neue",Arial,sans-serif}}
*{{box-sizing:border-box}}html,body{{margin:0;background:var(--black);color:var(--white);font:16px/1.5 var(--sans)}}
.w{{max-width:520px;margin:0 auto;padding:28px 16px 40px;min-height:100svh;display:flex;flex-direction:column}}
.kick{{font-family:var(--display);font-variation-settings:"wdth" 80;text-transform:uppercase;color:var(--muted);letter-spacing:.08em;font-size:14px;margin:0}}
h1{{font-family:var(--display);font-variation-settings:"wdth" 70;font-weight:900;font-size:clamp(54px,17vw,92px);line-height:.86;margin:10px 0 2px;text-transform:uppercase}}
h1 span{{display:block;color:var(--pink);font-size:.46em;line-height:1;margin-top:10px;font-weight:800;letter-spacing:.01em}}
.ig{{color:var(--muted);text-decoration:none;font-size:14px}}
.poster{{width:100%;border-radius:14px;margin:22px 0 18px;display:block;border:1px solid var(--line)}}
.facts{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:0 0 22px}}
.f{{background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:12px 14px}}
.f b{{display:block;font-family:var(--display);font-variation-settings:"wdth" 80;font-size:22px;line-height:1.1}}.f span{{color:var(--muted);font-size:13px}}
.cta{{display:block;text-align:center;background:var(--pink);color:#fff;text-decoration:none;font-family:var(--display);font-variation-settings:"wdth" 85;font-weight:800;font-size:22px;padding:18px;border-radius:14px;text-transform:uppercase;letter-spacing:.02em}}
.cta:focus-visible{{outline:3px solid #fff;outline-offset:3px}}
.small{{color:var(--muted);font-size:13px;text-align:center;margin:12px 0 0}}
</style></head><body><main class="w">
<p class="kick">Personal invitation</p>
<h1>{N}<span>invites you</span></h1>
{f'<a class="ig" href="https://instagram.com/{ig.lstrip("@")}" target="_blank" rel="noopener">{html.escape(ig)}</a>' if ig else ''}
<img class="poster" src="../halloween-31-10-2026.jpg?v=2" width="1100" height="1375" alt="She Moves First · Halloween Edition · 31.10.2026 · Basement Amsterdam">
<div class="facts">
 <div class="f"><b>Sat 31 Oct</b><span>22:00 – 04:00</span></div>
 <div class="f"><b>Basement</b><span>Leidseplein 19, Amsterdam</span></div>
 <div class="f"><b>Free</b><span>Ladies in costume until 01:00</span></div>
 <div class="f"><b>€10</b><span>Early Bird until Fri 30 · door €15</span></div>
</div>
<a class="cta" href="{html.escape(link)}">Claim your invite</a>
<p class="small">Latin house · Afrohouse · Tech house · Reggaeton · 18+ with valid ID · Costumes encouraged</p>
</main></body></html>"""
open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(page)

# Historia 1080x1920
W, H = 1080, 1920
F = '/System/Library/Fonts/Supplemental/'
def font(name, size):
    for p in [F + name, '/System/Library/Fonts/' + name]:
        if os.path.exists(p): return ImageFont.truetype(p, size)
    return ImageFont.load_default()
bg = Image.open(os.path.join(ROOT, 'halloween-31-10-2026.jpg')).convert('RGB')
blur = bg.resize((W, int(W * bg.height / bg.width))).filter(ImageFilter.GaussianBlur(40))
im = Image.new('RGB', (W, H), (8, 7, 10)); im.paste(blur.resize((W, H)), (0, 0))
im = Image.blend(im, Image.new('RGB', (W, H), (8, 7, 10)), 0.55)
poster = bg.resize((860, int(860 * bg.height / bg.width)), Image.LANCZOS)
px, py = (W - poster.width) // 2, 560
im.paste(poster, (px, py))
d = ImageDraw.Draw(im)
big = font('Impact.ttf', 150); mid = font('Impact.ttf', 78); sm = font('DIN Condensed Bold.ttf', 50)
def center(t, f, y, fill):
    w = d.textlength(t, font=f); d.text(((W - w) / 2, y), t, font=f, fill=fill)
center('PERSONAL INVITATION', sm, 150, (148, 143, 160))
size = 150
while d.textlength(name.upper(), font=font('Impact.ttf', size)) > W - 120: size -= 6
center(name.upper(), font('Impact.ttf', size), 215, (255, 255, 255))
center('INVITES YOU', mid, 215 + size + 10, (224, 18, 47))
by = py + poster.height + 50
center('SAT 31 OCT · BASEMENT AMSTERDAM', sm, by, (255, 255, 255))
center('TAP THE LINK', font('DIN Condensed Bold.ttf', 56), by + 70, (224, 18, 47))
center('FREE FOR LADIES IN COSTUME UNTIL 01:00', font('DIN Condensed Bold.ttf', 38), by + 135, (148, 143, 160))
im.save(os.path.join(out, 'story.jpg'), quality=92)
print('ok ->', out)
