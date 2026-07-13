"""
忠八 動画 v2 — 池袋→鶴瀬 路線アニメーション付き
しょぼくていい。ポップでいい。
"""

from moviepy.editor import VideoClip, AudioFileClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os, math, time as _time

AUDIO = os.path.join(os.path.dirname(__file__), "audio", "chuhachi_fast.mp3")
OUT = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUT, exist_ok=True)

W, H, FPS = 1080, 1920, 30

def h2r(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def _f(sz):
    for p in [r"C:\Windows\Fonts\meiryo.ttc", r"C:\Windows\Fonts\msgothic.ttc",
              r"C:\Windows\Fonts\yugothic.ttc", "arial.ttf"]:
        try: return ImageFont.truetype(p, sz)
        except: pass
    return ImageFont.load_default()

F = {k: _f(v) for k, v in [
    ('t56',56),('t48',48),('t42',42),('t38',38),('t34',34),('t32',32),('t30',30),
    ('t26',26),('t24',24),('t22',22),('t20',20),('t18',18),('t16',16),('emoji',90)
]}

def clamp(v,a=0,b=1): return max(a,min(b,v))
def lerp(a,b,t): return a+(b-a)*clamp(t)
def rr(d,x,y,w,h,r,fill,outline=None,width=0):
    d.rounded_rectangle([x,y,x+w,y+h],radius=r,fill=fill,outline=outline,width=width)

# ═══════════════════════════════════════
# SCENE 1: Map animation (池袋→鶴瀬)
# ═══════════════════════════════════════

STATIONS = [
    ("池袋", 1),("中板橋", 2),("ときわ台", 3),("上板橋", 4),
    ("東武練馬", 5),("下赤塚", 6),("成増", 7),("和光市", 8),
    ("朝霞", 9),("志木", 10),("柳瀬川", 11),("みずほ台", 12),("鶴瀬", 13),
]

def draw_map_scene(t, duration=6.0):
    """t: 0-duration"""
    img = Image.new('RGB', (W,H), (245,245,240))
    d = ImageDraw.Draw(img)

    progress = clamp(t / duration)

    # Title
    tw = int(d.textlength("🚃 東武東上線", font=F['t42']))
    d.text((W//2-tw//2, 50), "🚃 東武東上線", font=F['t42'], fill=h2r("#5b6abf"))

    # Subtitle
    if t < 3:
        stw = int(d.textlength("池袋駅から...", font=F['t26']))
        d.text((W//2-stw//2, 120), "池袋駅から...", font=F['t26'], fill=h2r("#999999"))
    else:
        stw = int(d.textlength("鶴瀬駅へ！", font=F['t26']))
        d.text((W//2-stw//2, 120), "鶴瀬駅へ！", font=F['t26'], fill=h2r("#ff6b35"))

    # Map area
    map_top = 180
    map_h = 1200
    line_x = W // 2

    # Background rectangle (map feel)
    rr(d, 140, map_top - 10, W-280, map_h + 40, 16, (235,235,230))

    # Draw line
    total_stations = len(STATIONS)
    station_spacing = map_h / (total_stations - 1)

    # Full line (faint)
    rr(d, line_x-3, map_top, 6, map_h, 3, (210,210,200))

    # Animated line (orange, growing)
    active_count = int(progress * (total_stations - 1)) + 1
    active_h = station_spacing * (active_count - 1)
    rr(d, line_x-4, map_top, 8, max(active_h, 8), 4, h2r("#ff6b35"))

    # Stations
    for i, (name, num) in enumerate(STATIONS):
        sy = map_top + i * station_spacing
        is_active = i < active_count
        is_current = i == active_count - 1 and active_count <= total_stations

        if is_current:
            # Highlight: big orange circle
            d.ellipse([line_x-22, sy-22, line_x+22, sy+22], fill=h2r("#ff6b35"))
            # Pulse ring
            pulse = math.sin(t * 4) * 5 + 28
            d.ellipse([line_x-int(pulse), sy-int(pulse), line_x+int(pulse), sy+int(pulse)],
                     outline=h2r("#ff6b35"), width=3)
        elif is_active:
            d.ellipse([line_x-14, sy-14, line_x+14, sy+14], fill=h2r("#ff6b35"))
        else:
            d.ellipse([line_x-10, sy-10, line_x+10, sy+10], fill=h2r("#cccccc"))

        # Label
        lw = int(d.textlength(name, font=F['t20']))
        label_color = h2r("#ff6b35") if is_current else (h2r("#555555") if is_active else h2r("#aaaaaa"))
        d.text((line_x - lw//2, sy + 20), name, font=F['t20'], fill=label_color)

    # Destination badge at bottom
    if progress > 0.8:
        badge_alpha = clamp((progress - 0.8) / 0.2)
        rr(d, 290, 1430, 500, 70, 20, (int(255*badge_alpha), int(107*badge_alpha), int(53*badge_alpha)))
        dw = int(d.textlength("🏠 鶴瀬駅", font=F['t34']))
        d.text((W//2-dw//2, 1438), "🏠 鶴瀬駅", font=F['t34'],
               fill=(int(255*badge_alpha), int(255*badge_alpha), int(255*badge_alpha)))

    return np.array(img)


# ═══════════════════════════════════════
# SCENE 2: Text cards (pop, simple)
# ═══════════════════════════════════════

def draw_text_card(t, title, sub, prices, note, emoji_icon="🏠", bg_color=None):
    """ポップな情報カード"""
    bg = bg_color or (255,255,255)
    img = Image.new('RGB', (W,H), bg)
    d = ImageDraw.Draw(img)

    # ヘッダー
    rr(d, 0, 0, W, 100, 0, (255,255,255))
    d.line([(0,100),(W,100)], fill=h2r("#e0e0e0"), width=2)
    d.text((60, 22), "🚃 東上リンク", font=F['t34'], fill=h2r("#5b6abf"))

    # メインカード
    rr(d, 40, 130, W-80, 800, 24, (255,255,255), outline=h2r("#ff6b35"), width=4)

    # アイコン + 店名
    d.text((70, 150), emoji_icon, font=F['emoji'])
    d.text((180, 155), title, font=F['t48'], fill=h2r("#1a1a2e"))

    # サブ
    d.text((80, 260), sub, font=F['t26'], fill=h2r("#888888"))

    # 価格リスト
    y = 320
    for label, val in prices:
        # Background pill
        lw = int(d.textlength(f"{label} {val}", font=F['t30'])) + 60
        rr(d, 80, y, min(lw, W-160), 48, 16, h2r("#f8f8f8"))
        d.text((95, y+6), label, font=F['t30'], fill=h2r("#555555"))
        vw = int(d.textlength(val, font=F['t30']))
        rx = 80 + min(lw, W-160) - 16 - vw - 10
        d.text((rx, y+6), val, font=F['t30'], fill=h2r("#ff6b35"))
        y += 58

    # 備考
    if note:
        d.text((80, 730), note, font=F['t24'], fill=h2r("#777777"))

    # 下部メッセージ
    msg = "あなた、行ったことある？"
    mw = int(d.textlength(msg, font=F['t34']))
    rr(d, W//2-mw//2-30, 1000, mw+60, 56, 28, h2r("#5b6abf"))
    d.text((W//2-mw//2, 1010), msg, font=F['t34'], fill=(255,255,255))

    # 行きたいボタン
    rr(d, 290, 1100, 500, 76, 22, h2r("#ff6b35"))
    bw = int(d.textlength("🙋 行きたい！", font=F['t32']))
    d.text((W//2-bw//2, 1110), "🙋 行きたい！", font=F['t32'], fill=(255,255,255))

    # コメント案内
    cw = int(d.textlength("↓ コメントで教えてね！", font=F['t22']))
    d.text((W//2-cw//2, 1200), "↓ コメントで教えてね！", font=F['t22'], fill=h2r("#999999"))

    return np.array(img)


# ═══════════════════════════════════════
# SCENE 3: End screen
# ═══════════════════════════════════════

def draw_end_scene(t):
    img = Image.new('RGB', (W,H), h2r("#1a1a2e"))
    d = ImageDraw.Draw(img)

    d.text((W//2-45, 650), "🚃", font=F['emoji'])
    tw = int(d.textlength("東上リンク", font=F['t56']))
    d.text((W//2-tw//2, 770), "東上リンク", font=F['t56'], fill=(255,255,255))
    sw = int(d.textlength("やばい店を発掘しよう", font=F['t30']))
    d.text((W//2-sw//2, 850), "やばい店を発掘しよう", font=F['t30'], fill=h2r("#cccccc"))

    return np.array(img)


# ═══════════════════════════════════════
# MASTER: タイミング合わせ
# ═══════════════════════════════════════

# 音声: 46.2秒
# 0-6s:   路線アニメーション
# 6-42s:  情報カード（3-4シーン）
# 42-46s: エンド

def make_frame(t):
    # Scene 1: Map animation (0-6s)
    if t < 6:
        return draw_map_scene(t, duration=6.0)

    # Scene 2: Info cards (6-42s)
    ct = t - 6  # card time

    if ct < 9:  # 6-15s: 基本情報
        return draw_text_card(ct % 9,
            "やきとり大衆酒蔵 忠八",
            "🚃 鶴瀬駅徒歩1分 | 昭和60年創業 | 39年目",
            [
                ("焼き鳥", "1本 80円"),
                ("刺身盛り4種", "480円"),
                ("マグロ寿司5貫", "300円"),
            ],
            "えっ、ほんと？ってなるわよね",
            "🏠"
        )

    if ct < 18:  # 15-24s: 激安メニュー
        return draw_text_card(ct % 9,
            "お通し代すらない！",
            "枝豆は1人1つ限定、馬刺しもあるよ",
            [
                ("枝豆（限定）", "100円"),
                ("馬刺し", "680円"),
                ("お通し代", "なし！"),
                ("ガリ", "100円"),
            ],
            "スーパーより安いわよ",
            "💰"
        )

    if ct < 27:  # 24-33s: 雰囲気
        return draw_text_card(ct % 9,
            "壁一面、手書きメニュー",
            "入ったらまずびっくり！レトロな空間",
            [
                ("創業", "昭和60年（1985年）"),
                ("席数", "30席"),
                ("営業", "11:00-23:00"),
                ("定休", "水曜日"),
            ],
            "地元の人がずっと通ってるの",
            "📋"
        )

    if ct < 36:  # 33-42s: まとめ
        return draw_text_card(ct % 9,
            "鶴瀬駅やばい店 No.1",
            "何頼んでもハズレなし！",
            [
                ("焼き鳥", "1本 80円"),
                ("刺身盛り", "480円"),
                ("お通し代", "なし！"),
            ],
            "忠八。昭和60年創業、徒歩1分。",
            "🏆",
            bg_color=(255,248,225)
        )

    # Scene 3: End (42-46s)
    return draw_end_scene(t - 42)


# ═══════════════════════════════════════
# MAIN
# ═══════════════════════════════════════

if __name__ == "__main__":
    print("🎬 忠八 動画 v2 スタート...")
    print(f"  音声: {AUDIO}")
    print(f"  出力: {OUT}/chuhachi_v2.mp4\n")

    t0 = _time.time()
    audio = AudioFileClip(AUDIO)
    duration = audio.duration
    print(f"  音声長: {duration:.1f}秒")

    clip = VideoClip(make_frame, duration=duration).set_audio(audio)

    clip.write_videofile(
        os.path.join(OUT, "chuhachi_v2.mp4"),
        fps=FPS, codec="libx264", audio_codec="aac",
        preset="medium", logger="bar", threads=4,
    )

    elapsed = _time.time() - t0
    print(f"\n✅ Done in {elapsed:.1f}s")
    print(f"📁 {OUT}/chuhachi_v2.mp4")
