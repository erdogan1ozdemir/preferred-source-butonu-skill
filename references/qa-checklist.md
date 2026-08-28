# QA kontrol listesi

## Otomatik tarama (yayın öncesi zorunlu)

36 kombinasyon (3 ton x 3 yerleşim x 4 çerçeve) masaüstü ve mobil olmak üzere 72 kez taranır. Hepsi geçmeden yayınlanmaz.

| Kontrol | Eşik |
|---|---|
| Kartın kolondan taşması | 0px |
| Buton yüksekliği | >= 44px |
| Butonun kart içinde kalması | tümünde |
| Sayfa yatay kaydırması | 0px |
| Metin/zemin kontrastı | >= 4.5:1 |
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
- **Script tekrarı:** `publisher.js` sayfada bir kez mi yükleniyor.
- **Glow taşması:** çerçeve efekti kartın ~11px dışına taşar. Gövde kapsayıcısında `overflow:hidden` varsa parıltı kırpılır.
- **Hareket kısıtı:** işletim sisteminde hareket azaltma açıkken animasyon duruyor mu.
- **Font:** kart markanın kendi fontuyla mı geliyor (lisanslı fontlar önizlemede sistem fontuna düşer).
- **Mobil:** gerçek telefonda buton tam genişliğe açılıyor mu (viewport media query'sine bağlı, artifact önizlemesinde görünmez).
- **CLS:** script yüklenirken sayfa zıplıyor mu.
- **Ekran okuyucu:** logo `alt` metni marka adını taşıyor mu.
