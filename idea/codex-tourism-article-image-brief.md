# Codex 依頼書 — 観光業 記事カード画像（800×500）

作成: 2026-08-02 / 発注 = Claude / 実装 = Codex
関連: `site/column/tourism/index.html` / `idea/codex-note-cover-brief.md`

---

## 0. これは何の画像か

`site/column/tourism/index.html` の記事一覧カードに乗るサムネイル。
**noteのカバー画像（1280×670）とは別物**なので、`codex-note-cover-brief.md` の仕様（左55%を暗い余白にする）は**適用しない**。

| | note カバー | 記事カード画像（本書） |
|---|---|---|
| サイズ | 1280×670 | **800×500** |
| 文字の乗せ方 | 画像の上にPillowで組版 | **乗せない**（文字はカード内の別要素） |
| ネガティブスペース | 左55%が必須 | **不要**。被写体を中央に置く |
| 保存先 | `note/covers/source/` | `site/assets/img/` |

カードでは `object-fit:cover` で高さ210pxに切られる（[industry-columns.css](../site/assets/css/industry-columns.css) の `.tourism-columns .ic-article__visual img`）。
上下が大きく削られるため、**被写体は中央の帯に収める**こと。

---

## 1. 納品物（1点）

| 項目 | 値 |
|---|---|
| 保存先 | `site/assets/img/tourism-article-cancellation-refund.webp` |
| サイズ | **800 × 500 px**（1.6:1） |
| 形式 | WebP / RGB / 目標 20〜30KB |
| 生成時の入稿サイズ | **1536 × 1024 px 以上**（横長PNG。後述の手順で縮小・変換） |

対象記事：[旅行会社の取消料・返金判断を標準化｜担当者ごとの差をなくす](../site/column/tourism/cancellation-refund/index.html)

---

## 2. 世界観（既存10枚と揃える）

`site/assets/img/tourism-article-*.webp` を先に見てから作ること。共通しているのは以下。

- **実写のドキュメンタリー調**。演出されたストックフォト感を出さない
- 日本人のオフィスワーカー。**顔は画面外へ切れていてよい**（むしろ寄りの構図が既存の特徴）
- 落ち着いたネイビー／グレー基調、自然光。彩度は低め
- 画面内の文字は**すべて判読不能**であること（モニタ・書類はボケているか浅い被写界深度の外）
- 手元の作業（タブレット、電話、書類）が主題。人物の表情ではなく**動作**を撮る

### 禁止事項（ブランド上の必須条件）

- 文字・数字・ロゴ・透かし・判読可能な書類/画面
- テック演出（ホログラム、光るUI、回路パターン、青い粒子、ロボット）
  → **「AIっぽさ」を出さないこと**（[docs/BUSINESS-DEFINITION.md](../docs/BUSINESS-DEFINITION.md) §5）
- 危機の誇張（怒った客、頭を抱える社員、赤い警告表示、散らかった机）
- 実在ブランド、企業ロゴ、個人情報、クレジットカードの実券面

---

## 3. プロンプト

```
Use case: editorial-blog-thumbnail. Wide 1.6:1 documentary-style photograph for a
Japanese B2B article about standardizing cancellation-fee and refund decisions at a
small Japanese travel agency. Two Japanese office workers at a travel agency desk
reviewing a printed booking cancellation record together: one points at a line on the
paper while the other holds a calculator and a pen over a notepad. Tight editorial crop
from slightly above; faces may be partially cut off by the frame edge; the emphasis is
on the hands, the paper, and the calculator, not on facial expression. Subject centered
in the middle horizontal band of the frame. Muted navy and warm gray office interior,
soft natural window light, shallow depth of field, low saturation, calm and orderly.
No text, letters, numbers, logos, watermarks, readable documents or screens, no credit
cards, no angry or distressed expressions, no futuristic holograms, glowing interfaces,
circuit patterns, or robots.
```

**電卓と紙の取消記録**を主題にしているのは、既存10枚がタブレット・PC・電話に寄っていて、
「金額を計算して決める」画がまだ無いため。カード一覧に並べたとき絵柄が重複しない。

### 検収の観点

1. 中央の横帯（上下25%を切り落とした残り）だけを見て、主題が成立しているか
2. 判読できる文字が1つも無いか（モニタの文字列、書類の見出し、電卓の数字表示）
3. 既存の `tourism-article-agency-costing.webp` と並べて、色温度と彩度が浮いていないか

いずれかを外していたら再生成する。

---

## 4. 変換手順（生成後）

生成PNGを `800×500` の WebP へ落とす。中央クロップしてからリサイズする。

```bash
python - <<'EOF'
from PIL import Image
src = Image.open("<生成したPNGのパス>").convert("RGB")
W, H = 800, 500
r = max(W / src.width, H / src.height)
im = src.resize((round(src.width * r), round(src.height * r)), Image.LANCZOS)
l, t = (im.width - W) // 2, (im.height - H) // 2
im.crop((l, t, l + W, t + H)).save(
    "site/assets/img/tourism-article-cancellation-refund.webp",
    "WEBP", quality=80, method=6)
EOF
```

`quality=80` で 20〜30KB に収まる（既存10枚は18〜29KB）。
40KBを超えるようなら `quality=72` まで落としてよい。

---

## 5. 差し替え（納品後にClaude側で実行）

現在このカードは `tourism-article-agency-costing.webp` を流用している。
[site/column/tourism/index.html](../site/column/tourism/index.html) の1箇所を書き換えるだけで完了する。

```diff
 <a class="ic-article" data-category="agency" href="cancellation-refund/index.html">
-<span class="ic-article__visual"><img src="../../assets/img/tourism-article-agency-costing.webp"
+<span class="ic-article__visual"><img src="../../assets/img/tourism-article-cancellation-refund.webp"
  alt="旅行会社の取消料と返金を確認するイメージ"></span>
```

記事ページ側（`site/column/tourism/cancellation-refund/index.html`）は本文に画像を持たず、
OGPは `tourism-hero.webp` を使うため**変更不要**。

差し替え後、`site/` を `.publish-yournist/site/` へ同期して再デプロイする。
