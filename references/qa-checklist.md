# QA kontrol listesi

## Otomatik tarama (yayın öncesi zorunlu)

45 kombinasyon (3 ton x 3 yerleşim x 5 çerçeve) masaüstü ve mobil olmak üzere 90 kez taranır. Hepsi geçmeden yayınlanmaz.

| Kontrol | Eşik |
|---|---|
| Kartın kolondan taşması | 0px |
| Buton yüksekliği | >= 44px |
| Butonun kart içinde kalması | tümünde |
| Sayfa yatay kaydırması | 0px |
| Metin/zemin kontrastı | >= 4.5:1 |
| Buton/kart ayrışması | >= 2:1 |
| Üretim kodunda yorum satırı | 0 |
| Üretim kodunda `data:` URI | 0 |

**Ölçüm tuzağı:** `.viewport` üzerinde `transition:width` varsa cihaz değişiminden hemen sonra okunan genişlik yanlış çıkar. Tarama öncesi geçiş kapatılır:

```js
const st=document.createElement('style');
st.textContent='.viewport{transition:none!important}';
document.head.appendChild(st);
```

**Pane tuzağı:** ölçümden önce viewport 1440px veya üzerine sabitlenir. Dar pane'de sayfa yatay taşar ve tüm ölçümler kayar.

**Derleme tuzağı:** üretilen JS her derlemeden sonra `node --check` ile denetlenir. Python `re.sub` **değiştirme metnindeki** `\n` kaçışları gerçek satır sonuna dönüşüp JS string'lerini böler; sayfa sessizce boş açılır.

- **İz uzunluğu:** parlak yay çemberin dörtte birini aşmamalı, kuyruk alfası `.10` civarında kalmalı. Aksi halde dönen iz yerine sürekli parlak halka görünür.

## Google butonu yalnız gerçek alan adında test edilir

Butona tıklandığında Google'a açılan istek, **sayfanın kendi adresini** kaynak olarak gönderir
(`publisher.js` içinde `source: location.href`). Bu yüzden:

- `localhost` veya `file://` üzerinde butona tıklamak **400 Bad Request** döndürür. Bu bir kurulum
  hatası değildir; Google localhost'u geçerli bir kaynak olarak kabul etmez.
- Buton yerel ortamda **görünür ve render olur**, yalnız tıklama akışı tamamlanamaz.
- Tıklama akışının testi gerçek alan adında ya da Google'ın çözebildiği bir staging alan adında
  yapılmalıdır.
- Kaynak her zaman sayfanın bulunduğu alan adıdır; buton başka bir alan adını ekleyecek biçimde
  yönlendirilemez.

Yerel ortamda tıklama akışını denemek gerekiyorsa deeplink yöntemi kullanılır
(`google.com/preferences/source?q=<domain>`); orada alan adı parametreyle verildiği için
localhost'tan da çalışır.

## Elle kontrol (canlıda)

- **Uygunluk:** domain `google.com/preferences/source?q=<domain>` listesinde mi (giriş gerekir).
- **`data-theme`:** buton kartla aynı tona düşüyor mu; düşüyorsa değer çevrilir.
  Ölçülen risk: açık kart (`t2`, `t3`) + `data-theme="light"` beyaz butonu beyaz karta gömer, ayrışma **1.0:1**. Öntanımlılar bunu önler; elle değiştirilirse yapılandırıcı uyarır.
  Koyu kart (`t1`) + `data-theme="dark"` de zayıftır (1.7:1).
- **Script tekrarı:** `publisher.js` sayfada bir kez mi yükleniyor.
- **Butonun gerçek ölçüsü:** `publisher.js` butonu iframe olarak basar ve öntanımlı genişliği ~540px'dir. Dar kolonlarda ve mobilde kartın taşmadığı canlıda doğrulanır; mock önizleme bu ölçüyü göstermez.
- **Tıklama event'i:** staging'de butona tıklanıp `dataLayer`'a event düşüyor mu bakılır (iframe yüzünden düşmeyebilir).
- **Taşma:** conic ve gökkuşağı kenarlık kartın 2px dışında dolaşır, pulse glow ~11px, geniş hale ~24px taşar. Gövdede `overflow:hidden` varsa kırpılır.
- **Çifte çerçeve çizgisi:** halka aktifken kartın kendi kenarlığı `transparent` olmalı. İkisi birlikte görünürse aralarında boşluk kalan iki çizgi oluşur.
- **Çerçeve sürekliliği:** halkanın düşük alfalı kuyruğu çemberin tamamını kapatmalı. Kuyruk `transparent` bırakılırsa kart, kendi kenarlığı da şeffaf olduğu için çerçevesiz görünür.
- **Dönüş algılanıyor mu:** gradyanda parlak yoğunluk bölgesi yoksa dönüş görünmez. `--tcps-a` iki farklı açıya sabitlenip parlak bölgenin yer değiştirdiği doğrulanır.
- **Hız değişimi:** `animation-delay` negatif değerlerle tura sarılıp `--tcps-a` örneklenir; ardışık açı farkları hızın değiştiğini göstermelidir. Döngü ek yerinde son ve ilk hız birbirine yakın olmalı, yoksa tur başa sarınca sıçrama görünür.
- **Halka görünürlüğü:** conic kenarlıkta `::before` üzerinde ne `z-index` ne `isolation` olmalı. `isolation:isolate` + `z-index:-1` parıltıyı kartın zemininin üstüne boyar ve renk kart yüzeyine taşar; `isolation` olmadan `z-index:-1` ise halkayı sayfa zemininin arkasına düşürür. Kartın arkasına parıltı gerekiyorsa (geniş hale) sarmalayıcı kullanılır.
- **Hareket kısıtı:** işletim sisteminde hareket azaltma açıkken animasyon duruyor mu.
- **Font:** kart markanın kendi fontuyla mı geliyor (lisanslı fontlar önizlemede sistem fontuna düşer).
- **Mobil:** gerçek telefonda buton tam genişliğe açılıyor mu (viewport media query'sine bağlı, artifact önizlemesinde görünmez).
- **CLS:** script yüklenirken sayfa zıplıyor mu.
- **Ekran okuyucu:** logo `alt` metni marka adını taşıyor mu.
