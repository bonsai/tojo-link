"""
東上リンク Demo MP4 v2 — おおきく、かんたん、おばさんにわかりやすく
45-second vertical phone video (1080x1920, 30fps)
"""

from moviepy.editor import VideoClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os, math, time as _time

OUT = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)

W, H, FPS, DUR = 1080, 1920, 30, 45

# Colors
BG = "#ffffff"
ORANGE = "#ff6b35"
INDIGO = "#5b6abf"
IND_LT = "#f0f4ff"
GOLD_BG = "#fff8e1"
GRAY = "#999999"
GRAY_LT = "#e0e0e0"
DARK = "#1a1a2e"
GOLD = "#8d6e00"
CARD_BG = "#ffffff"

def h2r(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def _font(sz):
    for p in [r"C:\Windows\Fonts\meiryo.ttc", r"C:\Windows\Fonts\msgothic.ttc",
              r"C:\Windows\Fonts\yugothic.ttc", "arial.ttf"]:
        try: return ImageFont.truetype(p, sz)
        except: pass
    return ImageFont.load_default()

F = {'t50': _font(50), 't42': _font(42), 't38': _font(38), 't32': _font(32),
     't28': _font(28), 't26': _font(26), 't24': _font(24), 't22': _font(22),
     't20': _font(20), 't18': _font(18)}

DATA = [
    {"id":"a1","st":"鶴瀬","ti":"鶴瀬駅徒歩5分🌸 甘酒＆麹カフェ",
     "lnk":"麹カフェ つるせ","tags":["麹","甘酒"],"com":5},
    {"id":"a2","st":"池袋","ti":"英会話カフェ 🇬🇧 初心者歓迎",
     "lnk":"東上線 英会話カフェ","tags":["英会話"],"com":12},
    {"id":"a3","st":"川越","ti":"レコード喫茶 🎵 アナログ1000枚",
     "lnk":"レコード喫茶 小江戸","tags":["レコード"],"com":23},
]

STAS = [("池袋",True),("鶴瀬",True),("志木",False),("川越",True)]

def clamp(v,a=0,b=1): return max(a,min(b,v))
def lerp(a,b,t): return a+(b-a)*clamp(t)
def jelly(t): return 1-math.cos(t*math.pi*2.5)*(1-t)**2 if 0<t<1 else clamp(t)

def rr(d,x,y,w,h,r,fill,outline=None,width=0):
    d.rounded_rectangle([x,y,x+w,y+h],radius=r,fill=fill,outline=outline,width=width)

# ── Draw a BIG card ──
def big_card(d, post, x, y, saved=False, highlight=False, dim=False):
    h2 = 300  # card height
    rr(d, x, y, W-2*x, h2, 22, CARD_BG, outline=ORANGE if highlight else GRAY_LT, width=3 if highlight else 2)
    if dim: return  # will be overridden with opacity by caller

    # Station + time
    d.text((x+24, y+14), f"🚃 {post['st']}", font=F['t32'], fill=h2r(ORANGE))
    d.text((W-x-160, y+18), "2時間前", font=F['t20'], fill=GRAY)

    # Title BIG
    d.text((x+24, y+56), post["ti"], font=F['t32'], fill=h2r(DARK))

    # Link box
    rr(d, x+20, y+120, W-2*x-40, 56, 12, h2r(IND_LT))
    d.text((x+36, y+128), f"🔗 {post['lnk']}", font=F['t24'], fill=h2r(INDIGO))

    # Tags
    tx = x + 20
    for tag in post["tags"]:
        tw = int(d.textlength(f"#{tag}", font=F['t24'])) + 30
        rr(d, tx, y+190, tw, 36, 18, h2r(IND_LT))
        d.text((tx+15, y+194), f"#{tag}", font=F['t24'], fill=h2r(INDIGO))
        tx += tw + 10

    # Save button
    sw = 360; sh = 60; sx = W-x-20-sw; sy = y+234
    sc = (200,200,200) if saved else h2r(ORANGE)
    tc = DARK if saved else "#ffffff"
    rr(d, sx, sy, sw, sh, 16, sc)
    d.text((sx+30, sy+10), "✓ 保存したよ！" if saved else "📍 行ってみたい！", font=F['t26'], fill=tc)


def header(d):
    rr(d, 0, 0, W, 130, 0, BG)
    d.line([(0,130),(W,130)], fill=h2r(GRAY_LT), width=2)
    d.text((60, 28), "🚃 東上リンク", font=F['t50'], fill=h2r(INDIGO))


def subtitle(d, text, alpha=1.0):
    a = clamp(alpha)
    tw = int(d.textlength(text, font=F['t32']))
    pw = tw + 70; px = (W-pw)//2; py = H-90
    rr(d, px, py, pw, 54, 27, (int(26*a), int(26*a), int(26*a)))
    d.text((px+35, py+8), text, font=F['t32'], fill=(int(255*a), int(255*a), int(255*a)))


# ═══════════════ SCENES ═══════════════

def s1_opening(t):
    img = Image.new('RGB',(W,H),h2r(BG)); d = ImageDraw.Draw(img)
    header(d)

    # Logo slide in
    lx = lerp(-200, 60, clamp(t/0.5))
    d.text((lx, 28), "🚃 東上リンク", font=F['t50'], fill=h2r(INDIGO))

    # Section title
    st_t = clamp((t-0.8)/0.4)
    if st_t > 0:
        d.text((40, 160), "✨ おすすめ", font=F['t42'], fill=h2r(GOLD))

    # Recommend items
    for i, (p, ic) in enumerate(zip(DATA, ["🎯","🔥","💡"])):
        it = clamp((t-(1.2+i*0.3))/0.3)
        if it > 0:
            iy = 230 + i*80
            ix = int(lerp(-30, 0, it))
            rr(d, 30+ix, iy, W-60, 64, 16, h2r(GOLD_BG), outline=h2r("#ffcc80"), width=2)
            d.text((50+ix, iy+8), ic, font=F['t38'])
            d.text((105+ix, iy+4), p["ti"], font=F['t28'], fill=h2r(DARK))
            d.text((105+ix, iy+34), f'{p["st"]} · 共通{p["com"]}人', font=F['t22'], fill=GRAY)

    # Chips
    ct = clamp((t-2.5)/0.3)
    if ct > 0:
        cy = 490
        for i, chip in enumerate(["すべて","鶴瀬","池袋","川越"]):
            cx = 30 + i*180
            cw = int(d.textlength(chip, font=F['t28'])) + 50
            active = i == 0
            fill = h2r(INDIGO) if active else BG
            rr(d, cx, cy, cw, 48, 24, fill, outline=h2r(INDIGO) if active else h2r(GRAY_LT), width=2)
            tf = "#ffffff" if active else h2r(DARK)
            d.text((cx+25, cy+6), chip, font=F['t28'], fill=tf)

    # Cards
    for i, p in enumerate(DATA):
        card_t = clamp((t-(2.8+i*0.3))/0.3)
        if card_t > 0:
            cy = 560 + i*320 + int(lerp(40,0,card_t))
            big_card(d, p, 30, int(cy), saved=False)

    # Subtitle
    if 0.3 <= t <= 4.2:
        sa = 1.0 if t < 3.7 else clamp(1-(t-3.7)/0.5)
        subtitle(d, "東上線沿線の、リンク発見ボード", sa)

    return np.array(img)


def s2_picker(t):
    img = Image.new('RGB',(W,H),h2r(BG)); d = ImageDraw.Draw(img)
    header(d)

    # Always show recommends behind
    d.text((40, 160), "✨ おすすめ", font=F['t42'], fill=h2r(GOLD))
    for i, (p, ic) in enumerate(zip(DATA, ["🎯","🔥","💡"])):
        iy = 230 + i*80
        rr(d, 30, iy, W-60, 64, 16, h2r(GOLD_BG), outline=h2r("#ffcc80"), width=2)
        d.text((50, iy+8), ic, font=F['t38'])
        d.text((105, iy+4), p["ti"], font=F['t28'], fill=h2r(DARK))
        d.text((105, iy+34), f'{p["st"]} · 共通{p["com"]}人', font=F['t22'], fill=GRAY)

    for i, chip in enumerate(["すべて","鶴瀬","池袋","川越"]):
        cx = 30 + i*180
        cw = int(d.textlength(chip, font=F['t28'])) + 50
        active = i == 0
        rr(d, cx, 500, cw, 48, 24, h2r(INDIGO) if active else BG,
           outline=h2r(INDIGO) if active else h2r(GRAY_LT), width=2)
        d.text((cx+25, 506), chip, font=F['t28'], fill="#fff" if active else h2r(DARK))

    # Picker slides up
    pt = clamp((t-0.5)/0.6); pj = jelly(pt)
    ph = 600; py = H - int(ph*pj)
    if py < H:
        rr(d, 0, py, W, H-py, 28, BG)
        rr(d, W//2-30, py+14, 60, 8, 4, h2r(GRAY_LT))
        d.text((W//2-int(d.textlength("🚃 駅を選んでね",font=F['t38'])/2), py+40),
               "🚃 駅を選んでね", font=F['t38'], fill=h2r(DARK))

        for i, (name, rec) in enumerate(STAS):
            iy = py + 110 + i*72
            bg = h2r(IND_LT) if rec else BG
            rr(d, 24, iy, W-48, 58, 16, bg)
            d.text((50, iy+10), f"🚃 {name}", font=F['t32'], fill=h2r(DARK))
            if rec:
                rw = int(d.textlength("おすすめ", font=F['t22'])) + 20
                rr(d, W-50-rw, iy+14, rw, 30, 10, h2r(ORANGE))
                d.text((W-50-rw+10, iy+16), "おすすめ", font=F['t22'], fill="#fff")

        # Jelly bounce on 鶴瀬 at t=2.0
        if 2.0 <= t <= 3.0:
            bt = t - 2.0
            bounce = math.sin(bt*math.pi*4)*(1-bt)*5
            iy2 = py + 110 + 1*72 + bounce
            rr(d, 24, iy2, W-48, 58, 16, (200,210,255))
            # ripple
            rv = int(70*clamp(bt*2))
            d.ellipse([W//2-rv, iy2+20-rv, W//2+rv, iy2+20+rv], outline=(255,107,53), width=3)

    if t <= 4.5:
        sa = 1.0 if t < 4.0 else clamp(1-(t-4.0)/0.5)
        subtitle(d, "駅を選んでね — ぷるぷる動くよ！", sa)

    return np.array(img)


def s3_filter(t):
    img = Image.new('RGB',(W,H),h2r(BG)); d = ImageDraw.Draw(img)
    header(d)
    d.text((40, 160), "✨ おすすめ", font=F['t42'], fill=h2r(GOLD))
    for i, (p, ic) in enumerate(zip(DATA, ["🎯","🔥","💡"])):
        iy = 230 + i*80
        rr(d, 30, iy, W-60, 64, 16, h2r(GOLD_BG), outline=h2r("#ffcc80"), width=2)
        d.text((50, iy+8), ic, font=F['t38'])
        d.text((105, iy+4), p["ti"], font=F['t28'], fill=h2r(DARK))
        d.text((105, iy+34), f'{p["st"]} · 共通{p["com"]}人', font=F['t22'], fill=GRAY)

    hl = t >= 1.0
    for i, chip in enumerate(["すべて","鶴瀬","池袋","川越"]):
        cx = 30 + i*180
        cw = int(d.textlength(chip, font=F['t28'])) + 50
        is_ts = i == 1
        active = (not hl and i == 0) or (hl and is_ts)
        if hl and is_ts: fill = h2r(ORANGE)
        elif active: fill = h2r(INDIGO)
        else: fill = BG
        rr(d, cx, 500, cw, 48, 24, fill,
           outline=fill if active else h2r(GRAY_LT), width=2)
        tf = "#fff" if active else h2r(DARK)
        d.text((cx+25, 506), chip, font=F['t28'], fill=tf)

        if hl and is_ts:
            pulse = math.sin(t*6)*0.3+0.7
            rc = (int(255*pulse),int(107*pulse),int(53*pulse))
            rr(d, cx-4, 496, cw+8, 56, 28, None, outline=rc, width=3)

    # Cards
    for i, p in enumerate(DATA):
        dim = hl and p["id"] != "a1"
        hl_border = hl and p["id"] == "a1"
        big_card(d, p, 30, 570+i*320, saved=False, highlight=hl_border)
        if dim:
            # Draw dim overlay on top
            rr(d, 30, 570+i*320, W-60, 300, 22, (240,240,240))

    if t <= 4.2:
        sa = 1.0 if t < 3.7 else clamp(1-(t-3.7)/0.5)
        subtitle(d, "駅ごとに、リンクが並ぶ", sa)

    return np.array(img)


def s4_save(t):
    img = Image.new('RGB',(W,H),h2r(BG)); d = ImageDraw.Draw(img)
    header(d)

    scroll = min(60, t*20)
    d.text((40, 160-scroll), "✨ おすすめ", font=F['t42'], fill=h2r(GOLD))
    for i, (p, ic) in enumerate(zip(DATA, ["🎯","🔥","💡"])):
        iy = 230-scroll + i*80
        rr(d, 30, iy, W-60, 64, 16, h2r(GOLD_BG), outline=h2r("#ffcc80"), width=2)
        d.text((50, iy+8), ic, font=F['t38'])
        d.text((105, iy+4), p["ti"], font=F['t28'], fill=h2r(DARK))
        d.text((105, iy+34), f'{p["st"]} · 共通{p["com"]}人', font=F['t22'], fill=GRAY)

    for i, chip in enumerate(["すべて","鶴瀬","池袋","川越"]):
        cx = 30 + i*180
        cw = int(d.textlength(chip, font=F['t28'])) + 50
        rr(d, cx, 500-scroll, cw, 48, 24, BG, outline=h2r(GRAY_LT), width=2)
        d.text((cx+25, 506-scroll), chip, font=F['t28'], fill=h2r(DARK))

    cards_y = 560 - scroll
    for i, p in enumerate(DATA):
        is_saved = p["id"] == "a3" and t >= 3.0
        big_card(d, p, 30, int(cards_y+i*320), saved=is_saved)

    # Tap ripple at t=2.0 on a3 save button
    if 1.8 <= t <= 2.8:
        rt = t - 1.8
        rr2 = int(60*clamp(rt*2))
        rx = W - 30 - 180 - 360//2
        ry = int(cards_y + 2*320 + 234 + 30)
        d.ellipse([rx-rr2, ry-rr2, rx+rr2, ry+rr2], outline=(255,107,53), width=3)

    # Pulse save button redraw
    if 2.2 <= t <= 3.2:
        pulse = math.sin((t-2.2)*math.pi)*0.12 + 1.0
        cy = int(cards_y + 2*320)
        sw = int(360*pulse); sh = int(60*pulse); sx = W-50-sw; sy = cy+234
        saved = t >= 2.8
        sc = (200,200,200) if saved else h2r(ORANGE)
        rr(d, sx, sy, sw, sh, int(16*pulse), sc)
        d.text((sx+int(30*pulse), sy+int(10*pulse)),
               "✓ 保存したよ！" if saved else "📍 行ってみたい！",
               font=F['t26'], fill=DARK if saved else "#fff")

    if t <= 4.5:
        sa = 1.0 if t < 4.0 else clamp(1-(t-4.0)/0.5)
        subtitle(d, "「行ってみたい！」ボタンをタッチ", sa)

    return np.array(img)


def s5_connect(t):
    img = Image.new('RGB',(W,H),h2r(BG)); d = ImageDraw.Draw(img)
    header(d)
    d.text((40, 160), "✨ おすすめ", font=F['t42'], fill=h2r(GOLD))
    for i, (p, ic) in enumerate(zip(DATA, ["🎯","🔥","💡"])):
        iy = 230 + i*80
        rr(d, 30, iy, W-60, 64, 16, h2r(GOLD_BG), outline=h2r("#ffcc80"), width=2)
        d.text((50, iy+8), ic, font=F['t38'])
        d.text((105, iy+4), p["ti"], font=F['t28'], fill=h2r(DARK))
        d.text((105, iy+34), f'{p["st"]} · 共通{p["com"]}人', font=F['t22'], fill=GRAY)

    for i, chip in enumerate(["すべて","鶴瀬","池袋","川越"]):
        cx = 30 + i*180
        cw = int(d.textlength(chip, font=F['t28'])) + 50
        rr(d, cx, 500, cw, 48, 24, BG, outline=h2r(GRAY_LT), width=2)
        d.text((cx+25, 506), chip, font=F['t28'], fill=h2r(DARK))

    for i, p in enumerate(DATA):
        big_card(d, p, 30, 560+i*320, saved=(p["id"]=="a3"))

    # Common users banner on a2
    if t >= 1.2:
        ba = clamp((t-1.2)/0.5)
        p2_cy = 560 + 1*320
        bx = 46; by = p2_cy + 260
        bw = W-92; bh = 38
        rr(d, bx, by, bw, bh, 12, h2r(GOLD_BG))
        ga = int(ba*255)
        d.text((bx+14, by+4), "👥 #英会話 に興味がある人と共通しています",
               font=F['t22'], fill=(int(141*ba), int(110*ba), 0))

    if t <= 4.2:
        sa = 1.0 if t < 3.7 else clamp(1-(t-3.7)/0.5)
        subtitle(d, "同じことに興味がある人がいるかも", sa)

    return np.array(img)


def s6_post(t):
    img = Image.new('RGB',(W,H),h2r(BG)); d = ImageDraw.Draw(img)
    header(d)

    d.text((40, 160), "✨ おすすめ", font=F['t42'], fill=h2r(GOLD))
    for i, (p, ic) in enumerate(zip(DATA, ["🎯","🔥","💡"])):
        iy = 230 + i*80
        rr(d, 30, iy, W-60, 64, 16, h2r(GOLD_BG), outline=h2r("#ffcc80"), width=2)
        d.text((50, iy+8), ic, font=F['t38'])
        d.text((105, iy+4), p["ti"], font=F['t28'], fill=h2r(DARK))
        d.text((105, iy+34), f'{p["st"]} · 共通{p["com"]}人', font=F['t22'], fill=GRAY)

    for i, chip in enumerate(["すべて","鶴瀬","池袋","川越"]):
        cx = 30 + i*180
        cw = int(d.textlength(chip, font=F['t28'])) + 50
        rr(d, cx, 500, cw, 48, 24, BG, outline=h2r(GRAY_LT), width=2)
        d.text((cx+25, 506), chip, font=F['t28'], fill=h2r(DARK))

    for i, p in enumerate(DATA):
        big_card(d, p, 30, 560+i*320, saved=False)

    # Form slides up
    ft = clamp((t-0.5)/0.5); fj = jelly(ft)
    fh = 550; fy = H - int(fh*fj)

    if fy < H:
        rr(d, 0, fy, W, H-fy, 28, BG)
        rr(d, W//2-25, fy+12, 50, 6, 3, h2r(GRAY_LT))
        tw2 = int(d.textlength("📎 リンクを投稿", font=F['t38']))
        d.text((W//2-tw2//2, fy+34), "📎 リンクを投稿", font=F['t38'], fill=h2r(DARK))

        fields = [("🚃 駅","鶴瀬",1.0),("タイトル","新しいカフェ",1.6),("URL","https://example.com",2.2)]
        for fi, (label, val, ftime) in enumerate(fields):
            active = t >= ftime
            f_y = fy + 100 + fi*80
            d.text((30, f_y), label, font=F['t28'], fill=h2r("#666666"))
            bc = BG if active else h2r("#f8f9fa")
            oc = h2r(INDIGO) if active else h2r(GRAY_LT)
            ow = 3 if active else 2
            rr(d, 30, f_y+30, W-60, 50, 14, bc, outline=oc, width=ow)
            d.text((46, f_y+36), val, font=F['t28'], fill=h2r(DARK))

        if t >= 3.0:
            sb_y = fy + 360
            rr(d, 30, sb_y, W-60, 60, 16, h2r(INDIGO))
            stw = int(d.textlength("投稿する", font=F['t32']))
            d.text((W//2-stw//2, sb_y+12), "投稿する", font=F['t32'], fill="#fff")

    # Toast
    if t >= 4.0:
        ta2 = 1.0 if t < 5.0 else clamp(1-(t-5.0)/0.5)
        taw = int(d.textlength("📎 投稿したよ！", font=F['t28']))
        rr(d, W//2-taw//2-30, 90, taw+60, 50, 25, (int(51*ta2),int(51*ta2),int(51*ta2)))
        d.text((W//2-taw//2, 98), "📎 投稿したよ！", font=F['t28'],
               fill=(int(255*ta2),int(255*ta2),int(255*ta2)))

    # New card flash
    if t >= 4.2:
        nc_t = clamp((t-4.2)/0.3)
        nc_y = int(560 + lerp(-30, 0, nc_t))
        rr(d, 30, nc_y, W-60, 300, 22, BG, outline=h2r(INDIGO), width=4)
        d.text((54, nc_y+14), "🚃 鶴瀬", font=F['t32'], fill=h2r(ORANGE))
        d.text((W-160, nc_y+18), "たった今", font=F['t20'], fill=GRAY)
        d.text((54, nc_y+56), "新しいカフェ オープン ☕", font=F['t32'], fill=h2r(DARK))
        rr(d, 50, nc_y+120, W-100, 56, 12, h2r(IND_LT))
        d.text((66, nc_y+128), "🔗 新カフェ 鶴瀬", font=F['t24'], fill=h2r(INDIGO))
        sw2 = 360; sh2 = 60; sx2 = W-50-sw2; sy2 = nc_y+234
        rr(d, sx2, sy2, sw2, sh2, 16, h2r(ORANGE))
        d.text((sx2+30, sy2+10), "📍 行ってみたい！", font=F['t26'], fill="#fff")

    if t <= 5.5:
        sa = 1.0 if t < 5.0 else clamp(1-(t-5.0)/0.5)
        subtitle(d, "あなたも、1日に1回投稿できるよ", sa)

    return np.array(img)


def s7_end(t):
    img = Image.new('RGB',(W,H),h2r(BG)); d = ImageDraw.Draw(img)
    header(d)

    # Darken
    ba = clamp(t/1.0)
    dr = int(255*(1-ba)+10*ba); dg = int(255*(1-ba)+10*ba); db2 = int(255*(1-ba)+26*ba)
    d.rectangle([0,0,W,H], fill=(dr,dg,db2))

    ta = clamp((t-0.2)/0.5)
    d.text((W//2-40, 680), "🚃", font=_font(90))
    d.text((W//2-130, 790), "東上リンク", font=F['t50'], fill=(int(255*ta),int(255*ta),int(255*ta)))
    sa2 = int(153*ta)
    d.text((W//2-100, 870), "もうすぐはじまるよ", font=F['t32'], fill=(sa2,sa2,sa2))

    if t >= 1.5:
        sb = clamp((t-1.5)/0.5)
        subtitle(d, "写真もログインも、いらない 🚃", sb)

    return np.array(img)


# ═══════════════ MASTER ═══════════════
def make_frame(t):
    if t < 5:   return s1_opening(t)
    if t < 15:  return s2_picker(t-5)
    if t < 20:  return s3_filter(t-15)
    if t < 30:  return s4_save(t-20)
    if t < 35:  return s5_connect(t-30)
    if t < 42:  return s6_post(t-35)
    return s7_end(t-42)


if __name__ == "__main__":
    print(f"🚃 東上リンク Demo v2 — おおきく、かんたん")
    print(f"  {W}x{H}  {DUR}s  {FPS}fps")
    print(f"  {OUT}/demo_v2.mp4\n")
    t0 = _time.time()
    clip = VideoClip(make_frame, duration=DUR)
    clip.write_videofile(os.path.join(OUT,"demo_v2.mp4"), fps=FPS,
                         codec="libx264", audio=False, preset="medium",
                         logger="bar", threads=4)
    print(f"\n✅ Done in {_time.time()-t0:.1f}s")
    print(f"📁 {OUT}/demo_v2.mp4")
