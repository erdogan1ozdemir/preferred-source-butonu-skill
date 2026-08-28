# GA4 takibi

## Kod

Kart sarmalayıcısına `id="preferred-source-button"` verilir, dinleyici onun üzerine bağlanır.

```html
<script>
(function(){
  var el = document.getElementById("preferred-source-button");
  if(!el || el.dataset.psBound) return;
  el.dataset.psBound = "1";
  el.addEventListener("click", function(){
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
      event: "preferred_source_click",
      cta_id: "preferred-source-button",
      cta_variant: "t1-p1-f0",
      page_path: location.pathname
    });
  }, {passive:true});
})();
</script>
```

`psBound` bayrağı, script şablonda birden çok kez çalışırsa event'in ikilenmesini engeller.

## GTM

| Katman | Ayar |
|---|---|
| Trigger | Custom Event, event name `preferred_source_click` |
| Tag | GA4 Event, aynı ad |
| Parametreler | `cta_id`, `cta_variant`, `page_path` |
| GA4 admin | `cta_variant` custom dimension olarak tanımlanır |

`cta_variant` ton-yerleşim-çerçeve kodunu taşır (`t1-p1-f0`). Hangi kombinasyonun çalıştığı bu boyutla ayrışır; birden çok varyant aynı anda yayındaysa karşılaştırma buradan yapılır.

## Ölçüm sınırı

Event **butona tıklamayı** sayar. Google'ın onay ekranının tamamlanıp tamamlanmadığı ölçülemez, çünkü onay Google tarafında gerçekleşir ve siteye sinyal dönmez.

Raporlamada "kaç kişi tercih edilen kaynak olarak ekledi" **denmez**; "kaç kişi butona tıkladı" denir. Bu sınır müşteriye iletilen her çıktıda yazılır.
