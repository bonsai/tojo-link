# DJバー JSONL DB

`data/dj-bars/tobu-tojo-dj-bars.jsonl` は1行1店舗のJSONLデータベースです。

## 設計

店舗情報とコンテンツ素材を同じレコードに保持します。

- `id`: 固定ID
- `name` / `area` / `station`: 場所情報
- `dj_evidence` / `dj_status`: DJ可否の調査状態
- `instagram`: 公式Instagram
- `instagram_search`: アカウント未特定時の検索導線
- `sources`: エビデンスURL配列
- `next_action`: 次のリサーチ
- `shorts`: YouTube Shorts転用用の原稿
  - `title`
  - `hook`
  - `script`
  - `cta`
  - `duration_sec`

## JSONLにした理由

- Git diffで1店舗単位の変更を追える
- 後からBigQuery等へロードしやすい
- RAGや検索インデックスの1レコードとして扱いやすい
- 店舗情報からShorts原稿を自動生成しやすい

## 運用

エビデンスが更新されたら同じ`id`のレコードを更新します。Shorts原稿は店舗情報の再利用なので、事実情報と演出テキストを混同しないようにします。
