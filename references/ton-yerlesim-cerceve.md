# Ton, yerleşim ve çerçeve spesifikasyonu

Üç eksen **bağımsızdır**. 3 x 3 x 5 = 45 kombinasyon serbestçe eşleşir; kullanıcı yapılandırıcıda üçünü ayrı ayrı seçer.

Varyant kodu `t<n>-p<n>-f<n>` biçimindedir ve GA4'te `cta_variant` olarak taşınır.

## Ton (kartın zemini)

Üçü de ölçülen gövde zeminine göre türetilir.

| Kod | Ad | Zemin | Metin | Kaide | Kullanımı |
|---|---|---|---|---|---|
| `t1` | Koyu kontrast | marka koyu rengi | beyaz | yok, logo doğrudan durur | Zeminden en çok ayrışır |
| `t2` | Marka tinti | marka vurgusunun açık tonu | ölçülen başlık rengi | marka koyu rengi, 10px yarıçap | Sayfaya gömülü durur |
| `t3` | Minimal çerçeve | gövde zemini | ölçülen başlık rengi | marka koyu rengi, 10px yarıçap | En az müdahale |

**Logo kaidesi kuralı.** Marka sembolü açık renkliyse (sarı, açık turuncu) açık tonlarda yıkanır. `t2` ve `t3`'te sembol marka koyu renginde yuvarlak kaideye oturtulur; `t1`'de kaide şeffaftır, sembol doğrudan koyu kartta durur.

Her tonun başlık ve açıklama kontrastı hesaplanır; 4.5:1 altındaysa ton düzeltilir.

## Yerleşim

| Kod | Ad | Konum | Padding | Logo | Başlık | Açıklama |
|---|---|---|---|---|---|---|
| `p1` | Tam genişlik banner | İlk paragraftan sonra | 20px 24px | 38px | 17px | var |
| `p2` | Kompakt şerit | İlk paragraftan sonra | 14px 18px | 32px | 15px | yok, kısa başlık |
| `p3` | Yazı sonu kutusu | Gövde sonunda | 26px 28px | 46px | 20px | var, buton alt satırda |

- Kart, ölçülen içerik kolonu genişliğini aşmaz.
- `p2` için ayrı **kısa başlık** kullanılır; uzun başlık dar şeritte yer yer.
- **`p3`'te logo ve metin aynı satırdadır**, logo metnin üstüne alınmaz. Yalnız buton alt satıra iner (`.tcps__act{flex:1 0 100%}`). Dikey yığın denenmişti; logo tek başına bir satır işgal edip kartı dağıtıyordu.
- Yığılma `flex-wrap` ile kendiliğinden olur, container query gerekmez. Kopya kutusu `flex:1 1 200px`, buton `flex:0 0 auto`.
- 640px altında buton tam genişliğe açılır.

## Çerçeve

| Kod | Ad | Teknik | Konum | Taşma |
|---|---|---|---|---|
| `f0` | Sade | efekt yok | - | yok |
| `f1` | Conic kenarlık | dönen ışık yayı, marka rengi | çerçevenin 4px dışında | ~4px |
| `f2` | Gökkuşağı kenarlık | aynı halka, pastel spektrum | çerçevenin 4px dışında | ~4px |
| `f3` | Pulse glow | nefes alan `box-shadow` | kart üzerinde | ~11px |
| `f4` | Geniş hale | bulanık conic, kartın arkasında | sarmalayıcıda | ~24px |

### Conic kenarlık (f1, f2)

Işık yayı **kartın kenar çizgisinin dışında** dolaşır. Gradyan `mask-composite` ile 1.5px'lik şeride kırpılır, `inset:-4px` ile dışarı taşınır.

```css
@property --tcps-a{syntax:'<angle>';initial-value:0deg;inherits:false}
.tcps{position:relative}
.tcps::before{
  content:'';position:absolute;inset:-4px;border-radius:16px;padding:1.5px;
  background:conic-gradient(from var(--tcps-a), <duraklar>);
  -webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);
  -webkit-mask-composite:xor;
          mask-composite:exclude;
  pointer-events:none;
  animation:tcps-spin 6s linear infinite;
}
@keyframes tcps-spin{to{--tcps-a:360deg}}
```

- **`padding` + `mask-composite:exclude` çifti zorunlu.** Maske pseudo-element'in içini dışarıda bırakır, geriye yalnız kenar şeridi kalır. `padding` kaldırılırsa gradyan tüm alanı doldurur.
- **`inset:-4px`** halkayı kartın kenar çizgisinin dışına taşır. Kartın kendi kenarlığı yerinde kalır, ikisi üst üste binmez.
- **`z-index` verilmez ve `isolation` kullanılmaz.** Halka zaten kartın dışında; `z-index:-1` onu sayfa zeminine düşürüp görünmez yapar.
- **`f1` durakları** tek parlak yay üretir: `transparent` -> marka rengi `60deg` -> `transparent 130deg`. Yay rengi tona göre gelir: koyu kartta marka vurgusu, açık kartlarda marka koyu rengi.
- **`f2` durakları pastel spektrumdur** ve premium bir geçiş için 9 durak kullanılır, doygun renk yoktur:
  `#F2B8B5, #F6CDA0, #F7E6A8, #C8E6B4, #A8D8CE, #9DC0F5, #BDB2F0, #E9BEDC, #F2B8B5`
  Az sayıda doygun durak sert bantlar üretir; yumuşak geçiş için durak sayısı artırılır ve doygunluk düşürülür.

### Pulse (f3)

```css
.tcps{position:relative;animation:tcps-pulse 2.8s ease-in-out infinite}
@keyframes tcps-pulse{
  0%,100%{box-shadow:0 0 14px rgba(<marka>,.28)}
  50%{box-shadow:0 0 32px rgba(<marka>,.6)}
}
```

### Geniş hale (f4)

Bulanık conic parıltı kartın **arkasında** durur. Bunun için sarmalayıcı zorunludur.

```html
<div class="tcps-wrap"><div class="tcps" id="preferred-source-button">…</div></div>
```
```css
.tcps-wrap{position:relative;margin:28px 0}
.tcps-wrap>.tcps{margin:0;position:relative}
.tcps-wrap::before{
  content:'';position:absolute;inset:-9px;border-radius:21px;
  background:conic-gradient(from var(--tcps-a), <marka durakları>);
  filter:blur(15px);opacity:.55;pointer-events:none;
  animation:tcps-spin 6s linear infinite;
}
```

**Neden sarmalayıcı:** parıltıyı `.tcps::before` üzerinde `z-index:-1` ile denemek çalışmaz. `isolation:isolate` eklenirse `.tcps` yığın bağlamı olur ve negatif z-index'li pseudo kartın zemininin **üstüne** boyanır, renk kartın yüzeyine taşar. `isolation` eklenmezse pseudo bu kez sayfa zemininin arkasına düşer. Sarmalayıcının `::before`'u DOM sırasında karttan önce geldiği için hiçbir z-index ayarı gerekmez.

### Ortak kurallar

- Hareket kısıtı yalnız aktif seçiciye uygulanır: `f3` için `.tcps`, `f4` için `.tcps-wrap::before`, diğerleri için `.tcps::before`.
- `@property` desteklenmeyen tarayıcıda halka **statik** kalır; kart yine düzgün görünür. Bilinçli zarif düşüş.
- `f0` seçildiğinde üretilen kodda `conic`, `animation`, `@property`, `mask` ve `tcps-wrap` **hiç bulunmaz**.
