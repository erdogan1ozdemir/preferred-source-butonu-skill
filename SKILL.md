---
name: preferred-source-butonu
description: Bir markanın blog veya haber sayfası için Google "tercih edilen kaynak" (preferred source) butonunu marka renklerine ve sayfa yapısına uygun bir kart içinde üretir. Markanın canlı sayfasını tarayıcıda ölçüp gerçek token'ları (zemin, metin rengi, içerik kolonu genişliği, tipografi, köşe yarıçapı, marka vurgusu) çıkarır; 3 ton x 3 yerleşim x 5 çerçeve efektini serbestçe eşleştirilebilir tek dosyalık bir HTML yapılandırıcıda sunar (Artifact aracı varsa yayınlanır, yoksa dosya olarak teslim edilir); seçim sonrası yalın HTML+CSS kod bloğu, GA4 takibi, yerleştirme notu ve QA listesi teslim eder. Bu skill'i şu durumlarda kullan - kullanıcı "preferred source butonu", "tercih edilen kaynak butonu", "Google tercih edilen kaynak", "preferred sources ekle", "şu markaya preferred source kartı yap" dediğinde; bir domain verip "Google'da tercih edilen kaynak olarak eklensin" istediğinde; mevcut bir preferred source kartını revize etmek istediğinde. Kullanıcı "buton" kelimesini kullanmasa bile Google preferred sources özelliğinden söz edip markaya uygulamak istiyorsa tetikle.
---

# Preferred Source Butonu

Google'ın 20 Ağustos 2026'da site sahiplerine açtığı **tercih edilen kaynak** butonunu, markanın kendi tasarım diline oturan bir kart içinde üretir.

Temel karar: **kart da buton da yayıncınındır.** Buton, Google'ın tercihler ekranına giden kendi bağlantımızdır (`google.com/preferences/source?q=<domain>`), yeni sekmede açılır. Google'ın gömme butonu kullanılmaz.

Gerekçe **ölçüm**: gömme butonu cross-origin bir iframe olduğu için tıklaması hiçbir yöntemle net ölçülemez. Kendi bağlantımızda tıklama sayfada gerçekleşir ve GA4'e doğrudan yazılır. Bedeli, Google'ın otomatik dil çevirisinden vazgeçmektir; metin Türkçe olarak sabit verilir. Karşılaştırma tablosu: `references/google-preferred-sources.md`

Ayrıntılı dokümantasyon: `references/google-preferred-sources.md`

## Akış

Altı aşama sırayla işletilir. Aşama 0 geçilmeden kod üretilmez, Aşama 2 paylaşılmadan varyant üretilmez.

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

### Aşama 2 · Markaya sunum dokümanı

Varyantlardan **önce**, süreci markaya anlatan bir doküman üretilir. İki biçim vardır:

- **Word / Google Docs (varsayılan):** `node scripts/build_brand_docx.js` · markanın kendi ekibinde dolaşacak, yorumlanacak ve düzenlenecek doküman için. `docx` npm paketi gerekir.
- **HTML:** `python3 scripts/build_button.py config.json dokuman.html --doc` · bağlantı olarak paylaşılacaksa.

Bu doküman "şu butonu ekleyelim" demez; **neden** eklendiğini ve markanın ne kazanacağını anlatır. Yedi bölüm:

| Bölüm | İçerik |
|---|---|
| 01 Ne değişti | Google'ın 20 Ağustos 2026'da açtığı yetki, eskisinden farkı |
| 02 Okuyucu tarafında nasıl işliyor | Üç adımlık akış: görür, yeni sekmede onaylar, sonraki aramalarında görür |
| 03 Marka için ne ifade ediyor | Sadık okuyucu bağı, AI cevaplarında görünürlük, erken konumlanma, düşük uygulama maliyeti |
| 04 Uygunluk koşulu | Domain / subdomain / alt dizin tablosu, markanın kendi durumu |
| 05 Örnek | Markanın ölçülen değerleriyle kurulmuş **canlı kart**, yazı akışı içinde |
| 06 Teslim kapsamı | Hangi parçaların verileceği |
| 07 Ölçüm ve sınırlar | Neyin ölçülebildiği, neyin ölçülemediği |

**Örnek bölümü zorunludur.** Marka kartı yazıda göreceği biçimde görmeden karar veremez. HTML biçiminde kart canlı basılır; Word biçiminde üç ton tarayıcıda render edilip PNG olarak gömülür.

**Kart render tuzağı:** üç varyant tek sayfada gösterilirken her biri ayrı sınıfa alınmalıdır. Üçü de `.tcps` seçicisini kullanırsa son `<style>` bloğu diğerlerini ezer ve üç kart aynı görünür.

**Dil rejimi [A] kurumsal.** `icerik-dili-rehberi` kuralları bağlayıcıdır: em dash yok, emoji yok, kesin vaat yok, pasif ton, CSS `text-transform:uppercase` ile Türkçe etiket üretilmez. Logo bandı zorunludur: marka logosu solda, Inbound logosu sağda, ikisi de `data:` URI olarak gömülü.

**Kaynaksız istatistik yazılmaz.** Dolaşımdaki "iki kat tıklama" ve "600.000 kaynak seçildi" gibi sayılar Google'ın resmî dokümantasyonunda doğrulanamadı; doğrulanabilir bir kaynak bulunmadıkça dokümana girmez.

### Aşama 3 · Ton, yerleşim, çerçeve üretimi

Ölçülen token'lardan 3 ton, 3 yerleşim ve 5 çerçeve türetilir. Üçü **bağımsız eksendir**, 45 kombinasyon serbestçe eşleşir. Tam spesifikasyon: `references/ton-yerlesim-cerceve.md`

Her tonun metin/zemin kontrastı `scripts/contrast.py` ile hesaplanır; WCAG AA (4.5:1) altındaysa ton otomatik düzeltilir.

### Aşama 4 · Yapılandırıcı

`scripts/build_button.py` token JSON'undan **tek dosyalık, kendi kendine yeten bir HTML** üretir: ton, yerleşim, çerçeve, cihaz ve `data-theme` seçicileri; markanın kendi tipografisiyle kurulmuş sahte yazı sayfası içinde canlı önizleme; anında güncellenen kod bloğu ve kontrast uyarısı.

**Çıktı her ortamda çalışır.** Dosya tarayıcıda doğrudan açılır; harici bağımlılığı yoktur (logo `data:` URI, JS ve CSS gömülü). Tek dış istek Google Fonts'tur ve erişilemezse sistem fontuna düşer, yapılandırıcı çalışmaya devam eder.

**Yayınlama isteğe bağlıdır.** Artifact aracı varsa (Claude Code) dosya artifact olarak yayınlanıp bağlantı paylaşılabilir. Araç yoksa (Cursor, başka bir IDE, düz terminal) **akış değişmez**: aynı HTML dosyası teslim edilir, kullanıcı tarayıcıda açar ve seçimini yapar. Artifact bir gereklilik değil, bir kolaylıktır.

Yayınlamadan veya teslim etmeden önce **45 kombinasyon taranır** (bkz. `references/qa-checklist.md`). Taşma, buton dokunma alanı ve yatay kaydırma sıfır olmalıdır.

### Aşama 5 · Teslim

İki doküman üretilir, alıcıları farklıdır. **Uzun doküman markayı bilgilendirir, IT dokümanı işi yaptırır.** Biri diğerinin yerini tutmaz; IT ekibine uzun doküman gönderilmez.

| Doküman | Alıcı | Üretim |
|---|---|---|
| Markaya sunum dokümanı | marka, pazarlama | `node scripts/build_brand_docx.js` |
| IT talep dokümanı | geliştirici ekip | `python3 scripts/build_it_talep.py` |

**IT talep dokümanı** `turkcell-talep-skilli` biçimini taşır: numaralı maddeler, her maddede Mevcut durum -> Talep edilen değişiklik -> Örnek, kopyalanabilir kod. Kapak süsü, "Hazırlayan" satırı ve dokümanın kendini anlattığı cümle bulunmaz. Teslim kontrolü o skill'in `references/teslim-kontrolu.md` listesiyle programatik çalıştırılır; kod satırları 85 karakteri aşmaz.



Kullanıcı seçimini yaptıktan sonra dört parça verilir:

1. **Yalın HTML + CSS kod bloğu.** Yorum satırı yok, açıklama yok. Logo markanın kendi CDN adresinden çekilir, base64 gömülmez.
2. **GA4 takibi.** `references/ga4-tracking.md`
3. **Yerleştirme ve CMS notu.** Hangi şablona, gövdenin neresine; script'in sayfa başına bir kez yükleneceği.
4. **QA kontrol listesi.** `references/qa-checklist.md`

## Değişmez kurallar

- **Doküman varyantlardan önce gelir.** Marka süreci anlamadan tasarım seçimi yapmaz.
- **Kod yalın olur.** Üretilen HTML, CSS ve JS'te `<!-- -->` yorumu bulunmaz. Açıklama koda değil, sohbete veya not bölümüne yazılır.
- **Logo dış adresten çekilir.** Üretim kodunda `data:` URI kullanılmaz; yalnız artifact önizlemesinde gömülür.
- **Butona sabit `min-height:44px`** verilir. Script geç yüklendiğinde sayfa zıplamaz ve dokunma alanı korunur.
- **Hareket kısıtı:** çerçeve efektlerine `@media (prefers-reduced-motion:reduce)` ile durdurma eklenir.
- **Ölçüm dürüstlüğü:** tıklama net ölçülür. Okuyucunun Google ekranında onayı tamamlayıp tamamlamadığı ölçülemez; raporda "kaç kişi tıkladı" denir, "kaç kişi ekledi" denmez.
- **Alan adı `q` parametresiyle verilir.** Yalnız domain veya subdomain yazılır, alt dizin yazılmaz.
- **Buton yeni sekmede açılır** (`target="_blank" rel="noopener noreferrer"`); okuyucu yazıdan ayrılmaz.

## Marka dili

Çıktı Türkçe. Müşteriye giden metinlerde `icerik-dili-rehberi` kuralları geçerlidir: em dash yok, emoji yok, CSS `text-transform:uppercase` ile Türkçe etiket üretilmez (İ tuzağı), etiketler kaynakta doğru harflenir.
