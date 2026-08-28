# Google Preferred Sources · uygulama notları

Kaynak: https://developers.google.com/search/docs/appearance/preferred-sources
Özellik site sahiplerine 20 Ağustos 2026'da açıldı.

## Ne yapar

Okuyucu butona basar, açılan Google ekranından onaylar, kaldığı satıra geri döner. Sonrasında markayı Top Stories'de ve AI Mode cevaplarında tercih edilen rozetiyle görür.

## Resmî gömme (kullanılan yöntem)

```html
<div google-add-preferred-source-btn data-theme="dark" data-lang="tr"></div>
<script async src="https://news.google.com/swg/js/v1/publisher.js"></script>
```

- `data-theme`: `light` veya `dark`. Öntanımlı `light`.
- `data-lang`: tarayıcı dilini ezer. Türkçe için `tr`.
- Script **sayfa başına bir kez** yüklenir. Şablona konuyorsa kart parçasından çıkarılır.

## Deeplink (yedek yöntem)

```
https://www.google.com/preferences/source?q=example.com
```

JavaScript'siz uygulama için. Resmî butonun otomatik çeviri ve geri dönüş davranışını taşımaz; bu skill varsayılan olarak kullanmaz.

## Uygunluk

Yalnız **domain ve subdomain** seviyesi kabul edilir.

| Adres | Durum |
|---|---|
| `https://www.example.com/` | uygun |
| `https://blog.example.com/` | uygun |
| `https://www.example.com/blog` | uygun değil |

Kontrol adresi `https://www.google.com/preferences/source?q=<domain>` **Google hesabıyla giriş ister**. Skill giriş yapmaz; kontrol kullanıcıya bırakılır ve sonucu alınmadan kod üretilmez.

## Çözülmemiş nokta · data-theme

Dokümanda `data-theme` değerinin "butonun kendi görünümü" mü yoksa "içinde durduğu zemin" mi olduğu yazmıyor ve script yüklenmeden ayırt edilemiyor.

Skill'in varsayımı: değer **butonun kendi görünümünü** tanımlar. Bu yüzden karta göre **zıt** değer verilir.

| Kart tonu | Öntanımlı `data-theme` | Gerekçe |
|---|---|---|
| Koyu | `light` | Beyaz buton koyu kartta okunur |
| Açık | `dark` | Koyu buton açık kartta ayrışır |

Varsayım QA'da doğrulanır. Buton kartla aynı tona düşüyorsa değer çevrilir.

## Google'ın grafik varlıkları

Google, özel uygulamalar için çevrilmiş grafik varlıklar da yayımlıyor. Bu skill resmî gömmeyi kullandığı için onlara ihtiyaç duymaz; deeplink yedeğine geçilirse gerekir.
