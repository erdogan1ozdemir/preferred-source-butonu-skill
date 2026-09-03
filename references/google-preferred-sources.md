# Google Preferred Sources · uygulama notları

Kaynak: https://developers.google.com/search/docs/appearance/preferred-sources

Okuyucu, arama sonuçlarında öne çıkmasını istediği kaynakları seçebilir. Seçilen kaynaklar AI Overviews ve AI Mode yanıtlarında Preferred etiketiyle işaretlenir.

## Kullanılan yöntem: deeplink

Buton yayıncının kendi bağlantısıdır.

```html
<a href="https://www.google.com/preferences/source?q=example.com"
   target="_blank" rel="noopener noreferrer">Tercih edilen kaynak olarak ekle</a>
```

Alan adı `q` parametresiyle **açıkça verilir**. Google'ın tercihler ekranı yeni sekmede açılır, okuyucu yazının bulunduğu sekmeden ayrılmaz.

**Neden bu yöntem seçildi:** tıklama sayfada gerçekleşir, bu yüzden GA4 ile **net ölçülür**. Karar gerekçesi `ga4-tracking.md` içindedir.

## Alternatif: Google'ın gömme butonu

```html
<div google-add-preferred-source-btn data-theme="dark" data-lang="tr"></div>
<script async src="https://news.google.com/swg/js/v1/publisher.js"></script>
```

Bu yöntem varsayılan değildir. Karşılaştırma:

| | Deeplink (kullanılan) | Gömme butonu |
|---|---|---|
| Tıklama ölçümü | Net | Ölçülemez (cross-origin iframe) |
| Buton görünümü | Tamamen kontrol edilebilir | Google belirler |
| Dil | Elle verilir | Otomatik çevrilir |
| Dış script | Yok | `publisher.js` |
| Okuma akışı | Yeni sekme, yazı açık kalır | Onaydan sonra kaldığı satıra döner |
| Yerel test | Çalışır | Çalışmaz (400) |

Gömme butonuna dönülürse `ga4-tracking.md` içindeki iframe bölümü geçerli olur.

## Uygunluk

Yalnız **domain ve subdomain** seviyesi kabul edilir.

| Adres | Durum |
|---|---|
| `https://www.example.com/` | uygun |
| `https://blog.example.com/` | uygun |
| `https://www.example.com/blog` | uygun değil |

Kontrol adresi `https://www.google.com/preferences/source?q=<domain>` Google hesabıyla giriş ister. Skill giriş yapmaz; kontrol kullanıcıya bırakılır ve sonucu alınmadan kod üretilmez.

## Google'ın grafik varlıkları

Google, özel uygulamalar için çevrilmiş grafik varlıklar yayımlamaktadır. Buton kendi işaretlememizle üretildiği için, üzerindeki Google logosunun Google'ın kendi asset setinden alınması önerilir.

## Ölçülen davranış · gömme butonu

Aşağıdakiler yerel testte doğrulanmıştır ve alternatife dönülürse geçerlidir.

- Buton `<iframe src="https://news.google.com/swg/ui/v1/addpreferredsourcebuttoniframe?...">` olarak basılır, aynı köken değildir.
- Tıklandığında Google'a açılan istek **sayfanın kendi adresini** kaynak olarak gönderir (`source: location.href`). Bu yüzden `localhost` ve `file://` üzerinde tıklamak **400 Bad Request** döndürür; buton render olur, akış tamamlanamaz.
- iframe ana sayfayla `postMessage` üzerinden haberleşir (`__ACTIVITIES__` sentinel; `connect`, `ready`, `msg`).
- Script içinde `IMPRESSION_ADD_PREFERRED_SOURCES_BUTTON`, `ACTION_ADD_PREFERRED_SOURCES_BUTTON_CLICK`, `EVENT_ADD_PREFERRED_SOURCE_SUCCESS / FAILURE / ALREADY_ADDED` olayları tanımlıdır. Bunların ana sayfaya iletilip iletilmediği doğrulanmamıştır.
