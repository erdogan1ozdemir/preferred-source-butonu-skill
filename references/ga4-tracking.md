# Ölçüm

**Şablona ölçüm kodu eklenmez.** Buton alan adı dışına giden bir bağlantı olduğu için GA4 tıklamayı kendiliğinden kaydeder.

## Nasıl çalışıyor

GA4'ün **Gelişmiş Ölçüm** özelliğindeki *giden bağlantı tıklamaları* varsayılan olarak açıktır ve alan adı dışına giden her tıklamayı `click` olayı olarak kaydeder. Buton `google.com` adresine gittiğinden bu kapsama girer.

Otomatik toplanan parametreler:

| Parametre | Değer |
|---|---|
| `link_url` | `https://www.google.com/preferences/source?q=<domain>` |
| `link_domain` | `www.google.com` |
| `link_id` | `preferred-source-link` |
| `link_classes` | `tcps__btn tcps__btn--light` |
| `outbound` | `true` |

Butona bu nedenle **`id="preferred-source-link"`** verilir. Kimliğin tek işlevi budur; GA4 bunu `link_id` olarak toplar ve raporlama bu değerle filtrelenir.

## Raporlama

GA4 Keşif (Exploration) oluşturulur:

| Alan | Değer |
|---|---|
| Boyut | `Link ID`, sayfa kırılımı için `Sayfa yolu` |
| Metrik | `Olay sayısı` |
| Filtre | `Olay adı = click` ve `Link ID = preferred-source-link` |

## Kurulum öncesi tek kontrol

GA4 yönetiminde ilgili veri akışında **Gelişmiş Ölçüm > Giden bağlantı tıklamaları** ayarının açık olduğu doğrulanır. Kapalıysa açılması yeterlidir; sitede değişiklik gerekmez.

Rıza yönetimi (consent) tıklamayı engelliyorsa ölçüm de etkilenir; bu marka tarafında kontrol edilir.

## Ölçülemeyen

Okuyucunun Google ekranında **onayı tamamlayıp tamamlamadığı**. Onay Google tarafında gerçekleşir ve siteye sinyal dönmez.

Raporlamada tıklama net sayı olarak verilir, ekleme sayısı verilmez. Doğru ifade "kaç kişi butona tıkladı", "kaç kişi ekledi" değil.

## Tek varyant kuralı

Aynı anda **tek kart varyantı** yayınlanır. Bu yüzden ölçümün varyant ayırt etmesine gerek yoktur ve `cta_variant` gibi bir parametre kullanılmaz.

Bir gün iki varyantın karşılaştırılması istenirse, şablona dokunmadan etiket yöneticisinde ayrı bir kural kurulur; yapılandırıcıdaki ton, yerleşim ve çerçeve kodu (`t1-p1-f1`) o kuralda etiket olarak kullanılabilir.

## Gömme butonuna dönülürse

Google'ın kendi butonu cross-origin iframe olduğundan giden bağlantı ölçümü çalışmaz; tıklama ana dokümana ulaşmaz. Ayrıntı: `google-preferred-sources.md` son bölüm.
