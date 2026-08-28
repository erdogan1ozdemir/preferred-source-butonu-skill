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

| Kod | Ad | Teknik | Taşma | Karakter |
|---|---|---|---|---|
| `f0` | Sade | efekt yok | yok | En sakin, öntanımlı |
| `f1` | Conic kenarlık | kenarlık şeridinde dönen ışık yayı, marka rengi | yok | İstenen referans efekt |
| `f2` | Gökkuşağı kenarlık | aynı teknik, çok renkli yay | yok | En dikkat çekici kenarlık |
| `f3` | Pulse glow | nefes alan `box-shadow` | ~11px | Yumuşak, sürekli |
| `f4` | Dış hale | kartın arkasında bulanık conic | ~11px | Kart yüzer gibi durur |

### Conic kenarlık (f1, f2)

Işık yayı **kenarlığın kendisindedir**, arkada bulanık bir hale değil. Gradyan `mask-composite` ile 1.5px'lik şeride kırpılır.

```css
@property --tcps-a{syntax:'<angle>';initial-value:0deg;inherits:false}
.tcps{position:relative;border-color:transparent}
.tcps::before{
  content:'';position:absolute;inset:0;border-radius:12px;padding:1.5px;
  background:conic-gradient(from var(--tcps-a), <duraklar>);
  -webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);
  -webkit-mask-composite:xor;
          mask-composite:exclude;
  pointer-events:none;
  animation:tcps-spin 6s linear infinite;
}
@keyframes tcps-spin{to{--tcps-a:360deg}}
```

- **`padding` + `mask-composite:exclude` çifti zorunlu.** Maske, pseudo-element'in content-box'ını dışarıda bırakır; geriye yalnız 1.5px'lik kenar şeridi kalır. `padding` kaldırılırsa gradyan kartın tamamını kaplar.
- **`border-color:transparent`** verilir; kartın kendi kenarlığı ışık yayının altında ikinci bir çizgi olarak görünmesin.
- **`z-index` verilmez.** Halka kart zemininin üstünde durmalıdır; `z-index:-1` onu sayfa zeminine düşürür ve halka kaybolur (bu yalnız `f4` için doğrudur).
- `f1` durakları tek parlak yay üretir: `transparent 0deg` -> marka rengi `60deg` -> `transparent 130deg`. `f2` tam spektrumdur, boşluksuz.
- Yay rengi tona göre gelir: koyu kartta marka vurgusu, açık kartlarda marka koyu rengi.
- **Kart dışına taşmaz.** Gövdede `overflow:hidden` olsa bile kırpılmaz.

### Pulse (f3)

```css
.tcps{animation:tcps-pulse 2.8s ease-in-out infinite}
@keyframes tcps-pulse{
  0%,100%{box-shadow:0 0 14px rgba(<marka>,.28)}
  50%{box-shadow:0 0 32px rgba(<marka>,.6)}
}
```

### Dış hale (f4)

Kartın **arkasında** bulanık conic parıltı. `f1`'den farkı: halka değil hale.

```css
.tcps{position:relative;isolation:isolate}
.tcps::before{
  content:'';position:absolute;inset:-3px;border-radius:15px;z-index:-1;
  background:conic-gradient(from var(--tcps-a), <marka durakları>);
  filter:blur(8px);opacity:.9;pointer-events:none;
  animation:tcps-spin 6s linear infinite;
}
```

`isolation:isolate` şart: `z-index:-1` olan pseudo-element aksi halde sayfa zeminine düşer.

### Ortak kurallar

- Her efekt için `@media (prefers-reduced-motion:reduce){.tcps,.tcps::before{animation:none}}` eklenir.
- `@property` desteklenmeyen tarayıcıda halka **statik** kalır; kart yine düzgün görünür. Bilinçli zarif düşüş.
- `f0` seçildiğinde üretilen kodda `conic`, `animation`, `@property` ve `mask` **hiç bulunmaz**; sade seçim gerçekten sade kod üretir.
