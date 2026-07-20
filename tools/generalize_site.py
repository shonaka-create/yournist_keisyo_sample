from pathlib import Path

root = Path(__file__).resolve().parents[1] / "site"

common = {
    "医薬品卸売の受発注・配送・問い合わせの属人化を解消し、標準化・事業承継につなげるサービスです。": "卸業界の受発注・在庫・配送・問い合わせの属人化を解消し、標準化・事業承継につなげるサービスです。",
    "https://example.com/assets/img/ogp.svg": "https://example.com/assets/img/ogp.png",
}

specific = {
    "service/order/index.html": {
        "受発注・価格ルールの標準化｜医薬品卸売": "受発注・価格ルールの標準化｜卸売業",
        "医薬品卸売の得意先別掛率・仕切価・薬価改定・未妥結などの価格ルール": "卸売業の得意先別単価・仕入条件・価格改定・値引き例外などの価格ルール",
        "医薬品卸売の受発注・価格ルール標準化": "卸売業の受発注・価格ルール標準化",
        '"name":"医薬品卸売業"': '"name":"卸売業"',
        "得意先別の掛率・仕切価、薬価改定、未妥結や総価取引、値引き例外。": "得意先別の卸価格・仕入条件、価格改定、暫定単価や一括値引き、個別の例外。",
        "基幹システム、Excel、紙の覚書で掛率や仕切価": "基幹システム、Excel、紙の覚書で卸価格や仕入条件",
        "薬価改定時の対象抽出": "仕入価格改定時の対象抽出",
        "未妥結、総価取引、特別値引き": "暫定単価、一括値引き、特別条件",
        "掛率・仕切価・薬価・契約条件": "仕入条件・卸価格・契約条件",
        "未妥結時の扱い": "暫定単価の扱い",
        "未妥結、総価取引、返品": "暫定単価、一括値引き、返品",
        "医薬品卸の商習慣を前提に": "対象となる卸業界の商習慣を確認し",
        "急配、期限・ロット・温度帯、返品・回収": "急配、納期・ロット・保管条件、返品・回収",
    },
    "service/delivery/index.html": {
        "配送・返品回収手順の標準化｜医薬品卸売": "在庫・配送・返品手順の標準化｜卸売業",
        "医薬品卸売の急配判断、使用期限・ロット・温度帯、返品・回収": "卸売業の発注・引当・急配判断、期限・ロット・保管条件、返品・回収",
        "医薬品卸売の配送・返品回収手順標準化": "卸売業の在庫・配送・返品手順標準化",
        '"name":"医薬品卸売業"': '"name":"卸売業"',
        "急配判断、使用期限・ロット・温度帯": "発注・引当・急配判断、期限・ロット・保管条件",
        "使用期限・ロット・温度帯": "期限・ロット・保管条件",
        "常温・冷所・冷凍の扱い、使用期限の許容条件": "商材別の保管条件、期限の許容条件",
        "品名、数量、使用期限、ロット、温度帯": "品名、数量、期限、ロット、保管条件",
        "医薬品卸の温度帯・期限・ロット管理を前提に": "対象商材の期限・ロット・保管条件を確認し",
        "得意先別の価格ルール": "得意先別の取引・価格ルール",
    },
    "service/support/index.html": {
        "問い合わせ対応の標準化｜医薬品卸売": "問い合わせ・社内ナレッジの標準化｜卸売業",
        "医薬品卸売の在庫・納期・欠品・代替品": "卸売業の在庫・納期・欠品・代替商品",
        "医薬品卸売の問い合わせ対応標準化": "卸売業の問い合わせ・社内ナレッジ標準化",
        '"name":"医薬品卸売業"': '"name":"卸売業"',
        "代替品": "代替商品",
        "営業・管理薬剤師・メーカー等": "営業・商品管理責任者・仕入先等",
        "使用期限・ロット": "商品仕様・ロット",
        "医薬品卸のバックオフィス業務": "卸売業のバックオフィス業務",
        "急配、期限・ロット・温度帯": "急配、納期・ロット・保管条件",
    },
    "contact/index.html": {
        "医薬品卸売の受発注・配送・問い合わせ": "卸業界の受発注・在庫・配送・問い合わせ",
        "例）○○医薬品株式会社": "例）○○商事株式会社",
        "例）受発注の価格計算がベテラン1名に依存しており": "例）得意先別の価格計算がベテラン1名に依存しており",
    },
    "column/index.html": {
        "医薬品卸売の業務属人化、業務標準化の進め方、事業承継における実務の引き継ぎ": "卸業界の業務属人化、業務標準化の進め方、事業承継における実務の引き継ぎ",
        "医薬品卸売の業務属人化、標準化、事業承継を解説する記事一覧。": "卸業界の業務属人化、標準化、事業承継を解説する記事一覧。",
        "業務の属人化、標準化、事業承継に加え、GDP・安定供給・回収・BCPなど医薬品卸の実務を、公的資料をもとに解説します。": "卸業界に共通する属人化・標準化・事業承継と、初期対象である医薬品卸の専門実務を、カテゴリ別に解説します。",
        "医薬品卸売の受発注・配送・問い合わせ": "卸業界の受発注・在庫・配送・問い合わせ",
        '<span class="card__tag">業務属人化</span>': '<span class="card__tag">卸業界共通 / 業務属人化</span>',
        '<span class="card__tag">業務標準化</span>': '<span class="card__tag">卸業界共通 / 業務標準化</span>',
        '<span class="card__tag">事業承継</span>': '<span class="card__tag">卸業界共通 / 事業承継</span>',
        '<span class="card__tag">GDP・品質管理</span>': '<span class="card__tag">医薬品卸 / GDP・品質管理</span>',
        '<span class="card__tag">安定供給</span>': '<span class="card__tag">医薬品卸 / 安定供給</span>',
        '<span class="card__tag">返品・回収</span>': '<span class="card__tag">医薬品卸 / 返品・回収</span>',
        '<span class="card__tag">BCP</span>': '<span class="card__tag">医薬品卸 / BCP</span>',
        '<span class="card__tag">価格交渉</span>': '<span class="card__tag">医薬品卸 / 価格交渉</span>',
        '<span class="card__tag">薬価改定</span>': '<span class="card__tag">医薬品卸 / 薬価改定</span>',
        '<span class="card__tag">温度管理</span>': '<span class="card__tag">医薬品卸 / 温度管理</span>',
        '<span class="card__tag">情報セキュリティ</span>': '<span class="card__tag">医薬品卸 / 情報セキュリティ</span>',
        '<span class="card__tag">物流改善</span>': '<span class="card__tag">医薬品卸 / 物流改善</span>',
        '<span class="card__tag">在庫管理</span>': '<span class="card__tag">医薬品卸 / 在庫管理</span>',
        "医薬品卸での解消ステップ": "卸売業での解消ステップ",
    },
}

for rel, replacements in specific.items():
    path = root / rel
    text = path.read_text(encoding="utf-8")
    for old, new in common.items():
        text = text.replace(old, new)
    for old, new in replacements.items():
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")

# Keep generated article chrome aligned with the broader wholesale positioning.
generator = root.parent / "tools" / "generate_columns.py"
if generator.exists():
    text = generator.read_text(encoding="utf-8")
    text = text.replace("医薬品卸売の属人化を解消し、標準化・事業承継につなげるサービスです。", "卸業界の属人化を解消し、標準化・事業承継につなげるサービスです。")
    generator.write_text(text, encoding="utf-8")

for path in root.rglob("*.html"):
    text = path.read_text(encoding="utf-8")
    text = text.replace("https://example.com/assets/img/ogp.svg", "https://example.com/assets/img/ogp.png")
    path.write_text(text, encoding="utf-8")

generic_articles = [
    root / "column" / "attribution" / "index.html",
    root / "column" / "standardization" / "index.html",
    root / "column" / "succession" / "index.html",
]
generic_terms = {
    "医薬品卸売": "卸売業",
    "医薬品卸": "卸売業",
    "医薬品": "商品",
    "薬価改定": "仕入価格改定",
    "薬価": "仕入価格",
    "掛率・仕切価": "掛率・仕入条件",
    "未妥結・総価取引": "暫定単価・一括値引き",
    "使用期限・ロット・温度帯": "期限・ロット・保管条件",
    "常温・冷所・冷凍": "商材別の保管条件",
    "代替品": "代替商品",
    "医療機関・薬局": "取引先",
    "管理薬剤師": "商品管理責任者",
}
for path in generic_articles:
    text = path.read_text(encoding="utf-8")
    for old, new in generic_terms.items():
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")
