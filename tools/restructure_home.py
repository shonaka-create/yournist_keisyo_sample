from pathlib import Path
import re

path = Path(__file__).resolve().parents[1] / "site" / "index.html"
text = path.read_text(encoding="utf-8")
text = text.replace('<a href="#industries">業界別</a><a href="#service">支援領域</a><a href="#flow">進め方</a><a href="column/">ナレッジ</a>', '<a href="#business">事業一覧</a><a href="#flow">私たちの支援</a><a href="news/">企業ニュース</a><a href="column/">お役立ち記事</a>')
text = text.replace('href="#industries">業界別の支援を見る', 'href="#business">事業一覧を見る')

business = '''<section class="r-industries" id="business">
  <div class="r-shell">
    <div class="r-heading"><div><p class="r-section-no">02 / BUSINESS</p><h2>業界の違いに、<br>事業で応える。</h2></div><p>属人化という共通課題に対し、卸売業と製造業では残すべき判断も、現場への入り方も異なります。業界別の専用事業として、支援内容と成果を設計します。</p></div>
    <div class="r-business-list">
      <a class="r-business-card" href="business/wholesale/">
        <div class="r-business-card__copy"><span>01 / WHOLESALE</span><h3>卸売業向け事業</h3><p>受発注・価格・在庫・配送・問い合わせにある属人判断を、誰でも回せる仕組みへ。</p><ul><li>得意先別価格と請求</li><li>発注・在庫・配送判断</li><li>問い合わせ・業務承継</li></ul><strong>事業LPを見る ↗</strong></div>
        <img src="assets/img/hero-wholesale.webp" alt="卸売会社で業務を引き継ぐ担当者" loading="lazy"><em>初期は医薬品卸から提供開始</em>
      </a>
      <a class="r-business-card r-business-card--reverse" href="business/manufacturing/">
        <div class="r-business-card__copy"><span>02 / MANUFACTURING</span><h3>メーカー向け事業</h3><p>見積・工程・品質・保全にある熟練判断を、次世代が再現・改善できる技術資産へ。</p><ul><li>見積・原価判断</li><li>工程条件・品質対応</li><li>設備保全・技術承継</li></ul><strong>事業LPを見る ↗</strong></div>
        <img src="assets/img/manufacturing.webp" alt="製造現場で技術を引き継ぐエンジニア" loading="lazy"><em>個別相談を受付中</em>
      </a>
    </div>
  </div>
</section>'''
text = re.sub(r'<section class="r-industries" id="industries">.*?</section>', business, text, count=1, flags=re.S)

news = '''<section class="r-corporate-news">
  <div class="r-shell"><div class="r-heading"><div><p class="r-section-no">08 / CORPORATE NEWS</p><h2>企業ニュース</h2></div><a class="r-view-all" href="news/">ニュース一覧を見る ↗</a></div>
    <div class="r-news-list"><a href="news/"><time>2026.07.20</time><span>企業情報</span><p>事業承継レスキューのサイトを刷新しました</p><b>↗</b></a><a href="news/"><time>2026.07.20</time><span>サービス</span><p>医薬品卸を初期対象として相談受付を開始しました</p><b>↗</b></a><a href="news/"><time>2026.07.20</time><span>お知らせ</span><p>資料請求・無料相談窓口を開設しました</p><b>↗</b></a></div>
  </div>
</section>

'''
text = text.replace('<section class="r-knowledge">', news + '<section class="r-knowledge">')
text = text.replace('08 / KNOWLEDGE', '09 / SERVICE KNOWLEDGE').replace('属人化を解くための、<br>実務ナレッジ。', 'サービスの<br>お役立ち記事。')
text = text.replace('09 / CONTACT', '10 / CONTACT')
text = text.replace('<a href="#industries">業界別</a><a href="#service">支援領域</a><a href="#flow">進め方</a><a href="column/">ナレッジ</a>', '<a href="#business">事業一覧</a><a href="news/">企業ニュース</a><a href="column/">お役立ち記事</a><a href="#flow">私たちの支援</a>')
text = text.replace('href="contact/">無料診断', 'href="request/">資料請求・相談')
text = text.replace('href="contact/">無料で引き継ぎリスクを診断', 'href="request/">資料請求・無料相談')
path.write_text(text, encoding="utf-8")
