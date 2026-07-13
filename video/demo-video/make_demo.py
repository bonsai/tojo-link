"""
東上リンク — Demo MP4 Generator (MoviePy + Pillow)
45-second vertical phone video (1080x1920, 30fps)

Usage: python make_demo.py
Output: out/demo.mp4
"""

from moviepy.editor import VideoClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os, math, time as _time

OUT_DIR = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 1080, 1920
FPS = 30
DURATION = 45

# ── Colors ──
BG = "#f8f9fa"
WHITE = "#ffffff"
ORANGE = "#ff6b35"
INDIGO = "#5b6abf"
INDIGO_LT = "#e8ecff"
GRAY = "#999999"
GRAY_LT = "#e0e0e0"
DARK = "#1a1a2e"
GOLD = "#8d6e00"
GOLD_BG = "#fff8e1"
BLACK33 = "#333333"

def h2r(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# ── Fonts ──
def _font(size):
    for p in [r"C:\Windows\Fonts\meiryo.ttc", r"C:\Windows\Fonts\msgothic.ttc",
              r"C:\Windows\Fonts\yugothic.ttc", "arial.ttf"]:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()

F = {
    'title': _font(52), 'sub': _font(28), 'b40': _font(40), 'b32': _font(32),
    'b28': _font(28), 'b24': _font(24), 'b22': _font(22), 'b20': _font(20),
    'b18': _font(18), 'b16': _font(16), 'r18': _font(18), 'r16': _font(16), 'r14': _font(14),
}

# ── Data ──
POSTS = [
    {"id":"p1","sid":"TJ-13","sname":"鶴瀬","title":"鶴瀬駅徒歩5分🌸 甘酒＆麹カフェ",
     "og":"麹カフェ つるせ","desc":"6種類の麹で1day Lesson","tags":["麹","甘酒","鶴瀬"],
     "clicks":42,"common":5,"img":True},
    {"id":"p2","sid":"TJ-01","sname":"池袋","title":"英会話カフェ募集 🇬🇧 池袋〜川越",
     "og":"東上線 英会話カフェ","desc":"初心者歓迎・毎週土曜","tags":["英会話","募集"],
     "clicks":89,"common":12,"img":False},
    {"id":"p3","sid":"TJ-17","sname":"川越","title":"川越のレコード喫茶 🎵 アナログ1000枚",
     "og":"レコード喫茶 小江戸","desc":"コーヒーとレコードの休日","tags":["レコード","川越"],
     "clicks":156,"common":23,"img":True},
    {"id":"p4","sid":"TJ-10","sname":"志木","title":"志木駅前 隠れ家パン屋 🥐 朝6時",
     "og":"ブーランジェリー 志木","desc":"天然酵母・夜はワインバー","tags":["パン","志木"],
     "clicks":67,"common":8,"img":True},
    {"id":"p5","sid":"TJ-26","sname":"東松山","title":"東松山やきとり祭り 🍢 2026年秋",
     "og":"やきとり祭り","desc":"醤油たれ・毎年10月開催","tags":["グルメ","東松山"],
     "clicks":203,"common":31,"img":True},
]
CHIPS = ["すべて","鶴瀬","池袋","川越","志木","東松山"]
STATIONS = [
    ("TJ-01","池袋","東京都豊島区"),("TJ-07","成増","東京都板橋区"),
    ("TJ-10","志木","埼玉県新座市"),("TJ-13","鶴瀬","埼玉県富士見市"),
    ("TJ-17","川越","埼玉県川越市"),("TJ-26","東松山","埼玉県東松山市"),
]

# ── Jelly easing ──
def jelly(t):
    if t <= 0 or t >= 1: return max(0, min(1, t))
    return 1 - math.cos(t * math.pi * 2.5) * (1 - t) ** 2

def clamp(v, lo=0, hi=1): return max(lo, min(hi, v))
def lerp(a, b, t): return a + (b - a) * t

# ── Draw helpers ──
def rr(draw, x, y, w, h, r, fill, outline=None, width=0):
    draw.rounded_rectangle([x, y, x+w, y+h], radius=r, fill=fill, outline=outline, width=width)

def card(draw, post, x, y, alpha=1.0, saved=False, highlight_border=False, scale_save=1.0):
    """Draw a link card at (x,y). alpha controls fade/dim."""
    # aw = min(1, max(0, alpha))
    # Card background
    rr(draw, x, y, W-2*x, 260, 18, WHITE)
    if highlight_border:
        rr(draw, x, y, W-2*x, 260, 18, None, outline=ORANGE, width=4)

    # Station header
    draw.text((x+20, y+12), f'{post["sid"]} {post["sname"]}', font=F['b20'], fill=h2r(ORANGE))
    draw.text((W-x-100, y+14), "2時間前", font=F['r14'], fill=h2r(GRAY))

    # Title
    draw.text((x+20, y+42), post["title"], font=F['b22'], fill=h2r(DARK))

    # URL preview
    rr(draw, x+16, y+76, W-2*x-32, 70, 10, h2r(BG))
    rr(draw, x+26, y+88, 36, 36, 6, (220,220,220))
    draw.text((x+33, y+92), "🔗", font=F['b16'])
    draw.text((x+74, y+84), post["og"], font=F['b18'], fill=h2r(DARK))
    draw.text((x+74, y+108), post["desc"], font=F['r14'], fill=h2r("#666666"))
    if post["img"]:
        rr(draw, W-x-106, y+82, 80, 60, 8, (102,126,234))

    # Tags
    tx = x + 16
    for tag in post["tags"]:
        tw = int(draw.textlength(f"#{tag}", font=F['b16'])) + 20
        rr(draw, tx, y+156, tw, 26, 13, h2r(INDIGO_LT))
        draw.text((tx + 10, y+158), f"#{tag}", font=F['b16'], fill=h2r(INDIGO))
        tx += tw + 8

    # Actions
    draw.text((x+20, y+195), f'🔗 {post["clicks"]}', font=F['r16'], fill=h2r(GRAY))
    if post["common"] > 0:
        draw.text((x+120, y+195), f'👥 {post["common"]}', font=F['r16'], fill=h2r(GRAY))

    # Save button
    bw = max(160, int(draw.textlength("📍 行ってみたい", font=F['b18']) * scale_save) + 36)
    bh = int(36 * scale_save)
    bx = W - x - 20 - bw
    by = y + 190
    saved_colors = ((200,200,200), BLACK33) if saved else (h2r(ORANGE), WHITE)
    rr(draw, bx, by, bw, bh, int(bh/2), saved_colors[0])
    draw.text((bx+14, by+6), "✓ 保存済" if saved else "📍 行ってみたい", font=F['b18'], fill=saved_colors[1])

    # Common users banner
    if post["common"] > 10:
        rr(draw, x+16, y+234, W-2*x-32, 24, 8, h2r(GOLD_BG))
        draw.text((x+26, y+236), f'👥 #{post["tags"][0]} に興味がある人と共通しています', font=F['r14'], fill=h2r(GOLD))

def draw_subtitle(draw, text, alpha=1.0):
    """Dark pill subtitle at bottom."""
    a = clamp(alpha)
    tw = int(draw.textlength(text, font=F['sub']))
    pw = int(tw + 80)
    px = (W - pw) // 2
    py = H - 100
    rr(draw, px, py, pw, 48, 24, (int(26*a), int(26*a), int(26*a)))
    draw.text((px + 40, py + 8), text, font=F['sub'], fill=(int(255*a), int(255*a), int(255*a)))

def draw_header(draw):
    rr(draw, 0, 0, W, 140, 0, WHITE)
    draw.line([(0, 140), (W, 140)], fill=h2r(GRAY_LT), width=1)
    draw.text((60, 35), "🚃 東上リンク", font=F['title'], fill=h2r(INDIGO))

# ═══════════════════════════════════════
# SCENE FRAME GENERATORS
# Each: frame_function(t) -> np.ndarray
# ═══════════════════════════════════════

def opening(t):
    """0-5s"""
    img = Image.new('RGB', (W, H), h2r(BG))
    d = ImageDraw.Draw(img)

    # Header
    draw_header(d)

    # Logo slide in
    lx = lerp(-200, 60, clamp(t / 0.5))
    d.text((lx, 35), "🚃 東上リンク", font=F['title'], fill=h2r(INDIGO))

    # Recommend section
    rec_t = clamp((t - 1.2) / 0.6)
    rec_y = int(lerp(220, 155, rec_t))

    # Section bg
    if rec_t > 0:
        rr(d, 0, rec_y, W, 280, 0, h2r(GOLD_BG))
        d.text((40, rec_y + 10), "✨ あなたへのおすすめ", font=F['b24'], fill=h2r(GOLD))

        for i, (p, icon) in enumerate(zip(POSTS[:3], ["🎯","🔥","💡"])):
            it = clamp((t - (1.5 + i*0.25)) / 0.25)
            if it > 0:
                ix = int(lerp(-30, 0, it))
                iy = rec_y + 50 + i * 72
                rr(d, 30+ix, iy, W-60, 58, 14, WHITE)
                d.text((50+ix, iy+10), icon, font=F['b28'])
                d.text((95+ix, iy+8), p["title"], font=F['b20'], fill=h2r(DARK))
                d.text((95+ix, iy+32), f'{p["sid"]} {p["sname"]}', font=F['r16'], fill=h2r(GRAY))
                if p["common"] > 5:
                    bw = int(d.textlength(f'共通{p["common"]}人', font=F['b16'])) + 24
                    bx = W - 50 - bw
                    rr(d, bx, iy+14, bw, 26, 13, h2r(ORANGE))
                    d.text((bx+12, iy+16), f'共通{p["common"]}人', font=F['b16'], fill=WHITE)

    # Chips
    chips_t = clamp((t - 2.3) / 0.3)
    if chips_t > 0:
        cy = rec_y + 290 if rec_t > 0 else 170
        for i, chip in enumerate(CHIPS):
            cx = 30 + i * 140
            cw = int(d.textlength(chip, font=F['b20'])) + 44
            active = i == 0
            fill = h2r(INDIGO) if active else WHITE
            outline = h2r(INDIGO) if active else h2r(GRAY_LT)
            tf = WHITE if active else h2r(DARK)
            rr(d, cx, cy, cw, 40, 20, fill, outline=outline, width=2)
            d.text((cx+22, cy+6), chip, font=F['b20'], fill=tf)

    # Cards
    cards_base = (rec_y + 340) if rec_t > 0 else 230
    for i, p in enumerate(POSTS[:3]):
        ct = clamp((t - (2.6 + i*0.25)) / 0.25)
        if ct > 0:
            card(d, p, 30, int(cards_base + i*270 + lerp(40, 0, ct)), ct, saved=False)

    # Subtitle
    if 0.3 <= t <= 4.2:
        sa = 1.0 if t < 3.7 else clamp(1 - (t-3.7)/0.5)
        draw_subtitle(d, "東上線沿線の、リンク発見ボード", sa)

    return np.array(img)


def station_picker(t):
    """5-15s (local 0-10)"""
    img = Image.new('RGB', (W, H), h2r(BG))
    d = ImageDraw.Draw(img)
    draw_header(d)

    # Recommend (always visible behind)
    rr(d, 0, 150, W, 280, 0, h2r(GOLD_BG))
    d.text((40, 165), "✨ あなたへのおすすめ", font=F['b24'], fill=h2r(GOLD))
    for i, (p, icon) in enumerate(zip(POSTS[:3], ["🎯","🔥","💡"])):
        rr(d, 30, 205+i*72, W-60, 58, 14, WHITE)
        d.text((50, 215+i*72), icon, font=F['b28'])
        d.text((95, 208+i*72), p["title"], font=F['b20'], fill=h2r(DARK))
        d.text((95, 232+i*72), f'{p["sid"]} {p["sname"]}', font=F['r16'], fill=h2r(GRAY))

    # Chips
    for i, chip in enumerate(CHIPS):
        cx = 30 + i * 140
        cw = int(d.textlength(chip, font=F['b20'])) + 44
        active = i == 0
        fill = h2r(INDIGO) if active else WHITE
        rr(d, cx, 445, cw, 40, 20, fill, outline=h2r(INDIGO) if active else h2r(GRAY_LT), width=2)
        d.text((cx+22, 451), chip, font=F['b20'], fill=WHITE if active else h2r(DARK))

    # Picker slides up (starts at t=0.5)
    pt = clamp((t - 0.5) / 0.6)
    pj = jelly(pt)
    ph = 780
    py = H - int(ph * pj)

    if py < H:
        rr(d, 0, py, W, H-py, 30, WHITE)
        rr(d, W//2-30, py+16, 60, 8, 4, h2r(GRAY_LT))
        d.text((40, py+40), "🚃 駅を選んでください", font=F['b24'], fill=h2r(GRAY))

        for i, (sid, name, muni) in enumerate(STATIONS):
            is_rec = sid in ("TJ-13","TJ-01","TJ-17")
            iy = py + 95 + i * 68
            if is_rec:
                rr(d, 20, iy-4, W-40, 60, 14, h2r(INDIGO_LT))
            rr(d, 40, iy+8, 80, 36, 18, h2r(ORANGE))
            stw = d.textlength(sid, font=F['b18'])
            d.text((80-stw/2, iy+12), sid, font=F['b18'], fill=WHITE)
            d.text((140, iy+12), name, font=F['b24'], fill=h2r(DARK))
            mw = d.textlength(muni, font=F['r16'])
            d.text((W-30-mw, iy+20), muni, font=F['r16'], fill=h2r(GRAY))
            if is_rec:
                d.text((W-65, iy+12), "⭐", font=F['b24'])

        # Jelly bounce on 鶴瀬 selection (t=2.0)
        if 2.0 <= t <= 3.0:
            bt = (t - 2.0)
            bounce = math.sin(bt * math.pi * 4) * (1 - bt) * 6
            idx = 3
            iy = py + 95 + idx * 68 + bounce
            rr(d, 20, iy-4, W-40, 60, 14, (200, 210, 255))
            # Ripple
            rr_val = int(80 * clamp(bt * 2))
            d.ellipse([W//2-rr_val, iy+22-rr_val, W//2+rr_val, iy+22+rr_val],
                     outline=(91,106,191), width=3)

    # Subtitle
    if t <= 4.5:
        sa = 1.0 if t < 4.0 else clamp(1-(t-4.0)/0.5)
        draw_subtitle(d, "ぷるぷる弾む、駅ピッカー", sa)

    return np.array(img)


def filter_scene(t):
    """15-20s (local 0-5)"""
    img = Image.new('RGB', (W, H), h2r(BG))
    d = ImageDraw.Draw(img)
    draw_header(d)

    rr(d, 0, 150, W, 280, 0, h2r(GOLD_BG))
    d.text((40, 165), "✨ あなたへのおすすめ", font=F['b24'], fill=h2r(GOLD))
    for i, (p, icon) in enumerate(zip(POSTS[:3], ["🎯","🔥","💡"])):
        rr(d, 30, 205+i*72, W-60, 58, 14, WHITE)
        d.text((50, 215+i*72), icon, font=F['b28'])
        d.text((95, 208+i*72), p["title"], font=F['b20'], fill=h2r(DARK))
        d.text((95, 232+i*72), f'{p["sid"]} {p["sname"]}', font=F['r16'], fill=h2r(GRAY))

    # Chips - 鶴瀬 highlights at t=1.0
    hl = t >= 1.0
    for i, chip in enumerate(CHIPS):
        cx = 30 + i * 140
        cw = int(d.textlength(chip, font=F['b20'])) + 44
        is_ts = i == 1
        active = (not hl and i == 0) or (hl and is_ts)
        if hl and is_ts:
            fill = h2r(ORANGE); outline = h2r(ORANGE)
        elif active:
            fill = h2r(INDIGO); outline = h2r(INDIGO)
        else:
            fill = WHITE; outline = h2r(GRAY_LT)
        tf = WHITE if active else h2r(DARK)
        rr(d, cx, 445, cw, 40, 20, fill, outline=outline, width=2)
        d.text((cx+22, 451), chip, font=F['b20'], fill=tf)

        if hl and is_ts:
            pulse = math.sin(t*6)*0.3 + 0.7
            rc = (int(255*pulse), int(107*pulse), int(53*pulse))
            rr(d, cx-4, 441, cw+8, 48, 24, None, outline=rc, width=3)

    # Cards
    cy = 505
    for i, p in enumerate(POSTS[:3]):
        dim = hl and p["sid"] != "TJ-13"
        if dim:
            alpha = max(0.2, 1-(t-1.0)*0.4)
            card(d, p, 30, int(cy+i*270), alpha, saved=False)
        else:
            card(d, p, 30, int(cy+i*270), 1.0, saved=False,
                 highlight_border=(hl and p["sid"] == "TJ-13"))

    # Subtitle
    if t <= 4.2:
        sa = 1.0 if t < 3.7 else clamp(1-(t-3.7)/0.5)
        draw_subtitle(d, "駅ごとに、気になるリンクが並ぶ", sa)

    return np.array(img)


def save_scene(t):
    """20-30s (local 0-10)"""
    img = Image.new('RGB', (W, H), h2r(BG))
    d = ImageDraw.Draw(img)
    draw_header(d)

    scroll = min(80, t * 25)
    d.text((40, 150-scroll), "✨ あなたへのおすすめ", font=F['b24'], fill=h2r(GOLD))
    for i, (p, icon) in enumerate(zip(POSTS[:3], ["🎯","🔥","💡"])):
        rr(d, 30, 195-scroll+i*72, W-60, 58, 14, WHITE)
        d.text((50, 205-scroll+i*72), icon, font=F['b28'])
        d.text((95, 198-scroll+i*72), p["title"], font=F['b20'], fill=h2r(DARK))
        d.text((95, 222-scroll+i*72), f'{p["sid"]} {p["sname"]}', font=F['r16'], fill=h2r(GRAY))

    for i, chip in enumerate(CHIPS):
        cx = 30 + i * 140
        cw = int(d.textlength(chip, font=F['b20'])) + 44
        rr(d, cx, 425-scroll, cw, 40, 20, WHITE, outline=h2r(GRAY_LT), width=2)
        d.text((cx+22, 431-scroll), chip, font=F['b20'], fill=h2r(DARK))

    # Cards - scroll to card 3 (川越)
    cards_y = 485 - scroll
    for i, p in enumerate(POSTS[:3]):
        card(d, p, 30, int(cards_y + i*270), 1.0, saved=(p["id"]=="p3" and t>=3.5))

    # Tap ripple on save button at t=2.5 (card 3 save button)
    if 2.0 <= t <= 3.0:
        ripple_t = (t - 2.0)
        ripple_r = int(60 * clamp(ripple_t * 2))
        rx = W - 30 - 180
        ry = cards_y + 2*270 + 200
        d.ellipse([rx-ripple_r, ry-ripple_r, rx+ripple_r, ry+ripple_r],
                 outline=(255,107,53), width=3)

    # Scale pulse on save button
    if 2.5 <= t <= 3.5:
        pulse = math.sin((t-2.5)*math.pi) * 0.15 + 1.0
        # Redraw card 3 save button with scale
        cy = cards_y + 2*270
        rr(d, 30, cy, W-60, 260, 18, WHITE)
        d.text((50, cy+12), f'{POSTS[2]["sid"]} {POSTS[2]["sname"]}', font=F['b20'], fill=h2r(ORANGE))
        d.text((W-130, cy+14), "2時間前", font=F['r14'], fill=h2r(GRAY))
        d.text((50, cy+42), POSTS[2]["title"], font=F['b22'], fill=h2r(DARK))
        rr(d, 46, cy+76, W-92, 70, 10, h2r(BG))
        rr(d, 56, cy+88, 36, 36, 6, (220,220,220))
        d.text((63, cy+92), "🔗", font=F['b16'])
        d.text((104, cy+84), POSTS[2]["og"], font=F['b18'], fill=h2r(DARK))
        d.text((104, cy+108), POSTS[2]["desc"], font=F['r14'], fill=h2r("#666666"))
        rr(d, W-136, cy+82, 80, 60, 8, (102,126,234))

        saved = t >= 3.0
        bw = int(170 * pulse)
        bh = int(36 * pulse)
        bx = W - 50 - bw
        by = cy + 190
        sc = (200,200,200) if saved else h2r(ORANGE)
        tc = BLACK33 if saved else WHITE
        rr(d, bx, by, bw, bh, int(bh/2), sc)
        d.text((bx+12, by+6), "✓ 保存済" if saved else "📍 行ってみたい", font=F['b18'], fill=tc)

    # Subtitle
    if t <= 4.5:
        sa = 1.0 if t < 4.0 else clamp(1-(t-4.0)/0.5)
        draw_subtitle(d, "「行ってみたい」を、ワンタップで保存", sa)

    return np.array(img)


def connection_scene(t):
    """30-35s (local 0-5)"""
    img = Image.new('RGB', (W, H), h2r(BG))
    d = ImageDraw.Draw(img)
    draw_header(d)

    d.text((40, 160), "✨ あなたへのおすすめ", font=F['b24'], fill=h2r(GOLD))
    for i, (p, icon) in enumerate(zip(POSTS[:3], ["🎯","🔥","💡"])):
        rr(d, 30, 205+i*72, W-60, 58, 14, WHITE)
        d.text((50, 215+i*72), icon, font=F['b28'])
        d.text((95, 208+i*72), p["title"], font=F['b20'], fill=h2r(DARK))
        d.text((95, 232+i*72), f'{p["sid"]} {p["sname"]}', font=F['r16'], fill=h2r(GRAY))

    for i, chip in enumerate(CHIPS):
        cx = 30 + i * 140
        cw = int(d.textlength(chip, font=F['b20'])) + 44
        rr(d, cx, 445, cw, 40, 20, WHITE, outline=h2r(GRAY_LT), width=2)
        d.text((cx+22, 451), chip, font=F['b20'], fill=h2r(DARK))

    cy = 505
    for i, p in enumerate(POSTS[:3]):
        card(d, p, 30, int(cy+i*270), 1.0, saved=(p["id"]=="p3"))

    # Common users banner fade in
    if t >= 1.5:
        banner_alpha = clamp((t-1.5)/0.5)
        # Draw common users banner on p2 card
        p2_cy = cy + 1*270
        bx = 46
        by = p2_cy + 234
        rr(d, bx, by, W-92, 24, 8, h2r(GOLD_BG))
        # Alpha simulation via lighter color
        gold_a = (int(141*banner_alpha), int(110*banner_alpha), 0)
        d.text((bx+10, by+2), f'👥 #英会話 に興味がある人と共通しています', font=F['r14'], fill=gold_a)

    # Subtitle
    if t <= 4.2:
        sa = 1.0 if t < 3.7 else clamp(1-(t-3.7)/0.5)
        draw_subtitle(d, "共通の趣味の人と、出会えるかも", sa)

    return np.array(img)


def post_scene(t):
    """35-42s (local 0-7)"""
    img = Image.new('RGB', (W, H), h2r(BG))
    d = ImageDraw.Draw(img)
    draw_header(d)

    # Main content
    d.text((40, 160), "✨ あなたへのおすすめ", font=F['b24'], fill=h2r(GOLD))
    for i, (p, icon) in enumerate(zip(POSTS[:3], ["🎯","🔥","💡"])):
        rr(d, 30, 205+i*72, W-60, 58, 14, WHITE)
        d.text((50, 215+i*72), icon, font=F['b28'])
        d.text((95, 208+i*72), p["title"], font=F['b20'], fill=h2r(DARK))
        d.text((95, 232+i*72), f'{p["sid"]} {p["sname"]}', font=F['r16'], fill=h2r(GRAY))

    for i, chip in enumerate(CHIPS):
        cx = 30 + i * 140
        cw = int(d.textlength(chip, font=F['b20'])) + 44
        rr(d, cx, 445, cw, 40, 20, WHITE, outline=h2r(GRAY_LT), width=2)
        d.text((cx+22, 451), chip, font=F['b20'], fill=h2r(DARK))

    # Post form slides up at t=0.5
    form_start = 0.5
    ft = clamp((t - form_start) / 0.5)
    fj = jelly(ft)
    fh = 620
    fy = H - int(fh * fj)

    # Cards visible when form is closed
    if t < form_start:
        for i, p in enumerate(POSTS[:3]):
            card(d, p, 30, 505+i*270, 1.0, saved=False)

    # Post form
    if fy < H:
        rr(d, 0, fy, W, H-fy, 30, WHITE)
        rr(d, W//2-25, fy+14, 50, 6, 3, h2r(GRAY_LT))
        d.text((60, fy+35), "📎 リンクを投稿する", font=F['b32'], fill=h2r(DARK))

        # Fields animate active
        fields = [
            ("🚃 駅", "鶴瀬（TJ-13）", 1.0),
            ("タイトル", "鶴瀬駅🌸 新しいカフェ", 1.8),
            ("URL", "https://example.com/new-cafe", 2.5),
        ]
        for fi, (label, value, ftime) in enumerate(fields):
            active = t >= ftime
            f_y = fy + 85 + fi * 75

            d.text((30, f_y), label, font=F['b18'], fill=h2r("#666666"))
            if active:
                rr(d, 30, f_y+24, W-60, 46, 12, WHITE, outline=h2r(INDIGO), width=2)
            else:
                rr(d, 30, f_y+24, W-60, 46, 12, h2r(BG), outline=h2r(GRAY_LT), width=2)
            d.text((46, f_y+30), value, font=F['b20'], fill=h2r(DARK))

        # Submit button at t=3.5
        if t >= 3.5:
            sb_y = fy + 330
            rr(d, 30, sb_y, W-60, 52, 14, h2r(INDIGO))
            d.text((W//2 - d.textlength("投稿する", font=F['b24'])//2, sb_y+10), "投稿する", font=F['b24'], fill=WHITE)

    # Submitted + toast at t=5.0
    if t >= 5.0:
        toast_alpha = 1.0 if t < 6.0 else clamp(1-(t-6.0)/0.5)
        tw = d.textlength("📎 投稿しました！", font=F['b22'])
        rr(d, W//2-int(tw/2)-30, 100, int(tw)+60, 44, 22, (int(51*toast_alpha), int(51*toast_alpha), int(51*toast_alpha)))
        d.text((W//2-int(tw/2), 108), "📎 投稿しました！", font=F['b22'], fill=(int(255*toast_alpha), int(255*toast_alpha), int(255*toast_alpha)))

        # New card flash
        flash_t = clamp((t-5.2)/0.3)
        if flash_t > 0:
            rr(d, 30, 505, W-60, 260, 18, WHITE, outline=h2r(INDIGO), width=4)
            d.text((50, 517), "TJ-13 鶴瀬", font=F['b20'], fill=h2r(ORANGE))
            d.text((W-130, 519), "たった今", font=F['r14'], fill=h2r(GRAY))
            d.text((50, 547), "鶴瀬駅🌸 新しいカフェ オープン", font=F['b22'], fill=h2r(DARK))
            rr(d, 46, 581, W-92, 70, 10, h2r(BG))
            d.text((80, 589), "新カフェ 鶴瀬", font=F['b18'], fill=h2r(DARK))
            d.text((80, 613), "駅から徒歩3分。本格派コーヒー", font=F['r14'], fill=h2r("#666666"))
            rr(d, 46, 661, 80, 26, 10, h2r(INDIGO_LT))
            d.text((56, 663), "#カフェ", font=F['b16'], fill=h2r(INDIGO))
            rr(d, 134, 661, 90, 26, 10, h2r(INDIGO_LT))
            d.text((144, 663), "#鶴瀬", font=F['b16'], fill=h2r(INDIGO))

            # Existing cards below
            for i, p in enumerate(POSTS[:2]):
                card(d, p, 30, 790+i*270, 1.0, saved=False)

    # Subtitle
    if t <= 6.0:
        sa = 1.0 if t < 5.5 else clamp(1-(t-5.5)/0.5)
        draw_subtitle(d, "あなたも、1日1回投稿できる", sa)

    return np.array(img)


def end_scene(t):
    """42-45s (local 0-3)"""
    img = Image.new('RGB', (W, H), h2r(BG))
    d = ImageDraw.Draw(img)
    draw_header(d)

    # Background darkens - simple RGB approach
    bg_alpha = clamp(t / 1.0)
    # Draw dark rectangle with simulated alpha
    dark_r = int(255 * (1-bg_alpha) + 10 * bg_alpha)
    dark_g = int(255 * (1-bg_alpha) + 10 * bg_alpha)
    dark_b = int(255 * (1-bg_alpha) + 26 * bg_alpha)
    d.rectangle([0, 0, W, H], fill=(dark_r, dark_g, dark_b))

    # End text
    text_alpha = clamp((t-0.2)/0.5)
    ta = int(255 * text_alpha)

    # Emoji
    d.text((W//2-35, 700), "🚃", font=_font(80))

    # Title
    d.text((W//2-130, 800), "東上リンク", font=F['title'], fill=(ta, ta, ta))

    # Sub
    sub_a = int(153 * text_alpha)
    d.text((W//2-80, 880), "もうすぐ開始", font=F['b28'], fill=(sub_a, sub_a, sub_a))

    # Final subtitle
    if t >= 1.5:
        sa2 = clamp((t-1.5)/0.5)
        draw_subtitle(d, "写真もログインも、いらない 🚃", sa2)

    return np.array(img)


# ── Master frame function ──
def make_frame(t):
    if t < 5:
        return opening(t)
    elif t < 15:
        return station_picker(t - 5)
    elif t < 20:
        return filter_scene(t - 15)
    elif t < 30:
        return save_scene(t - 20)
    elif t < 35:
        return connection_scene(t - 30)
    elif t < 42:
        return post_scene(t - 35)
    else:
        return end_scene(t - 42)


# ── Progress callback ──
def progress_cb(t):
    pct = t / DURATION * 100
    print(f"\r  Rendering: {pct:.0f}% ({t:.1f}s / {DURATION}s)", end="", flush=True)


# ═══════════════════════════════════════
# MAIN
# ═══════════════════════════════════════
if __name__ == "__main__":
    print(f"🚃 東上リンク Demo MP4 Generator")
    print(f"  Resolution: {W}x{H}")
    print(f"  Duration: {DURATION}s @ {FPS}fps")
    print(f"  Output: {OUT_DIR}/demo.mp4")
    print()

    t0 = _time.time()
    clip = VideoClip(make_frame, duration=DURATION)
    clip.write_videofile(
        os.path.join(OUT_DIR, "demo.mp4"),
        fps=FPS,
        codec="libx264",
        audio=False,
        preset="medium",
        logger="bar",
        threads=4,
    )

    elapsed = _time.time() - t0
    print(f"\n\n✅ Done in {elapsed:.1f}s")
    print(f"📁 {os.path.join(OUT_DIR, 'demo.mp4')}")
