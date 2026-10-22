#!/usr/bin/env python3
"""Charts of the LongMemEval page, second round: accuracy by type against the
first round, and what happened to the first round's misses. Plain SVG, light
and dark, English and Portuguese. Numbers come from
evals/longmemeval/results/2026-10-20 and 2026-10-22-merged in the chatcli repo;
edit DATA when a new run lands.

    python3 scripts/gen-longmemeval-charts.py
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "images" / "longmemeval"

# (key, first round pass, final pass, total)
DATA = [
    ("user", 70, 70, 70),
    ("assistant", 56, 55, 56),
    ("updates", 74, 77, 78),
    ("temporal", 117, 123, 133),
    ("preference", 26, 29, 30),
    ("multi", 111, 119, 133),
]
FIRST_TOTAL, FINAL_TOTAL = 454, 473
VAL_PASS, VAL_TOTAL = 243, 260
FLIPS = {"fixed": 27, "stayed": 19, "new": 8}  # 46 misses before, 27 now

TEXT = {
    "en": {
        "labels": {"user": "Facts the user said", "assistant": "Facts the assistant said",
                   "updates": "Knowledge updates", "temporal": "Temporal reasoning",
                   "preference": "Preferences", "multi": "Multi-session reasoning"},
        "title": "chatcli on LongMemEval-S — %d/500 = %s",
        "sub": "Accuracy by question type · validation half (260 never read): %d/%d = %s",
        "first": "First round (2026-10-20)", "final": "Second round, merged main (2026-10-22)",
        "flip_title": "What happened to the 46 first-round misses",
        "flip_sub": "54 questions were wrong in at least one of the two rounds",
        "row1": "First round: 46 misses", "row2": "Now: 27 misses",
        "fixed": "27 fixed", "stayed": "19 still wrong", "new": "8 new",
        "legend": "fixed = wrong then, right now · new = right then, wrong now",
        "dec": ".",
    },
    "pt": {
        "labels": {"user": "Fatos ditos pelo usuário", "assistant": "Fatos ditos pelo assistente",
                   "updates": "Fatos atualizados", "temporal": "Raciocínio temporal",
                   "preference": "Preferências", "multi": "Várias sessões"},
        "title": "chatcli no LongMemEval-S — %d/500 = %s",
        "sub": "Acurácia por tipo · metade de validação (260 nunca lidas): %d/%d = %s",
        "first": "Primeira rodada (20/10/2026)", "final": "Segunda rodada, main mergeada (22/10/2026)",
        "flip_title": "O que aconteceu com as 46 falhas da primeira rodada",
        "flip_sub": "54 perguntas erraram em pelo menos uma das duas rodadas",
        "row1": "Primeira rodada: 46 falhas", "row2": "Agora: 27 falhas",
        "fixed": "27 corrigidas", "stayed": "19 continuam", "new": "8 novas",
        "legend": "corrigida = errava, acerta agora · nova = acertava, errou agora",
        "dec": ",",
    },
}

THEME = {
    "light": dict(bg="#F7F7F5", ink="#17171a", sub="#46464e", mute="#6b6b74", track="#e4e3df",
                  teal="#0d9488", first="#aeb9b6", red="#e5533d", new="#17171a", onfill="#ffffff"),
    "dark": dict(bg="#0E0F10", ink="#ededed", sub="#bcbcc4", mute="#8b8b94", track="#24262a",
                 teal="#16a394", first="#4a5a57", red="#e05a45", new="#ededed", onfill="#0E0F10"),
}


def pct(a, b, dec):
    return ("%.1f%%" % (100 * a / b)).replace(".", dec)


def accuracy(lang, mode):
    t, c = TEXT[lang], THEME[mode]
    W, top, rowh = 760, 92, 50
    H = top + len(DATA) * rowh + 62
    dec = t["dec"]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'font-family="Inter, -apple-system, Segoe UI, sans-serif" role="img" '
           f'aria-label="{t["title"] % (FINAL_TOTAL, pct(FINAL_TOTAL, 500, dec))}">',
           f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>',
           f'<text x="24" y="34" font-size="18" font-weight="600" fill="{c["ink"]}">'
           f'{t["title"] % (FINAL_TOTAL, pct(FINAL_TOTAL, 500, dec))}</text>',
           f'<text x="24" y="56" font-size="13" fill="{c["sub"]}">'
           f'{t["sub"] % (VAL_PASS, VAL_TOTAL, pct(VAL_PASS, VAL_TOTAL, dec))}</text>']
    x0, bw = 232, 330
    for i, (key, a, b, n) in enumerate(sorted(DATA, key=lambda r: -r[2] / r[3])):
        y = top + i * rowh
        out.append(f'<text x="220" y="{y + 15}" font-size="13" text-anchor="end" fill="{c["ink"]}">{t["labels"][key]}</text>')
        for j, (v, col) in enumerate(((a, c["first"]), (b, c["teal"]))):
            by = y + j * 15
            out.append(f'<rect x="{x0}" y="{by}" width="{bw}" height="11" rx="3" fill="{c["track"]}"/>')
            out.append(f'<rect x="{x0}" y="{by}" width="{bw * v / n:.1f}" height="11" rx="3" fill="{col}">'
                       f'<title>{t["labels"][key]}: {pct(v, n, dec)} ({v}/{n})</title></rect>')
            weight = "600" if j else "400"
            fill = c["ink"] if j else c["mute"]
            out.append(f'<text x="{x0 + bw + 12}" y="{by + 10}" font-size="12" font-weight="{weight}" fill="{fill}">'
                       f'{pct(v, n, dec)}  ·  {v}/{n}</text>')
    ly = top + len(DATA) * rowh + 18
    out.append(f'<rect x="24" y="{ly}" width="12" height="12" rx="3" fill="{c["first"]}"/>')
    out.append(f'<text x="44" y="{ly + 10}" font-size="12" fill="{c["sub"]}">{t["first"]}: {FIRST_TOTAL}/500 = {pct(FIRST_TOTAL, 500, dec)}</text>')
    out.append(f'<rect x="24" y="{ly + 22}" width="12" height="12" rx="3" fill="{c["teal"]}"/>')
    out.append(f'<text x="44" y="{ly + 32}" font-size="12" fill="{c["sub"]}">{t["final"]}: {FINAL_TOTAL}/500 = {pct(FINAL_TOTAL, 500, dec)}</text>')
    out.append("</svg>")
    return "\n".join(out)


def flips(lang, mode):
    t, c = TEXT[lang], THEME[mode]
    W, H, unit = 760, 262, 10.0
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'font-family="Inter, -apple-system, Segoe UI, sans-serif" role="img" aria-label="{t["flip_title"]}">',
           f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>',
           f'<text x="24" y="34" font-size="18" font-weight="600" fill="{c["ink"]}">{t["flip_title"]}</text>',
           f'<text x="24" y="56" font-size="13" fill="{c["sub"]}">{t["flip_sub"]}</text>']
    x0 = 24

    def seg(x, y, n, col, label, textcol):
        w = n * unit
        s = (f'<rect x="{x}" y="{y}" width="{w:.1f}" height="44" rx="5" fill="{col}"><title>{label}</title></rect>'
             f'<text x="{x + w / 2:.1f}" y="{y + 27}" font-size="13" font-weight="600" text-anchor="middle" fill="{textcol}">{label}</text>')
        return s, x + w + 3

    y1, y2 = 92, 158
    out.append(f'<text x="{x0}" y="{y1 - 8}" font-size="12" fill="{c["mute"]}">{t["row1"]}</text>')
    s, x = seg(x0, y1, FLIPS["fixed"], c["teal"], t["fixed"], c["onfill"]); out.append(s)
    s, x = seg(x, y1, FLIPS["stayed"], c["red"], t["stayed"], "#ffffff"); out.append(s)
    out.append(f'<text x="{x0}" y="{y2 - 8}" font-size="12" fill="{c["mute"]}">{t["row2"]}</text>')
    s, x = seg(x0 + FLIPS["fixed"] * unit + 3, y2, FLIPS["stayed"], c["red"], t["stayed"], "#ffffff"); out.append(s)
    s, x = seg(x, y2, FLIPS["new"], c["new"], t["new"], c["onfill"]); out.append(s)
    out.append(f'<text x="24" y="{H - 28}" font-size="12" fill="{c["sub"]}">{t["legend"]}</text>')
    out.append("</svg>")
    return "\n".join(out)


def main():
    for lang in TEXT:
        for mode in THEME:
            (OUT / f"accuracy-r2-{lang}-{mode}.svg").write_text(accuracy(lang, mode) + "\n")
            (OUT / f"flips-{lang}-{mode}.svg").write_text(flips(lang, mode) + "\n")
    print("wrote", len(TEXT) * len(THEME) * 2, "charts to", OUT)


if __name__ == "__main__":
    main()
