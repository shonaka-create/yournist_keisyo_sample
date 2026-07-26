# -*- coding: utf-8 -*-
"""公開済みGoogleフォームのURLから entry ID を自動で読み取り、
   site/request/form-config.js を書き換える。

使い方:
    python tools/setup_google_form.py "https://docs.google.com/forms/d/e/XXXX/viewform"

フォーム側の質問タイトルを FIELD_TITLES と一致させておけば、
どの質問がどの入力欄に対応するかは自動で決まる。
entry ID を手で探す必要はない。
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "site" / "request" / "form-config.js"

# フォーム側の質問タイトル → form-config.js のキー
FIELD_TITLES = {
    "お問い合わせ種別": "requestType",
    "会社名": "company",
    "お名前": "name",
    "メールアドレス": "email",
    "電話番号": "phone",
    "業界": "industry",
    "従業員規模": "employees",
    "役職・部門": "role",
    "検討時期": "timing",
    "関心のあるテーマ": "topic",
    "現在の状況・知りたいこと": "message",
    "診断スコア": "diagnosisScore",
    "診断レベル": "diagnosisLevel",
}

ORDER = ["requestType", "company", "name", "email", "industry", "topic",
         "phone", "employees", "role", "timing", "message",
         "diagnosisScore", "diagnosisLevel"]

COMMENTS = {
    "requestType": "お問い合わせ種別（送信値は「資料を請求する」「無料相談を申し込む」）",
    "company": "会社名",
    "name": "お名前",
    "email": "メールアドレス",
    "industry": "業界",
    "topic": "関心のあるテーマ",
    "phone": "電話番号",
    "employees": "従業員規模",
    "role": "役職・部門",
    "timing": "検討時期",
    "message": "現在の状況・知りたいこと（※長文。診断結果もここへ入る）",
    "diagnosisScore": "危険度スコア 0〜100",
    "diagnosisLevel": "危険度レベル 1〜4",
}


def normalize(title):
    """先頭の通し番号・空白・必須記号などの揺れを吸収する。
    フォーム側で「1. お問い合わせ種別」のように番号を振っても対応づけできるようにする。"""
    t = re.sub(r"^\s*\d+\s*[.．、)）]\s*", "", title or "")
    t = re.sub(r"[\s　]+", "", t)
    return t.rstrip("*＊必須")


def fetch(url):
    """HTMLと、リダイレクト解決後の実URLを返す。
    forms.gle の短縮URLをそのまま渡せるようにするため、解決後のURLを使う。"""
    view = url.replace("/formResponse", "/viewform")
    req = urllib.request.Request(view, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as res:
        return res.read().decode("utf-8", "replace"), res.geturl()


def parse_questions(html):
    """公開フォームに埋まっている FB_PUBLIC_LOAD_DATA_ から質問一覧を取り出す"""
    m = re.search(r"FB_PUBLIC_LOAD_DATA_\s*=\s*(\[.*?\]);\s*</script>", html, re.S)
    if not m:
        raise SystemExit("フォームの定義を読み取れませんでした。"
                         "「リンクを知っている全員が回答可能」な公開URLか確認してください。")
    data = json.loads(m.group(1))
    questions = []
    for item in (data[1][1] or []):
        title = item[1] if len(item) > 1 else None
        entries = item[4] if len(item) > 4 else None
        if not title or not entries:
            continue  # 見出しや説明文のみのブロック
        entry_id = entries[0][0]
        raw = (entries[0][1] or []) if len(entries[0]) > 1 else []
        # 5番目の要素が1の空文字は Google の「その他（自由入力）」。通常の選択肢ではない。
        options = [o[0] for o in raw if not (len(o) > 4 and o[4] == 1)]
        has_other = any(len(o) > 4 and o[4] == 1 for o in raw)
        required = bool(entries[0][2]) if len(entries[0]) > 2 else False
        questions.append({"title": title, "entry": "entry.%s" % entry_id, "options": options,
                          "required": required, "other": has_other, "choice": bool(raw)})
    return questions


def probe_anonymous_post(action):
    """回答を1件も作らずに、匿名で送信できるかだけを確かめる。
    必須項目を空にしたPOSTは記録されず、入力検証エラー(400)になる。
    ログインが必要な設定だと、その手前で401が返るので区別できる。"""
    import urllib.error
    import urllib.parse
    body = urllib.parse.urlencode({"entry.0": ""}).encode()
    req = urllib.request.Request(action, data=body, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            return res.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return None


def site_form_spec():
    """サイト側フォームの選択肢と必須/任意を読み取る"""
    html = (ROOT / "site" / "request" / "index.html").read_text(encoding="utf-8")
    form = re.search(r'<form class="request-form".*?</form>', html, re.S).group(0)
    spec = {}
    for m in re.finditer(r'<(select|input|textarea)([^>]*)id="([^"]+)"([^>]*)>(.*?)</\1>|'
                         r'<input([^>]*)id="([^"]+)"([^>]*)>', form, re.S):
        attrs = "".join(x for x in m.groups()[:4] if x) if m.group(1) else "".join(
            x for x in m.groups()[5:] if x)
        fid = m.group(3) or m.group(7)
        if not fid:
            continue
        opts = [o for o in re.findall(r'<option[^>]*>([^<]+)</option>', m.group(5) or "")
                if o != "選択してください"]
        spec[fid] = {"required": "required" in attrs, "options": opts}
    return spec


def check_consistency(questions):
    """必須設定と選択肢のズレを洗い出す。ズレたまま繋ぐと送信が失敗する。"""
    site = site_form_spec()
    key_by_title = {normalize(t): k for t, k in FIELD_TITLES.items()}
    problems = []
    for q in questions:
        key = key_by_title.get(normalize(q["title"]))
        if not key or key not in site:
            continue
        s = site[key]
        if q.get("required") and not s["required"]:
            problems.append("「%s」がフォーム側で必須。サイト側は任意のため、"
                            "未入力のまま送ると送信が失敗します → 必須を外してください" % q["title"])
        if "" in q["options"]:
            problems.append("「%s」に空の選択肢が残っています → 削除してください" % q["title"])
        # 「その他（自由入力）」があれば、選択肢に無い値もそちらへ載せて送れる
        missing = [o for o in s["options"] if o and o not in q["options"]]
        if missing and not q.get("other"):
            problems.append("「%s」にサイト側の選択肢がありません: %s → "
                            "フォームに追加するか、サイト側の選択肢を合わせてください"
                            % (q["title"], " / ".join(missing)))
    return problems


def choice_maps(questions):
    """選択肢と「その他」の有無を、サイト側が参照できる形で書き出す"""
    key_by_title = {normalize(t): k for t, k in FIELD_TITLES.items()}
    choices, others = {}, {}
    for q in questions:
        key = key_by_title.get(normalize(q["title"]))
        if not key or not q.get("choice"):
            continue
        choices[key] = q["options"]
        if q.get("other"):
            others[key] = True
    return choices, others


def render_config(action, mapping, choices=None, others=None):
    lines = [
        "/* Googleフォーム連携の設定",
        " * tools/setup_google_form.py が自動生成しました。手で編集しても構いません。",
        " * 再取得する場合:",
        ' *   python tools/setup_google_form.py "<公開フォームのURL>"',
        " *",
        " * action が空の場合は、メール下書き(mailto)へフォールバックします。",
        " * choices はフォーム側が受け付ける選択肢。ここに無い値をそのまま送ると",
        " * Googleが400で弾くため、other が true の項目は「その他」へ載せて送ります。",
        " */",
        "window.GOOGLE_FORM_CONFIG = {",
        '  action: "%s",' % action,
        "  fields: {",
    ]
    for key in ORDER:
        lines.append('    %s: "%s",%s' % (
            key, mapping.get(key, ""),
            "".ljust(max(1, 22 - len(key) - len(mapping.get(key, "")))) + "// " + COMMENTS[key]))
    lines.append("  },")
    lines.append("  choices: {")
    for key, opts in (choices or {}).items():
        lines.append("    %s: [%s]," % (key, ", ".join('"%s"' % o for o in opts)))
    lines.append("  },")
    lines.append("  other: {")
    for key in (others or {}):
        lines.append("    %s: true," % key)
    lines.append("  }")
    lines += ["};", ""]
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    url = sys.argv[1].strip()
    html, resolved = fetch(url)
    questions = parse_questions(html)

    mapping, matched_titles = {}, set()
    for q in questions:
        key = None
        for title, k in FIELD_TITLES.items():
            if normalize(q["title"]) == normalize(title):
                key = k
                break
        if key:
            mapping[key] = q["entry"]
            matched_titles.add(q["title"])

    action = re.sub(r"/viewform.*$", "/formResponse", resolved.split("?")[0])
    if not action.endswith("/formResponse"):
        action = resolved.split("?")[0].rstrip("/") + "/formResponse"

    print("解決後のフォームURL: %s" % resolved.split("?")[0])
    print("action: %s" % action)
    print("\n--- 対応づけできた項目 (%d/%d) ---" % (len(mapping), len(FIELD_TITLES)))
    for key in ORDER:
        if key in mapping:
            print("  OK   %-16s %s" % (key, mapping[key]))
    missing = [k for k in FIELD_TITLES.values() if k not in mapping]
    if missing:
        print("\n--- フォーム側に見つからなかった質問 ---")
        for key in ORDER:
            if key in missing:
                title = [t for t, v in FIELD_TITLES.items() if v == key][0]
                print("  --   %-16s 「%s」" % (key, title))
        print("  ※ この項目は送信対象から外れます（フォームに追加すれば次回取得で入ります）")
    extra = [q["title"] for q in questions if q["title"] not in matched_titles]
    if extra:
        print("\n--- 対応先がないフォーム側の質問 ---")
        for t in extra:
            print("  ??   「%s」" % t)

    blockers = []
    status = probe_anonymous_post(action)
    print("\n匿名送信の可否: HTTP %s -> %s" % (
        status, {400: "OK（入力検証エラー＝送信自体は通る）",
                 401: "NG（Googleログインが必要）"}.get(status, "要確認")))
    if status == 401:
        blockers.append("回答にGoogleログインが必要な設定です。"
                        "サイトからの送信が401で拒否され、訪問者にもログインが強制されます。\n"
                        "       → 設定タブ →「回答」→「メールアドレスを収集する」を"
                        "「回答者からの入力」または「収集しない」へ変更してください。")
    blockers += check_consistency(questions)

    choices, others = choice_maps(questions)
    if blockers:
        print("\n=== 送信が失敗する設定が残っています（要修正） ===")
        for i, b in enumerate(blockers, 1):
            print("  %d. %s" % (i, b))
        # 不備があるまま action を書くと、サイトは「送信しました」と表示しつつ
        # Googleフォーム側で弾かれ、問い合わせが消える。直るまで mailto を使い続ける。
        CONFIG.write_text(render_config("", mapping, choices, others), encoding="utf-8")
        print("\n  → 取りこぼしを防ぐため、action は空のままにしました"
              "（サイトは従来どおりメール下書きへフォールバックします）。")
        print("  → 修正後にもう一度このコマンドを実行すると、Googleフォームへ切り替わります。")
    else:
        CONFIG.write_text(render_config(action, mapping, choices, others), encoding="utf-8")
        print("\n設定の不一致はありません。Googleフォームへの送信を有効にしました。")
        for key, opts in choices.items():
            print("  選択肢 %-12s %s%s" % (key, " / ".join(opts),
                                        "  + その他(自由入力)" if others.get(key) else ""))

    print("\n%s を更新しました。" % CONFIG.relative_to(ROOT))


if __name__ == "__main__":
    main()
