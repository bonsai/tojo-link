"""
忠八 動画生成 — 池袋→鶴瀬 アニメーション付き
音声: chuhachi_fast.mp3 (45秒)
"""

from moviepy.editor import VideoClip, AudioFileClip, concatenate_videoclips
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os, math, time as _time

AUDIO_FILE = os.path.join(os.path.dirname(__file__), "audio", "chuhachi_fast.mp3")
OUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUT_DIR, exist_ok=True)

W, H, FPS = 1080, 1920, 30

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
     't20': _font(20), 't18': _font(18), 't16': _font(16), 't14': _font(14)}

ORANGE = "#ff6b35"
INDIGO = "#5b6abf"
WHITE = "#ffffff"
GRAY_LT = "#e0e0e0"
DARK = "#1a1a2e"
BG = "#ffffff"
MAP_BG = "#f0f0f0"

def clamp(v,a=0,b=1): return max(a,min(b,v))
def lerp(a,b,t): return a+(b-a)*clamp(t)
def rr(d,x,y,w,h,r,fill,outline=None,width=0):
    d.rounded_rectangle([x,y,x+w,y+h],radius=r,fill=fill,outline=outline,width=width)

# ── 駅座標（簡易マップ用） ──
# 路線図: 上から下へ（池袋 → 鶴瀬）
STATION_LINE = [
    ("池袋", 540, 300),
    ("中板橋", 540, 400),
    ("ときわ台", 540, 480),
    ("上板橋", 540, 560),
    ("東武練馬", 540, 640),
    ("下赤塚", 540, 720),
    ("成増", 540, 800),
    ("和光市", 540, 880),
    ("朝霞", 540, 960),
    ("志木", 540, 1040),
    ("柳瀬川", 540, 1120),
    ("みずほ台", 540, 1200),
    ("鶴瀬", 540, 1280),
]

def draw_map_frame(progress, highlight_station=None, show_tsuruse=False):
    """progress: 0=池袋, 1=鶴瀬"""
    img = Image.new('RGB', (W, H), h2r("#f5f5f0"))
    d = ImageDraw.Draw(img)

    # Title
    tw = int(d.textlength("🚃 東武東上線", font=F['t42']))
    d.text((W//2 - tw//2, 60), "🚃 東武東上線", font=F['t42'], fill=h2r(INDIGO))

    # Line
    line_x = 540
    rr(d, line_x - 3, 250, 6, 1100, 3, h2r("#cccccc"))

    # Stations
    for name, sx, sy in STATION_LINE:
        is_highlight = (highlight_station and name == highlight_station) or (show_tsuruse and name == "鶴瀬")

        # Dot
        dot_r = 18 if is_highlight else 10
        dot_color = h2r(ORANGE) if is_highlight else h2r("#999999")
        d.ellipse([sx - dot_r, sy - dot_r, sx + dot_r, sy + dot_r], fill=dot_color)

        # Label
        lw = int(d.textlength(name, font=F['t22']))
        d.text((sx - lw//2, sy + 26), name, font=F['t22'],
               fill=h2r(ORANGE) if is_highlight else h2r("#666666"))

    # Animated train dot (moves from 池袋 to 鶴瀬)
    if progress > 0:
        train_y = int(lerp(300, 1280, progress))
        # Train icon
        rr(d, line_x - 24, train_y - 20, 48, 40, 8, h2r(ORANGE))
        tw2 = int(d.textlength("🚃", font=F['t24']))
        d.text((line_x - tw2//2, train_y - 16), "🚃", font=F['t24'])

    # Destination label
    if show_tsuruse:
        rr(d, 340, 1340, 400, 70, 20, h2r(ORANGE))
        tw3 = int(d.textlength("鶴瀬駅", font=F['t38']))
        d.text((W//2 - tw3//2, 1348), "鶴瀬駅", font=F['t38'], fill=WHITE)

    return np.array(img)


def draw_card_frame(shop_name, tags, prices, atmosphere, bottom_text):
    """カード風フレーム"""
    img = Image.new('RGB', (W, H), h2r(BG))
    d = ImageDraw.Draw(img)

    # ヘッダー
    rr(d, 0, 0, W, 120, 0, WHITE)
    d.line([(0,120),(W,120)], fill=h2r(GRAY_LT), width=2)
    d.text((60, 30), "🚃 東上リンク", font=F['t42'], fill=h2r(INDIGO))

    # カード
    rr(d, 40, 160, W-80, 600, 24, WHITE, outline=h2r(ORANGE), width=4)

    # 店名
    d.text((80, 190), shop_name, font=F['t50'], fill=h2r(DARK))

    # タグ
    tx = 80
    for tag in tags:
        tw = int(d.textlength(f"#{tag}", font=F['t24'])) + 30
        rr(d, tx, 270, tw, 38, 14, h2r(INDIGO))
        d.text((tx + 15, 274), f"#{tag}", font=F['t24'], fill=WHITE)
        tx += tw + 12

    # 価格
    y = 330
    for price in prices:
        label, val = price
        d.text((80, y), label, font=F['t26'], fill=h2r("#666666"))
        tw2 = int(d.textlength(val, font=F['t32']))
        d.text((W - 100 - tw2, y), val, font=F['t32'], fill=h2r(ORANGE))
        y += 50

    # 雰囲気
    d.text((80, 520), atmosphere, font=F['t26'], fill=h2r("#555555"))

    # 下部テキスト
    bw = int(d.textlength(bottom_text, font=F['t32']))
    rr(d, W//2 - bw//2 - 30, 1600, bw + 60, 60, 30, h2r(INDIGO))
    d.text((W//2 - bw//2, 1610), bottom_text, font=F['t32'], fill=WHITE)

    # 「行きたい」ボタン
    rr(d, 290, 1720, 500, 80, 24, h2r(ORANGE))
    bw2 = int(d.textlength("🙋 行きたい！", font=F['t32']))
    d.text((W//2 - bw2//2, 1730), "🙋 行きたい！", font=F['t32'], fill=WHITE)

    return np.array(img)


# ── テロップ用フレーム ──
def draw_subtitle_frame(text, sub_text=None, emoji="🚃"):
    img = Image.new('RGB', (W, H), h2r("#1a1a2e"))
    d = ImageDraw.Draw(img)

    # 絵文字
    d.text((W//2 - 40, 600), emoji, font=_font(100))

    # メインテキスト
    tw = int(d.textlength(text, font=F['t50']))
    d.text((W//2 - tw//2, 740), text, font=F['t50'], fill=WHITE)

    # サブ
    if sub_text:
        sw = int(d.textlength(sub_text, font=F['t28']))
        d.text((W//2 - sw//2, 820), sub_text, font=F['t28'], fill=h2r("#cccccc"))

    return np.array(img)


# ── 音声タイミングに合わせたシーン ──
"""
ねぇ、知ってる？鶴瀬駅に、やばい居酒屋あるの！  → 0-3s
忠八。駅徒歩1分。昭和60年から続いてるの。        → 3-9s
入ったらびっくり、メニューが壁一面！全部手書きよ。→ 9-14s
焼き鳥1本80円。えっ、ほんと？ってなるわよね。      → 14-19s
お刺身盛り4種類で480円。これがね、ほんとに新鮮なの。→ 19-25s
マグロのお寿司5貫で300円。スーパーより安いわよ。   → 25-30s
お通し代すらないの！枝豆100円、馬刺し680円。      → 30-35s
レトロな雰囲気でね、地元の人がずっと通ってるの。    → 35-40s
あなた、行ったことある？コメントで教えてね！        → 40-45s
"""

SCENES = [
    # (start_sec, end_sec, draw_func)
    (0, 3, lambda t: draw_subtitle_frame("ねぇ、知ってる？", "鶴瀬駅に、やばい居酒屋あるの！", "😲")),
    (3, 9, lambda t: draw_subtitle_frame("忠八", "駅徒歩1分・昭和60年創業", "🏠")),
    (9, 14, lambda t: draw_subtitle_frame("壁一面、手書きメニュー", "入ったらびっくり！", "📋")),
    (14, 19, lambda t: draw_card_frame(
        "🍢 やきとり大衆酒蔵 忠八",
        ["鶴瀬", "昭和60年", "コスパ"],
        [("焼き鳥", "1本 80円")],
        "えっ、ほんと？ってなるわよね",
        "徒歩1分"
    )),
    (19, 25, lambda t: draw_card_frame(
        "🐟 お刺身盛り",
        ["新鮮", "安い"],
        [("刺身盛り4種", "480円")],
        "これがね、ほんとに新鮮なの",
        "選べる4種類"
    )),
    (25, 30, lambda t: draw_card_frame(
        "🍣 マグロ寿司",
        ["スーパーより安い"],
        [("マグロ5貫", "300円")],
        "スーパーより安いわよ",
        "5貫で300円"
    )),
    (30, 35, lambda t: draw_card_frame(
        "✅ お通し代なし！",
        ["枝豆", "馬刺し"],
        [("枝豆", "100円"), ("馬刺し", "680円"), ("お通し代", "なし！")],
        "お通し代すらないの！",
        "無料"
    )),
    (35, 40, lambda t: draw_card_frame(
        "🏮 レトロな雰囲気",
        ["地元民", "39年"],
        [],
        "地元の人がずっと通ってるの",
        "昭和60年創業"
    )),
    (40, 45, lambda t: draw_subtitle_frame(
        "行ったことある？",
        "コメントで教えてね！",
        "💬"
    )),
]


def make_frame(t):
    for start, end, draw_func in SCENES:
        if start <= t < end:
            return draw_func(t)
    return np.array(Image.new('RGB', (W, H), h2r("#1a1a2e")))


if __name__ == "__main__":
    print("🎬 忠八 動画作成スタート...")
    print(f"  音声: {AUDIO_FILE}")
    print(f"  出力: {OUT_DIR}/chuhachi_video.mp4\n")

    t0 = _time.time()

    # 音声ファイル読み込み
    audio = AudioFileClip(AUDIO_FILE)
    duration = audio.duration
    print(f"  音声長: {duration:.1f}秒")

    clip = VideoClip(make_frame, duration=duration)
    clip = clip.set_audio(audio)

    clip.write_videofile(
        os.path.join(OUT_DIR, "chuhachi_video.mp4"),
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        preset="medium",
        logger="bar",
        threads=4,
    )

    elapsed = _time.time() - t0
    print(f"\n✅ Done in {elapsed:.1f}s")
    print(f"📁 {OUT_DIR}/chuhachi_video.mp4")
