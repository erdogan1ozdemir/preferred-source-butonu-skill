# GA4 takibi

Buton yayıncının kendi bağlantısı olduğu için **tıklama doğrudan ölçülür.** Ayrı bir yönteme, tahmine veya doğrulama adımına gerek yoktur.

## Kod

Kart sarmalayıcısına `id="preferred-source-button"` verilir, dinleyici onun üzerine bağlanır.

```html
<script>
(function(){
  var el = document.getElementById("preferred-source-button");
  if(!el || el.dataset.psBound) return;
  el.dataset.psBound = "1";
  el.addEventListener("click", function(e){
    if(!e.target.closest("a")) return;
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
      event: "preferred_source_click",
      cta_id: "preferred-source-button",
      cta_variant: "t1-p1-f1",
      page_path: location.pathname
    });
  }, {passive:true});
})();
</script>
```

`closest("a")` kontrolü, kartın boş alanına yapılan tıklamaların olay üretmesini engeller. `psBound` bayrağı, şablon birden çok kez çalışırsa olayın ikilenmesini engeller.

## Görüntülenme (isteğe bağlı)

Tıklama oranı hesaplanacaksa görüntülenme de ölçülür.

```html
<script>
(function(){
  var el = document.getElementById("preferred-source-button");
  if(!el || el.dataset.psSeen || !("IntersectionObserver" in window)) return;
  new IntersectionObserver(function(girisler, gozlemci){
    girisler.forEach(function(g){
      if(!g.isIntersecting || el.dataset.psSeen) return;
      el.dataset.psSeen = "1";
      gozlemci.disconnect();
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({
        event: "preferred_source_view",
        cta_id: "preferred-source-button",
        cta_variant: "t1-p1-f1",
        page_path: location.pathname
      });
    });
  }, {threshold: 0.5}).observe(el);
})();
</script>
```

## GTM

Kod `dataLayer`'a yazar. Site GTM yerine doğrudan `gtag.js` kullanıyorsa `dataLayer.push(...)` satırları `gtag('event', ...)` ile değiştirilir.

| Katman | Ayar |
|---|---|
| Trigger | Custom Event · `preferred_source_click`, varsa `preferred_source_view` |
| Tag | GA4 Event, aynı ad |
| Parametreler | `cta_id`, `cta_variant`, `page_path` |
| GA4 admin | `cta_variant` custom dimension olarak tanımlanır |

`cta_variant` ton-yerleşim-çerçeve kodunu taşır (`t1-p1-f1`); birden çok varyant yayındaysa karşılaştırma bu boyutla yapılır.

## Ölçülemeyen tek şey

Okuyucunun Google ekranında **onayı tamamlayıp tamamlamadığı**. Onay Google tarafında gerçekleşir ve siteye sinyal dönmez.

Raporlamada tıklama net sayı olarak verilir; ekleme sayısı verilmez. Doğru ifade "kaç kişi butona tıkladı", "kaç kişi ekledi" değil.

## Gömme butonuna dönülürse

Google'ın kendi butonu cross-origin iframe olduğu için yukarıdaki kod çalışmaz; tıklama ana dokümana ulaşmaz. O durumda görüntülenme `IntersectionObserver` ile ölçülür, tıklama için `news.google.com` kökenli `postMessage` kanalı test ortamında incelenir. Ayrıntı: `google-preferred-sources.md` son bölüm.
