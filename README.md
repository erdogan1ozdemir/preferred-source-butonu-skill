# preferred-source-butonu

Claude Code skill'i. Bir markanın blog veya haber sayfası için Google **tercih edilen kaynak** (preferred source) butonunu, markanın kendi tasarım diline oturan bir kart içinde üretir.

Google özelliği site sahiplerine 20 Ağustos 2026'da açtı. Okuyucu butona basıyor, açılan Google ekranından onaylıyor, kaldığı satıra dönüyor; sonrasında markayı Top Stories'de ve AI Mode cevaplarında tercih edilen rozetiyle görüyor.

## Temel karar

**Kart bizim, tıklama öğesi Google'ın.** Logo, marka rengi, Türkçe metin ve çerçeve efekti bizde; tıklanan öğe Google'ın resmî butonu (`publisher.js` + `google-add-preferred-source-btn`). Böylece otomatik çeviri, kaldığı satıra dönüş ve Google'ın ileride ekleyeceği davranışlar bedava geliyor.

Bunun bedeli açıkça yazılır: üç ton **kartı** değiştirir, Google'ın butonunu değiştirmez.

## Akış

| Aşama | İş |
|---|---|
| 0 | Uygunluk ön kontrolü (manuel, Google girişi ister) |
| 1 | Canlı marka denetimi · `getComputedStyle` ile gerçek token'lar |
| 2 | Markaya sunum dokümanı · Word veya HTML, süreci ve gerekçeyi anlatır, örnek içerir |
| 3 | 3 ton x 3 yerleşim x 5 çerçeve üretimi, WCAG AA düzeltmesi |
| 4 | Tek dosyalık HTML yapılandırıcı · 45 kombinasyon serbest eşleşir |
| 5 | Yalın kod + GA4 + yerleştirme notu + QA listesi |

## Eksenler

**Ton:** koyu kontrast · marka tinti · minimal çerçeve
**Yerleşim:** tam genişlik banner · kompakt şerit · yazı sonu kutusu
**Çerçeve:** sade · conic kenarlık · gökkuşağı kenarlık · pulse glow · geniş hale

Üçü bağımsızdır ve serbestçe mixlenir. Sade seçim gerçekten sade kod üretir: `f0` seçiliyken çıktıda `conic`, `animation`, `@property`, `mask` ve `tcps-wrap` hiç bulunmaz.

## Dosyalar

```
SKILL.md
references/
  google-preferred-sources.md   resmî dokümantasyon, uygunluk, data-theme belirsizliği
  ton-yerlesim-cerceve.md       45 kombinasyonun tam spesifikasyonu
  ga4-tracking.md               event, GTM kurulumu, ölçüm sınırı
  qa-checklist.md               otomatik tarama eşikleri ve bilinen tuzaklar
scripts/
  inspect_brand.js              tarayıcıda çalışan token çıkarıcı
  contrast.py                   WCAG hesabı ve otomatik ton düzeltmesi
  build_button.py               config -> doküman ve yapılandırıcı, statik doğrulamalı
  brand_doc_template.html       markaya sunum dokümanı (HTML)
  build_brand_docx.js           markaya sunum dokümanı (Word / Google Docs)
  configurator_template.html    yapılandırıcı şablonu
examples/
  turkcell-config.json
  Turkcell-Tercih-Edilen-Kaynak-Butonu.docx  markaya sunum dokümanı (Word)
  turkcell-preferred-source-doc.html   markaya sunum dokümanı (HTML)
  kart-ornek.png                       üç ton render'ı
  turkcell-preferred-source.html       yapılandırıcı
  tc-corp.png
```

## Turkcell pilotu

`turkcell.com.tr/blog/fps-nedir` üzerinde ölçüldü: içerik kolonu 846px, paragraf `#5F6B76` 17.6/31.68, başlık `#253342`, marka lacivert `#164193`, marka sarı `#EFE700`, köşe yarıçapı 12px, font greycliff.

Doğrulama: 90 kombinasyon (45 x 2 cihaz) tarandı; taşma 0, buton yüksekliği 44px, yatay kaydırma 0. Kontrast koyu tonda 9.5:1, tint tonda 12.3:1.

`build_button.py`, `turkcell-config.json`'dan yapılandırıcıyı **birebir** yeniden üretir (bayt eşitliği doğrulandı).

## Kurulum

```bash
git clone https://github.com/erdogan1ozdemir/preferred-source-butonu-skill.git ~/.claude/skills/preferred-source-butonu
```

## Ortam bağımsızlığı

Yapılandırıcı **tek dosyalık, kendi kendine yeten bir HTML**tir. Tarayıcıda doğrudan açılır; logo `data:` URI olarak gömülüdür, JS ve CSS dosyanın içindedir. Tek dış istek Google Fonts'tur ve erişilemezse sistem fontuna düşer.

Bu yüzden skill **Artifact aracına bağımlı değildir**. Claude Code'da dosya artifact olarak yayınlanıp bağlantı paylaşılabilir; Cursor'da, başka bir IDE'de veya düz terminalde ise aynı dosya doğrudan teslim edilir ve tarayıcıda açılır. Akış ve çıktı iki durumda da aynıdır.

## Bilinen sınırlar

- **Uygunluk kontrolü otomatikleştirilemiyor.** `google.com/preferences/source` Google hesabı girişi ister; skill giriş yapmaz.
- **`data-theme` anlamı dokümanda net değil.** Karta göre zıt değer öntanımlı verilir, QA'da canlı doğrulama istenir.
- **Google'ın butonu cross-origin iframe olarak basılır** (`news.google.com`), bu yüzden `id` bazlı klasik tıklama kuralı çalışmaz. Buton ana sayfayla `postMessage` üzerinden haberleşiyor ve script'inde tıklama ile ekleme sonucu olayları tanımlı; bunların parent'a iletilip iletilmediği test ortamında doğrulanmalıdır.
- **Artifact önizlemesinde Google butonu temsilidir.** Artifact CSP'si dış script'e izin vermez.
