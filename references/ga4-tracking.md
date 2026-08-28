# GA4 takibi

## Önce bu: takip zorunlu değil

Buton, hiçbir ölçüm kodu eklenmeden çalışır. GA4 yalnız "bu kart işe yarıyor mu" sorusuna cevap almak isteniyorsa eklenir. İstenmiyorsa bu dosya atlanır.

## Ölçülen gerçek: buton bir iframe

`publisher.js` butonu satır içi DOM olarak değil, **`<iframe title="Add Preferred Source">`** olarak basar (ölçüldü: tek çocuk düğüm `IFRAME`, shadow DOM yok, öntanımlı 540x60px).

Bunun sonucu: **iframe içindeki tıklama ana dokümana çıkmaz.** Sarmalayıcı karta bağlanan `click` dinleyicisi de, GTM'in kendi otomatik tıklama dinleyicisi de butona yapılan tıklamayı görmeyebilir.

Bu yüzden ölçüm iki katmana ayrılır: **görüntülenme güvenilirdir, tıklama değildir.**

## Katman 1 · Görüntülenme (güvenilir)

Kartın ekranda gerçekten görüldüğünü sayar. iframe'den bağımsızdır, her koşulda çalışır.

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
        cta_variant: "t1-p1-f0",
        page_path: location.pathname
      });
    });
  }, {threshold: 0.5}).observe(el);
})();
</script>
```

## Katman 2 · Tıklama (yaklaşık, staging'de doğrulanır)

Önce **staging'de** şu denenir: sarmalayıcıya `click` dinleyicisi bağlanır, butona tıklanır, `dataLayer`'a event düşüyor mu bakılır.

- **Düşüyorsa** basit dinleyici yeterlidir.
- **Düşmüyorsa** (beklenen durum) iframe'e odak geçişi ölçülür: kullanıcı iframe'e tıkladığında ana pencere odağı kaybeder.

```html
<script>
(function(){
  var el = document.getElementById("preferred-source-button");
  if(!el || el.dataset.psBound) return;
  el.dataset.psBound = "1";
  var uzerinde = false;
  el.addEventListener("mouseenter", function(){ uzerinde = true; });
  el.addEventListener("mouseleave", function(){ uzerinde = false; });
  window.addEventListener("blur", function(){
    if(!uzerinde || el.dataset.psClicked) return;
    if(document.activeElement !== el.querySelector("iframe")) return;
    el.dataset.psClicked = "1";
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
      event: "preferred_source_click",
      cta_id: "preferred-source-button",
      cta_variant: "t1-p1-f0",
      page_path: location.pathname,
      olcum: "yaklasik"
    });
  });
})();
</script>
```

`olcum: "yaklasik"` parametresi bilinçlidir; raporda bu sayının kesin olmadığı buradan görünür. Dokunmatik cihazda `mouseenter` çalışmaz, bu yüzden mobil tıklamalar eksik sayılır.

## GTM kurulumu

Kod `dataLayer`'a yazar, yani sitede GTM olmalıdır. Site GTM yerine doğrudan `gtag.js` kullanıyorsa `dataLayer.push(...)` satırları `gtag('event','preferred_source_view',{...})` ile değiştirilir.

| Katman | Ayar |
|---|---|
| Trigger | Custom Event, `preferred_source_view` (ve varsa `preferred_source_click`) |
| Tag | GA4 Event, aynı ad |
| Parametreler | `cta_id`, `cta_variant`, `page_path`, `olcum` |
| GA4 admin | `cta_variant` ve `olcum` custom dimension olarak tanımlanır |

`cta_variant` ton-yerleşim-çerçeve kodunu taşır (`t1-p1-f0`); birden çok varyant yayındaysa karşılaştırma bu boyutla yapılır.

## Nereye konur

Script kart parçasının hemen ardına, aynı şablon dosyasına konur. `psSeen` / `psBound` bayrakları şablon birden çok kez çalışırsa event'in ikilenmesini engeller.

## Raporlama dili

- **Görüntülenme** net bildirilir: "kart X kez görüntülendi".
- **Tıklama** yaklaşık bildirilir: "yaklaşık X tıklama". Kesin sayı gibi sunulmaz.
- **Ekleme sayısı hiç bildirilmez.** Onay Google tarafında gerçekleşir, siteye sinyal dönmez. "Kaç kişi tercih edilen kaynak olarak ekledi" sorusu bu kurulumla cevaplanamaz.
