/* ブラックボックス危険度診断
   12問・5軸。各設問の回答は 0〜3 点。
   危険度スコアは「業務の集中度・仕組みの不透明さ・停止時の影響・復旧力」の4軸(満点30)を100点換算する。
   「時間の余裕のなさ」はスコアに混ぜず、対処に使える残り時間として別枠で評価し、
   猶予が乏しい場合のみ危険度レベルを1段階引き上げる。 */
(function () {
  'use strict';

  var AXES = {
    concentration: { label: '業務の集中度', max: 9, note: '判断が特定の人に依存している度合い' },
    legacy: { label: '仕組みの不透明さ', max: 9, note: 'Excel・自作ツール・システムの中身を追えるか' },
    impact: { label: '停止時の影響', max: 6, note: '止まったとき何がどれだけ早く困るか' },
    recovery: { label: '復旧・代替の弱さ', max: 6, note: '元に戻せるか、代わりの人が動けるか' },
    time: { label: '時間の余裕のなさ', max: 6, note: '引き継ぎに使える残り時間' }
  };

  var QUESTIONS = [
    { axis: 'concentration', q: '主要な業務のうち、特定の1人しか最後まで実行できないものはありますか。',
      a: ['ない', '1〜2業務ある', '3業務以上ある', 'ほとんどの主要業務がそうだ'] },
    { axis: 'concentration', q: 'その担当者が1週間不在になったとき、業務はどうなりますか。',
      a: ['代行者が問題なく回せる', '多少遅れるが回る', '一部の業務が止まる', '受注・請求など基幹業務が止まる'] },
    { axis: 'concentration', q: '例外対応（急配・特別値引き・返品・イレギュラー処理など）の判断基準は文書化されていますか。',
      a: ['文書化され、更新されている', '文書はあるが更新が止まっている', '一部だけ文書がある', '文書はなく口頭で共有している'] },

    { axis: 'legacy', q: '業務にExcel関数・マクロ(VBA)・Access・自作ツールがどの程度組み込まれていますか。',
      a: ['ほとんど使っていない', '補助的に使う程度', '基幹業務の一部を担っている', 'それ無しでは基幹業務が回らない'] },
    { axis: 'legacy', q: 'それらを作った本人は、今も社内にいますか。',
      a: ['該当なし／作成者が現役で在籍', '在籍しているが別部署・多忙', '退職済みだが引き継ぎは済んでいる', '退職済みで、中身が分からない'] },
    { axis: 'legacy', q: '「この数字がどう計算されているか」を、担当者以外が説明できますか。',
      a: ['説明できる', '主要なものは説明できる', '一部しか説明できない', '誰も説明できない'] },

    { axis: 'impact', q: 'その業務が止まったとき、最初に影響が出るのはどこですか。',
      a: ['社内資料の作成が遅れる程度', '社内業務が滞る', '得意先への回答・納品が遅れる', '受注・出荷・請求が止まる'] },
    { axis: 'impact', q: '止まった場合、何日以内に復旧する必要がありますか。',
      a: ['1週間以上の猶予がある', '2〜3日以内', '翌日中', '当日中'] },

    { axis: 'recovery', q: 'バックアップから実際にデータを復元してみたことはありますか。',
      a: ['定期的に復元テストをしている', '過去に試したことがある', 'バックアップはあるが復元は未検証', 'バックアップの有無を把握していない'] },
    { axis: 'recovery', q: '手順書を、作成者以外が実際に見ながら業務を実行したことはありますか。',
      a: ['定期的に実施している', '一度試したことがある', '手順書はあるが試していない', '手順書自体がない'] },

    { axis: 'time', q: '業務の中心にいる方の退職・異動・世代交代の予定はありますか。',
      a: ['予定なし（5年以上先）', '3〜5年以内', '1〜2年以内', '1年以内、または既に退職された'] },
    { axis: 'time', q: '引き継ぎに充てられる期間は、どの程度確保できそうですか。',
      a: ['1年以上かけられる', '半年程度', '3か月程度', '1か月未満、または未定'] }
  ];

  var LEVELS = [
    { level: 1, min: 0, max: 24, name: '低', headline: '大きなブラックボックスは見当たりません',
      lead: '現時点で業務が止まる可能性は低い状態です。ただし担当者の交代や業務変更で状況は変わります。今の状態を記録として残し、定期的に確認できる形にしておくことが次の一手になります。' },
    { level: 2, min: 25, max: 49, name: '注意', headline: '一部の業務が特定の人に依存し始めています',
      lead: 'まだ全体は回っていますが、放置すると引き継ぎ時に確認できない範囲が広がります。影響の大きい業務から順に、判断の根拠を記録へ残していく段階です。' },
    { level: 3, min: 50, max: 74, name: '高', headline: '止まると影響の大きい業務がブラックボックス化しています',
      lead: '担当者が不在になった時点で、業務の再現が難しくなる可能性が高い状態です。全体を一度に整理しようとせず、止まると困る業務を特定して優先順位をつけることから始める必要があります。' },
    { level: 4, min: 75, max: 100, name: '危険', headline: '担当者の不在が、そのまま業務停止につながる状態です',
      lead: '判断の根拠を確認できる相手が社内に限られており、退職・異動が発生すると復元が困難になります。現状の証拠保全と、優先度の高い業務の洗い出しを早急に行うことをお勧めします。' }
  ];

  var ADVICE = {
    concentration: {
      title: '判断の根拠が、人の中にしか残っていません',
      body: '手順そのものより「なぜその判断になるのか」が失われると、業務は再現できなくなります。通常処理だけでなく、例外条件・確認先・承認範囲までを、実際の伝票や画面出力と突き合わせながら記録へ落とす作業が有効です。',
      service: 'デジタル継承パック'
    },
    legacy: {
      title: '仕組みの中身が追えなくなっています',
      body: 'Excelや自作ツールは動いている限り問題が見えないため、壊れて初めて依存に気付きます。どのファイル・システムが何の業務を支えているかを一覧化し、変更したときに何が壊れるかを把握することが先決です。',
      service: 'ブラックボックス危険度診断（詳細版）'
    },
    impact: {
      title: '止まったときの影響範囲が大きい業務があります',
      body: '全業務を均等に扱うと手が回りません。停止したときの影響と、復旧までに許される時間の2軸で業務を並べ替え、上位から着手すると限られた工数でも効果が出ます。',
      service: 'ブラックボックス危険度診断（詳細版）'
    },
    recovery: {
      title: '元に戻せる状態かどうかが確認できていません',
      body: 'バックアップも手順書も、実際に使ってみるまで有効かどうかは分かりません。復元テストと、作成者以外による手順の実行確認まで行って初めて「引き継げる状態」になります。',
      service: '継続運用・変更管理'
    },
    time: {
      title: '確認できる相手がいるうちに動く必要があります',
      body: '退職や世代交代が決まってからでは、聞ける相手がいる期間が限られます。残り時間が短い場合は範囲を広げず、止まると最も困る業務を1つに絞って着手するほうが確実です。',
      service: 'デジタル継承パック'
    },
    /* 全軸が低い場合。リスクを指摘するのではなく、現状を維持する提案を返す。 */
    _stable: {
      title: '今の状態を、記録として残しておく段階です',
      body: '現時点で大きな停止リスクは見当たりません。ただし今回の回答は「現在の担当者がいる前提」の評価です。担当者の交代・業務量の変化・システム更新のタイミングで状況は変わるため、いま回っている手順と判断基準を記録に残し、年に一度この診断で変化を確認することをお勧めします。',
      service: '継続運用・変更管理'
    }
  };

  var STORAGE_KEY = 'yournist:diagnosis';

  var answers = new Array(QUESTIONS.length).fill(null);
  var root, stepsEl, resultEl, barEl, countEl;

  /* ---------- 採点 ---------- */

  function evaluate() {
    var axes = {};
    Object.keys(AXES).forEach(function (k) { axes[k] = 0; });
    QUESTIONS.forEach(function (q, i) {
      if (answers[i] !== null) axes[q.axis] += answers[i];
    });

    var riskMax = AXES.concentration.max + AXES.legacy.max + AXES.impact.max + AXES.recovery.max;
    var riskRaw = axes.concentration + axes.legacy + axes.impact + axes.recovery;
    var score = Math.round((riskRaw / riskMax) * 100);

    var level = LEVELS.filter(function (l) { return score >= l.min && score <= l.max; })[0].level;
    var timeRatio = axes.time / AXES.time.max;
    var escalated = false;
    if (timeRatio >= 0.67 && level < 4) { level += 1; escalated = true; }
    var shown = LEVELS.filter(function (l) { return l.level === level; })[0];

    var ranked = Object.keys(AXES).map(function (k) {
      return {
        key: k, label: AXES[k].label, note: AXES[k].note,
        raw: axes[k], max: AXES[k].max, pct: Math.round((axes[k] / AXES[k].max) * 100)
      };
    }).sort(function (a, b) { return b.pct - a.pct; });

    // 50%以上の軸を優先課題とする。該当が無い場合、最上位が30%未満なら
    // 「弱点なし」とみなして維持の提案を返し、30%以上なら最上位1件だけ返す。
    var priorities = ranked.filter(function (r) { return r.pct >= 50; }).slice(0, 3);
    if (!priorities.length) {
      priorities = ranked[0].pct >= 30 ? ranked.slice(0, 1) : [{ key: '_stable', pct: ranked[0].pct }];
    }

    return {
      score: score, level: level, shown: shown, escalated: escalated,
      timeRatio: timeRatio, axes: ranked, priorities: priorities
    };
  }

  function summaryText(r) {
    var lines = [];
    lines.push('【ブラックボックス危険度診断の結果】');
    lines.push('危険度スコア: ' + r.score + '/100（危険度レベル' + r.level + '：' + r.shown.name + '）');
    if (r.escalated) lines.push('※引き継ぎに使える時間が限られているため、危険度を1段階引き上げています。');
    lines.push('');
    lines.push('■ 軸ごとの状況');
    r.axes.forEach(function (a) {
      lines.push('・' + a.label + '：' + a.pct + '%（' + a.raw + '/' + a.max + '点）');
    });
    lines.push('');
    lines.push('■ 優先して着手すべき点');
    r.priorities.forEach(function (p, i) {
      lines.push((i + 1) + '. ' + ADVICE[p.key].title);
    });
    lines.push('');
    lines.push('■ 回答内容');
    QUESTIONS.forEach(function (q, i) {
      lines.push('Q' + (i + 1) + '. ' + q.q);
      lines.push('　→ ' + (answers[i] === null ? '(未回答)' : q.a[answers[i]]));
    });
    return lines.join('\n');
  }

  /* ---------- 描画 ---------- */

  function h(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function answered() {
    return answers.filter(function (v) { return v !== null; }).length;
  }

  function updateProgress() {
    var n = answered();
    barEl.style.width = (n / QUESTIONS.length * 100) + '%';
    countEl.textContent = n + ' / ' + QUESTIONS.length;
    root.querySelector('.dg-submit').disabled = n < QUESTIONS.length;
  }

  function renderQuestions() {
    QUESTIONS.forEach(function (q, i) {
      var card = h('li', 'dg-q');
      card.id = 'dg-q' + (i + 1);

      var head = h('div', 'dg-q__head');
      head.appendChild(h('span', 'dg-q__no', 'Q' + (i + 1)));
      head.appendChild(h('span', 'dg-q__axis', AXES[q.axis].label));
      card.appendChild(head);

      var fs = document.createElement('fieldset');
      fs.className = 'dg-q__body';
      var lg = document.createElement('legend');
      lg.className = 'dg-q__text';
      lg.textContent = q.q;
      fs.appendChild(lg);

      var opts = h('div', 'dg-opts');
      q.a.forEach(function (label, v) {
        var id = 'q' + i + '_' + v;
        var wrap = h('label', 'dg-opt');
        wrap.setAttribute('for', id);
        var input = document.createElement('input');
        input.type = 'radio';
        input.name = 'q' + i;
        input.id = id;
        input.value = String(v);
        input.addEventListener('change', function () {
          answers[i] = v;
          card.classList.add('is-answered');
          updateProgress();
          var next = root.querySelector('#dg-q' + (i + 2));
          if (next) next.scrollIntoView({ behavior: 'smooth', block: 'center' });
        });
        wrap.appendChild(input);
        wrap.appendChild(h('span', 'dg-opt__mark'));
        wrap.appendChild(h('span', 'dg-opt__label', label));
        opts.appendChild(wrap);
      });
      fs.appendChild(opts);
      card.appendChild(fs);
      stepsEl.appendChild(card);
    });
  }

  function renderResult(r) {
    resultEl.innerHTML = '';

    var head = h('div', 'dg-result__head dg-level-' + r.level);
    head.appendChild(h('p', 'dg-result__eyebrow', '診断結果'));

    var scoreRow = h('div', 'dg-score');
    var gauge = h('div', 'dg-score__gauge');
    gauge.style.setProperty('--pct', r.score);
    gauge.appendChild(h('strong', null, String(r.score)));
    gauge.appendChild(h('small', null, '/100'));
    scoreRow.appendChild(gauge);

    var meta = h('div', 'dg-score__meta');
    meta.appendChild(h('p', 'dg-score__level', '危険度レベル' + r.level + '：' + r.shown.name));
    meta.appendChild(h('h3', 'dg-score__headline', r.shown.headline));
    meta.appendChild(h('p', 'dg-score__lead', r.shown.lead));
    scoreRow.appendChild(meta);
    head.appendChild(scoreRow);

    if (r.escalated) {
      head.appendChild(h('p', 'dg-note',
        '引き継ぎに使える時間が限られているため、危険度を1段階引き上げて表示しています。スコア自体は ' + r.score + '/100 です。'));
    }
    resultEl.appendChild(head);

    var axesSec = h('section', 'dg-block');
    axesSec.appendChild(h('h3', 'dg-block__title', '軸ごとの状況'));
    var list = h('div', 'dg-axes');
    r.axes.forEach(function (a) {
      var row = h('div', 'dg-axis');
      var top = h('div', 'dg-axis__top');
      top.appendChild(h('span', 'dg-axis__label', a.label));
      top.appendChild(h('span', 'dg-axis__pct', a.pct + '%'));
      row.appendChild(top);
      var track = h('div', 'dg-axis__track');
      var fill = h('div', 'dg-axis__fill');
      fill.style.width = a.pct + '%';
      if (a.pct >= 67) fill.classList.add('is-high');
      else if (a.pct >= 34) fill.classList.add('is-mid');
      track.appendChild(fill);
      row.appendChild(track);
      row.appendChild(h('p', 'dg-axis__note', a.note));
      list.appendChild(row);
    });
    axesSec.appendChild(list);
    resultEl.appendChild(axesSec);

    var advSec = h('section', 'dg-block');
    advSec.appendChild(h('h3', 'dg-block__title', '優先して着手すべき点'));
    var ol = h('ol', 'dg-advice');
    r.priorities.forEach(function (p) {
      var a = ADVICE[p.key];
      var li = h('li', 'dg-advice__item');
      li.appendChild(h('h4', null, a.title));
      li.appendChild(h('p', null, a.body));
      li.appendChild(h('span', 'dg-advice__tag', '関連する支援：' + a.service));
      ol.appendChild(li);
    });
    advSec.appendChild(ol);
    resultEl.appendChild(advSec);

    var cta = h('section', 'dg-cta');
    cta.appendChild(h('h3', null, 'この結果をもとに、対象業務を一緒に整理します'));
    cta.appendChild(h('p', null,
      '無料相談では、診断結果をお持ちいただければ、止まると困る業務の特定と優先順位づけまでを30分程度で行います。回答内容は問い合わせフォームへ自動で引き継がれます。'));

    var actions = h('div', 'dg-cta__actions');
    var primary = h('a', 'dg-btn dg-btn--primary', '診断結果をつけて無料相談する →');
    primary.href = '../request/index.html?type=consultation&from=diagnosis';
    actions.appendChild(primary);

    var copy = h('button', 'dg-btn dg-btn--ghost', '結果をコピーする');
    copy.type = 'button';
    copy.addEventListener('click', function () {
      var text = summaryText(r);
      var done = function () { copy.textContent = 'コピーしました'; setTimeout(function () { copy.textContent = '結果をコピーする'; }, 2000); };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, function () { window.prompt('コピーしてください', text); });
      } else {
        window.prompt('コピーしてください', text);
      }
    });
    actions.appendChild(copy);

    var again = h('button', 'dg-btn dg-btn--ghost', 'もう一度診断する');
    again.type = 'button';
    again.addEventListener('click', function () {
      answers = new Array(QUESTIONS.length).fill(null);
      root.querySelectorAll('input[type=radio]').forEach(function (n) { n.checked = false; });
      root.querySelectorAll('.dg-q').forEach(function (n) { n.classList.remove('is-answered'); });
      resultEl.hidden = true;
      root.querySelector('.dg-form').hidden = false;
      updateProgress();
      root.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
    actions.appendChild(again);

    cta.appendChild(actions);
    resultEl.appendChild(cta);

    resultEl.appendChild(h('p', 'dg-disclaimer',
      'この診断は、いただいた回答のみに基づく簡易評価です。実際の停止リスクは業務量・体制・システム構成によって変わるため、結果は着手順位の目安としてご利用ください。回答内容はお使いのブラウザ内にのみ保存され、送信されません。'));
  }

  /* ---------- 初期化 ---------- */

  function init() {
    root = document.getElementById('diagnosis');
    if (!root) return;

    var form = h('form', 'dg-form');
    form.noValidate = true;

    var progress = h('div', 'dg-progress');
    progress.appendChild(h('span', 'dg-progress__label', '回答状況'));
    countEl = h('span', 'dg-progress__count', '0 / ' + QUESTIONS.length);
    progress.appendChild(countEl);
    var track = h('div', 'dg-progress__track');
    barEl = h('div', 'dg-progress__bar');
    track.appendChild(barEl);
    progress.appendChild(track);
    form.appendChild(progress);

    stepsEl = h('ol', 'dg-questions');
    form.appendChild(stepsEl);

    var submit = h('button', 'dg-btn dg-btn--primary dg-submit', '診断結果を見る →');
    submit.type = 'submit';
    submit.disabled = true;
    form.appendChild(submit);

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (answered() < QUESTIONS.length) return;
      var r = evaluate();
      try {
        sessionStorage.setItem(STORAGE_KEY, JSON.stringify({
          score: r.score, level: r.level, name: r.shown.name, summary: summaryText(r), at: Date.now()
        }));
      } catch (err) { /* プライベートモード等では保存できないが診断表示は続行する */ }
      renderResult(r);
      resultEl.hidden = false;
      form.hidden = true;
      resultEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });

    root.appendChild(form);

    resultEl = h('div', 'dg-result');
    resultEl.hidden = true;
    resultEl.setAttribute('role', 'region');
    resultEl.setAttribute('aria-label', '診断結果');
    root.appendChild(resultEl);

    renderQuestions();
    updateProgress();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
