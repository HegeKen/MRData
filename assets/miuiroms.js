$(document).ready(function () {
  $("body").addClass("mdui-bottom-nav-fixed");
  var pathName = window.document.location.pathname;
  var height = $(document).width();
  var lang = navigator.language.substr(0, 2);
  if (pathName == "" || pathName == "/") {
    if (height < "550") {
      if (lang === "zh") {
        window.location = "/mobile/zh-CN/";
      } else {
        window.location = "/mobile/en-US/";
      }
    } else {
      if (lang === "zh") {
        window.location = "/zh-CN/";
      } else {
        window.location = "/en-US/";
      }
    }
  }
  if (pathName == "/mobile" || pathName == "/mobile/") {
    if (lang === "zh") {
      window.location = "/mobile/zh-CN/";
    } else {
      window.location = "/mobile/en-US/";
    }
  }
});
(function (c, l, a, r, i, t, y) {
  c[a] =
    c[a] ||
    function () {
      (c[a].q = c[a].q || []).push(arguments);
    };
  t = l.createElement(r);
  t.async = 1;
  t.src = "https://www.clarity.ms/tag/" + i + "?ref=bwt";
  y = l.getElementsByTagName(r)[0];
  y.parentNode.insertBefore(t, y);
})(window, document, "clarity", "script", "ecb8j7x9aw");
window.dataLayer = window.dataLayer || [];
function gtag() {
  dataLayer.push(arguments);
}
gtag("js", new Date());
gtag("config", "UA-153213840-1");
var _hmt = _hmt || [];
(function () {
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?f107e28fc41495046dc606c8b53ee24e";
  var s = document.getElementsByTagName("script")[0];
  s.parentNode.insertBefore(hm, s);
})();
