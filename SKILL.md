---
name: preferred-source-butonu
description: Bir markanın blog veya haber sayfası için Google "tercih edilen kaynak" (preferred source) butonunu marka renklerine ve sayfa yapısına uygun bir kart içinde üretir. Markanın canlı sayfasını tarayıcıda ölçüp gerçek token'ları (zemin, metin rengi, içerik kolonu genişliği, tipografi, köşe yarıçapı, marka vurgusu) çıkarır; 3 ton x 3 yerleşim x 5 çerçeve efektini serbestçe eşleştirilebilir tek dosyalık bir HTML yapılandırıcıda sunar (Artifact aracı varsa yayınlanır, yoksa dosya olarak teslim edilir); seçim sonrası yalın HTML+CSS kod bloğu, GA4 takibi, yerleştirme notu ve QA listesi teslim eder. Bu skill'i şu durumlarda kullan - kullanıcı "preferred source butonu", "tercih edilen kaynak butonu", "Google tercih edilen kaynak", "preferred sources ekle", "şu markaya preferred source kartı yap" dediğinde; bir domain verip "Google'da tercih edilen kaynak olarak eklensin" istediğinde; mevcut bir preferred source kartını revize etmek istediğinde. Kullanıcı "buton" kelimesini kullanmasa bile Google preferred sources özelliğinden söz edip markaya uygulamak istiyorsa tetikle.
---

# Preferred Source Butonu

Google'ın 20 Ağustos 2026'da site sahiplerine açtığı **tercih edilen kaynak** butonunu, markanın kendi tasarım diline oturan bir kart içinde üretir.

Temel karar: **kart bizim, tıklama öğesi Google'ın.** Logo, marka rengi, Türkçe metin ve çerçeve efekti bizim kontrolümüzde; tıklanan öğe Google'ın resmî butonu. Böylece otomatik çeviri, kullanıcıyı kaldığı satıra döndürme ve Google'ın ileride ekleyeceği davranışlar bedava gelir.

Ayrıntılı dokümantasyon: `references/google-preferred-sources.md`

## Akış

Beş aşama sırayla işletilir. Aşama 0 geçilmeden kod üretilmez.

### Aşama 0 · Uygunluk ön kontrolü

`https://www.google.com/preferences/source?q=<domain>` adresinde marka listede mi bakılır.

- **Bu adım manuel.** Sayfa Google hesabıyla giriş ister; otomatikleştirilemez ve skill giriş yapmaz. Kullanıcıdan kontrol etmesi istenir.
- Google **yalnız domain ve subdomain** seviyesini kabul eder. `site.com` ve `blog.site.com` uygun; `site.com/blog` **uygun değil**.
- Marka listede değilse akış burada durur ve kullanıcıya bildirilir. Çalışmayan buton yayına alınmaz.

### Aşama 1 · Canlı marka denetimi

Markanın **gerçek bir yazı sayfası** tarayıcıda açılır (anasayfa değil, yazı detayı). `scripts/inspect_brand.js` içeriği `javascript_tool` ile çalıştırılır; tek çağrıda token JSON'u döner.

Ölçülenler: gövde zemini ve metin rengi, içerik kolonu genişliği, paragraf font-family/size/line-height, başlık renkleri ve ölçüleri, mevcut kart ve buton köşe yarıçapı, sayfadaki baskın marka renkleri, koyu tema desteği, logo adresi.

Kurallar:
- Viewport **1440px veya üzerine sabitlenir**; ölçümden önce `resize_window` çağrılır. Dar pane'de içerik kolonu yanlış okunur.
- Çerez bandı varsa **reddedilir** (kabul edilmez), sonra ölçülür.
- **Logo seçimi:** header'daki lockup çoğu markada kendi zemin plakasını taşır. Kurumsal sembol (şeffaf, kare) varsa o tercih edilir; kartın her tonunda çalışır ve büyütülebilir.

### Aşama 2 · Ton, yerleşim, çerçeve üretimi

Ölçülen token'lardan 3 ton, 3 yerleşim ve 5 çerçeve türetilir. Üçü **bağımsız eksendir**, 45 kombinasyon serbestçe eşleşir. Tam spesifikasyon: `references/ton-yerlesim-cerceve.md`

Her tonun metin/zemin kontrastı `scripts/contrast.py` ile hesaplanır; WCAG AA (4.5:1) altındaysa ton otomatik düzeltilir.

### Aşama 3 · Yapılandırıcı

`scripts/build_button.py` token JSON'undan **tek dosyalık, kendi kendine yeten bir HTML** üretir: ton, yerleşim, çerçeve, cihaz ve `data-theme` seçicileri; markanın kendi tipografisiyle kurulmuş sahte yazı sayfası içinde canlı önizleme; anında güncellenen kod bloğu ve kontrast uyarısı.

**Çıktı her ortamda çalışır.** Dosya tarayıcıda doğrudan açılır; harici bağımlılığı yoktur (logo `data:` URI, JS ve CSS gömülü). Tek dış istek Google Fonts'tur ve erişilemezse sistem fontuna düşer, yapılandırıcı çalışmaya devam eder.

**Yayınlama isteğe bağlıdır.** Artifact aracı varsa (Claude Code) dosya artifact olarak yayınlanıp bağlantı paylaşılabilir. Araç yoksa (Cursor, başka bir IDE, düz terminal) **akış değişmez**: aynı HTML dosyası teslim edilir, kullanıcı tarayıcıda açar ve seçimini yapar. Artifact bir gereklilik değil, bir kolaylıktır.

Yayınlamadan veya teslim etmeden önce **45 kombinasyon taranır** (bkz. `references/qa-checklist.md`). Taşma, buton dokunma alanı ve yatay kaydırma sıfır olmalıdır.

### Aşama 4 · Teslim

Kullanıcı seçimini yaptıktan sonra dört parça verilir:

1. **Yalın HTML + CSS kod bloğu.** Yorum satırı yok, açıklama yok. Logo markanın kendi CDN adresinden çekilir, base64 gömülmez.
2. **GA4 takibi.** `references/ga4-tracking.md`
3. **Yerleştirme ve CMS notu.** Hangi şablona, gövdenin neresine; script'in sayfa başına bir kez yükleneceği.
4. **QA kontrol listesi.** `references/qa-checklist.md`

## Değişmez kurallar

- **Kod yalın olur.** Üretilen HTML, CSS ve JS'te `<!-- -->` yorumu bulunmaz. Açıklama koda değil, sohbete veya not bölümüne yazılır.
- **Logo dış adresten çekilir.** Üretim kodunda `data:` URI kullanılmaz; yalnız artifact önizlemesinde gömülür.
- **Butona sabit `min-height:44px`** verilir. Script geç yüklendiğinde sayfa zıplamaz ve dokunma alanı korunur.
- **`data-lang="tr"`** ile dil sabitlenir.
- **Hareket kısıtı:** çerçeve efektlerine `@media (prefers-reduced-motion:reduce)` ile durdurma eklenir.
- **Ölçüm dürüstlüğü:** Google'ın butonu bir iframe'dir. Görüntülenme güvenilir ölçülür, tıklama yalnız yaklaşık; ekleme sayısı hiç ölçülemez. Raporda "kaç kişi ekledi" denmez.
- **`data-theme` varsayımı yazılır.** Değerin anlamı Google dokümanında net değil; karta göre zıt değer öntanımlı verilir ve QA'da canlı doğrulama istenir.

## Marka dili

Çıktı Türkçe. Müşteriye giden metinlerde `icerik-dili-rehberi` kuralları geçerlidir: em dash yok, emoji yok, CSS `text-transform:uppercase` ile Türkçe etiket üretilmez (İ tuzağı), etiketler kaynakta doğru harflenir.
