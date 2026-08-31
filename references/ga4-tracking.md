# GA4 takibi

## Önce bu: takip zorunlu değil

Buton, hiçbir ölçüm kodu eklenmeden çalışır. GA4 yalnız "bu kart işe yarıyor mu" sorusuna cevap almak isteniyorsa eklenir.

## Ölçülen gerçek: buton cross-origin iframe

`publisher.js` butonu satır içi DOM olarak değil **iframe** olarak basar. Yerel testte doğrulandı (localhost üzerinden, gerçek script yüklenerek):

```
iframe src : https://news.google.com/swg/ui/v1/addpreferredsourcebuttoniframe?...&hl=tr&theme=light
title      : Add Preferred Source
ölçü       : 866x60 (konteyner genişliğine göre değişir)
aynı köken : HAYIR (cross-origin)
```

**Bunun sonucu kesindir:** kart sarmalayıcısına verilen `id` üzerinden kurulan klasik tıklama kuralı bu butonda çalışmaz. Ne `addEventListener("click")` ne GTM'in otomatik tıklama dinleyicisi tıklamayı görür, çünkü farklı alan adındaki bir iframe'in içindeki tıklama ana dokümana **hiç ulaşmaz**. Bu bir GTM veya GA4 yapılandırma konusu değil, tarayıcının aynı köken politikasıdır. Kuralı GA4'te tanımlamak sonucu değiştirmez.

## Ama kapalı bir kapı değil: mesaj kanalı

iframe ana sayfayla `postMessage` üzerinden haberleşir. Yerel testte sayfa yüklenirken **8 mesaj** ölçüldü; hepsi `https://news.google.com` kökenli ve `__ACTIVITIES__` sentinel protokolünü kullanıyor (`connect`, `ready` gibi komutlar).

`publisher.js` içinde şu olay adları tanımlıdır:

| Sabit | Anlamı |
|---|---|
| `IMPRESSION_ADD_PREFERRED_SOURCES_BUTTON` | Buton görüntülendi |
| `ACTION_ADD_PREFERRED_SOURCES_BUTTON_CLICK` | **Butona tıklandı** |
| `EVENT_ADD_PREFERRED_SOURCE_SUCCESS` | **Ekleme başarılı** |
| `EVENT_ADD_PREFERRED_SOURCE_FAILURE` | Ekleme başarısız |
| `EVENT_PREFERRED_SOURCE_ALREADY_ADDED` | Kaynak zaten ekli |
| `AddPreferredSourceResponse.getStatus()` | Sonuç durumu iframe'den parent'a döner |

**DOĞRULANMAMIŞ NOKTA:** bu olayların ana sayfaya iletilip iletilmediği, yoksa yalnız Google'ın kendi ölçümüne mi gittiği test edilmedi. Doğrulamak için butona gerçekten tıklanması ve Google hesabıyla akışın tamamlanması gerekir. Bu adım marka tarafında, test ortamında yapılmalıdır.

## Doğrulama adımı (kurulumdan önce)

Test ortamına aşağıdaki dinleyici konur, butona tıklanır ve konsola ne düştüğüne bakılır.

```html
<script>
window.addEventListener("message", function(e){
  if (e.origin !== "https://news.google.com") return;
  var d = e.data;
  if (!d || d.sentinel !== "__ACTIVITIES__") return;
  console.log("[preferred-source]", d.cmd, d.payload);
});
</script>
```

- **Tıklama veya sonuç bilgisi düşüyorsa:** ilgili `cmd` / `payload` deseni `dataLayer.push` ile GA4'e bağlanır. Tıklama ve ekleme sonucu **net** ölçülür.
- **Yalnız `connect` / `ready` düşüyorsa:** kanal yalnız kurulum içindir. O durumda aşağıdaki iki katman kullanılır.

## Katman 1 · Görüntülenme (her koşulda güvenilir)

iframe'den bağımsızdır.

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

## Katman 2 · Tıklama (mesaj kanalı çalışmıyorsa, yaklaşık)

Kullanıcı iframe'e tıkladığında ana pencere odağı kaybeder.

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

`olcum: "yaklasik"` bilinçlidir; raporda bu sayının kesin olmadığı buradan görünür. Dokunmatik cihazda `mouseenter` çalışmaz, mobil tıklamalar eksik sayılır.

## GTM kurulumu

Kod `dataLayer`'a yazar. Site GTM yerine doğrudan `gtag.js` kullanıyorsa `dataLayer.push(...)` satırları `gtag('event', ...)` ile değiştirilir.

| Katman | Ayar |
|---|---|
| Trigger | Custom Event · `preferred_source_view`, `preferred_source_click` |
| Tag | GA4 Event, aynı ad |
| Parametreler | `cta_id`, `cta_variant`, `page_path`, `olcum` |
| GA4 admin | `cta_variant` ve `olcum` custom dimension olarak tanımlanır |

## Nereye konur

Script kart parçasının hemen ardına, aynı şablon dosyasına konur. `psSeen` / `psBound` bayrakları şablon birden çok kez çalışırsa event'in ikilenmesini engeller.

## Raporlama dili

- **Görüntülenme** net bildirilir.
- **Tıklama**, mesaj kanalı doğrulanmadıysa "yaklaşık" ibaresiyle bildirilir.
- **Ekleme sayısı**, mesaj kanalı doğrulanana kadar hiç bildirilmez.
