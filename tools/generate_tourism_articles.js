const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..', 'site', 'column', 'tourism');
const published = '2026-07-25';
const sources = {
  agency: [
    ['観光庁「旅行業法」', 'https://www.mlit.go.jp/kankocho/seisaku_seido/ryokogyoho/ryokogyohogaiyo.html'],
    ['観光庁「観光DX」', 'https://www.mlit.go.jp/kankocho/seisaku_seido/kihonkeikaku/jizoku_kankochi/kanko-dx.html']
  ],
  hotel: [
    ['観光庁「観光DX」', 'https://www.mlit.go.jp/kankocho/seisaku_seido/kihonkeikaku/jizoku_kankochi/kanko-dx.html'],
    ['観光庁「宿泊業の生産性向上」', 'https://www.mlit.go.jp/kankocho/seisaku_seido/kihonkeikaku/jizoku_kankochi/kankosangyokakushin/saiseishien/seisanseikojo.html']
  ]
};

const articles = [
  {
    slug:'travel-agency-standardization', type:'agency', category:'旅行会社', title:'旅行会社の業務を標準化する方法', sub:'見積・手配の属人化を解消',
    description:'海外エージェント別条件、仕入、見積、手配、回答期限をチームで確認できる形へ整える手順を解説します。',
    lead:'「この顧客の見積は担当者にしか作れない」「手配先との約束がメールの中にしかない」という状態は、繁忙期の対応力と利益管理を不安定にします。',
    sections:[
      ['標準化する範囲を一案件で確かめる','問い合わせから入金までを一度に変えず、代表的な一案件を選びます。依頼受付、条件確認、原価計算、見積承認、予約、精算の順に、担当者と使用データを確認します。'],
      ['顧客別・仕入先別の条件を台帳へ集める','契約単価、手数料、取消条件、支払条件、回答期限を、参照元と更新日を含めて整理します。口頭合意や過去メールは未確認事項として分けます。'],
      ['通常処理と変更処理を分ける','新規手配だけでなく、人数変更、日程変更、取消、代替手配の判断と連絡順序を確認します。例外を通常フローへ無理に押し込まないことが重要です。'],
      ['別担当者が同じ見積を作れるか試す','資料を読んだ別担当者が過去案件を再現し、原価と回答内容を比較します。迷った点をルールへ戻し、実務で使える状態にします。']
    ]
  },
  {
    slug:'inbound-itinerary-change', type:'agency', category:'旅行会社', title:'インバウンド旅行の旅程変更対応', sub:'手配漏れを防ぐ業務フロー',
    description:'交通、宿泊、体験、飲食の変更順序と連絡・精算を整理し、緊急変更でも漏れを防ぐ方法を紹介します。',
    lead:'訪日旅行の旅程変更は、一つの変更が交通、宿泊、体験、食事、ガイド、精算へ連鎖します。判断順序が人に依存すると、手配漏れと二重予約が起こります。',
    sections:[
      ['影響を確認する順序を決める','変更を受けたら、旅行者の安全、当日運行、取消期限、代替可能性、費用影響の順に確認します。案件ごとに順序を変えないことが初動を速めます。'],
      ['変更対象と連絡先を一枚で把握する','旅程表だけでなく、各予約番号、担当窓口、営業時間、取消条件、緊急連絡先を関連付けます。誰に何を連絡したかも同じ場所へ記録します。'],
      ['顧客承認と費用負担を記録する','追加費用、返金、為替差、手数料について、説明内容と承認者を残します。口頭承認は日時と担当者を記録し、精算時に追える状態にします。'],
      ['緊急時の一次判断範囲を決める','夜間や移動中に責任者へ連絡できない場合、担当者が決められる金額や代替範囲を定めます。判断を止める条件も同時に明確にします。']
    ]
  },
  {
    slug:'travel-agency-costing', type:'agency', category:'旅行会社', title:'旅行会社の見積原価と粗利管理', sub:'担当者依存を減らす確認項目',
    description:'為替、仕入、手数料、取消条件を見積へ反映し、案件別の利益を同じ基準で確認する方法を解説します。',
    lead:'旅行商品の見積は、仕入価格を足すだけではありません。為替、税、送客手数料、添乗・ガイド費、変更リスクまで含めて初めて、案件の採算が見えます。',
    sections:[
      ['原価に含める項目を統一する','宿泊、交通、食事、体験、ガイド、通信、送金、決済、緊急対応など、案件で確認する原価項目を固定します。'],
      ['為替と価格の有効期限を明示する','適用レート、換算日、見積有効期限、仕入価格の確定時期を残します。誰が見ても同じ条件で再計算できることが重要です。'],
      ['変更・取消リスクを見積時に確認する','無料取消期限、デポジット、人数変動、繁忙期条件を確認し、利益を圧迫する条件を承認者へ示します。'],
      ['見積と実績の差を次回へ戻す','催行後に原価差、追加手配、返金、値引きを振り返り、差が生じた理由を見積基準へ反映します。']
    ]
  },
  {
    slug:'hotel-reservation-standardization', type:'hotel', category:'ホテル', title:'ホテル予約業務の標準化', sub:'OTA・在庫・料金管理を引き継ぐ',
    description:'PMS、OTA、サイトコントローラー、自社予約の確認点と変更履歴を整理する方法を解説します。',
    lead:'予約業務は画面操作を覚えるだけでは引き継げません。在庫を開閉する理由、料金変更の判断、例外予約の扱いを共有して初めて、担当交代に耐えられます。',
    sections:[
      ['予約経路とシステムのつながりを描く','OTA、自社サイト、電話、団体予約が、サイトコントローラーとPMSへどう連携するかを確認します。手入力と自動連携を分けます。'],
      ['在庫差異を確認する時刻と担当を決める','販売在庫、清掃済み客室、故障客室、団体枠の差異を、いつ誰が確認するかを定めます。'],
      ['例外予約の扱いを標準化する','アーリーチェックイン、連泊分割、アップグレード、部屋移動、ノーショーなど、通常外の処理と承認範囲を整理します。'],
      ['変更履歴を次の担当者が追える形にする','在庫や料金を変更した理由、対象期間、販売経路、承認者を残します。結果の振り返りまで一つの運用にします。']
    ]
  },
  {
    slug:'hotel-revenue-management', type:'hotel', category:'ホテル', title:'中小ホテルのレベニューマネジメント', sub:'料金判断を属人化させない',
    description:'需要、在庫、競合、販売経路を確認する順序をそろえ、料金変更の根拠を残す方法を紹介します。',
    lead:'料金設定を自動化しても、例外時の判断は残ります。中小ホテルでは、限られた人員で確認する指標を絞り、変更理由を残すことが引き継ぎの第一歩です。',
    sections:[
      ['確認する指標を絞る','予約進捗、残室、曜日、イベント、競合、キャンセル率など、自社の判断に使う指標を決めます。数字を増やしすぎないことが継続の条件です。'],
      ['判断する頻度と対象期間を決める','毎日見る期間、週次で見る期間、繁忙期だけ見る条件を分けます。担当者不在時の代行者も決めます。'],
      ['料金変更の理由を記録する','上げた・下げただけでなく、確認した指標、仮説、対象チャネル、期間を残します。後から結果を比較できる粒度が必要です。'],
      ['例外と承認範囲を明確にする','団体、連泊、法人契約、返金不可、直前割引など、通常料金から外れる場合の承認者と下限を定めます。']
    ]
  },
  {
    slug:'hotel-housekeeping-handover', type:'hotel', category:'ホテル', title:'ホテルの清掃・客室引き渡しを標準化', sub:'確認漏れを防ぐ方法',
    description:'清掃状況、忘れ物、設備不具合、優先客室をフロントと清掃担当が共有する運用を解説します。',
    lead:'客室が「清掃済み」でも、販売できる状態とは限りません。設備不具合、忘れ物、特別対応をフロントと清掃担当が同じ基準で共有する必要があります。',
    sections:[
      ['客室状態の定義をそろえる','未清掃、清掃中、点検待ち、販売可、故障、保留など、現場で使う状態と変更権限を決めます。'],
      ['優先順位の判断条件を決める','到着予定、部屋タイプ、連泊、特別対応を基に、どの客室から仕上げるかを共有します。'],
      ['不具合と忘れ物の連絡を標準化する','写真、部屋番号、発見時刻、対応状況、引き継ぎ先を記録し、口頭だけで終わらせません。'],
      ['引き渡し前の確認点を絞る','清掃品質、備品、設備、安全、特別リクエストを確認し、点検漏れの傾向を定期的に見直します。']
    ]
  },
  {
    slug:'multilingual-customer-service', type:'hotel', category:'インバウンド対応', title:'ホテル・旅行会社の多言語対応マニュアル', sub:'翻訳前に決めること',
    description:'案内文の翻訳だけでなく、判断範囲、例外、緊急時の連絡先を言語共通で整理する方法を解説します。',
    lead:'多言語対応で最初に必要なのは、文章を増やすことではありません。日本語の案内内容と判断範囲が曖昧なまま翻訳すると、言語ごとに異なる約束が生まれます。',
    sections:[
      ['問い合わせを目的別に分類する','予約前、到着前、滞在中、変更・取消、緊急時に分け、よくある質問と必要情報を整理します。'],
      ['回答できる範囲を明確にする','返金、アップグレード、医療、災害、紛失など、現場担当者が回答できる範囲と確認先を決めます。'],
      ['原文を短く具体的にする','一文一意、日時と金額の明記、主語の省略防止を徹底します。翻訳しやすい原文は日本語対応の品質も高めます。'],
      ['更新元を一つにする','言語別ファイルを個別更新せず、原文、翻訳、承認日、更新責任者を一つの台帳で管理します。']
    ]
  },
  {
    slug:'inbound-night-emergency', type:'hotel', category:'インバウンド対応', title:'ホテルの夜間・緊急対応を標準化', sub:'判断基準と連絡体制の作り方',
    description:'設備、体調不良、鍵、騒音、災害時の一次対応とエスカレーションを整理します。',
    lead:'夜間対応では人員と情報が限られます。すべてを責任者へ確認する運用では回答が遅れるため、一次対応と止める条件を先に決めます。',
    sections:[
      ['事象を分類して優先順位を決める','生命・安全、施設継続、顧客影響、金銭影響の順に確認し、緊急度を分類します。'],
      ['一次対応の範囲を決める','代替客室、簡易復旧、返金・値引き、外部連絡について、夜間担当者が決められる範囲を明示します。'],
      ['連絡先と伝える情報をそろえる','事象、客室、発生時刻、応急対応、顧客の要望を記録し、責任者や外部業者へ同じ情報を渡します。'],
      ['翌朝の引き継ぎまでを手順に含める','未解決事項、顧客への約束、費用、設備状態を日勤へ渡し、対応完了まで追跡します。']
    ]
  },
  {
    slug:'hotel-pms-data-handover', type:'hotel', category:'システム・データ', title:'ホテルのPMS引き継ぎチェックリスト', sub:'予約・顧客データを守る',
    description:'アカウント、権限、マスタ、連携、帳票、バックアップを棚卸しし、担当交代に備える方法を解説します。',
    lead:'PMSの操作手順だけでは、設定変更や障害時に対応できません。アカウント、連携、マスタ、出力、問い合わせ先までをデジタル資産として引き継ぎます。',
    sections:[
      ['管理者と権限を棚卸しする','個人アカウント、共有アカウント、退職者、外部委託先を確認し、管理者権限と日常権限を分けます。'],
      ['マスタと連携を一覧にする','客室タイプ、料金、商品、税、決済、OTA、サイトコントローラー、会計連携の責任者と更新手順を記録します。'],
      ['重要帳票とデータ出力を確認する','日次売上、予約、宿泊者名簿、精算、監査に必要な出力と保存期間を整理します。'],
      ['障害時の復旧手順を試す','ベンダー連絡、手書き受付、後入力、バックアップ確認を、担当者交代前にケースで試します。']
    ]
  },
  {
    slug:'tourism-business-succession', type:'agency', category:'属人化・事業承継', title:'中小観光事業者の事業承継', sub:'予約・取引先・現場判断を残す',
    description:'経営権だけでなく、販売先、仕入先、予約、料金、接客判断を次の担い手へ渡す確認項目を整理します。',
    lead:'観光事業の承継では、契約やシステムだけでなく、海外エージェントとの関係、仕入条件、料金判断、顧客対応の勘所を残す必要があります。',
    sections:[
      ['事業を止める業務を特定する','予約、手配、在庫、料金、精算、緊急対応について、代行者がいない業務と停止影響を確認します。'],
      ['取引条件と窓口を整理する','顧客・仕入先別の契約、連絡方法、締切、支払、取消、暗黙の注意点を根拠と一緒に残します。'],
      ['システムとデータの所在を確認する','予約、顧客、料金、会計、メール、表計算、クラウドサービスの管理者、権限、保存先を一覧にします。'],
      ['次の担当者による再現で確かめる','過去案件や代表的な一日の業務を別担当者が実行し、迷った判断と不足情報を引き継ぎ資料へ戻します。']
    ]
  }
];

function esc(s){return s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;')}
function render(a){
  const sourceLinks = sources[a.type].map(([t,u])=>`<li><a href="${u}" target="_blank" rel="noopener noreferrer">${t}</a></li>`).join('');
  const relatedLinks = articles.filter(x=>x.slug!==a.slug && (x.type===a.type || x.category===a.category)).slice(0,2).map(x=>`<li><a href="../${x.slug}/">${esc(x.title)}｜${esc(x.sub)}</a></li>`).join('');
  const sectionsHtml = a.sections.map(([h,p],i)=>`<h2 id="section-${i+1}">${esc(h)}</h2><p>${esc(p)}</p>`).join('');
  const toc = a.sections.map(([h],i)=>`<a href="#section-${i+1}">${esc(h)}</a>`).join('');
  return `<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(a.title)}｜${esc(a.sub)}｜YOURNIST</title><meta name="description" content="${esc(a.description)}"><link rel="canonical" href="https://yournist-keisyo-sample.vercel.app/column/tourism/${a.slug}/"><meta property="og:type" content="article"><meta property="og:title" content="${esc(a.title)}｜${esc(a.sub)}"><meta property="og:description" content="${esc(a.description)}"><meta property="og:site_name" content="YOURNIST"><meta property="og:image" content="https://yournist-keisyo-sample.vercel.app/assets/img/tourism-hero.webp"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700&family=Noto+Sans+JP:wght@400;500;600;700;900&display=swap" rel="stylesheet"><link rel="stylesheet" href="../../../assets/css/article-standard.css"><link rel="stylesheet" href="../../../assets/css/motion.css"><script type="application/ld+json">${JSON.stringify({"@context":"https://schema.org","@type":"Article","headline":`${a.title}｜${a.sub}`,"description":a.description,"datePublished":published,"dateModified":published,"inLanguage":"ja","author":{"@type":"Organization","name":"YOURNIST株式会社"},"publisher":{"@type":"Organization","name":"YOURNIST株式会社"},"mainEntityOfPage":`https://yournist-keisyo-sample.vercel.app/column/tourism/${a.slug}/`})}</script></head><body><header class="as-header"><a class="as-logo" href="../../../index.html"><img src="../../../assets/img/yournist-logo-transparent.png" alt="YOURNIST"></a><nav class="as-nav"><a href="../index.html">中小観光業の記事</a><a href="../../../business/tourism/index.html">支援内容</a><a class="as-nav__cta" href="../../../request/index.html?type=consultation">無料相談 ↗</a></nav></header><main><section class="as-hero"><div class="as-shell"><span class="as-category">${esc(a.category)}</span><h1>${esc(a.title)}<span class="as-h1-sub">${esc(a.sub)}</span></h1><p class="as-summary">${esc(a.description)}</p><div class="as-meta"><time datetime="${published}">2026.07.25</time><span>対象：インバウンド旅行を扱う中小旅行会社・ホテル</span></div></div></section><nav class="as-breadcrumb-bar" aria-label="パンくず"><div class="as-shell"><ol class="as-breadcrumb"><li><a href="../../../index.html">トップ</a></li><li><a href="../index.html">中小観光業の記事</a></li><li>${esc(a.category)}</li></ol></div></nav><div class="as-shell as-layout"><article class="as-article"><p class="as-lead">${esc(a.lead)}</p>${sectionsHtml}<h2 id="section-5">実行前のチェックリスト</h2><ul class="checklist"><li>対象業務と責任者が決まっている</li><li>通常時だけでなく変更・取消・緊急時も確認した</li><li>判断根拠と参照データが残っている</li><li>別の担当者が実際のケースで試している</li><li>変更時の更新責任者が決まっている</li></ul><h2 id="section-6">まとめ</h2><p>重要なのは、資料の量ではなく、担当者が替わっても同じ情報から同じ判断へたどり着けることです。影響の大きい一業務から始め、実案件で検証しながら更新してください。</p><aside class="source-note"><h2 id="section-7">企画時に参照した公的情報</h2><p>制度や公的情報は更新されます。実務へ適用する際は最新の原文をご確認ください。</p><ul>${sourceLinks}</ul></aside><aside class="article-related"><h2>関連記事</h2><ul>${relatedLinks}</ul></aside><aside class="article-related"><h2>観光業の業務引き継ぎを具体化したい方へ</h2><p>旅行会社・ホテルの止まる可能性がある業務と、優先して残す判断を無料相談で整理します。</p><div class="article-cta"><h3>まずは対象業務をお聞かせください</h3><p>資料請求のみでも受け付けています。</p><a href="../../../request/index.html?type=consultation">無料相談を申し込む ↗</a></div></aside></article><aside class="as-side"><nav class="as-toc"><p>目次</p>${toc}<a href="#section-5">実行前のチェックリスト</a><a href="#section-6">まとめ</a><a href="#section-7">企画時に参照した公的情報</a></nav><div class="as-side-card"><small>中小観光事業者向け</small><h2>繁忙期や担当交代の前に、残す業務を整理しませんか。</h2><p>旅行会社・ホテルの業態に合わせて優先順位を整理します。</p><a href="../../../request/index.html?type=document">資料を請求する ↗</a></div></aside></div></main><footer class="as-footer"><div class="as-shell"><div class="as-footer__top"><div><span class="as-footer__logo"><img src="../../../assets/img/yournist-logo-transparent.png" alt="YOURNIST"></span><p>中小観光事業者の予約・手配・接客を、次の担い手が使える経営資産へ。</p></div><div class="as-footer__links"><a href="../index.html">記事一覧</a><a href="../../../business/tourism/index.html">支援内容</a><a href="../../../request/index.html">お問い合わせ</a></div></div><small>© <span id="yr"></span> YOURNIST株式会社</small></div></footer><script>document.getElementById('yr').textContent=new Date().getFullYear()</script><script src="../../../assets/js/motion.js" defer></script></body></html>`;
}

for(const article of articles){
  const dir = path.join(root, article.slug);
  fs.mkdirSync(dir, {recursive:true});
  fs.writeFileSync(path.join(dir, 'index.html'), render(article), 'utf8');
}
console.log(`Generated ${articles.length} tourism article pages.`);
