"""WCAG kontrast hesabı ve ton düzeltmesi."""


def to_rgb(c):
    c = c.strip()
    if c.startswith("#"):
        h = c[1:]
        if len(h) == 3:
            h = "".join(ch * 2 for ch in h)
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    nums = [float(n) for n in __import__("re").findall(r"[\d.]+", c)]
    return tuple(int(n) for n in nums[:3])


def to_hex(rgb):
    return "#%02X%02X%02X" % tuple(max(0, min(255, int(round(v)))) for v in rgb)


def luminance(c):
    def ch(v):
        v /= 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(v) for v in to_rgb(c))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def fix(fg, bg, target=4.5, step=0.06):
    """fg'yi bg'den uzaklastirarak hedef kontrasta getirir. (renk, oran, degisti) doner."""
    if ratio(fg, bg) >= target:
        return to_hex(to_rgb(fg)), round(ratio(fg, bg), 2), False
    darken = luminance(bg) > luminance(fg)
    rgb = list(to_rgb(fg))
    for _ in range(40):
        rgb = [v * (1 - step) if darken else v + (255 - v) * step for v in rgb]
        if ratio(to_hex(rgb), bg) >= target:
            break
    return to_hex(rgb), round(ratio(to_hex(rgb), bg), 2), True


def audit(tones):
    """[{'ad','zemin','ink','sub'}] -> rapor listesi."""
    out = []
    for t in tones:
        ink, r_ink, f_ink = fix(t["ink"], t["zemin"])
        sub, r_sub, f_sub = fix(t["sub"], t["zemin"])
        out.append({
            "ad": t["ad"], "zemin": t["zemin"],
            "ink": ink, "ink_orani": r_ink, "ink_duzeltildi": f_ink,
            "sub": sub, "sub_orani": r_sub, "sub_duzeltildi": f_sub,
            "gecti": r_ink >= 4.5 and r_sub >= 4.5,
        })
    return out


if __name__ == "__main__":
    import json, sys
    raw = "" if sys.stdin.isatty() else sys.stdin.read().strip()
    data = json.loads(raw) if raw else [
        {"ad": "Koyu kontrast", "zemin": "#164193", "ink": "#FFFFFF", "sub": "#C6D3EA"},
        {"ad": "Marka tinti", "zemin": "#FDFBE3", "ink": "#253342", "sub": "#5F6B76"},
        {"ad": "Minimal", "zemin": "#FFFFFF", "ink": "#253342", "sub": "#5F6B76"},
    ]
    print(json.dumps(audit(data), ensure_ascii=False, indent=1))
