#!/usr/bin/env python3
"""Charts of the LongMemEval page. Plain SVG, light and dark, English and
Portuguese:

- accuracy-r3: accuracy by type in the three rounds (page header);
- validation: the validation half in every full run (third round);
- accuracy-r2: accuracy by type, first against second round (second round);
- flips: what happened to the first round's misses (second round).

Numbers come from evals/longmemeval/results/ in the chatcli repo
(2026-10-20, 2026-10-22-merged, 2026-10-24, 2026-10-24-session-search);
add a column to DATA and a row to VALIDATION when a new run lands.

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

# Third round (2026-10-24-session-search): pass per DATA key, and totals.
THIRD = {"user": 70, "assistant": 56, "updates": 76, "temporal": 127, "preference": 28, "multi": 122}
THIRD_TOTAL, THIRD_VAL = 479, 247
# Validation half (260) in every full run, in order.
VALIDATION = [("v1", 237), ("v2", 243), ("v3base", 240), ("v3", 247)]

TEXT = {
    "en": {
        "labels": {"user": "Facts the user said", "assistant": "Facts the assistant said",
                   "updates": "Knowledge updates", "temporal": "Temporal reasoning",
                   "preference": "Preferences", "multi": "Multi-session reasoning"},
        "title": "chatcli on LongMemEval-S — %d/500 = %s",
        "sub": "Accuracy by question type · validation half (260 never read): %d/%d = %s",
        "first": "First round (2026-10-20)", "final": "Second round, merged main (2026-10-22)",
        "third": "Third round, session search (2026-10-24)",
        "val_title": "Validation half: 260 questions never read while tuning",
        "val_sub": "Correct answers per full run · the base run of 2026-10-24 is main after the memory graph",
        "v1": "First round (2026-10-20)", "v2": "Second round, merged main (2026-10-22)",
        "v3base": "Main + memory graph (2026-10-24)", "v3": "+ session search (2026-10-24)",
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
        "third": "Terceira rodada, busca de sessões (24/10/2026)",
        "val_title": "Metade de validação: 260 perguntas nunca lidas durante o ajuste",
        "val_sub": "Respostas corretas por rodada completa · a base de 24/10 é a main depois do grafo de memória",
        "v1": "Primeira rodada (20/10/2026)", "v2": "Segunda rodada, main mergeada (22/10/2026)",
        "v3base": "Main + grafo de memória (24/10/2026)", "v3": "+ busca de sessões (24/10/2026)",
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
                  teal="#0d9488", first="#aeb9b6", red="#e5533d", new="#17171a", onfill="#ffffff",
                  second="#7fc3ba"),
    "dark": dict(bg="#0E0F10", ink="#ededed", sub="#bcbcc4", mute="#8b8b94", track="#24262a",
                 teal="#16a394", first="#4a5a57", red="#e05a45", new="#ededed", onfill="#0E0F10",
                 second="#2f7d73"),
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


def accuracy3(lang, mode):
    """Accuracy by type in the three rounds; the third round is emphasized."""
    t, c = TEXT[lang], THEME[mode]
    W, top, rowh = 760, 92, 64
    H = top + len(DATA) * rowh + 84
    dec = t["dec"]
    title = t["title"] % (THIRD_TOTAL, pct(THIRD_TOTAL, 500, dec))
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'font-family="Inter, -apple-system, Segoe UI, sans-serif" role="img" aria-label="{title}">',
           f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>',
           f'<text x="24" y="34" font-size="18" font-weight="600" fill="{c["ink"]}">{title}</text>',
           f'<text x="24" y="56" font-size="13" fill="{c["sub"]}">'
           f'{t["sub"] % (THIRD_VAL, VAL_TOTAL, pct(THIRD_VAL, VAL_TOTAL, dec))}</text>']
    x0, bw = 232, 330
    for i, (key, a, b, n) in enumerate(sorted(DATA, key=lambda r: -THIRD[r[0]] / r[3])):
        y = top + i * rowh
        out.append(f'<text x="220" y="{y + 23}" font-size="13" text-anchor="end" fill="{c["ink"]}">{t["labels"][key]}</text>')
        for j, (v, col) in enumerate(((a, c["first"]), (b, c["second"]), (THIRD[key], c["teal"]))):
            by = y + j * 15
            last = j == 2
            out.append(f'<rect x="{x0}" y="{by}" width="{bw}" height="11" rx="3" fill="{c["track"]}"/>')
            out.append(f'<rect x="{x0}" y="{by}" width="{bw * v / n:.1f}" height="11" rx="3" fill="{col}">'
                       f'<title>{t["labels"][key]}: {pct(v, n, dec)} ({v}/{n})</title></rect>')
            out.append(f'<text x="{x0 + bw + 12}" y="{by + 10}" font-size="12" font-weight="{"600" if last else "400"}" '
                       f'fill="{c["ink"] if last else c["mute"]}">{pct(v, n, dec)}  ·  {v}/{n}</text>')
    ly = top + len(DATA) * rowh + 4
    for k, (label, total, col) in enumerate(((t["first"], FIRST_TOTAL, c["first"]),
                                             (t["final"], FINAL_TOTAL, c["second"]),
                                             (t["third"], THIRD_TOTAL, c["teal"]))):
        out.append(f'<rect x="24" y="{ly + k * 22}" width="12" height="12" rx="3" fill="{col}"/>')
        out.append(f'<text x="44" y="{ly + k * 22 + 10}" font-size="12" fill="{c["sub"]}">{label}: {total}/500 = {pct(total, 500, dec)}</text>')
    out.append("</svg>")
    return "\n".join(out)


def validation(lang, mode):
    """The validation half in every full run. Full scale on purpose: a cut
    axis would make a few questions look like a large gap; the labels carry
    the exact counts."""
    t, c = TEXT[lang], THEME[mode]
    W, top, step, x0, bw = 760, 84, 34, 300, 300
    H = top + len(VALIDATION) * step + 8
    dec = t["dec"]
    cols = {"v1": c["first"], "v2": c["second"], "v3base": c["first"], "v3": c["teal"]}
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'font-family="Inter, -apple-system, Segoe UI, sans-serif" role="img" aria-label="{t["val_title"]}">',
           f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>',
           f'<text x="24" y="34" font-size="18" font-weight="600" fill="{c["ink"]}">{t["val_title"]}</text>',
           f'<text x="24" y="56" font-size="13" fill="{c["sub"]}">{t["val_sub"]}</text>']
    for i, (key, v) in enumerate(VALIDATION):
        y = top + i * step
        last = i == len(VALIDATION) - 1
        label = f"{pct(v, VAL_TOTAL, dec)}  ·  {v}/{VAL_TOTAL}"
        out.append(f'<text x="{x0 - 12}" y="{y + 13}" font-size="13" text-anchor="end" fill="{c["ink"]}">{t[key]}</text>')
        out.append(f'<rect x="{x0}" y="{y}" width="{bw}" height="18" rx="3" fill="{c["track"]}"/>')
        out.append(f'<rect x="{x0}" y="{y}" width="{bw * v / VAL_TOTAL:.1f}" height="18" rx="3" fill="{cols[key]}">'
                   f'<title>{t[key]}: {label}</title></rect>')
        out.append(f'<text x="{x0 + bw + 12}" y="{y + 13}" font-size="12" font-weight="{"600" if last else "400"}" '
                   f'fill="{c["ink"] if last else c["mute"]}">{label}</text>')
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
            (OUT / f"accuracy-r3-{lang}-{mode}.svg").write_text(accuracy3(lang, mode) + "\n")
            (OUT / f"validation-{lang}-{mode}.svg").write_text(validation(lang, mode) + "\n")
    print("wrote", len(TEXT) * len(THEME) * 4, "charts to", OUT)


if __name__ == "__main__":
    main()
