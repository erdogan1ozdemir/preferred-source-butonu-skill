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
| `f1` | Conic kenarlık | dönen ışık yayı, marka rengi | kart kenarına yapışık, 2px dışında | ~2px |
| `f2` | Gökkuşağı kenarlık | aynı halka, pastel spektrum | kart kenarına yapışık, 2px dışında | ~2px |
| `f3` | Pulse glow | nefes alan `box-shadow` | kart üzerinde | ~11px |
| `f4` | Geniş hale | bulanık conic, kartın arkasında | sarmalayıcıda | ~24px |

### Conic kenarlık (f1, f2)

Işık yayı **kartın kenar çizgisinin dışında** dolaşır. Gradyan `mask-composite` ile 1.5px'lik şeride kırpılır, `inset:-4px` ile dışarı taşınır.

```css
@property --tcps-a{syntax:'<angle>';initial-value:0deg;inherits:false}
.tcps{position:relative;border-color:transparent}
.tcps::before{
  content:'';position:absolute;inset:-2px;border-radius:14px;padding:2px;
  background:conic-gradient(from var(--tcps-a), <duraklar>);
  -webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);
  -webkit-mask-composite:xor;
          mask-composite:exclude;
  pointer-events:none;
  animation:tcps-spin 7s linear infinite;
}
@keyframes tcps-spin{
  0%  {--tcps-a:0deg;   animation-timing-function:cubic-bezier(.5,0,.5,1)}
  38% {--tcps-a:205deg; animation-timing-function:cubic-bezier(.5,0,.5,1)}
  62% {--tcps-a:250deg; animation-timing-function:cubic-bezier(.5,0,.5,1)}
  100%{--tcps-a:360deg}
}
```

- **`padding` + `mask-composite:exclude` çifti zorunlu.** Maske pseudo-element'in içini dışarıda bırakır, geriye yalnız kenar şeridi kalır. `padding` kaldırılırsa gradyan tüm alanı doldurur.
- **`inset:-2px` + `border-color:transparent` birlikte kullanılır.** Halka kartın kenarına yapışır ve kartın **kendi kenar çizgisinin yerini alır**. İkisi birlikte bırakılırsa aralarında boşluk kalan **iki ayrı çerçeve çizgisi** oluşur ve kart oturmamış görünür; `inset:-4px` denenip bu yüzden geri alındı.
- Halkanın yarıçapı kartınkinden 2px büyüktür (`14px` / `12px`), böylece köşelerde iç içe geçme olmaz.
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
  animation:tcps-spin 7s linear infinite;
}
```

**Neden sarmalayıcı:** parıltıyı `.tcps::before` üzerinde `z-index:-1` ile denemek çalışmaz. `isolation:isolate` eklenirse `.tcps` yığın bağlamı olur ve negatif z-index'li pseudo kartın zemininin **üstüne** boyanır, renk kartın yüzeyine taşar. `isolation` eklenmezse pseudo bu kez sayfa zemininin arkasına düşer. Sarmalayıcının `::before`'u DOM sırasında karttan önce geldiği için hiçbir z-index ayarı gerekmez.

### Dönüşün görünür olması · kritik kural

Halka ve hale **her zaman döner**, ama dönüş yalnız gradyanın çember boyunca **eşit olmayan** dağılımıyla algılanır. Düzgün dağılmış bir renk çarkı döndüğünde göz hiçbir hareket görmez.

Bu yüzden üç efektin de duraklarında bir **parlak yoğunluk bölgesi** ve düşük alfalı bir kuyruk bulunur:

| Efekt | Yoğunluk | Kuyruk |
|---|---|---|
| `f1` | marka rengi tam opak, `60deg` | `.28` alfa, kalan çember |
| `f2` | pastel spektrum `30deg`-`180deg` tam opak | `.22` alfa, `225deg`-`360deg` |
| `f4` | marka rengi `55deg`, mavi `110deg` | `.12` alfa, `200deg` sonrası |

**Kuyruk şeffaf değil, düşük alfalı olmalıdır.** Tamamen `transparent` bırakılırsa çemberin büyük bölümünde hiç çizgi kalmaz; halka aktifken kartın kendi kenarlığı zaten `transparent` olduğu için kart **çerçevesiz** görünür. Bu hata bir kez yapıldı: `f1`'in kuyruğu `transparent`ti, lacivert kartta çerçeve hiç görünmüyordu.

### Değişken dönüş hızı

Sabit hızlı (`linear`, tek `to{}` karesi) dönüş mekanik durur. Bunun yerine anahtar kareler **eşit olmayan açı adımlarıyla** yazılır ve her kareye `cubic-bezier(.5,0,.5,1)` yumuşatması verilir.

- `0%` -> `38%` arası 205 derece: hızlı süpürme.
- `38%` -> `62%` arası yalnız 45 derece: neredeyse duraklama.
- `62%` -> `100%` arası 110 derece: orta hızda tamamlama.

Ölçülen sonuç: hız **7 ile 146 derece/saniye** arasında değişiyor, oran 20 kat.

**Döngü ek yeri kuralı:** son ve ilk karedeki hız birbirine yakın olmalıdır. Kare başına yumuşatma verildiği için her anahtar karede hız sıfıra yaklaşır; `100%` ve `0%` de yavaş olduğundan tur başa sardığında sıçrama görünmez. Kareler `linear` bırakılırsa ek yerinde ani hız değişimi fark edilir.

### Ortak kurallar

- Hareket kısıtı yalnız aktif seçiciye uygulanır: `f3` için `.tcps`, `f4` için `.tcps-wrap::before`, diğerleri için `.tcps::before`.
- `@property` desteklenmeyen tarayıcıda halka **statik** kalır; kart yine düzgün görünür. Bilinçli zarif düşüş.
- `f0` seçildiğinde üretilen kodda `conic`, `animation`, `@property`, `mask` ve `tcps-wrap` **hiç bulunmaz**.
