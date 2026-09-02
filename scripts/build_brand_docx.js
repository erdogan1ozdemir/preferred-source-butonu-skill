const fs = require('fs');
const d = require('docx');
const {Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell,
       WidthType, ShadingType, AlignmentType, BorderStyle, ImageRun, ExternalHyperlink,
       LevelFormat, convertInchesToTwip} = d;

const W = 9026;                      // A4 kullanilabilir genislik (DXA)
const TEAL = "10332F", CORAL = "B0421F", LINE = "DFD9D0", SOFT = "FAF8F5";
const INK = "10332F", BODY = "2F3B38", MUTED = "6B7F7A";

const P = (text, o={}) => new Paragraph({
  spacing:{after:o.after??160, line:300},
  alignment:o.align,
  children:[new TextRun({text, size:o.size??21, color:o.color??BODY, bold:o.bold, italics:o.italics, font:"Calibri"})]
});
const RICH = (runs, o={}) => new Paragraph({
  spacing:{after:o.after??160, line:300},
  children: runs.map(r => new TextRun({text:r.t, size:21, color:r.c??BODY, bold:r.b, font:"Calibri"}))
});
const H1 = t => new Paragraph({heading:HeadingLevel.HEADING_1, spacing:{before:80, after:220},
  children:[new TextRun({text:t, size:34, bold:true, color:INK, font:"Calibri"})]});
const H2 = t => new Paragraph({heading:HeadingLevel.HEADING_2, spacing:{before:340, after:150},
  children:[new TextRun({text:t, size:26, bold:true, color:INK, font:"Calibri"})]});
const EYEBROW = t => new Paragraph({spacing:{after:90},
  children:[new TextRun({text:t, size:17, bold:true, color:CORAL, font:"Calibri", characterSpacing:30})]});
const SRC = t => new Paragraph({spacing:{before:60, after:220},
  children:[new TextRun({text:t, size:17, color:MUTED, italics:true, font:"Calibri"})]});
// Kaynak notu: ad gomulu link olarak verilir
const SRCL = (onek, links) => {
  const kids = [new TextRun({text:onek, size:17, color:MUTED, italics:true, font:"Calibri"})];
  links.forEach(([ad,url],i) => {
    if (i) kids.push(new TextRun({text:" · ", size:17, color:MUTED, italics:true, font:"Calibri"}));
    kids.push(new ExternalHyperlink({link:url, children:[
      new TextRun({text:ad, size:17, color:"0B5FA5", italics:true, underline:{}, font:"Calibri"})]}));
  });
  return new Paragraph({spacing:{before:60, after:220}, children:kids});
};
const L_DIL  = "https://blog.google/products-and-platforms/products/search/preferred-sources-language-expansion/";
const L_KESF = "https://blog.google/products-and-platforms/products/search/explore-web-generative-ai-search/";
const L_ORJ  = "https://blog.google/products-and-platforms/products/search/original-high-quality-content-search/";
const L_DEV  = "https://developers.google.com/search/docs/appearance/preferred-sources";
const L_SEJ  = "https://www.searchenginejournal.com/ai-overviews-cut-organic-clicks-38-field-study-finds/573145/";
const BULLET = t => new Paragraph({numbering:{reference:"pts", level:0}, spacing:{after:110, line:300},
  children:[new TextRun({text:t, size:21, color:BODY, font:"Calibri"})]});
const BULLET_R = runs => new Paragraph({numbering:{reference:"pts", level:0}, spacing:{after:110, line:300},
  children: runs.map(r=>new TextRun({text:r.t, size:21, color:r.c??BODY, bold:r.b, font:"Calibri"}))});

function cell(text, {head=false, w, bold=false}={}) {
  return new TableCell({
    width:{size:w, type:WidthType.DXA},
    shading:{type:ShadingType.CLEAR, fill: head ? TEAL : "FFFFFF", color:"auto"},
    margins:{top:100, bottom:100, left:130, right:130},
    children:[new Paragraph({spacing:{after:0, line:280}, children:[
      new TextRun({text, size:20, bold: head||bold, color: head ? "FFFFFF" : BODY, font:"Calibri"})]})]
  });
}
function table(cols, rows) {
  const total = cols.reduce((a,b)=>a+b,0);
  return new Table({
    width:{size:total, type:WidthType.DXA}, columnWidths:cols,
    borders:{ top:{style:BorderStyle.SINGLE,size:4,color:LINE}, bottom:{style:BorderStyle.SINGLE,size:4,color:LINE},
      left:{style:BorderStyle.SINGLE,size:4,color:LINE}, right:{style:BorderStyle.SINGLE,size:4,color:LINE},
      insideHorizontal:{style:BorderStyle.SINGLE,size:4,color:LINE}, insideVertical:{style:BorderStyle.SINGLE,size:4,color:LINE}},
    rows: rows.map((r,i)=> new TableRow({
      tableHeader: i===0,
      children: r.map((c,j)=> cell(c, {head:i===0, w:cols[j]}))
    }))
  });
}
const GAP = (a=200) => new Paragraph({spacing:{after:a}, children:[]});

const img = fs.readFileSync("kart-ornek.png");

const kids = [
  EYEBROW("TURKCELL BLOG | GOOGLE GÖRÜNÜRLÜĞÜ"),
  H1("Tercih Edilen Kaynak Butonu"),
  P("Kapsam: turkcell.com.tr/blog · Hazırlık tarihi: 28.08.2026 · Uygulama: tek parça HTML",
    {size:19, color:MUTED, after:280}),

  P("Google, arama sonuçlarında öne çıkmasını istediği kaynakları okuyucunun kendisinin seçebildiği bir yapı kurmuştur. 2026 yılının ikinci çeyreğinde bu yapı Türkçe dâhil tüm dillere açılmış, yapay zeka yanıtlarına taşınmış ve yayıncıların kendi sayfalarına yerleştirebileceği bir butonla desteklenmiştir."),
  RICH([{t:"Turkcell Blog için önerilen adım, bu butonun blog yazılarının akışına markaya özel bir kart içinde yerleştirilmesidir. Okuyucu tek tıklamayla Turkcell Blog'u tercih edilen kaynaklarına ekleyebilir; sonraki aramalarında markanın içerikleri "},
    {t:"Preferred", b:true}, {t:" etiketiyle öne çıkar."}], {after:60}),

  H2("Google'ın üç adımı"),
  P("30 Nisan ile 27 Mayıs 2026 arasındaki üç duyuru aynı yönü işaret etmektedir: orijinal içeriği ve kullanıcının seçtiği kaynakları yapay zeka aramasında daha görünür kılmak."),
  table([1500, 4426, 3100], [
    ["Tarih", "Adım", "Sonuç"],
    ["30 Nisan 2026", "Tercih edilen kaynaklar Türkçe dâhil tüm dillerde sunuldu", "Türkiye pazarı kapsama girdi"],
    ["6 Mayıs 2026", "AI Mode ve AI Overviews'a query fan-out tekniğiyle beş yeni keşif yöntemi eklendi", "Yanıtlar özetin ötesine geçip kaynağa yönlendirir hale geldi"],
    ["27 Mayıs 2026", "Highly Cited rozeti ve iki yeni carousel devreye alındı", "Orijinal habercilik ve birinci-el bakış açıları belirginleşti"],
  ]),
  SRCL("Kaynak: ", [["Preferred Sources dil genişlemesi", L_DIL], ["Web'i keşfetmenin beş yeni yolu", L_KESF], ["Orijinal ve yüksek kaliteli içerik", L_ORJ]]),
  RICH([{t:"➔ ", c:CORAL, b:true},
        {t:"Bir ay içindeki üç adım, arama görünürlüğünün klasik sıralamanın yanı sıra yapay zeka yanıtlarının içinde şekillendiğini göstermektedir."}], {after:60}),

  H2("Okuyucu tarafında işleyiş"),
  BULLET_R([{t:"Yazının içinde görür. ", b:true},{t:"Kart, blog yazısının akışına yerleştirilir; okuyucu içeriği okurken karşısına çıkar."}]),
  BULLET_R([{t:"Butona basar ve onaylar. ", b:true},{t:"Google'ın kendi onay ekranı açılır. Onay verildikten sonra okuyucu kaldığı satıra geri döner."}]),
  BULLET_R([{t:"Sonraki aramalarında görür. ", b:true},{t:"Markanın içerikleri, o okuyucunun AI Overviews ve AI Mode yanıtlarında Preferred etiketiyle işaretlenir."}]),
  P("Taze içerik yayımlayan her site uygun kabul edilmektedir; ayrı bir başvuru veya onay süreci bulunmamaktadır.", {after:60}),
  SRCL("Kaynak: ", [["Orijinal ve yüksek kaliteli içerik duyurusu", L_ORJ]]),

  H2("Ölçek ve etki"),
  table([3000, 6026], [
    ["Gösterge", "Değer"],
    ["Tıklama olasılığı", "Tercih edilen bir kaynağa tıklama olasılığı iki kata çıkmaktadır"],
    ["Seçilen kaynak sayısı", "Mayıs 2026 itibarıyla 345.000+ benzersiz kaynak; Nisan 2026'da 200.000 seviyesindeydi"],
    ["Dil kapsamı", "Türkçe dâhil tüm diller"],
  ]),
  SRCL("Kaynak: ", [["Preferred Sources dil genişlemesi", L_DIL], ["Orijinal ve yüksek kaliteli içerik", L_ORJ]]),
  RICH([{t:"➔ ", c:CORAL, b:true},
        {t:"Seçilen kaynak sayısının bir ay içinde 200.000 seviyesinden 345.000'in üzerine çıkması, özelliğin hızla benimsendiğine işaret etmektedir. Türkiye'de yaygınlaşmanın henüz sınırlı olduğu dikkate alındığında, erken konumlanma değerlendirilebilir."}], {after:60}),

  H2("Bu dönemde neden önem kazanıyor?"),
  P("Yapay zeka yanıtlarının arama sonuçlarında yaygınlaşması, klasik organik tıklama davranışını değiştirmektedir. Bağımsız bir saha çalışması, AI Overviews görünen sorgularda organik tıklamaların %38 düştüğünü ortaya koymuştur."),
  SRCL("Kaynak: ", [["Search Engine Journal · AI Overviews organik tıklama saha çalışması", L_SEJ]]),
  P("Bu tabloda görünürlük yalnız sıralamayla değil, yanıtın içinde kaynak olarak seçilmekle de ilişkilenmektedir. Tercih edilen kaynak seçimi, okuyucunun kendi iradesiyle kurulduğu için algoritma değişikliklerinden görece bağımsız bir bağ oluşturmaktadır.", {after:60}),

  H2("Uygunluk koşulu"),
  P("Tercih edilen kaynak seçiminde yalnız domain ve subdomain seviyesi kabul edilmektedir; alt dizinler bu kapsamda değerlendirilmemektedir."),
  table([3200, 1700, 4126], [
    ["Adres", "Durum", "Açıklama"],
    ["turkcell.com.tr", "Uygun", "Domain seviyesi"],
    ["blog.turkcell.com.tr", "Uygun", "Subdomain seviyesi"],
    ["turkcell.com.tr/blog", "Uygun değil", "Alt dizin, ayrı kaynak sayılmamaktadır"],
  ]),
  SRCL("Kaynak: ", [["Google Search Central · Preferred Sources yayıncı dokümantasyonu", L_DEV]]),
  P("Blog içeriği turkcell.com.tr alan adı altında yayınlandığından seçim domain seviyesinde gerçekleşir. Butonun yayına alınmasından önce markanın Google'ın kaynak tercihleri listesinde göründüğünün doğrulanması önerilir; bu kontrol Google hesabıyla giriş gerektirdiğinden marka tarafında yapılabilir.", {after:60}),

  H2("Kart tasarımı"),
  P("Kartın rengi, logosu, metni ve çerçevesi markaya özeldir; içindeki buton Google'ın standart butonudur ve marka renklerine göre değiştirilememektedir. Tasarım değerleri turkcell.com.tr/blog/fps-nedir sayfasından ölçülmüştür: içerik kolonu genişliği, paragraf tipografisi, başlık rengi ve köşe yarıçapı canlı sayfadan alınmıştır."),
  P("Aşağıda üç kart tonu yer almaktadır. Yerleşim ve çerçeve efekti ayrı eksenlerdir; toplam 45 kombinasyon ayrı bir yapılandırıcı üzerinden karşılaştırılabilir.", {after:200}),
  new Paragraph({spacing:{after:120}, children:[ new ImageRun({type:"png", data:img, transformation:{width:602, height:349}}) ]}),
  SRC("Ton seçenekleri: lacivert kontrast, sarı tint, minimal çerçeve · Ölçüm tarihi 28.08.2026"),

  H2("Teslim kapsamı"),
  table([2600, 6426], [
    ["Parça", "İçerik"],
    ["Kart kodu", "Tek parça HTML ve CSS. Yorum satırı içermez, blog şablonuna doğrudan yerleştirilir."],
    ["Google script'i", "Sayfa başına bir kez yüklenen resmî buton script'i."],
    ["Ölçüm kodu", "Görüntülenme ve tıklama için GA4 katmanı. İsteğe bağlıdır; buton ölçüm kodu olmadan da çalışmaktadır."],
    ["Yerleştirme notu", "Hangi şablona ve gövdenin neresine ekleneceği."],
    ["Kontrol listesi", "Yayın öncesi mobil, kontrast, sayfa kayması ve erişilebilirlik kontrolleri."],
  ]),

  H2("Ölçüm ve sınırlar"),
  P("Google'ın butonu sayfaya ayrı bir çerçeve (iframe) içinde yerleşmektedir ve bu çerçeve news.google.com alan adından gelmektedir. Tarayıcı güvenlik kuralları gereği farklı alan adındaki bir çerçevenin içindeki tıklama, ana sayfaya olay olarak ulaşmamaktadır."),
  RICH([{t:"Bunun pratik sonucu: kart sarmalayıcısına verilen bir kimliğe (id) dayalı klasik tıklama kuralı, etiket yöneticisinde tanımlansa dahi bu butonda çalışmamaktadır. Kural yanlış kurulduğu için değil, tıklamanın ana sayfaya hiç ulaşmaması nedeniyle. "},
        {t:"Bu bir yapılandırma konusu değil, tarayıcı sınırıdır.", b:true}]),
  P("Buna karşılık çerçeve, ana sayfayla mesaj kanalı üzerinden haberleşmektedir. Sayfa yüklenirken bu kanaldan mesaj alışverişi gerçekleştiği ölçümlenmiştir. Butonun script'i ayrıca buton görüntülenmesi, buton tıklaması ve ekleme sonucu (başarılı, zaten ekli, uygun değil) için tanımlı olay adları içermektedir."),
  table([3400, 5626], [
    ["Ölçüm", "Durum"],
    ["Kart görüntülenmesi", "Ölçülebilir. Ekran görünürlüğü üzerinden, çerçeveden bağımsız çalışır."],
    ["Buton tıklaması", "Klasik tıklama kuralıyla ölçülemez. Mesaj kanalı üzerinden ölçüm ihtimali bulunmaktadır; kurulum öncesi test ortamında doğrulanması gerekmektedir."],
    ["Ekleme sonucu", "Aynı mesaj kanalında ilgili olay adları tanımlıdır. Ana sayfaya iletilip iletilmediği test ortamında doğrulanmalıdır."],
  ]),
  P("Doğrulama tamamlanana kadar raporlamada görüntülenme net sayı olarak, tıklama ise yaklaşık değer olarak paylaşılır. Doğrulama olumlu sonuçlanırsa tıklama ve ekleme sonucu da net sayıya dönüşebilir.", {after:60}),
  SRCL("Kaynak: ", [["Google Search Central · Preferred Sources yayıncı dokümantasyonu", L_DEV]]),

  H2("Kaynaklar"),
];

const links = [
  ["Preferred Sources tüm dillerde · 30 Nisan 2026", "https://blog.google/products-and-platforms/products/search/preferred-sources-language-expansion/"],
  ["Web'i keşfetmenin beş yeni yolu · 6 Mayıs 2026", "https://blog.google/products-and-platforms/products/search/explore-web-generative-ai-search/"],
  ["Orijinal ve yüksek kaliteli içerik · 27 Mayıs 2026", "https://blog.google/products-and-platforms/products/search/original-high-quality-content-search/"],
  ["Preferred Sources yayıncı dokümantasyonu · Google Search Central", "https://developers.google.com/search/docs/appearance/preferred-sources"],
  ["AI Overviews organik tıklama saha çalışması · Search Engine Journal", "https://www.searchenginejournal.com/ai-overviews-cut-organic-clicks-38-field-study-finds/573145/"],
];
links.forEach(([t,u]) => kids.push(new Paragraph({
  numbering:{reference:"pts", level:0}, spacing:{after:110, line:300},
  children:[ new TextRun({text:t+" · ", size:21, color:BODY, font:"Calibri"}),
    new ExternalHyperlink({link:u, children:[new TextRun({text:u, size:18, color:"0B5FA5", underline:{}, font:"Calibri"})]}) ]
})));

const doc = new Document({
  numbering:{config:[{reference:"pts", levels:[{level:0, format:LevelFormat.BULLET, text:"•",
    alignment:AlignmentType.LEFT, style:{paragraph:{indent:{left:360, hanging:220}}}}]}]},
  sections:[{ properties:{page:{margin:{top:1440, bottom:1440, left:1440, right:1440}}}, children:kids }]
});
Packer.toBuffer(doc).then(b => {
  fs.writeFileSync("Turkcell-Tercih-Edilen-Kaynak-Butonu.docx", b);
  console.log("yazildi:", b.length, "bayt");
});
