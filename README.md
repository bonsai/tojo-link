# 🚃 東上リンク

> 東武東上線 やばい店発掘プラットフォーム

---

## 📂 フォルダ構成

```
tojo-link-board/
├── demo/          ← HTMLデモ（ブラウザで開くだけ）
│   ├── index.html      ← 元UIデモ
│   ├── simple.html     ← シンプル版デモ（おばさんにわかりやすく）
│   ├── route.html      ← 路線図アニメーション（池袋→鶴瀬）
│   └── auto-play.html  ← 自動再生デモ（画面録画用）
│
├── docs/          ← 戦略・設計ドキュメント
│   ├── STRATEGY-v6.md        ← 最新戦略（バズらせ→ループ）
│   ├── BUSINESS-v5.md        ← ビジネスモデル（だれでも広告）
│   ├── 3-DAY-LOOP.md         ← 3日改善ループ
│   └── ...
│
├── video/         ← 動画制作まわり
│   ├── demo-video/       ← Remotion動画（MP4生成）
│   │   ├── out/              ← 出力MP4
│   │   └── src/              ← Remotionソース
│   └── video-scripts/    ← 忠八動画作成
│       ├── audio/            ← 音声ファイル（edge-tts）
│       ├── output/           ← 出力MP4（忠八v1, v2）
│       ├── generate_audio.py   ← 音声生成スクリプト
│       └── make_video_v2.py    ← 動画作成スクリプト
│
└── app/           ← Webアプリ（Firebase連携予定）
    ├── package.json
    ├── public/data/stations.json  ← 駅データ
    └── src/
        ├── components/   ← UIコンポーネント
        └── styles/       ← CSS
```

---

## 🚀 クイックスタート

### デモを見る
```
demo/simple.html をブラウザで開く
```

### 路線図アニメーション
```
demo/route.html をブラウザで開く
```

### 忠八動画を再生
```
video/video-scripts/output/chuhachi_v2.mp4
```

### 音声を聞き比べ
```
video/video-scripts/audio/
  ├── chuhachi_fast.mp3    ← 推奨（テンポ良い）
  ├── chuhachi_normal.mp3
  ├── chuhachi_deep.mp3
  └── chuhachi_energetic.mp3
```
