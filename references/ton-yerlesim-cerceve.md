# Ton, yerleşim ve çerçeve spesifikasyonu

Üç eksen **bağımsızdır**. 3 x 3 x 4 = 36 kombinasyon serbestçe eşleşir; kullanıcı yapılandırıcıda üçünü ayrı ayrı seçer.

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
| `p3` | Yazı sonu kutusu | Gövde sonunda | 26px 28px | 46px | 20px | var, dikey yığın |

- Kart, ölçülen içerik kolonu genişliğini aşmaz.
- `p2` için ayrı **kısa başlık** kullanılır; uzun başlık dar şeritte yer yer.
- Yığılma `flex-wrap` ile kendiliğinden olur, container query gerekmez. Kopya kutusu `flex:1 1 200px`, buton `flex:0 0 auto`.
- 640px altında buton tam genişliğe açılır.

## Çerçeve

| Kod | Ad | Teknik | Karakter |
|---|---|---|---|
| `f0` | Sade | efekt yok | En sakin, öntanımlı |
| `f1` | Conic glow | dönen conic-gradient halka, marka renkleri | Dikkat çeker, marka içinde kalır |
| `f2` | Pulse glow | nefes alan `box-shadow` | Yumuşak, sürekli |
| `f3` | Gökkuşağı conic | dönen çok renkli conic halka | En dikkat çekici |

### Conic halka (f1, f3)

```css
@property --tcps-a{syntax:'<angle>';initial-value:0deg;inherits:false}
.tcps{position:relative;isolation:isolate}
.tcps::before{
  content:'';position:absolute;inset:-3px;border-radius:15px;z-index:-1;
  background:conic-gradient(from var(--tcps-a), <duraklar>);
  filter:blur(8px);opacity:.9;
  animation:tcps-spin 6s linear infinite;
}
@keyframes tcps-spin{to{--tcps-a:360deg}}
```

- Duraklar `f1`'de markanın kendi renkleri, `f3`'te tam spektrum.
- `@property` desteklenmeyen tarayıcıda halka **statik** kalır; kart yine düzgün görünür. Bilinçli zarif düşüş.
- `isolation:isolate` şart: `z-index:-1` olan pseudo-element aksi halde sayfa zeminine düşer.

### Pulse (f2)

```css
.tcps{animation:tcps-pulse 2.8s ease-in-out infinite}
@keyframes tcps-pulse{
  0%,100%{box-shadow:0 0 14px rgba(<marka>,.28)}
  50%{box-shadow:0 0 32px rgba(<marka>,.6)}
}
```

Parıltı rengi tona göre seçilir: koyu kartta marka vurgusu, açık kartlarda marka koyu rengi.

### Ortak kurallar

- Her efekt için `@media (prefers-reduced-motion:reduce){.tcps,.tcps::before{animation:none}}` eklenir.
- Efektler kartın **~11px dışına** taşar (inset -3px + blur 8px). Gövde kapsayıcısında `overflow:hidden` varsa kırpılır; QA'da kontrol edilir.
- `f0` seçildiğinde üretilen kodda `conic`, `animation` ve `@property` **hiç bulunmaz**; sade seçim gerçekten sade kod üretir.
