/**
 * 問い合わせフォームの回答を yournist@gmail.com へ通知する（Google Apps Script）
 *
 * Googleフォーム標準の通知はリンク中心で、件名から内容を判断できない。
 * このスクリプトは、件名だけで「誰から・どの種別か・急ぎか」が分かる通知を送る。
 *
 * 導入手順:
 *   1. Googleフォームを開く → 右上の︙ →「Apps Script」
 *   2. このファイルの内容を貼り付けて保存
 *   3. 左の時計アイコン（トリガー）→「トリガーを追加」
 *        実行する関数        : onFormSubmit
 *        イベントのソース     : フォームから
 *        イベントの種類       : フォーム送信時
 *   4. 初回だけ承認を求められるので許可する
 *   5. サイトのフォームからテスト送信し、通知が届くことを確認
 *
 * 注意: 送信元は、このスクリプトを承認したGoogleアカウントになる。
 *       yournist@gmail.com 本人のアカウントで作成すること。
 */

var NOTIFY_TO = 'yournist@gmail.com';

/* 診断スコアがこの値以上なら件名へ「要優先」を付ける。
   危険度レベル3（高）の下限が50のため、それに合わせている。 */
var PRIORITY_SCORE = 50;

/* 件名・本文で使う質問。フォーム側のタイトルと対応する（先頭の番号は無視する）。 */
var Q = {
  type: 'お問い合わせ種別',
  company: '会社名',
  name: 'お名前',
  email: 'メールアドレス',
  phone: '電話番号',
  industry: '業界',
  employees: '従業員規模',
  role: '役職・部門',
  timing: '検討時期',
  topic: '関心のあるテーマ',
  message: '現在の状況・知りたいこと',
  score: '診断スコア',
  level: '診断レベル'
};

function onFormSubmit(e) {
  var answers = collectAnswers(e);
  var get = function (key) { return answers[normalize(Q[key])] || ''; };

  var company = get('company') || '(会社名なし)';
  /* 件名は一覧で読むので短くする */
  var type = ({ '資料を請求する': '資料請求', '無料相談を申し込む': '無料相談' })[get('type')]
    || get('type') || 'お問い合わせ';
  var score = get('score');
  var urgent = score && Number(score) >= PRIORITY_SCORE;

  var subject = '【' + type + '】' + company;
  if (score) subject += '（危険度 ' + score + '/100）';
  if (urgent) subject = '[要優先] ' + subject;

  MailApp.sendEmail({
    to: NOTIFY_TO,
    subject: subject,
    body: buildBody(get, answers),
    /* 通知メールにそのまま返信すれば、問い合わせ者へ返せるようにする */
    replyTo: get('email') || undefined,
    name: 'YOURNIST 問い合わせ通知'
  });
}

function buildBody(get, answers) {
  var lines = [];
  lines.push('サイトのフォームから問い合わせがありました。');
  lines.push('このメールに返信すると、問い合わせ者へ直接返信されます。');
  lines.push('');

  if (get('score')) {
    lines.push('■ 診断結果');
    lines.push('  危険度スコア : ' + get('score') + '/100（レベル' + get('level') + '）');
    if (Number(get('score')) >= PRIORITY_SCORE) {
      lines.push('  ※ 危険度が高い状態です。優先して連絡してください。');
    }
    lines.push('');
  }

  lines.push('■ 問い合わせ内容');
  [['種別', 'type'], ['会社名', 'company'], ['お名前', 'name'], ['メール', 'email'],
   ['電話', 'phone'], ['業界', 'industry'], ['従業員規模', 'employees'],
   ['役職・部門', 'role'], ['検討時期', 'timing'], ['テーマ', 'topic']].forEach(function (pair) {
    var v = get(pair[1]);
    if (v) lines.push('  ' + pad(pair[0]) + ' : ' + v);
  });
  lines.push('');

  if (get('message')) {
    lines.push('■ 現在の状況・知りたいこと');
    lines.push(get('message'));
    lines.push('');
  }

  /* 想定外の質問が増えていても取りこぼさない */
  var known = {};
  Object.keys(Q).forEach(function (k) { known[normalize(Q[k])] = true; });
  var extras = Object.keys(answers).filter(function (t) { return !known[t] && answers[t]; });
  if (extras.length) {
    lines.push('■ その他の回答');
    extras.forEach(function (t) { lines.push('  ' + t + ' : ' + answers[t]); });
    lines.push('');
  }

  lines.push('---');
  try {
    lines.push('回答一覧: ' + FormApp.getActiveForm().getEditUrl() + '#responses');
  } catch (err) { /* 権限が無い場合もメール本文は送る */ }
  return lines.join('\n');
}

/* フォーム回答を「質問タイトル（正規化済み） → 回答」の形にする */
function collectAnswers(e) {
  var out = {};
  if (!e || !e.response) return out;
  e.response.getItemResponses().forEach(function (item) {
    var value = item.getResponse();
    if (Array.isArray(value)) value = value.join(', ');
    out[normalize(item.getItem().getTitle())] = value;
  });
  return out;
}

/* 「5. 電話番号」のような通し番号と空白を落として突き合わせる */
function normalize(title) {
  return String(title || '').replace(/^\s*\d+\s*[.．、)）]\s*/, '').replace(/[\s　]+/g, '');
}

function pad(label) {
  while (label.length < 6) label += '　';
  return label;
}
