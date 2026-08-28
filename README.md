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
| 2 | 3 ton x 3 yerleşim x 4 çerçeve üretimi, WCAG AA düzeltmesi |
| 3 | Artifact yapılandırıcı · 36 kombinasyon serbest eşleşir |
| 4 | Yalın kod + GA4 + yerleştirme notu + QA listesi |

## Eksenler

**Ton:** koyu kontrast · marka tinti · minimal çerçeve
**Yerleşim:** tam genişlik banner · kompakt şerit · yazı sonu kutusu
**Çerçeve:** sade · conic glow · pulse glow · gökkuşağı conic

Üçü bağımsızdır ve serbestçe mixlenir. Sade seçim gerçekten sade kod üretir: `f0` seçiliyken çıktıda `conic`, `animation` ve `@property` hiç bulunmaz.

## Dosyalar

```
SKILL.md
references/
  google-preferred-sources.md   resmî dokümantasyon, uygunluk, data-theme belirsizliği
  ton-yerlesim-cerceve.md       36 kombinasyonun tam spesifikasyonu
  ga4-tracking.md               event, GTM kurulumu, ölçüm sınırı
  qa-checklist.md               otomatik tarama eşikleri ve bilinen tuzaklar
scripts/
  inspect_brand.js              tarayıcıda çalışan token çıkarıcı
  contrast.py                   WCAG hesabı ve otomatik ton düzeltmesi
  build_button.py               config -> yapılandırıcı, statik doğrulamalı
  configurator_template.html    yer tutuculu şablon
examples/
  turkcell-config.json
  turkcell-preferred-source.html
  tc-corp.png
```

## Turkcell pilotu

`turkcell.com.tr/blog/fps-nedir` üzerinde ölçüldü: içerik kolonu 846px, paragraf `#5F6B76` 17.6/31.68, başlık `#253342`, marka lacivert `#164193`, marka sarı `#EFE700`, köşe yarıçapı 12px, font greycliff.

Doğrulama: 72 kombinasyon (36 x 2 cihaz) tarandı; taşma 0, buton yüksekliği 44px, yatay kaydırma 0. Kontrast koyu tonda 9.5:1, tint tonda 12.3:1.

`build_button.py`, `turkcell-config.json`'dan yapılandırıcıyı **birebir** yeniden üretir (bayt eşitliği doğrulandı).

## Kurulum

```bash
git clone https://github.com/erdogan1ozdemir/preferred-source-butonu-skill.git ~/.claude/skills/preferred-source-butonu
```

## Bilinen sınırlar

- **Uygunluk kontrolü otomatikleştirilemiyor.** `google.com/preferences/source` Google hesabı girişi ister; skill giriş yapmaz.
- **`data-theme` anlamı dokümanda net değil.** Karta göre zıt değer öntanımlı verilir, QA'da canlı doğrulama istenir.
- **GA4 tıklamayı sayar, eklemeyi değil.** Onay Google tarafında gerçekleşir ve siteye sinyal dönmez.
- **Artifact önizlemesinde Google butonu temsilidir.** Artifact CSP'si dış script'e izin vermez.
