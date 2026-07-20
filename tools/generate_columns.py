from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "site" / "column"

articles = [
    dict(slug="gdp-basics", tag="GDP・品質管理", title="医薬品GDPガイドラインとは？卸売現場で整えるべき手順と記録", desc="医薬品の仕入・保管・供給を品質システムとして管理するGDPの要点を、医薬品卸の実務に沿って解説します。", lead="GDPは、温度管理だけのルールではありません。仕入先の適格性、受入、保管、出荷、返品、偽造品対策までを、責任・手順・記録でつなぐ考え方です。", sections=[
        ("GDPが医薬品卸に求めるもの", "厚生労働省のGDPガイドラインは、医薬品の同一性を保ち、外装に表示された条件に従って仕入・保管・供給することを基本にしています。担当者の経験だけで品質を守るのではなく、品質システムの中で責任者、手順、逸脱時の対応、記録を明確にすることが重要です。"),
        ("最初に標準化したい4つの業務", "優先したいのは、仕入先・販売先の確認、入荷時の外観と数量の確認、保管場所と温度の管理、出荷時の製品・ロット・期限の照合です。返品や回収品は通常在庫と混ざらない隔離ルールも必要です。"),
        ("手順書を置くだけでは足りない", "手順書は、誰が実行し、どこへ記録し、異常を誰へ報告するかまで書いて初めて運用できます。教育記録、自己点検、委託先評価、温度逸脱の判断など、低頻度の業務も定期的に訓練し、実態に合わせて更新します。"),
        ("属人化解消とGDPを同時に進める", "現場観察から業務の流れを描き、判断根拠と例外を聞き取り、帳票と記録先を結び付けます。品質部門だけに閉じず、受発注・倉庫・配送・問い合わせが同じ情報を参照できる状態にすると、監査対応と引き継ぎの双方が安定します。")], checks=["仕入先と販売先の確認方法が決まっている","受入・保管・出荷の記録を追跡できる","返品・回収・不適合品を隔離できる","温度逸脱時の判断者と連絡先が明確","教育・自己点検・手順改訂の記録がある"], sources=[("厚生労働省「医薬品の適正流通（GDP）ガイドライン」","https://www.mhlw.go.jp/content/11120000/000466215.pdf")]),
    dict(slug="supply-shortage", tag="安定供給", title="医薬品の供給不足に強い受発注へ｜限定出荷・欠品対応の標準化", desc="限定出荷や供給停止が続く環境で、医薬品卸が受発注・在庫・得意先案内を標準化する方法を解説します。", lead="供給不足時は、情報の更新頻度が上がり、在庫配分や納期回答の判断が集中します。平時の受発注手順だけでは、問い合わせと例外処理をさばき切れません。", sections=[
        ("供給情報を一つの入口へ集める", "厚生労働省は医療用医薬品の限定出荷・供給停止情報を公表し、供給状況を更新しています。メーカー通知や卸社内の在庫情報も含め、確認元、更新日時、対象品目、期間、代替可否を同じ形式で整理します。"),
        ("在庫配分の基準を先に決める", "担当者の関係性や声の大きさで決めると、判断の説明ができません。過去実績、医療上の必要性、既受注、供給見込みなど、社内で使う判断項目と承認者を定め、例外は理由を残します。"),
        ("得意先への回答を揃える", "一次対応では、品目、規格、希望数量、必要日、代替候補の確認項目を統一します。確定している事実と見込みを分け、次回更新時期まで伝えると、担当者ごとの回答差を減らせます。"),
        ("解除後まで記録する", "限定出荷の解除や入荷再開後も、滞留注文、過剰発注、代替品在庫を確認します。対応記録を振り返り、情報取得から得意先案内までの時間と再問い合わせ件数を改善指標にします。")], checks=["公的情報とメーカー通知の確認担当がいる","更新日時を含む供給一覧がある","在庫配分の基準と承認者が明確","得意先向け回答テンプレートがある","解除後の注文・在庫を点検している"], sources=[("厚生労働省「医薬品等の供給不安への対応について」","https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/kenkou_iryou/iryou/kouhatu-iyaku/index_00006.html")]),
    dict(slug="recall-response", tag="返品・回収", title="医薬品回収を止めない実務手順｜ロット特定から隔離・連絡まで", desc="医薬品回収時に卸売現場が行う情報確認、対象ロット特定、在庫隔離、得意先連絡、記録の流れを整理します。", lead="回収対応は発生頻度が低い一方、初動の遅れが大きな影響につながります。担当者の記憶ではなく、誰でも同じ順序で対象を追跡できる状態が必要です。", sections=[
        ("最初に確定する情報", "製品名、規格、商品コード、対象ロット、使用期限、回収クラス、通知元、連絡先を確認します。2026年にはPMDAの回収情報でGTINとロット番号を含むCSV提供が始まり、社内データとの照合に活用しやすくなりました。"),
        ("在庫を止め、対象範囲を追う", "対象在庫を通常在庫から隔離し、出荷停止がシステムと現場の両方で有効か確認します。入荷・保管・出荷記録から、支店、車両、得意先まで追跡し、調査中の範囲も明示します。"),
        ("得意先連絡を記録する", "連絡先、連絡時刻、相手、回答、回収数量、未回収理由を一つの台帳で管理します。電話、メール、FAXが混在しても、進捗を一覧で見られるようにします。"),
        ("訓練で手順の穴を見つける", "架空の対象ロットを決め、30分で出荷先を抽出できるか、休日の連絡網が機能するかを試します。訓練後は、検索できなかった記録や重複連絡を手順へ反映します。")], checks=["GTIN・ロット・期限で在庫と出荷を検索できる","対象品を物理・システム両面で隔離できる","休日を含む連絡網が最新","得意先別の連絡と回収進捗を記録できる","模擬回収を定期的に実施している"], sources=[("厚生労働省「医薬品等回収関連情報」","https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/kenkou_iryou/iyakuhin/kaisyu/index.html"),("厚生労働省「回収情報の提供方法について」","https://www.mhlw.go.jp/web/t_doc?dataId=00tc9698&dataType=1&pageNo=1")]),
    dict(slug="pharmaceutical-bcp", tag="BCP", title="医薬品卸のBCP入門｜災害時も受発注・配送を続けるための作り方", desc="地震・停電・通信障害時にも医薬品供給を継続するためのBCPを、重要業務、復旧目標、代替手段、訓練の順で解説します。", lead="BCPは厚い冊子を作る活動ではなく、緊急時に何を優先し、誰が、どの代替手段で再開するかを決める経営判断です。", sections=[
        ("止められない業務を絞る", "すべてを同時に復旧しようとせず、生命・供給・資金への影響から受注、緊急配送、冷所保管、請求などの優先順位を決めます。目標復旧時間と、最低限必要な人員・設備・情報を明確にします。"),
        ("人とシステムの代替を用意する", "キーパーソン不在、停電、通信断、倉庫閉鎖を別々に想定します。紙の受注票、代替拠点、非常電源、連絡網、手作業での在庫確認など、現実に使える代替手段を準備します。"),
        ("取引先と優先順位を共有する", "仕入先、配送委託先、医療機関・薬局と、緊急時の連絡方法と情報項目を確認します。自社だけの計画では、入荷や配送がつながらないため、サプライチェーン全体で連絡訓練を行います。"),
        ("BCPを運用サイクルにする", "中小企業庁の指針も、計画を維持する教育・訓練・更新を重視しています。年1回の読み合わせに加え、停電や担当者不在など短いシナリオ訓練を繰り返します。")], checks=["優先業務と目標復旧時間を決めている","キーパーソン不在時の代行者がいる","停電・通信断時の受注手段がある","冷所設備停止時の移送先を確認している","訓練結果から計画を更新している"], sources=[("中小企業庁「中小企業BCP策定運用指針」","https://www.chusho.meti.go.jp/bcp/"),("中小企業庁「事業継続力強化計画」","https://www.chusho.meti.go.jp/keiei/antei/bousai/keizokuryoku.html?post_id=7475")]),
    dict(slug="distribution-price", tag="価格交渉", title="単品単価交渉を属人化させない｜医薬品卸の価格管理と記録", desc="医薬品の価値と流通コストを踏まえた単品単価交渉を、担当者依存にしない価格管理の方法を解説します。", lead="価格交渉は経験が必要ですが、根拠まで個人の頭に置く必要はありません。条件・承認・適用期間・交渉履歴を構造化すると、引き継ぎと検証が可能になります。", sections=[
        ("流通改善ガイドラインの基本", "厚生労働省は、銘柄別薬価制度の趣旨を尊重した単品単価交渉、早期妥結、医薬品の価値や配送コスト等を踏まえた経済合理的な交渉を示しています。総価だけでなく、品目ごとの条件を説明できる管理が必要です。"),
        ("価格マスターに根拠を持たせる", "得意先、商品、適用開始日・終了日、価格、値引き理由、承認者、根拠資料を一組で管理します。上書きだけでは過去請求を説明できないため、履歴を残します。"),
        ("例外承認の線引きをする", "担当者が決められる範囲と、管理者承認が必要な範囲を金額・率・期間で定義します。口頭承認は後から追えないため、申請と承認の記録先を統一します。"),
        ("請求結果まで照合する", "交渉記録とマスター更新だけで終わらず、初回請求で価格・数量・税・端数・締め条件を照合します。差異が出た場合は、修正内容と再発防止を価格ルールへ戻します。")], checks=["単品ごとの価格根拠を追える","価格の適用期間と履歴が残る","例外値引きの承認基準がある","マスター変更を別担当者が確認する","初回請求で契約条件を照合する"], sources=[("厚生労働省「医療用医薬品の流通改善について」","https://www.mhlw.go.jp/web/t_doc?dataId=00tb6076&dataType=1&pageNo=1"),("厚生労働省「医療用医薬品の流通の改善に関する懇談会」","https://www.mhlw.go.jp/stf/shingi2/0000198898_00022.html")]),
    dict(slug="drug-price-revision", tag="薬価改定", title="薬価改定時の価格更新でミスを防ぐ｜卸売業の実務チェックリスト", desc="薬価改定時の価格データ受領からマスター更新、得意先条件反映、請求検証までの標準手順を解説します。", lead="薬価改定は短期間に大量の価格を扱い、得意先別条件も重なるため、手作業と個人チェックだけではミスを見つけにくい業務です。", sections=[
        ("作業を4段階に分ける", "データ受領、変換・更新、得意先条件の反映、請求結果の検証に分けます。各段階の入力、出力、担当、締切、完了条件を一覧にし、作業の抜けを防ぎます。"),
        ("更新前後の差分を残す", "新旧薬価、仕切価、得意先価格、適用日を比較できる差分表を作ります。増減幅が大きい品目、低薬価品、取引量の多い品目など、確認優先度を決めます。"),
        ("例外条件を先に棚卸しする", "未妥結、総価、特別値引き、経過措置、返品条件などを通常ルールから切り分けます。誰が判断し、いつまで暫定条件を使うかを記録します。"),
        ("本番前後にテストする", "本番環境を直接試すのではなく、代表的な得意先と商品で受注から請求まで計算します。改定後の初回請求でもサンプル照合し、差異の原因を記録します。")], checks=["入手データの版と受領日時を記録している","新旧価格の差分を確認できる","例外条件と判断者を一覧化している","代表ケースで事前計算している","改定後の初回請求を照合している"], sources=[("厚生労働省「医療用医薬品の流通改善について」","https://www.mhlw.go.jp/web/t_doc?dataId=00tb6076&dataType=1&pageNo=1")]),
    dict(slug="cold-chain", tag="温度管理", title="医薬品コールドチェーンの基本｜温度逸脱を見逃さない保管・配送手順", desc="冷所品を含む医薬品の受入、保管、出荷、配送、温度逸脱時の判断と記録をGDPの観点から整理します。", lead="温度記録があるだけでは、品質を守ったとは言えません。測定機器、許容範囲、アラート、逸脱時の隔離と判断までが一つの運用です。", sections=[
        ("製品条件を業務へ落とす", "外装や製品情報の保管条件を、倉庫ロケーション、梱包資材、配送方法、許容時間へ反映します。常温・冷所・冷凍などの区分をシステムと現場表示で一致させます。"),
        ("測る場所と機器を管理する", "倉庫内の温度分布を踏まえて測定点を決め、ロガーや温度計の校正・点検期限を管理します。記録の欠損やアラート未確認も逸脱候補として扱います。"),
        ("配送条件を再現できるようにする", "季節、配送時間、車両、保冷容器、蓄冷材の配置を標準化します。委託先にも同じ条件と記録を求め、引き渡し時刻を含む流れを追跡できるようにします。"),
        ("逸脱品は勝手に戻さない", "逸脱を検知したら対象を隔離し、時間、温度、製品、ロット、原因を記録します。品質への影響判断と再出荷承認の責任者を定め、個人判断で通常在庫へ戻さない運用にします。")], checks=["製品別の保管・配送条件を参照できる","測定機器の校正期限を管理している","配送条件を季節別に検証している","アラート確認者と代行者がいる","逸脱品の隔離と承認手順がある"], sources=[("厚生労働省「医薬品の適正流通（GDP）ガイドライン」","https://www.mhlw.go.jp/content/11120000/000466215.pdf")]),
    dict(slug="cybersecurity", tag="情報セキュリティ", title="受発注システムが止まったら？医薬品卸のサイバー対策と復旧手順", desc="ランサムウェアやシステム障害に備え、医薬品卸が平時に整える資産管理、バックアップ、代替受注、連絡、復旧確認を解説します。", lead="セキュリティ対策の目的は、攻撃をゼロにすることだけではありません。受発注や配送が止まった際に、影響を把握し、安全な代替手段で供給を続け、正しく復旧することです。", sections=[
        ("守る対象と責任者を明確にする", "受注端末、在庫、価格マスター、配送、メール、リモート接続、委託先を一覧にし、所有者と停止時の影響を整理します。使われていないアカウントや端末も定期的に見直します。"),
        ("バックアップは復元して確かめる", "バックアップの取得だけでなく、業務に必要な順で復元できるかを検証します。本番と同じ認証情報に依存せず、攻撃の影響を受けにくい保管方法を組み合わせます。"),
        ("手作業の代替受注を準備する", "電話・FAX・所定様式で最低限受け付ける項目、重複注文を防ぐ番号、復旧後の入力順を決めます。緊急品と通常品を分け、医療機関・薬局への案内文も用意します。"),
        ("復旧時の安全確認を急がない", "原因と影響範囲を確認しないまま接続を戻すと再侵入やデータ不整合につながります。復旧判断者、外部連絡先、請求・在庫差異の照合手順を事前に定めます。")], checks=["重要システムと委託先を一覧化している","不要アカウントを定期点検している","バックアップから復元テストをしている","システム停止時の受注様式がある","復旧後の在庫・請求照合手順がある"], sources=[("厚生労働省「医療情報システムの安全管理に関するガイドライン第6.0版改定」","https://www.mhlw.go.jp/content/12301000/001084098.pdf"),("厚生労働省 医療等情報利活用WG議事録","https://www.mhlw.go.jp/stf/newpage_59423.html")]),
    dict(slug="logistics-2024", tag="物流改善", title="物流2024年問題の先へ｜医薬品配送の待ち時間・急配・ルートを見直す", desc="ドライバー時間外労働の制約を踏まえ、医薬品卸が荷待ち、急配、検品、配送ルートを可視化して改善する方法を解説します。", lead="配送の制約が強まる中、従来どおりの頻回配送や曖昧な急配を続けるだけでは現場が持続しません。供給品質を守りながら、待ち時間と例外を減らす必要があります。", sections=[
        ("配送時間を分解して測る", "走行時間だけでなく、積込待ち、検品、荷下ろし、受領待ち、返品回収、再配達を記録します。支店・ルート・時間帯別に見ると、改善すべき停滞が見えます。"),
        ("急配の定義をそろえる", "希望があればすべて急配とするのではなく、医療上の緊急性、在庫状況、代替可能性、締切、承認者を決めます。受付時に必要情報を集め、判断理由を残します。"),
        ("荷主側の作業を短くする", "出荷確定時刻、バース予約、伝票準備、検品方法、返品の受付を見直します。配送会社だけでなく、倉庫と受発注の締め時刻を連動させます。"),
        ("得意先とサービス水準を共有する", "定期便の曜日・時間、当日便の受付締切、欠品時の連絡、緊急時の窓口を明文化します。例外件数を定期的に振り返り、必要なサービスと慣習を分けます。")], checks=["荷待ちを含む配送時間を記録している","急配の受付項目と承認基準がある","倉庫と受注の締め時刻が連動している","再配達・持戻り理由を集計している","得意先と配送条件を共有している"], sources=[("中小企業庁「中小企業BCP策定運用指針」","https://www.chusho.meti.go.jp/bcp/")]),
    dict(slug="inventory-accuracy", tag="在庫管理", title="医薬品卸の在庫精度を上げる｜ロット・使用期限・棚卸しの標準化", desc="欠品・過剰在庫・期限切れを減らすため、ロット・使用期限を含む入出庫と棚卸しの標準化を解説します。", lead="在庫差異は棚卸し日に突然生まれるのではなく、受入、格納、ピッキング、返品、破損、回収の小さな記録漏れが積み重なって現れます。", sections=[
        ("在庫が動く場面を洗い出す", "入荷、格納、補充、引当、ピッキング、出荷、返品、移動、廃棄、回収隔離を一覧化します。各場面で商品、数量、ロット、期限、場所をいつ記録するか決めます。"),
        ("先入れ先出しを条件化する", "単純な入荷順ではなく、使用期限と得意先条件を考慮した先期限先出しを基本にします。期限が近い在庫の警告時期、販売可否、返品・移動判断を明確にします。"),
        ("循環棚卸しで早く差異を見つける", "年1回だけでなく、高額品、動きの多い品、差異の多い棚を短い周期で確認します。差異を数量調整で終わらせず、発生工程と原因を記録します。"),
        ("在庫指標を現場改善へつなげる", "差異率、期限切れ、欠品、緊急補充、返品、ロケーション誤りを支店・工程別に見ます。個人を責めるためでなく、手順・表示・端末配置の改善に使います。")], checks=["全ての在庫移動に記録のタイミングがある","ロット・期限・場所で追跡できる","期限接近品の判断基準がある","高リスク品を循環棚卸ししている","差異原因を工程別に分析している"], sources=[("厚生労働省「医薬品の適正流通（GDP）ガイドライン」","https://www.mhlw.go.jp/content/11120000/000466215.pdf")]),
]

HEADER = '''<header class="site-header"><div class="container"><a class="brand" href="../../" aria-label="事業承継レスキュー トップ"><span class="brand__name">事業承継レスキュー</span><span class="brand__by">by YOURNIST</span></a><button class="nav-toggle" aria-label="メニュー" aria-expanded="false"><span></span><span></span><span></span></button><nav class="site-nav" id="siteNav"><a class="nav-link" href="../../#service">サービス</a><a class="nav-link" href="../../#flow">進め方</a><a class="nav-link" href="../../#price">料金</a><a class="nav-link" href="../">お役立ち記事</a><a class="btn btn--primary" href="../../contact/">無料診断</a></nav></div></header>'''
FOOTER = '''<footer class="site-footer"><div class="container"><div><span class="brand__name" style="font-size:1.125rem;font-weight:700;">事業承継レスキュー</span><p style="margin-top:var(--space-2)">卸業界の属人化を解消し、標準化・事業承継につなげるサービスです。</p><p style="margin-top:var(--space-3)">運営：<strong>YOURNIST株式会社</strong><br>お問い合わせ：<a href="mailto:yournist@gmail.com">yournist@gmail.com</a></p></div><nav><div class="foot-links"><a href="../../#service">サービス</a><a href="../">お役立ち記事</a><a href="../../contact/">お問い合わせ</a></div></nav></div><div class="container"><p class="foot-bottom">© <span id="yr"></span> YOURNIST株式会社. All rights reserved.</p></div></footer><script>var t=document.querySelector('.nav-toggle'),n=document.getElementById('siteNav');if(t)t.addEventListener('click',function(){var o=n.classList.toggle('open');t.setAttribute('aria-expanded',o)});n&&n.addEventListener('click',function(e){if(e.target.tagName==='A')n.classList.remove('open')});document.getElementById('yr').textContent=new Date().getFullYear();</script>'''

def render(a):
    sections = ''.join(f'<h2>{escape(h)}</h2><p>{escape(p)}</p>' for h,p in a['sections'])
    checks = ''.join(f'<li>{escape(x)}</li>' for x in a['checks'])
    sources = ''.join(f'<li><a href="{escape(url)}" target="_blank" rel="noopener noreferrer">{escape(name)}</a></li>' for name,url in a['sources'])
    title, desc, slug, tag = map(a.get, ('title','desc','slug','tag'))
    return f'''<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{escape(title)}｜事業承継レスキュー</title><meta name="description" content="{escape(desc)}"><link rel="canonical" href="https://example.com/column/{slug}/"><meta property="og:type" content="article"><meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(desc)}"><meta property="og:url" content="https://example.com/column/{slug}/"><meta property="og:site_name" content="事業承継レスキュー by YOURNIST"><meta property="og:locale" content="ja_JP"><meta property="og:image" content="https://example.com/assets/img/ogp.svg"><meta name="twitter:card" content="summary_large_image"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet"><link rel="stylesheet" href="../../assets/css/tokens.css"><link rel="stylesheet" href="../../assets/css/style.css"><script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"{escape(title)}","description":"{escape(desc)}","datePublished":"2026-07-20","dateModified":"2026-07-20","inLanguage":"ja","author":{{"@type":"Organization","name":"YOURNIST株式会社"}},"publisher":{{"@type":"Organization","name":"YOURNIST株式会社"}},"mainEntityOfPage":"https://example.com/column/{slug}/"}}</script></head><body>{HEADER}<main><nav class="breadcrumb" aria-label="パンくず"><ol class="container"><li><a href="../../">トップ</a></li><li><a href="../">お役立ち記事</a></li><li aria-current="page">{escape(tag)}</li></ol></nav><article><header class="article-header"><div class="container"><span class="eyebrow">{escape(tag)}</span><h1>{escape(title)}</h1><p class="article-meta"><time datetime="2026-07-20">2026年7月20日</time> ・ 想定読了 5分</p></div></header><div class="section"><div class="container article-layout prose"><p>{escape(a['lead'])}</p>{sections}<h2>現場チェックリスト</h2><ul class="checklist">{checks}</ul><h2>まとめ</h2><p>重要なのは、ルールを作って終わりにせず、別の担当者が同じ情報から同じ行動を取れるか確認することです。影響の大きい業務から小さく試し、記録と振り返りを通じて更新してください。</p><aside class="source-note"><h2>参照した公的資料</h2><p>制度やガイドラインは改定される場合があります。実務適用時は必ず最新の原文をご確認ください。</p><ul>{sources}</ul></aside><aside class="article-related"><h2>関連記事</h2><ul><li><a href="../attribution/">業務の属人化とは？原因・リスクと解消ステップ</a></li><li><a href="../standardization/">業務標準化の進め方</a></li></ul><div class="article-cta"><h3>止まる業務を把握したい方へ</h3><p>無料の簡易チェックで、引き継ぎの優先順位を整理できます。</p><a class="btn btn--primary" href="../../contact/">無料の引き継ぎリスク診断</a></div></aside></div></div></article></main>{FOOTER}</body></html>'''

for article in articles:
    target = OUT / article['slug']
    target.mkdir(parents=True, exist_ok=True)
    (target / 'index.html').write_text(render(article), encoding='utf-8')

