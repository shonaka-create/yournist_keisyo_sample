/* フローティングバナー：無料診断 + 無料相談
   - ヒーローを読み終えたあたり（600px スクロール）で出現
   - フッターに重なる位置まで来たら退避
   - 診断ページ・問い合わせページ自身には出さない
   - 閉じたらそのセッション中は再表示しない */
(function () {
  'use strict';

  var DISMISS_KEY = 'yournist:float-dismissed';
  var SHOW_AFTER = 600;

  var path = location.pathname.replace(/index\.html$/, '');
  if (/\/(diagnosis|request)\/?$/.test(path)) return;

  try {
    if (sessionStorage.getItem(DISMISS_KEY) === '1') return;
  } catch (e) { /* ストレージが使えなくてもバナー自体は動かす */ }

  function depthPrefix() {
    // /column/manufacturing/skill-transfer/ -> ../../../
    var parts = path.split('/').filter(Boolean);
    if (/\.html$/.test(parts[parts.length - 1] || '')) parts.pop();
    return parts.length ? new Array(parts.length + 1).join('../') : '';
  }

  function build() {
    var p = depthPrefix();

    var bar = document.createElement('aside');
    bar.className = 'y-float';
    bar.setAttribute('aria-label', '無料診断と無料相談');

    var diag = document.createElement('a');
    diag.className = 'y-float__link y-float__link--diag';
    diag.href = p + 'diagnosis/';
    diag.innerHTML = '<small>2分・登録不要</small><strong>無料診断</strong>';

    var contact = document.createElement('a');
    contact.className = 'y-float__link y-float__link--contact';
    contact.href = p + 'request/index.html?type=consultation';
    contact.innerHTML = '<small>30分・オンライン</small><strong>無料相談 →</strong>';

    var close = document.createElement('button');
    close.className = 'y-float__close';
    close.type = 'button';
    close.setAttribute('aria-label', 'バナーを閉じる');
    close.textContent = '✕';
    close.addEventListener('click', function () {
      bar.classList.remove('is-visible');
      try { sessionStorage.setItem(DISMISS_KEY, '1'); } catch (e) { /* noop */ }
      setTimeout(function () { bar.remove(); }, 300);
    });

    bar.appendChild(diag);
    bar.appendChild(contact);
    bar.appendChild(close);
    document.body.appendChild(bar);
    return bar;
  }

  function init() {
    var bar = build();
    var footer = document.querySelector('footer');
    var footerVisible = false;

    if (footer && 'IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        footerVisible = entries[0].isIntersecting;
        sync();
      }, { rootMargin: '0px 0px -10% 0px' }).observe(footer);
    }

    function sync() {
      var show = window.scrollY > SHOW_AFTER && !footerVisible;
      bar.classList.toggle('is-visible', show);
    }

    var ticking = false;
    window.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () { sync(); ticking = false; });
    }, { passive: true });

    sync();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
