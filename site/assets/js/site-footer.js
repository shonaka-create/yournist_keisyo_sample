/* 共通フッター：著作権表記の年号を埋める。
   ページ側の個別スクリプトに依存しないよう、全ページでこのファイルを読み込む。 */
(function () {
  'use strict';
  function fill() {
    var year = String(new Date().getFullYear());
    var nodes = document.querySelectorAll('.r-footer [data-year]');
    for (var i = 0; i < nodes.length; i++) nodes[i].textContent = year;
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fill);
  else fill();
})();
