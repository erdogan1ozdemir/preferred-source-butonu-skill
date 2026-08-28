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

## Elle kontrol (canlıda)

- **Uygunluk:** domain `google.com/preferences/source?q=<domain>` listesinde mi (giriş gerekir).
- **`data-theme`:** buton kartla aynı tona düşüyor mu; düşüyorsa değer çevrilir.
  Ölçülen risk: açık kart (`t2`, `t3`) + `data-theme="light"` beyaz butonu beyaz karta gömer, ayrışma **1.0:1**. Öntanımlılar bunu önler; elle değiştirilirse yapılandırıcı uyarır.
  Koyu kart (`t1`) + `data-theme="dark"` de zayıftır (1.7:1).
- **Script tekrarı:** `publisher.js` sayfada bir kez mi yükleniyor.
- **Taşma:** conic ve gökkuşağı kenarlık kart dışına taşmaz. Pulse glow ve dış hale ~11px taşar; gövdede `overflow:hidden` varsa kırpılır.
- **Halka görünürlüğü:** conic kenarlıkta `::before` üzerinde `z-index` olmamalı. `z-index:-1` halkayı sayfa zeminine düşürüp görünmez yapar.
- **Hareket kısıtı:** işletim sisteminde hareket azaltma açıkken animasyon duruyor mu.
- **Font:** kart markanın kendi fontuyla mı geliyor (lisanslı fontlar önizlemede sistem fontuna düşer).
- **Mobil:** gerçek telefonda buton tam genişliğe açılıyor mu (viewport media query'sine bağlı, artifact önizlemesinde görünmez).
- **CLS:** script yüklenirken sayfa zıplıyor mu.
- **Ekran okuyucu:** logo `alt` metni marka adını taşıyor mu.
