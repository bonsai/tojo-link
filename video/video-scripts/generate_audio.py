"""
東上リンク — 音声生成スクリプト
edge-tts で おばさんハスキーボイス（明るい45秒）
"""

import asyncio
import edge_tts
import os

SCRIPT_DIR = os.path.dirname(__file__)
OUT_DIR = os.path.join(SCRIPT_DIR, "audio")
os.makedirs(OUT_DIR, exist_ok=True)

# 45秒台本
TEXT = """ねぇ、知ってる？鶴瀬駅に、やばい居酒屋あるの！
忠八。駅徒歩1分。昭和60年から続いてるの。
入ったらびっくり、メニューが壁一面！全部手書きよ。
焼き鳥1本80円。えっ、ほんと？ってなるわよね。
お刺身盛り4種類で480円。これがね、ほんとに新鮮なの。
マグロのお寿司5貫で300円。スーパーより安いわよ。
お通し代すらないの！枝豆100円、馬刺し680円。
レトロな雰囲気でね、地元の人がずっと通ってるの。
あなた、行ったことある？コメントで教えてね！"""

# Nanami = 女性・明るめ
VOICE = "ja-JP-NanamiNeural"

async def generate():
    """通常バージョン"""
    out = os.path.join(OUT_DIR, "chuhachi_normal.mp3")
    comm = edge_tts.Communicate(TEXT, VOICE, rate="+0%", volume="+20%")
    await comm.save(out)
    print(f"✅ 通常: {out}")

async def generate_fast():
    """少し速め（テンポ良く）"""
    out = os.path.join(OUT_DIR, "chuhachi_fast.mp3")
    comm = edge_tts.Communicate(TEXT, VOICE, rate="+15%", volume="+20%")
    await comm.save(out)
    print(f"✅ 速め: {out}")

async def generate_deep():
    """少し低め（ハスキー寄り）"""
    out = os.path.join(OUT_DIR, "chuhachi_deep.mp3")
    comm = edge_tts.Communicate(TEXT, VOICE, rate="+5%", volume="+20%", pitch="-10Hz")
    await comm.save(out)
    print(f"✅ 低め: {out}")

async def generate_energetic():
    """明るくエネルギッシュ"""
    out = os.path.join(OUT_DIR, "chuhachi_energetic.mp3")
    comm = edge_tts.Communicate(TEXT, VOICE, rate="+10%", volume="+30%", pitch="+5Hz")
    await comm.save(out)
    print(f"✅ 元気: {out}")

async def main():
    print("🎙️ 音声生成スタート...")
    await generate()
    await generate_fast()
    await generate_deep()
    await generate_energetic()
    print("\n📁 出力先:", OUT_DIR)

if __name__ == "__main__":
    asyncio.run(main())
