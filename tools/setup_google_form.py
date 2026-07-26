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
    """全角空白・必須記号などの揺れを吸収する"""
    t = re.sub(r"[\s　]+", "", title or "")
    return t.rstrip("*＊必須")


def fetch(url):
    view = url.replace("/formResponse", "/viewform")
    req = urllib.request.Request(view, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as res:
        return res.read().decode("utf-8", "replace")


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
        options = [o[0] for o in (entries[0][1] or [])] if len(entries[0]) > 1 and entries[0][1] else []
        questions.append({"title": title, "entry": "entry.%s" % entry_id, "options": options})
    return questions


def render_config(action, mapping):
    lines = [
        "/* Googleフォーム連携の設定",
        " * tools/setup_google_form.py が自動生成しました。手で編集しても構いません。",
        " * 再取得する場合:",
        ' *   python tools/setup_google_form.py "<公開フォームのURL>"',
        " *",
        " * action が空の場合は、メール下書き(mailto)へフォールバックします。",
        " */",
        "window.GOOGLE_FORM_CONFIG = {",
        '  action: "%s",' % action,
        "  fields: {",
    ]
    for key in ORDER:
        lines.append('    %s: "%s",%s' % (
            key, mapping.get(key, ""),
            "".ljust(max(1, 22 - len(key) - len(mapping.get(key, "")))) + "// " + COMMENTS[key]))
    lines += ["  }", "};", ""]
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    url = sys.argv[1].strip()
    html = fetch(url)
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

    action = re.sub(r"/viewform.*$", "/formResponse", url)
    if not action.endswith("/formResponse"):
        action = url.rstrip("/") + "/formResponse"

    CONFIG.write_text(render_config(action, mapping), encoding="utf-8")

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
    print("\n%s を更新しました。" % CONFIG.relative_to(ROOT))


if __name__ == "__main__":
    main()
