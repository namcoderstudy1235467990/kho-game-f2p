/* Cấu hình quảng cáo cho toàn bộ Kho Game F2P.
   Khi tài khoản Google AdSense được duyệt, điền mã nhà xuất bản (dạng ca-pub-XXXXXXXXXXXXXXXX) vào CLIENT.
   Để trống thì trang không tải quảng cáo nào. */
(function () {
  var CLIENT = 'ca-pub-1132142690787198';
  if (!CLIENT) return;
  if (!document.querySelector('script[src*="adsbygoogle.js"]')) {
  var s = document.createElement('script');
  s.async = true;
  s.crossOrigin = 'anonymous';
  s.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + CLIENT;
  document.head.appendChild(s);
  }
  function fill() {
    var slots = document.querySelectorAll('.ad-slot');
    for (var i = 0; i < slots.length; i++) {
      var box = slots[i], ins = document.createElement('ins');
      ins.className = 'adsbygoogle';
      ins.style.display = 'block';
      ins.setAttribute('data-ad-client', CLIENT);
      ins.setAttribute('data-ad-format', 'auto');
      ins.setAttribute('data-full-width-responsive', 'true');
      if (box.dataset.slot) ins.setAttribute('data-ad-slot', box.dataset.slot);
      box.appendChild(ins);
      box.classList.add('on');
      try { (window.adsbygoogle = window.adsbygoogle || []).push({}); } catch (e) {}
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fill); else fill();
})();
