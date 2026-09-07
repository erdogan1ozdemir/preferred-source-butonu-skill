# GA4 takibi

Buton, alan adı dışına giden bir bağlantıdır. Bu yüzden **hiçbir kod eklenmeden ölçülebilir.** Üç seviye vardır; yukarıdan aşağı iş yükü artar, kazanç azalır.

| Seviye | Ne gerekir | Ne verir |
|---|---|---|
| 0 · Kod yok | GA4 Gelişmiş Ölçüm açık olsun | Tıklama sayısı, sayfa kırılımı |
| 1 · GTM trigger | GTM'de trigger + tag | Kendi olay adı, özel parametreler |
| 2 · Script | Şablona kod | `dataLayer` olayı, diğer araçlara açık |

## Seviye 0 · Hiç kod eklemeden

GA4'ün **Gelişmiş Ölçüm** özelliğindeki *giden bağlantı tıklamaları* varsayılan olarak açıktır ve alan adı dışına giden her tıklamayı otomatik `click` olayı olarak kaydeder. Buton `google.com` adresine gittiğinden bu kapsama girer.

Otomatik gelen parametreler:

| Parametre | Değer |
|---|---|
| `link_url` | `https://www.google.com/preferences/source?q=<domain>` |
| `link_domain` | `www.google.com` |
| `link_id` | `preferred-source-link` |
| `link_classes` | `tcps__btn tcps__btn--light` |
| `outbound` | `true` |

Butona bu nedenle `id="preferred-source-link"` verilir; GA4'te filtreleme bu kimlikle yapılır.

**Raporda görmek için:** Keşif (Exploration) oluşturulur, boyut olarak `Link ID` veya `Link URL`, metrik olarak `Olay sayısı` seçilir; `Olay adı = click` ve `Link ID = preferred-source-link` filtresi uygulanır. Sayfa kırılımı için `Sayfa yolu` boyutu eklenir.

**Kontrol edilmesi gerekenler:**

- GA4 yönetiminde ilgili veri akışında **Gelişmiş Ölçüm > Giden bağlantı tıklamaları** açık mı.
- Rıza yönetimi (consent) tıklamayı engelliyor mu.
- Bu seviyede kart varyantı (`t1-p1-f1`) ayırt edilemez. Tek varyant yayınlanacaksa sorun değildir; iki varyant karşılaştırılacaksa Seviye 1 veya 2 gerekir.

## Seviye 1 · GTM trigger, yine kod yok

Kendi olay adı ve `cta_variant` gibi özel parametreler isteniyorsa GTM arayüzünden kurulur, şablona dokunulmaz.

| Katman | Ayar |
|---|---|
| Yerleşik değişken | `Click Element` açık olmalı |
| Trigger | Click - Just Links · Some Link Clicks |
| Koşul | `Click Element` matches CSS selector `#preferred-source-link, #preferred-source-link *` |
| Tag | GA4 Event · `preferred_source_click` · `cta_id`, `cta_variant`, `page_path` |

Seçicideki `, #preferred-source-link *` bölümü zorunludur: buton içinde Google logosu satır içi SVG olarak durur, logoya yapılan tıklamada tıklanan öğe `<a>` değil `<svg>` olur.

## Seviye 2 · Şablona script

`dataLayer` olayının başka araçlar tarafından da kullanılması isteniyorsa eklenir. Kart işaretlemesinin hemen ardına, aynı şablon dosyasına konur.

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

### Görüntülenme (isteğe bağlı)

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

### GTM tarafı

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
