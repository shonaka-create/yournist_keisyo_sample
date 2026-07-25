# 観光業向け Instagram 広告クリエイティブ

インバウンド旅行会社・中小ホテルを対象にした、1080×1080pxのInstagram広告案です。生成写真には文字を含めず、YOURNISTロゴと日本語コピーをローカルで正確に組版しています。

## 1. 予約・手配業務の属人化

- 出力ファイル
  - `tourism-ad-reservation-handover.png`
  - `tourism-ad-reservation-handover.webp`
- 広告見出し：予約・手配の「あの人しかできない」を、チームの仕組みに。
- 本文案：見積・予約・送迎・変更対応。担当者の経験に埋もれた判断基準を整理し、次の担当者が迷わず動ける業務へ整えます。
- CTA：観光業向け支援を見る
- 想定ターゲット：インバウンド旅行会社の経営者、事業責任者、予約・手配部門の責任者
- 訴求目的：繁忙期、退職、担当交代による手配品質の低下や対応停止への危機意識を喚起する
- 生成プロンプト：`Use case: ads-marketing. Square Instagram advertisement background for a Japanese B2B consulting service. A premium photorealistic campaign image about eliminating person-dependent reservation and arrangement operations at a small inbound travel agency in Japan. Modern realistic Japanese travel agency office, two Japanese staff members from different generations reviewing a booking itinerary, reservation dashboard and paper vouchers together. Subjects and operational documents on the right half, dark calm negative space on the left for typography. High-end Japanese corporate editorial photography, deep navy and muted blue-gray. No text, letters, logos, watermark, futuristic holograms, exaggerated crisis or visible personal data.`

## 2. ホテル接客・PMS・多言語対応の引き継ぎ

- 出力ファイル
  - `tourism-ad-hotel-operations.png`
  - `tourism-ad-hotel-operations.webp`
- 広告見出し：接客・PMS・多言語対応。引き継げるホテル運営へ。
- 本文案：ベテランの対応力を、誰でも参照・実行できる形に。フロント業務、PMS操作、例外対応、多言語案内を現場で使える手順へ変えます。
- CTA：ホテル向け支援を見る
- 想定ターゲット：中小ホテル・旅館の経営者、支配人、フロント責任者、人材育成責任者
- 訴求目的：接客品質やシステム運用が個人の記憶に依存する状態を、再現可能な運営へ変える価値を伝える
- 生成プロンプト：`Use case: ads-marketing. Square Instagram advertisement background for a Japanese B2B consulting service. A premium photorealistic campaign image about preserving and handing over hotel front-desk operations, PMS workflows and multilingual guest-response know-how. Contemporary mid-sized Japanese hotel reception, an experienced manager and a younger staff member checking a tablet and operations binder. Subjects on the left and center, darker architectural negative space on the right for typography. High-end corporate editorial photography, warm hospitality light and cool navy shadows. No readable text, letters, logos, watermark, visible guest personal data or hotel brand marks.`

## 3. 観光DX・補助金活用可能性

- 出力ファイル
  - `tourism-ad-dx-subsidy-check.png`
  - `tourism-ad-dx-subsidy-check.webp`
- 広告見出し：観光DX、補助金の活用可能性も確認します。
- 本文案：業務整理を起点に、DX施策と対象経費・公募要件を確認。補助金ありきではなく、必要な投資と実行計画を優先して整理します。
- CTA：補助金関連記事を読む
- 想定ターゲット：インバウンド旅行会社・ホテルの経営者、DX推進担当者、設備・システム投資を検討する責任者
- 訴求目的：制度を過度に期待させず、対象になり得る費用を確認する入口を提供する
- 必須注記：対象可否は制度・公募要件により異なります。採択を保証するものではありません。
- 生成プロンプト：`Use case: ads-marketing. Square Instagram advertisement background for a Japanese B2B consulting service. A premium photorealistic campaign image about tourism digital transformation planning and carefully evaluating whether public subsidies may support eligible implementation costs, without implying approval or guaranteed funding. A small inbound tour operator or hotel management team reviews a phased digital transformation roadmap, operational workflow cards and budget checklist with an advisor. People and materials in the lower-right and center, clean negative space upper-left. Warm ivory, deep navy, muted cyan and restrained sand-gold. No readable text, letters, logos, watermark, currency symbols, government seals, certificates, checks, cash, coins or guaranteed-funding imagery.`

## 制作情報

- 画像生成：Codex組み込み `image_gen`（各案を個別生成）
- 日本語組版：Pillow + BIZ UDPゴシック
- ブランド素材：`site/assets/img/yournist-logo-transparent.png`
- 再生成スクリプト：`tools/build_tourism_instagram_ads.py`
- 元画像：`source/`
- 最終サイズ：1080×1080px
