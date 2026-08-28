"""Marka config'inden preferred source yapilandiricisini uretir.

Kullanim:
    python3 build_button.py config.json cikti.html

config.json anahtarlari configurator_template.html icindeki {{...}} yer
tutucularina birebir karsilik gelir. LOGO_B64 dogrudan verilebilir ya da
LOGO_FILE ile yerel bir dosyadan uretilir.

Onemli: LOGO_URL uretim koduna girer (markanin kendi CDN adresi),
LOGO_B64 yalniz artifact onizlemesinde kullanilir.
"""
import base64
import json
import mimetypes
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "configurator_template.html")

ZORUNLU = [
    "BRAND_NAME", "BLOG_URL", "ARTICLE_URL", "LOGO_URL",
    "TITLE_LONG", "TITLE_SHORT", "DESC",
    "BRAND_DARK", "BRAND_DARK_RGB", "BRAND_YELLOW", "BRAND_YELLOW_RGB",
    "BRAND_ACCENT", "BRAND_BLUE",
    "TINT_BG", "TINT_LINE", "DARK_SUB", "LINE", "INK", "BODY_COLOR",
    "FONT", "COL_W", "VIEWPORT_W", "P_SIZE", "P_LH", "H1_SIZE", "H2_SIZE",
    "OLCUM_TARIHI",
]


def logo_b64(cfg):
    if cfg.get("LOGO_B64"):
        return cfg["LOGO_B64"]
    path = cfg.get("LOGO_FILE")
    if not path:
        raise SystemExit("LOGO_B64 veya LOGO_FILE gerekli.")
    if not os.path.isabs(path):
        path = os.path.join(os.getcwd(), path)
    mime = mimetypes.guess_type(path)[0] or "image/png"
    raw = base64.b64encode(open(path, "rb").read()).decode()
    # sablon "data:image/png;base64,{{LOGO_B64}}" bicimindedir
    if mime != "image/png":
        print("uyari: logo %s, sablon data:image/png bekliyor" % mime, file=sys.stderr)
    return raw


def build(cfg):
    tpl = open(TEMPLATE, encoding="utf-8").read()
    eksik = [k for k in ZORUNLU if not cfg.get(k)]
    if eksik:
        raise SystemExit("Eksik config anahtarlari: " + ", ".join(eksik))
    cfg = dict(cfg)
    cfg["LOGO_B64"] = logo_b64(cfg)
    for k, v in sorted(cfg.items(), key=lambda kv: -len(kv[0])):
        tpl = tpl.replace("{{%s}}" % k, str(v))
    kalan = set(re.findall(r"\{\{([A-Z_0-9]+)\}\}", tpl))
    if kalan:
        raise SystemExit("Doldurulmamis yer tutucu: " + ", ".join(sorted(kalan)))
    return tpl


def dogrula(html):
    """Yayin oncesi statik kontroller."""
    sorun = []
    if "—" in html:
        sorun.append("em dash bulundu")
    if "text-transform:uppercase" in html:
        sorun.append("CSS uppercase bulundu (Turkce I tuzagi)")
    if "{{" in html:
        sorun.append("doldurulmamis yer tutucu")
    # gomulu <script> blogunu node ile denetle
    m = re.search(r"<script>\n(.*)\n</script>\s*$", html, re.S)
    if m:
        try:
            proc = subprocess.run(["node", "--check", "-"], input=m.group(1),
                                  capture_output=True, text=True)
            if proc.returncode != 0:
                sorun.append("JS sozdizimi: " + proc.stderr.strip().splitlines()[-1])
        except FileNotFoundError:
            print("uyari: node bulunamadi, JS denetimi atlandi", file=sys.stderr)
    return sorun


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    cfg = json.load(open(sys.argv[1], encoding="utf-8"))
    html = build(cfg)
    sorun = dogrula(html)
    if sorun:
        raise SystemExit("DOGRULAMA BASARISIZ:\n  - " + "\n  - ".join(sorun))
    open(sys.argv[2], "w", encoding="utf-8").write(html)
    print("yazildi: %s (%d bayt)" % (sys.argv[2], len(html.encode())))
    print("dogrulama gecti. 45 kombinasyonu tarayin, sonra dosyayi tarayicida acin")
    print("veya Artifact araci varsa yayinlayin. Dosya kendi kendine yeter.")


if __name__ == "__main__":
    main()
