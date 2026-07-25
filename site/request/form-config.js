/* Googleフォーム連携の設定
 * ------------------------------------------------------------------
 * 必要な情報は2種類だけです。
 *
 * 1) action … 送信先URL
 *      Googleフォームの編集画面から「プレビュー(目のアイコン)」で公開フォームを開き、
 *      そのURLの末尾 /viewform を /formResponse に置き換えたもの。
 *      例: https://docs.google.com/forms/d/e/1FAIpQLSxxxxxxxx/formResponse
 *
 * 2) fields … 各質問の entry ID
 *      公開フォームを開いて右クリックから「ページのソースを表示」→ entry. で検索。
 *      "entry.123456789" の形式で入れてください。
 *
 * 空欄のままの項目は送信対象から除外されます（全部埋めなくても動きます）。
 * action が空の場合は、従来どおりメール下書き(mailto)にフォールバックします。
 *
 * 対応するフォーム側の質問形式:
 *   requestType / industry / employees / timing / topic → ラジオボタン または プルダウン
 *   company / name / email / phone / role              → 記述式（短文）
 *   message                                            → 段落（長文）※必ず長文にすること
 *   diagnosisScore / diagnosisLevel                    → 記述式（短文）
 *
 * 注意: message には診断結果が最大約1,000字転記されます。
 *       フォーム側を「記述式（短文）」にすると文字数制限で送信が失敗します。
 *
 * ラジオ/プルダウンの選択肢は、フォーム側の文字列を
 * site/request/index.html の <option> と完全一致させてください。
 * 一致しない値はGoogleフォーム側で破棄されます。
 */
window.GOOGLE_FORM_CONFIG = {
  action: "",
  fields: {
    // --- 必須項目 ---
    requestType: "",    // お問い合わせ種別（送信値は「資料を請求する」「無料相談を申し込む」）
    company: "",        // 会社名
    name: "",           // お名前
    email: "",          // メールアドレス
    industry: "",       // 業界
    topic: "",          // 関心のあるテーマ

    // --- 任意項目 ---
    phone: "",          // 電話番号
    employees: "",      // 従業員規模
    role: "",           // 役職・部門
    timing: "",         // 検討時期
    message: "",        // 現在の状況・知りたいこと（※長文。診断結果もここへ入る）

    // --- 診断ツール経由の場合のみ値が入る（分けておくと後から集計できる） ---
    diagnosisScore: "", // 危険度スコア 0〜100
    diagnosisLevel: "", // 危険度レベル 1〜4
  }
};
