# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.expanduser("~/.claude/skills/turkcell-talep-skilli/scripts"))
import docx_stil as S

BURASI = os.path.dirname(os.path.abspath(__file__))

S.GORSEL_DIZIN = BURASI

KART_KODU_DOSYASI = os.path.join(BURASI, "kart-kodu.txt")
if not os.path.exists(KART_KODU_DOSYASI):
    raise SystemExit("kart-kodu.txt bulunamadi. Yapilandiricidan secilen varyantin kodu bu dosyaya kaydedilmeli.")
KART_KODU = open(KART_KODU_DOSYASI, encoding="utf-8").read().rstrip("\n").split("\n")

d = S.yeni_dokuman()
S.dokuman_basligi(d,
  "Turkcell Blog · Google Tercih Edilen Kaynak Butonu Kurulum Talep Dokümanı",
  "Hedef sayfa: turkcell.com.tr/blog · Ölçüm tarihi: 28 Ağustos 2026")

S.bolum_basligi(d, "TALEP KAPSAMI")
S.paragraf(d, "Turkcell Blog yazı şablonuna, Google'ın tercihler ekranına giden bir buton taşıyan markaya özel bir kart eklenmesi istenmektedir. Okuyucu bu buton üzerinden Turkcell Blog'u kendi arama tercihlerine ekleyebilmekte, sonraki aramalarında markanın içerikleri tercih edilen kaynak işaretiyle öne çıkmaktadır.")
S.paragraf(d, "Kartın tasarım değerleri canlı blog sayfasından alınmıştır; ölçümler Chrome DevTools üzerinden yapılmıştır. Maddeler uygulama sırasına göre listelenmiştir.")

S.madde_basligi(d, "Talep Amacı")
for m in [
  "Blog yazı şablonuna tek parça HTML kart eklemek.",
  "Butonu Google'ın tercihler ekranına bağlamak ve yeni sekmede açmak.",
  "Kartın içerik kolonu genişliğini aşmamasını ve mobilde taşmamasını sağlamak.",
]:
    S.madde_imi(d, m)

S.bolum_basligi(d, "ÖN KOŞUL")
_p = d.add_paragraph()
S._run(_p, "Butonun çalışması için Turkcell'in Google'ın kaynak tercihleri listesinde görünmesi gerekmektedir. Doğrulama google.com/preferences/source?q=turkcell.com.tr adresinden yapılır ")
S._run(_p, "ve Google hesabıyla giriş gerektirir. Doğrulama yapılıp aksiyona öyle devam edilmelidir.", bold=True)
S.paragraf(d, "Google yalnız domain ve subdomain seviyesini kabul etmektedir; turkcell.com.tr uygundur, turkcell.com.tr/blog alt dizin olduğu için ayrı bir kaynak sayılmamaktadır.")

S.bolum_basligi(d, "TALEP DETAYI")

S.madde_basligi(d, "1. Kart kodunun blog şablonuna eklenmesi")
S.etiketli(d, "Mevcut durum:", "Blog yazı şablonunda tercih edilen kaynak kartı bulunmamaktadır.")
S.etiketli(d, "Talep edilen değişiklik:")
S.madde_imi(d, "Aşağıdaki kod olduğu gibi eklenmelidir. Dış script yüklenmemektedir, kart tek parçadır.")
S.madde_imi(d, "Sarmalayıcının id değeri preferred-source-button, bağlantının id değeri preferred-source-link olarak kalmalıdır; ölçüm bu kimliklere bağlıdır.")
S.madde_imi(d, "Bağlantı yeni sekmede açılmalı, rel değeri noopener noreferrer olmalıdır.")
S.madde_imi(d, "Logo markanın kendi adresinden çekilmektedir; base64 gömülmemelidir.")
S.kod_ornegi(d, KART_KODU)
S.gorsel(d, "kart-ornek.png", "Kart tonu seçenekleri · yayına lacivert kontrast tonu alınmaktadır")

S.madde_basligi(d, "2. Kartın yerleştirileceği konum")
S.etiketli(d, "Mevcut durum:", "İçerik kolonu 846 px genişliktedir. Kart bu kolonun içine, yazı akışının parçası olarak girmektedir.")
S.etiketli(d, "Talep edilen değişiklik:")
S.madde_imi(d, "Kart, yazının istenen paragrafından sonra gövde akışının içine veya sonuna yerleştirilmelidir.")
S.madde_imi(d, "Kart, içerik kolonu genişliğini aşmamalıdır.")
S.madde_imi(d, "Dar ekranda öğeler alt satıra inmekte, 640 px altında buton tam genişliğe açılmaktadır; kodda bu davranış tanımlıdır.")

S.madde_basligi(d, "3. Ölçüm")
S.etiketli(d, "Mevcut durum:", "Buton alan adı dışına giden bir bağlantıdır. GA4'ün Gelişmiş Ölçüm özelliğindeki giden bağlantı tıklamaları varsayılan olarak açıktır ve bu tıklamayı kendiliğinden kaydeder.")
S.etiketli(d, "Talep edilen değişiklik:")
S.madde_imi(d, "Şablona ölçüm kodu eklenmesi gerekmemektedir. 1. maddedeki id yeterlidir.")
S.madde_imi(d, "GA4 yönetiminde ilgili veri akışında Gelişmiş Ölçüm altındaki giden bağlantı tıklamaları ayarının açık olduğu doğrulanmalıdır.")
S.etiketli(d, "Örnek:")
S.paragraf(d, "GA4 Keşif ekranında boyut olarak Link ID, metrik olarak Olay sayısı seçilir; Olay adı click ve Link ID preferred-source-link filtresi uygulanır. Sayfa kırılımı için Sayfa yolu boyutu eklenir.")

S.bolum_basligi(d, "NOT")
S.paragraf(d, "Ölçüm değerleri 28 Ağustos 2026 tarihli tek bir kesitten alınmıştır ve 1440 px genişlikte masaüstü görünümünü yansıtmaktadır. Buton tıklaması, şablona ek kod gerekmeden GA4 tarafında ölçülebilmektedir. Okuyucunun Google ekranında onayı tamamlayıp tamamlamadığı bilgisi Google tarafında kalmakta ve siteye dönmemektedir; bu nedenle raporlamada tıklama sayısı paylaşılır, ekleme sayısı paylaşılmaz.")
S.paragraf(d, "Kartın tonu, yerleşimi ve çerçevesi ayrı ayrı seçilebilmektedir; bu dokümandaki örnek lacivert kontrast tonu ile tam genişlik yerleşimini taşımaktadır. Maddelerin önceliklendirilmesi ekiple birlikte güncellenebilir.")

S.kaydet(d, os.path.join(BURASI, "Turkcell-Tercih-Edilen-Kaynak-Butonu-IT-Talep.docx"))
