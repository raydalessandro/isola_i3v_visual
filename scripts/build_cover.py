#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_cover.py — Generatore copertina KDP per "L'Isola dei Tre Venti".

Costruisce via codice (zero testo baked):
  - FRONTE: titolo + Volume N + sottotitolo del vento + autore + Spirale Editrice
  - DORSO : azzurro del vento con numero, titolo verticale, autore, logo spirale
  - QUARTA: 4 varianti -> 'collana' (vignetta personaggi) | isola 'A' cartolina |
            isola 'B' veduta a tutta pagina | isola 'C' oblo
  - WRAP  : quarta + dorso + fronte montati per KDP (A5 + bleed 3,175 mm)

Dipendenze: Pillow + scripts/design_system.py (palette, font, glifi camuni).
Uso:        python3 scripts/build_cover.py
Config:     vedi blocco CONFIG qui sotto.
"""
import sys, math, os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]          # radice repo (scripts/ sta sotto root)
sys.path.insert(0, str(ROOT/"scripts"))
import design_system as ds

# ─────────────────────────── CONFIG ───────────────────────────
# >>> per passare a un altro volume cambia SOLO questo numero <<<
CURRENT_VOLUME = 1

OUT          = ROOT/"output/copertina"
ASSET_ISLAND = ROOT/"visual/atlante/mappe/isola_aerea_v1.jpg"   # mappa isola: UGUALE per tutti i volumi

# --- stile della collana (uguale per tutti i volumi) ---
AUTHOR       = "Beatrice Mercuri"       # autore UFFICIALE
BYLINE_MODE  = "single"                 # "single" | "trio"
TRIO_NAMES   = ("Lucio", "Vincenzo", "Renato")   # (opzione terzetto, non in uso)
TRIO_SURNAME = "Mercuri"
TITLE_STYLE  = "T3"                     # T1 Fraunces sobrio | T2 terracotta | T3 Fredoka | T4 +fioritura
BACK_STYLE   = "island_C"               # collana | island_A | island_B | island_C
SUBTITLE_POS = "top"                    # "top" | "bottom" — posizione del sottotitolo del vento
PUBLISHER_FRONT = "logo"                # "none" | "logo" (solo sigillo) | "full" (sigillo + testo)
TITLE_TOP, SUB_Y = 0.058, 0.864
SPINE_MM     = 6.4                      # PROVVISORIA per volume: ricalcolare da pagine + carta

# --- dati PER VOLUME --- (titolo saga e mappa isola restano uguali; cambiano numero, vento, immagine, storie)
# Volumi 2-4 = SEGNAPOSTO: quando li produci aggiorna immagine pulita, sottotitolo del vento e le 3 storie.
VOLUMES = {
    1: dict(cover="visual/atlante/emblema/copertina_clean_v2.png",  wind="taglio",
            subtitle="IL VENTO CHE TAGLIA",    vento="Vento Taglio",    ordinale="primo",
            stories=("La Nebbia delle Montagne Gemelle","Il Riflesso nella Pozza","Il Pallone oltre la Foresta")),
    2: dict(cover="visual/atlante/emblema/copertina_clean_vol2.png", wind="intreccio",
            subtitle="IL VENTO CHE INTRECCIA", vento="Vento Intreccio", ordinale="secondo",
            stories=("(storia 4 — da definire)","(storia 5 — da definire)","(storia 6 — da definire)")),
    3: dict(cover="visual/atlante/emblema/copertina_clean_vol3.png", wind="mulinello",
            subtitle="IL VENTO CHE CAPOVOLGE", vento="Vento Mulinello", ordinale="terzo",
            stories=("(storia 7 — da definire)","(storia 8 — da definire)","(storia 9 — da definire)")),
    4: dict(cover="visual/atlante/emblema/copertina_clean_vol4.png", wind="autunno",
            subtitle="IL VENTO CHE TIENE",     vento="Vento d'Autunno", ordinale="quarto",
            stories=("(storia 10 — da definire)","(storia 11 — da definire)","(storia 12 — da definire)")),
}

# ─────────────────────────── GEOMETRIA ───────────────────────────
DPI = 200; MM = DPI/25.4; PT = DPI/72.0
TRIM_W, TRIM_H, BLEED = 148.0, 210.0, 3.175
A5 = TRIM_H/TRIM_W
def px(mm): return round(mm*MM)
def pt(p):  return round(p*PT)
H, BACK_W, SPINE_W, FRONT_W = px(TRIM_H+2*BLEED), px(BLEED+TRIM_W), px(SPINE_MM), px(TRIM_W+BLEED)
W = BACK_W+SPINE_W+FRONT_W
SAFE, BL = px(9), px(BLEED)

PAPER, PAPER_DEEP, INK, INK_SOFT, INK_FAINT = ds.PAPER, ds.PAPER_DEEP, ds.INK, ds.INK_SOFT, ds.INK_FAINT
SPIR, TAGLIO, INTRECCIO, MULINELLO = ds.SPIRALE, ds.VENTO_TAGLIO, ds.VENTO_INTRECCIO, ds.VENTO_MULINELLO
ACCENT, RULE = ds.ACCENT, ds.RULE
BROWN, CREAM, DK, SUB_STROKE = (78,52,30), PAPER, (16,22,30), (16,24,36)

# ─── risoluzione del volume corrente (deriva da VOLUMES[CURRENT_VOLUME]) ───
WIND_COLORS = {"taglio":TAGLIO, "intreccio":INTRECCIO, "mulinello":MULINELLO, "autunno":ACCENT}
_V          = VOLUMES[CURRENT_VOLUME]
VOLUME      = str(CURRENT_VOLUME)
SUBTITLE    = _V["subtitle"]
WIND        = WIND_COLORS[_V["wind"]]            # colore-vento del volume corrente (dorso, accenti, anello…)
ASSET_COVER = ROOT/_V["cover"]
STORIE      = _V["stories"]

# ─────────────────────────── TIPOGRAFIA ───────────────────────────
def F(which, size_pt, weight=None):
    s = pt(size_pt); return ds.font_weighted(which, s, weight) if weight else ds.font(which, s)
def tw(d,s,f): b=d.textbbox((0,0),s,font=f); return b[2]-b[0]
def th(d,s,f): b=d.textbbox((0,0),s,font=f); return b[3]-b[1], b[1]
def wrap(d,s,f,maxw):
    out,line=[],""
    for word in s.split():
        t=(line+" "+word).strip()
        if tw(d,t,f)<=maxw: line=t
        else:
            if line: out.append(line)
            line=word
    if line: out.append(line)
    return out
def center(d,s,cy,f,fill,pw,x0=0,stroke=0,sfill=None):
    w=tw(d,s,f); b=d.textbbox((0,0),s,font=f)
    d.text((x0+(pw-w)//2,cy-b[1]),s,font=f,fill=fill,stroke_width=stroke,stroke_fill=sfill); return b[3]-b[1]
def tracked(d,s,cx,cy,f,fill,sp,stroke=0,sfill=None):
    ws=[tw(d,c,f) for c in s]; tot=sum(ws)+sp*(len(s)-1); x=cx-tot/2
    b0=d.textbbox((0,0),"Hg",font=f)
    for c,w in zip(s,ws): d.text((x,cy-b0[1]),c,font=f,fill=fill,stroke_width=stroke,stroke_fill=sfill); x+=w+sp
def para(d,lines,x,y,f,fill,lead,stroke=0,sfill=None):
    for ln in lines: d.text((x,y),ln,font=f,fill=fill,stroke_width=stroke,stroke_fill=sfill); y+=lead
    return y
def vstrip(text,f,fill):
    tmp=Image.new("RGBA",(10,10),(0,0,0,0)); b=ImageDraw.Draw(tmp).textbbox((0,0),text,font=f)
    img=Image.new("RGBA",(b[2]-b[0]+4,b[3]-b[1]+4),(0,0,0,0))
    ImageDraw.Draw(img).text((2-b[0],2-b[1]),text,font=f,fill=fill)
    return img.rotate(-90,expand=True)

def band(canvas,cover,box,focus=0.50,feather=14):
    x0,y0,x1,y1=box; bw,bh=x1-x0,y1-y0; iw,ih=cover.size
    s=max(bw/iw,bh/ih); nw,nh=int(iw*s),int(ih*s); r=cover.resize((nw,nh),Image.LANCZOS)
    cx0=(nw-bw)//2; cy0=int(focus*nh-bh/2); cy0=max(0,min(nh-bh,cy0))
    crop=r.crop((cx0,cy0,cx0+bw,cy0+bh))
    m=Image.new("L",(bw,bh),0); ImageDraw.Draw(m).rounded_rectangle([feather,feather,bw-feather,bh-feather],radius=feather,fill=255)
    canvas.paste(crop,(x0,y0),m.filter(ImageFilter.GaussianBlur(feather*0.6)))

def barcode(d,pw,ph):
    bw,bh=px(45),px(26); x1,y1=pw-SAFE,ph-BL-SAFE; x0,y0=x1-bw,y1-bh
    d.rectangle([x0,y0,x1,y1],fill=(255,255,255),outline=RULE,width=1)
    d.text((x0+px(4),y0+px(4)),"spazio codice\na barre (KDP)",font=F("sans",5.4,600),fill=INK_FAINT)

def spirale_footer(d,L,col=INK_SOFT,stroke=0):
    ds.draw_spirale_logo(d,L+px(7),H-BL-SAFE-px(7),px(6),SPIR if col==INK_SOFT else col,0)
    d.text((L+px(18),H-BL-SAFE-px(10)),"Spirale Editrice",font=F("sans",8.2,800),fill=col,
           stroke_width=stroke,stroke_fill=DK if stroke else None)

# ─────────────────────────── TESTI ───────────────────────────
HOOK  = "Su un'isola in mezzo al mare soffiano tre venti."
BLURB = ("Uno separa le cose, uno le unisce, uno le capovolge. Ci vivono animali che "
         "parlano e tre fratelli diversi in tutto: Gabriel decide, Elias parla con tutti, "
         "Noah trova ciò che nessuno aveva visto.")
INTRO = f"In questo {_V['ordinale']} volume soffia il {_V['vento']}. Tre storie da leggere ad alta voce:"
SAGA  = "Una saga in quattro volumi e dodici storie, una per ogni stagione. Da leggere oggi, da ritrovare crescendo."

# ─────────────────────────── FRONTE ───────────────────────────
def crop_a5(im, top_cut=78):
    w,h=im.size; nh=round(w*A5); return im.crop((0,top_cut,w,top_cut+nh))

def draw_title(d,cx,top,style,Wc):
    big=int(Wc*0.132); sml=int(Wc*0.086)
    if style=="T3":
        fb=ds.font("mark",big); fs=ds.font("mark",sml); fill=BROWN; dei=WIND; stroke=int(big*0.05)
    else:
        wB=560 if style=="T2" else 520
        fb=ds.font_weighted("display",big,wB); fs=ds.font("display_i",sml)
        fill=ACCENT if style=="T2" else BROWN; dei=fill; stroke=int(big*0.045)
    s1a,s1b="L'Isola"," dei"
    wa=tw(d,s1a,fb); wb=tw(d,s1b,fs); ha,oa=th(d,s1a,fb); hb,ob=th(d,s1b,fs)
    base=top+ha; x1=cx-(wa+wb)//2
    d.text((x1,base-ha-oa),s1a,font=fb,fill=fill,stroke_width=stroke,stroke_fill=PAPER)
    d.text((x1+wa,base-hb-ob),s1b,font=fs,fill=dei,stroke_width=max(0,stroke-2),stroke_fill=PAPER)
    s2="Tre Venti"; w2=tw(d,s2,fb); h2,o2=th(d,s2,fb); y2=base+int(big*0.12)
    d.text((cx-w2//2,y2-o2),s2,font=fb,fill=fill,stroke_width=stroke,stroke_fill=PAPER)
    yend=y2+h2
    if style=="T4":
        ds.draw_wind_rule(d,int(cx-w2*0.32),int(cx+w2*0.32),yend+int(big*0.10),WIND,5)
        r=int(big*0.06)
        ds.small_spiral(d,int(cx-w2*0.40),yend+int(big*0.10),r,ACCENT,4)
        ds.small_spiral(d,int(cx+w2*0.40),yend+int(big*0.10),r,ACCENT,4,mirror=True)
        yend+=int(big*0.16)
    return yend

def build_front(style=TITLE_STYLE, title_top=TITLE_TOP, sub_y=SUB_Y):
    im=crop_a5(Image.open(ASSET_COVER).convert("RGB")); Wc,Hc=im.size; d=ImageDraw.Draw(im); cx=Wc//2
    yend=draw_title(d,cx,int(Hc*title_top),style,Wc)
    sw=max(2,int(Hc*0.0016)); vf=F("sans",10.0,700); vt=f"VOLUME {VOLUME}"

    if SUBTITLE_POS=="top":
        # ── blocco identità sotto il titolo: VOLUME N + vento + fioritura ──
        vy=yend+int(Hc*0.010)
        tracked(d,vt,cx,vy,vf,BROWN,int(Wc*0.010),stroke=3,sfill=PAPER)
        subf=F("sans",11.8,800); sp=int(Wc*0.0095)
        sy=vy+int(Hc*0.030)
        tracked(d,SUBTITLE,cx,sy,subf,WIND,sp,stroke=sw,sfill=SUB_STROKE)
        subw=sum(tw(d,c,subf) for c in SUBTITLE)+sp*(len(SUBTITLE)-1)
        fy=sy+int(Hc*0.026)
        ds.draw_wind_rule(d,int(cx-subw*0.30),int(cx+subw*0.30),fy,WIND,4)
        ds.small_spiral(d,int(cx-subw*0.40),fy,int(Hc*0.006),ACCENT,3)
        ds.small_spiral(d,int(cx+subw*0.40),fy,int(Hc*0.006),ACCENT,3,mirror=True)
    else:
        vy=yend+int(Hc*0.012); vw=tw(d,vt,vf)
        ds.draw_wind_rule(d,int(cx-vw*0.62-Wc*0.045),int(cx-vw*0.62-Wc*0.006),int(vy+Hc*0.009),WIND,3)
        ds.draw_wind_rule(d,int(cx+vw*0.62+Wc*0.006),int(cx+vw*0.62+Wc*0.045),int(vy+Hc*0.009),WIND,3)
        tracked(d,vt,cx,vy,vf,BROWN,int(Wc*0.010),stroke=3,sfill=PAPER)
        tracked(d,SUBTITLE,cx,int(Hc*sub_y),F("sans",11.3,800),WIND,int(Wc*0.0095),stroke=sw,sfill=SUB_STROKE)

    # ── firma in basso ──
    if BYLINE_MODE=="trio":
        tracked(d," · ".join(n.upper() for n in TRIO_NAMES),cx,int(Hc*0.905),ds.font_weighted("sans",int(Hc*0.0150),700),INK,int(Wc*0.006),stroke=3,sfill=PAPER)
        tracked(d,TRIO_SURNAME.upper(),cx,int(Hc*0.929),ds.font_weighted("display",int(Hc*0.0260),560),INK,int(Wc*0.012),stroke=4,sfill=PAPER)
        last=int(Hc*0.929)+int(Hc*0.028)
    else:
        tracked(d,AUTHOR.upper(),cx,int(Hc*0.905),ds.font_weighted("display",int(Hc*0.0265),560),INK,int(Wc*0.006),stroke=4,sfill=PAPER)
        last=int(Hc*0.905)+int(Hc*0.028)
    if PUBLISHER_FRONT=="full":
        sf=ds.font_weighted("display",int(Hc*0.0175),500); st="Spirale Editrice"; stw=tw(d,st,sf)
        ds.small_spiral(d,int(cx-stw*0.5-Wc*0.030),last+int(Hc*0.004),int(Hc*0.0072),SPIR,3)
        ds.small_spiral(d,int(cx+stw*0.5+Wc*0.030),last+int(Hc*0.004),int(Hc*0.0072),SPIR,3,mirror=True)
        center(d,st,last,sf,INK,Wc,stroke=4,sfill=PAPER)
    elif PUBLISHER_FRONT=="logo":
        r=int(Hc*0.013); cyl=last+int(Hc*0.013)
        ds.draw_spirale_logo(d,cx,cyl,r,PAPER,width=max(3,r//12)+5)   # contorno crema che segue la spirale
        ds.draw_spirale_logo(d,cx,cyl,r,SPIR,width=max(2,r//12))
    return im

# ─────────────────────────── DORSO ───────────────────────────
def spine(author=None):
    author = author or (TRIO_SURNAME if BYLINE_MODE=="trio" else AUTHOR)
    img=Image.new("RGB",(SPINE_W,H),WIND); d=ImageDraw.Draw(img); cx=SPINE_W//2
    fn=ds.font_weighted("mark",int(SPINE_W*0.80),600); bn=d.textbbox((0,0),VOLUME,font=fn)
    d.text((cx-(bn[2]-bn[0])//2-bn[0],BL+px(5)-bn[1]),VOLUME,font=fn,fill=PAPER)
    st=vstrip("L'Isola dei Tre Venti",ds.font_weighted("display",int(SPINE_W*0.42),600),PAPER)
    img.paste(st,(cx-st.width//2,px(40)),st)
    sa=vstrip(author.upper(),ds.font_weighted("sans",int(SPINE_W*0.26),700),(238,231,217))
    img.paste(sa,(cx-sa.width//2,px(40)+st.height+px(10)),sa)
    lr=int(SPINE_W*0.30)
    ds.draw_spirale_logo(d,cx,H-BL-px(6)-lr,lr,PAPER,0)
    sp=vstrip("SPIRALE EDITRICE",ds.font_weighted("sans",int(SPINE_W*0.20),700),PAPER)
    img.paste(sp,(cx-sp.width//2,H-BL-px(6)-2*lr-px(5)-sp.height),sp)
    return img

# ─────────────────────────── QUARTE ───────────────────────────
def back_collana(focus=0.60):
    """Finalista #1: vignetta a banda con i protagonisti (dall'illustrazione pulita)."""
    img=Image.new("RGB",(BACK_W,H),PAPER_DEEP); d=ImageDraw.Draw(img)
    L=BL+SAFE; Rr=BACK_W-SAFE; cw=Rr-L; cx=(L+Rr)//2
    cov=Image.open(ASSET_COVER).convert("RGB")
    vbox=(L+px(4),BL+px(9),Rr-px(4),BL+px(9)+px(46)); band(img,cov,vbox,focus=focus,feather=px(7))
    ds.cornice_angoli_vento(d,vbox,WIND,2,px(7)); y=vbox[3]+px(11)
    tracked(d,f"VOLUME {VOLUME}   ·   {SUBTITLE}",cx,y,F("sans",7.6,800),WIND,px(1.3)); y+=px(12)
    fh=F("display",16,600)
    for ln in wrap(d,HOOK,fh,cw): center(d,ln,y,fh,INK,cw,x0=L); y+=pt(18)
    y+=px(5); fb=F("serif",9.6,450)
    y=para(d,wrap(d,BLURB,fb,cw),L,y,fb,INK_SOFT,pt(13.6)); y+=px(5)
    fi=F("serif_i",9.6); y=para(d,wrap(d,INTRO,fi,cw),L,y,fi,INK,pt(13.6)); y+=px(4)
    fl=F("serif",10,520)
    for t in STORIE:
        ds.small_spiral(d,L+px(4),y+px(4),px(3),ACCENT,2); d.text((L+px(11),y-px(1)),t,font=fl,fill=INK); y+=pt(15.5)
    y+=px(5); fc=F("serif_i",9.2); y=para(d,wrap(d,SAGA,fc,cw),L,y,fc,INK_SOFT,pt(13))
    ky=y+px(8)
    for x,gf,c in zip((cx-px(32),cx,cx+px(32)),(ds.glifo_taglio,ds.glifo_intreccio,ds.glifo_mulinello),(TAGLIO,INTRECCIO,MULINELLO)):
        gf(d,x,ky,px(7),c,3)
    tracked(d,"4 VENTI   ·   4 VOLUMI   ·   12 STORIE",cx,ky+px(14),F("sans",7.2,700),INK_FAINT,px(1.1))
    center(d,"Dai 3 ai 6 anni",ky+px(24),F("mark",13,600),ACCENT,cw,x0=L)
    spirale_footer(d,L); barcode(d,BACK_W,H); return img

def _island_text_below(d,L,Rr,cw,cx,y):
    tracked(d,f"VOLUME {VOLUME}   ·   {SUBTITLE}",cx,y,F("sans",7.6,800),WIND,px(1.3)); y+=px(12)
    fh=F("display",15.5,600)
    for ln in wrap(d,HOOK,fh,cw): center(d,ln,y,fh,INK,cw,x0=L); y+=pt(17.5)
    y+=px(4); fb=F("serif",9.4,450); y=para(d,wrap(d,BLURB,fb,cw),L,y,fb,INK_SOFT,pt(13.2)); y+=px(6)
    fl=F("serif",9.6,520)
    for t in STORIE:
        ds.small_spiral(d,L+px(4),y+px(4),px(3),ACCENT,2); d.text((L+px(11),y-px(1)),t,font=fl,fill=INK); y+=pt(15)
    y+=px(8); center(d,"Dai 3 ai 6 anni",y,F("mark",13,600),ACCENT,cw,x0=L)
    spirale_footer(d,L); barcode(d,BACK_W,H)

def back_island_A():
    """Cartolina: grande veduta dell'isola incorniciata + testo sotto."""
    img=Image.new("RGB",(BACK_W,H),PAPER_DEEP); d=ImageDraw.Draw(img)
    L=BL+SAFE; Rr=BACK_W-SAFE; cw=Rr-L; cx=(L+Rr)//2
    vbox=(L,BL+px(7),Rr,BL+px(7)+px(86)); band(img,Image.open(ASSET_ISLAND).convert("RGB"),vbox,focus=0.52,feather=px(8))
    ds.cornice_angoli_vento(d,vbox,WIND,2,px(9))
    _island_text_below(d,L,Rr,cw,cx,vbox[3]+px(11)); return img

def back_island_C():
    """Oblo: l'isola dentro un cerchio + tre punti-vento ai cardinali."""
    img=Image.new("RGB",(BACK_W,H),PAPER_DEEP); d=ImageDraw.Draw(img)
    L=BL+SAFE; Rr=BACK_W-SAFE; cw=Rr-L; cx=(L+Rr)//2
    isl=Image.open(ASSET_ISLAND).convert("RGB"); R=px(44); cyc=BL+px(8)+R
    iw,ih=isl.size; s=(2*R)/min(iw,ih); nw,nh=int(iw*s),int(ih*s); rr=isl.resize((nw,nh),Image.LANCZOS)
    cx0=(nw-2*R)//2; cy0=max(0,min(nh-2*R,int(0.50*nh-R))); disc=rr.crop((cx0,cy0,cx0+2*R,cy0+2*R))
    m=Image.new("L",(2*R,2*R),0); ImageDraw.Draw(m).ellipse([3,3,2*R-3,2*R-3],fill=255)
    img.paste(disc,(cx-R,cyc-R),m.filter(ImageFilter.GaussianBlur(4)))
    d.ellipse([cx-R-px(3),cyc-R-px(3),cx+R+px(3),cyc+R+px(3)],outline=WIND,width=3)
    d.ellipse([cx-R-px(7),cyc-R-px(7),cx+R+px(7),cyc+R+px(7)],outline=WIND,width=1)
    rr2=R+px(7); rd=px(2.6)
    for ang,col in ((-90,TAGLIO),(150,INTRECCIO),(30,MULINELLO)):
        ax=cx+int(rr2*math.cos(math.radians(ang))); ay=cyc+int(rr2*math.sin(math.radians(ang)))
        d.ellipse([ax-rd,ay-rd,ax+rd,ay+rd],fill=col,outline=PAPER_DEEP,width=2)
    _island_text_below(d,L,Rr,cw,cx,cyc+R+px(16)); return img

def back_island_B():
    """Veduta dal mare: isola a tutta pagina, testo nel cielo e nel mare (contornato)."""
    isl=Image.open(ASSET_ISLAND).convert("RGB"); iw,ih=isl.size
    s=max(BACK_W/iw,H/ih); nw,nh=int(iw*s),int(ih*s); r=isl.resize((nw,nh),Image.LANCZOS)
    img=r.crop(((nw-BACK_W)//2,int((nh-H)*0.42),(nw-BACK_W)//2+BACK_W,int((nh-H)*0.42)+H)); d=ImageDraw.Draw(img)
    L=BL+SAFE; Rr=BACK_W-SAFE; cw=Rr-L; cx=(L+Rr)//2; so=px(0.6)
    y=BL+px(6)
    tracked(d,f"VOLUME {VOLUME}   ·   {SUBTITLE}",cx,y,F("sans",7.4,800),WIND,px(1.3),stroke=px(0.5),sfill=DK); y+=px(12)
    fh=F("display",16,700)
    for ln in wrap(d,HOOK,fh,cw): center(d,ln,y,fh,CREAM,cw,x0=L,stroke=px(0.7),sfill=DK); y+=pt(18)
    yb=H-BL-SAFE-px(78); fl=F("serif",9.8,560)
    for t in STORIE: center(d,t,yb,fl,CREAM,cw,x0=L,stroke=px(0.7),sfill=DK); yb+=pt(15.5)
    yb+=px(3); tracked(d,"4 VOLUMI · 12 STORIE · UNA PER STAGIONE",cx,yb,F("sans",6.8,700),CREAM,px(1.0),stroke=px(0.5),sfill=DK); yb+=px(12)
    center(d,"Dai 3 ai 6 anni",yb,F("mark",13,600),CREAM,cw,x0=L,stroke=px(0.8),sfill=DK)
    spirale_footer(d,L,col=CREAM,stroke=so); barcode(d,BACK_W,H); return img

BACKS = {"collana":back_collana,"island_A":back_island_A,"island_B":back_island_B,"island_C":back_island_C}

# ─────────────────────────── WRAP ───────────────────────────
def fill_front(front):
    iw,ih=front.size; s=max(FRONT_W/iw,H/ih); nw,nh=int(iw*s),int(ih*s)
    r=front.resize((nw,nh),Image.LANCZOS); cx0=(nw-FRONT_W)//2; cy0=int((nh-H)*0.72)
    return r.crop((cx0,cy0,cx0+FRONT_W,cy0+H))

def wrap_cover(front,back):
    wrap=Image.new("RGB",(W,H),PAPER)
    wrap.paste(back,(0,0)); wrap.paste(spine(),(BACK_W,0)); wrap.paste(fill_front(front),(BACK_W+SPINE_W,0))
    g=ImageDraw.Draw(wrap)
    for xline in (BACK_W,BACK_W+SPINE_W):
        for yy in range(0,H,px(5)): g.line([(xline,yy),(xline,yy+px(2))],fill=(208,196,176),width=1)
    return wrap

# ─────────────────────────── MAIN ───────────────────────────
def main():
    OUT.mkdir(parents=True, exist_ok=True)
    front=build_front()
    front.save(OUT/f"vol{VOLUME}_copertina_{TITLE_STYLE}.png")
    for name,fn in BACKS.items(): fn().save(OUT/f"vol{VOLUME}_quarta_{name}.png")
    back=BACKS[BACK_STYLE]()
    wrap_cover(front,back).save(OUT/f"vol{VOLUME}_wrap_{TITLE_STYLE}_{BACK_STYLE}.png")
    print(f"OK  Volume {VOLUME}  |  wrap {W}x{H}px @ {DPI}dpi  |  titolo={TITLE_STYLE} quarta={BACK_STYLE}  |  spina {SPINE_MM}mm (provvisoria)")

if __name__ == "__main__":
    main()
