# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.expanduser("~/.claude/skills/turkcell-talep-skilli/scripts"))
import docx_stil as S

BURASI = os.path.dirname(os.path.abspath(__file__))
S.GORSEL_DIZIN = BURASI

KART_CSS = """.tcps{--bg:#164193;--ink:#FFFFFF;--sub:#C6D3EA;--line:rgba(255,255,255,.20);
  display:flex;flex-wrap:wrap;align-items:center;gap:20px;margin:28px 0;padding:20px 24px;
  background:var(--bg);border:1px solid var(--line);border-radius:12px;
  font-family:greycliff,system-ui,-apple-system,Arial,sans-serif;color:var(--ink);box-sizing:border-box}
.tcps *{box-sizing:border-box}
.tcps__mark{flex:0 0 auto;display:flex;align-items:center;justify-content:center}
.tcps__logo{display:block;width:38px;height:38px}
.tcps__copy{flex:1 1 200px;min-width:0}
.tcps__ttl{display:block;font-size:17px;line-height:1.35;
  font-weight:700;letter-spacing:-.01em}
.tcps__sub{display:block;margin-top:5px;font-size:14.5px;
  line-height:1.5;color:var(--sub)}
.tcps__act{flex:0 0 auto;margin-left:auto;min-height:44px;
  display:flex;align-items:center}
@media (max-width:640px){
  .tcps{gap:14px}
  .tcps__act{margin-left:0;width:100%}
}""".split("\n")

KART_HTML = """<div class="tcps" id="preferred-source-button">
  <div class="tcps__mark">
    <img class="tcps__logo" alt="Turkcell" width="38" height="38"
         loading="lazy"
         src="https://ffo3gv1cf3ir.merlincdn.net/SiteAssets/
              Bireysel/Navigasyon/turkcell-logo.png">
  </div>
  <div class="tcps__copy">
    <strong class="tcps__ttl">Turkcell Blog'u Google'da tercih
      edilen kaynaklarınıza ekleyin</strong>
    <span class="tcps__sub">Teknoloji ve mobil dünyasına dair
      içeriklerimiz arama sonuçlarınızda daha önce çıksın.</span>
  </div>
  <div class="tcps__act">
    <div google-add-preferred-source-btn data-theme="light" data-lang="tr"></div>
  </div>
</div>""".split("\n")

d = S.yeni_dokuman()
S.dokuman_basligi(d,
  "Turkcell Blog · Google Tercih Edilen Kaynak Butonu Kurulum Talep Dokümanı",
  "Hedef sayfa: turkcell.com.tr/blog · Ölçüm tarihi: 28 Ağustos 2026")

S.bolum_basligi(d, "TALEP KAPSAMI")
S.paragraf(d, "Turkcell Blog yazı şablonuna, Google'ın tercih edilen kaynak butonunu taşıyan markaya özel bir kart eklenmesi istenmektedir. Okuyucu bu kart üzerinden Turkcell Blog'u kendi arama tercihlerine ekleyebilmekte, sonraki aramalarında markanın içerikleri tercih edilen kaynak işaretiyle öne çıkmaktadır.")
S.paragraf(d, "Kartın tasarım değerleri canlı blog sayfasından alınmıştır; ölçümler Chrome DevTools üzerinden yapılmıştır. Maddeler uygulama sırasına göre listelenmiştir.")

S.madde_basligi(d, "Talep Amacı")
for m in [
  "Blog yazı şablonuna tek parça HTML kart eklemek.",
  "Google'ın resmî buton script'ini sayfa başına yalnız bir kez yüklemek.",
  "Kartın içerik kolonu genişliğini aşmamasını ve mobilde taşmamasını sağlamak.",
  "Kart görüntülenmesini dataLayer üzerinden ölçülebilir hale getirmek.",
  "Butonun mesaj kanalından tıklama sinyali gelip gelmediğini test ortamında doğrulamak.",
]:
    S.madde_imi(d, m)

S.madde_basligi(d, "Mevcut Durum Özeti")
S.tablo(d, ["Alan", "Ölçülen değer"], [
  ["İçerik kolonu genişliği", "846 px (1440 px viewport)"],
  ["Gövde paragrafı", "greycliff · 17.6 px / 31.68 px · #5F6B76"],
  ["Başlık rengi", "#253342"],
  ["Kart köşe yarıçapı", "12 px"],
  ["Şablonda benzer kart bileşeni", "Bulunmuyor"],
], [2.6, 4.0])
S.paragraf(d, "Şablonda bu kartın devralabileceği hazır bir bileşen bulunmadığından, kart kendi stilini taşıyan bağımsız bir parça olarak eklenir.")
S.kaynak_notu(d, "Kaynak: turkcell.com.tr/blog/fps-nedir · getComputedStyle · 28 Ağustos 2026")

S.bolum_basligi(d, "ÖN KOŞUL")
S.paragraf(d, "Butonun çalışması için Turkcell'in Google'ın kaynak tercihleri listesinde görünmesi gerekmektedir. Doğrulama google.com/preferences/source?q=turkcell.com.tr adresinden yapılır ve Google hesabıyla giriş gerektirdiğinden marka tarafında tamamlanmalıdır.")
S.paragraf(d, "Google yalnız domain ve subdomain seviyesini kabul etmektedir; turkcell.com.tr uygundur, turkcell.com.tr/blog alt dizin olduğu için ayrı bir kaynak sayılmamaktadır. Doğrulama tamamlanmadan yayına alınırsa kart görünür, buton işlev göstermez.")

S.bolum_basligi(d, "TALEP DETAYI")

S.madde_basligi(d, "1. Buton script'inin blog şablonuna eklenmesi")
S.etiketli(d, "Mevcut durum:", "Blog şablonunda Google tercih edilen kaynak script'i yüklenmemektedir.")
S.etiketli(d, "Talep edilen değişiklik:")
S.madde_imi(d, "Script blog yazı şablonuna, gövde sonuna yakın bir konuma eklenmelidir.")
S.madde_imi(d, "Script sayfa başına yalnız bir kez yüklenmelidir; kart parçası birden çok kez basılsa dahi script tekrarlanmamalıdır.")
S.madde_imi(d, "async niteliği korunmalıdır.")
S.kod_ornegi(d, ['<script async src="https://news.google.com/swg/js/v1/publisher.js"></script>'])

S.madde_basligi(d, "2. Kart parçasının yazı gövdesine yerleştirilmesi")
S.etiketli(d, "Mevcut durum:", "Yazı gövdesinde tercih edilen kaynak kartı bulunmamaktadır.")
S.etiketli(d, "Talep edilen değişiklik:")
S.madde_imi(d, "Kart, yazının ilk paragrafından sonra gövde akışının içine yerleştirilmelidir.")
S.madde_imi(d, "Sarmalayıcı öğenin id değeri preferred-source-button olmalıdır; ölçüm bu kimliğe bağlıdır.")
S.madde_imi(d, "Logo markanın kendi adresinden çekilmelidir, base64 gömülmemelidir.")
S.madde_imi(d, "Buton öğesine data-lang=\"tr\" verilmelidir; dil bu değerle sabitlenir.")
S.kod_ornegi(d, KART_HTML)
S.gorsel(d, "kart-ornek.png", "Üç kart tonu · lacivert kontrast, sarı tint, minimal çerçeve")

S.madde_basligi(d, "3. Kart stilinin eklenmesi (kolon genişliği, mobil)")
S.etiketli(d, "Mevcut durum:", "İçerik kolonu 846 px genişliktedir. Google'ın butonu sayfaya iframe olarak yerleşmekte ve öntanımlı genişliği konteynere göre değişmektedir.")
S.etiketli(d, "Talep edilen değişiklik:")
S.madde_imi(d, "Kart, içerik kolonu genişliğini aşmamalıdır.")
S.madde_imi(d, "Yerleşim flex-wrap ile kurulmalıdır; dar ekranda öğeler kendiliğinden alt satıra inmelidir.")
S.madde_imi(d, "640 px altında buton tam genişliğe açılmalıdır.")
S.madde_imi(d, "Butona min-height:44px verilmelidir; script geç yüklendiğinde sayfa kaymamalı, dokunma alanı korunmalıdır.")
S.kod_ornegi(d, KART_CSS)

S.madde_basligi(d, "4. Kart görüntülenmesinin ölçülmesi")
S.etiketli(d, "Mevcut durum:", "Kart için tanımlı bir ölçüm bulunmamaktadır.")
S.etiketli(d, "Talep edilen değişiklik:")
S.madde_imi(d, "Kart ekranda göründüğünde dataLayer'a preferred_source_view olayı yazılmalıdır.")
S.madde_imi(d, "Olay sayfa başına bir kez yazılmalıdır.")
S.madde_imi(d, "Aynı script, Google'ın çerçevesinden gelen mesajları da dinleyip preferred_source_signal olayı yazmalıdır.")
S.madde_imi(d, "GTM tarafında iki olay için Custom Event trigger ve GA4 Event tag tanımlanmalıdır. Parametreler: cta_id, cta_variant, page_path, signal_cmd.")
exec(open(os.path.join(BURASI, "kod_parcalari.py")).read())
S.kod_ornegi(d, GA4.split("\n"))

S.madde_basligi(d, "5. Tıklama sinyalinin test ortamında doğrulanması")
S.etiketli(d, "Mevcut durum:", "Google'ın butonu news.google.com alan adından gelen bir iframe içinde yerleşmektedir. Farklı alan adındaki bir çerçevenin içindeki tıklama ana dokümana ulaşmadığından, kart kimliğine bağlanan klasik tıklama kuralı bu butonda sonuç vermemektedir.")
S.paragraf(d, "Buna karşılık çerçeve ana sayfayla mesaj kanalı üzerinden haberleşmektedir; sayfa yüklenirken bu kanalda mesaj alışverişi ölçülmüştür. Butonun script'inde buton tıklaması ve ekleme sonucu için tanımlı olay adları bulunmaktadır.")
S.etiketli(d, "Talep edilen değişiklik:")
S.madde_imi(d, "Test ortamında 4. maddedeki script yüklüyken butona tıklanmalı, dataLayer'a preferred_source_signal olayı düşüp düşmediği kontrol edilmelidir.")
S.madde_imi(d, "Düşen olayların signal_cmd ve signal_payload değerleri kaydedilip iletilmelidir.")
S.madde_imi(d, "Tıklama ve ekleme sonucuna karşılık gelen bir desen bulunursa, GA4 tarafında ayrı olay adlarına eşlenmelidir.")
S.etiketli(d, "Dikkat edilmesi gerekenler:", "Bu doğrulama tamamlanmadan tıklama sayısı raporlanmamalıdır.")

S.madde_basligi(d, "6. Erişilebilirlik ve sayfa kayması kontrolü")
S.etiketli(d, "Mevcut durum:", "Kart yeni bir bileşen olduğundan mevcut kontrol listelerinde yer almamaktadır.")
S.etiketli(d, "Talep edilen değişiklik:")
S.madde_imi(d, "Logo görselinin alt metni marka adını taşımalıdır.")
S.madde_imi(d, "Kart metniyle zemini arasındaki kontrast oranı en az 4.5:1 olmalıdır.")
S.madde_imi(d, "Buton çerçevesi yüklenirken sayfada kayma oluşmamalıdır; CLS değeri yayın öncesi ve sonrası karşılaştırılmalıdır.")
S.madde_imi(d, "Hareketli çerçeve tercih edilirse prefers-reduced-motion açıkken animasyon durmalıdır.")

S.bolum_basligi(d, "NOT")
S.paragraf(d, "Ölçüm değerleri 28 Ağustos 2026 tarihli tek bir kesitten alınmıştır ve 1440 px genişlikte masaüstü görünümünü yansıtmaktadır. Kart görüntülenmesi net ölçülebilmekte, tıklama ise 5. maddedeki doğrulama tamamlanana kadar raporlanmamaktadır. Okuyucunun markayı tercih edilen kaynak olarak ekleyip eklemediği bilgisi Google tarafında kalmakta ve siteye dönmemektedir.")
S.paragraf(d, "Kartın tonu, yerleşimi ve çerçevesi ayrı ayrı seçilebilmektedir; bu dokümandaki örnek lacivert kontrast tonu ile tam genişlik yerleşimini taşımaktadır. Maddelerin önceliklendirilmesi ekiple birlikte güncellenebilir.")

S.kaydet(d, os.path.join(BURASI, "Turkcell-Tercih-Edilen-Kaynak-Butonu-IT-Talep.docx"))
