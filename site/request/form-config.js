/* Googleフォーム連携の設定
 * tools/setup_google_form.py が自動生成しました。手で編集しても構いません。
 * 再取得する場合:
 *   python tools/setup_google_form.py "<公開フォームのURL>"
 *
 * action が空の場合は、メール下書き(mailto)へフォールバックします。
 * choices はフォーム側が受け付ける選択肢。ここに無い値をそのまま送ると
 * Googleが400で弾くため、other が true の項目は「その他」へ載せて送ります。
 */
window.GOOGLE_FORM_CONFIG = {
  action: "https://docs.google.com/forms/d/e/1FAIpQLSeYdAmCq3Pw20OHcDJB8TMRZNmdl1_po2yQN8wbcjXUpatq4g/formResponse",
  fields: {
    requestType: "entry.1578144237", // お問い合わせ種別（送信値は「資料を請求する」「無料相談を申し込む」）
    company: "entry.362742265", // 会社名
    name: "entry.2105466944",  // お名前
    email: "entry.1510488279", // メールアドレス
    industry: "entry.1286382792", // 業界
    topic: "entry.1853564839", // 関心のあるテーマ
    phone: "entry.2009223607", // 電話番号
    employees: "entry.1411238931", // 従業員規模
    role: "entry.1025082095",  // 役職・部門
    timing: "entry.2098373276", // 検討時期
    message: "entry.1680498183", // 現在の状況・知りたいこと（※長文。診断結果もここへ入る）
    diagnosisScore: "entry.1697907514", // 危険度スコア 0〜100
    diagnosisLevel: "entry.1775075836", // 危険度レベル 1〜4
  },
  choices: {
    requestType: ["資料を請求する", "無料相談を申し込む"],
    industry: ["卸売業", "製造業", "観光業"],
    employees: ["1〜19名", "20〜49名", "50〜99名", "100〜299名", "300名以上"],
    timing: ["すぐに相談したい", "3か月以内", "半年以内", "情報収集中"],
    topic: ["受発注・価格・請求の属人化", "在庫・発注・配送判断の属人化", "問い合わせ・社内ナレッジ", "製造技術・品質・保全の承継", "事業承継前の業務棚卸し", "どこから始めるべきか相談したい"],
  },
  other: {
    industry: true,
  }
};
