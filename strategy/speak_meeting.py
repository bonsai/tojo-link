"""
議事録読み上げスクリプト
"""
import pyttsx3
import os

TEXT_FILE = os.path.join(os.path.dirname(__file__), "meeting-minutes-v1.txt")

with open(TEXT_FILE, "r", encoding="utf-8") as f:
    text = f.read()

engine = pyttsx3.init()
engine.setProperty("rate", 160)  # 少し速め
engine.setProperty("volume", 1.0)

# 日本語音声を選択
voices = engine.getProperty("voices")
ja_voice = None
for v in voices:
    if "ja" in v.id.lower() or "haruka" in v.id.lower() or "japanese" in v.id.lower():
        ja_voice = v.id
        break

if ja_voice:
    engine.setProperty("voice", ja_voice)

print("🎙️ 議事録を読み上げます...")
engine.say(text)
engine.runAndWait()
print("✅ 読み上げ完了")
