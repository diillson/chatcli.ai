#!/usr/bin/env python3
"""Charts of the LongMemEval page. Plain SVG, light and dark, English and
Portuguese:

- accuracy-r3: accuracy by type in the three rounds (page header);
- validation: the validation half in every full run (third round);
- accuracy-r2: accuracy by type, first against second round (second round);
- flips: what happened to the first round's misses (second round);
- flips-r3: what happened to the second round's misses (third round);
- history: every full run, all 500 and the validation half, with intervals
  (page header, monthly checks);
- types-history: accuracy by type across the full runs (monthly checks);
- cost-history: cost, tool calls, input and time per question (monthly checks);
- stability: the 500 questions across every published run (monthly checks);
- flips-<yyyy-mm>: the previous run's misses in that month's run.

Numbers come from evals/longmemeval/results/ in the chatcli repo. A new
monthly run is one more entry in RUNS, STABILITY recounted over all packs
and one more flips-<yyyy-mm> pair; the charts of earlier rounds (DATA,
THIRD, VALIDATION, FLIPS, FLIPS3) stay as they are, byte for byte.

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
# The second round's 27 misses in the third round: fixed, still wrong, new.
FLIPS3 = {"fixed": 13, "stayed": 14, "new": 7}  # 27 misses before, 21 now

TEXT = {
    "en": {
        "labels": {"user": "Facts the user said", "assistant": "Facts the assistant said",
                   "updates": "Knowledge updates", "temporal": "Temporal reasoning",
                   "preference": "Preferences", "multi": "Multi-session reasoning"},
        "title": "chatcli on LongMemEval-S — %d/500 = %s",
        "sub": "Accuracy by question type · validation half (260 never read): %d/%d = %s",
        "first": "First round (2026-10-20)", "final": "Second round, merged main (2026-10-22)",
        "third": "Third round, session search (2026-10-24)",
        "val_title": "Validation half: 260 questions never read while fixing chatcli",
        "val_sub": "Correct answers per full run · the base run of 2026-10-24 is main after the memory graph",
        "v1": "First round (2026-10-20)", "v2": "Second round, merged main (2026-10-22)",
        "v3base": "Main + memory graph (2026-10-24)", "v3": "+ session search (2026-10-24)",
        "flip3": {"flip_title": "What happened to the 27 second-round misses",
                  "flip_sub": "34 questions were wrong in at least one of the two rounds",
                  "row1": "Second round: 27 misses", "row2": "Third round: 21 misses",
                  "fixed": "13 fixed", "stayed": "14 still wrong", "new": "7 new"},
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
        "val_title": "Metade de validação: 260 perguntas nunca lidas durante as correções",
        "val_sub": "Respostas corretas por rodada completa · a base de 24/10 é a main depois do grafo de memória",
        "v1": "Primeira rodada (20/10/2026)", "v2": "Segunda rodada, main mergeada (22/10/2026)",
        "v3base": "Main + grafo de memória (24/10/2026)", "v3": "+ busca de sessões (24/10/2026)",
        "flip3": {"flip_title": "O que aconteceu com as 27 falhas da segunda rodada",
                  "flip_sub": "34 perguntas erraram em pelo menos uma das duas rodadas",
                  "row1": "Segunda rodada: 27 falhas", "row2": "Terceira rodada: 21 falhas",
                  "fixed": "13 corrigidas", "stayed": "14 continuam", "new": "7 novas"},
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


# ---------------------------------------------------------------------------
# Monthly checks. Every full run on main, in order; a new monthly run is one
# more entry in RUNS (plus STABILITY and a FLIPS pair recomputed from the
# packs). Per run: correct of 500, correct of the 260 validation questions,
# correct per DATA key, cost per question (answer + judge, US$), tool calls
# per question, input tokens per question (thousands), median seconds.
RUNS = [
    dict(key="r1", total=454, val=237, cost=0.087, tools=4.9, intok=71.3, secs=22.0,
         types={"user": 70, "assistant": 56, "updates": 74, "temporal": 117, "preference": 26, "multi": 111}),
    dict(key="r2", total=473, val=243, cost=0.101, tools=5.0, intok=77.6, secs=22.1,
         types={"user": 70, "assistant": 55, "updates": 77, "temporal": 123, "preference": 29, "multi": 119}),
    dict(key="r3base", total=475, val=240, cost=0.099, tools=4.7, intok=77.0, secs=19.2,
         types={"user": 69, "assistant": 55, "updates": 74, "temporal": 127, "preference": 27, "multi": 123}),
    dict(key="r3", total=479, val=247, cost=0.100, tools=3.4, intok=78.0, secs=20.2,
         types={"user": 70, "assistant": 56, "updates": 76, "temporal": 127, "preference": 28, "multi": 122}),
    dict(key="m2611", total=481, val=246, cost=0.102, tools=3.5, intok=78.6, secs=19.1,
         types={"user": 70, "assistant": 55, "updates": 77, "temporal": 127, "preference": 28, "multi": 124}),
]
TYPE_N = {"user": 70, "assistant": 56, "updates": 78, "temporal": 133, "preference": 30, "multi": 133}
TYPE_ORDER = ["user", "assistant", "updates", "temporal", "preference", "multi"]
# Each question across the six published packs (the five runs above plus the
# pre-merge run of 2026-10-22): right in all six, changed, wrong in all six.
STABILITY = {"user": (69, 1, 0), "assistant": (54, 2, 0), "updates": (71, 7, 0),
             "temporal": (111, 19, 3), "preference": (26, 3, 1), "multi": (103, 27, 3)}
STABILITY_RUNS = 6
# The 21 misses of 2026-10-24-session-search in the 2026-11-22 run.
FLIPS4 = {"fixed": 10, "stayed": 11, "new": 8}  # 21 misses before, 19 now

TEXT["en"].update({
    "run_date": {"r1": "Oct 20", "r2": "Oct 22", "r3base": "Oct 24", "r3": "Oct 24", "m2611": "Nov 22"},
    "run_tag": {"r1": "round 1", "r2": "round 2", "r3base": "+ graph", "r3": "+ search", "m2611": "v1.232.0"},
    "hist_title": "chatcli on LongMemEval-S, run after run",
    "hist_sub": "Correct answers per full run, with the 95% interval · latest: v1.232.0 on 2026-11-22",
    "hist_all": "All 500 questions", "hist_val": "Validation half (260 questions never read)",
    "types_title": "Accuracy by question type, run after run",
    "types_sub": "Five full runs, 2026-10-20 to 2026-11-22 (v1.232.0) · each panel from 80% to 100%",
    "questions": "%d questions",
    "cost_title": "What a question costs, run after run",
    "cost_sub": "Averages over the 500 questions of each full run · latest: v1.232.0 on 2026-11-22",
    "m_cost": "Cost per question (answer + judge)", "m_tools": "Tool calls per question",
    "m_intok": "Input tokens per question", "m_secs": "Median time per question",
    "f_cost": "$%.3f", "f_tools": "%.1f", "f_intok": "%.1fk", "f_secs": "%.1f s",
    "stab_title": "The 500 questions across six published runs",
    "stab_sub": "One square per question, grouped by type · 2026-10-20 to 2026-11-22",
    "stab_row": "%d of %d every run",
    "stab_always": "%d right in all six runs",
    "stab_flip": "%d changed between runs (product fixes and run-to-run variation)",
    "stab_never": "%d wrong in all six runs",
    "flip4": {"flip_title": "What happened to the 21 misses of the October run",
              "flip_sub": "29 questions were wrong in at least one of the two runs",
              "row1": "2026-10-24, session search: 21 misses", "row2": "2026-11-22, v1.232.0: 19 misses",
              "fixed": "10 now right", "stayed": "11 still wrong", "new": "8 new",
              "legend": "No change was aimed at these questions: both directions are run-to-run variation"},
})
TEXT["pt"].update({
    "run_date": {"r1": "20/10", "r2": "22/10", "r3base": "24/10", "r3": "24/10", "m2611": "22/11"},
    "run_tag": {"r1": "rodada 1", "r2": "rodada 2", "r3base": "+ grafo", "r3": "+ busca", "m2611": "v1.232.0"},
    "hist_title": "chatcli no LongMemEval-S, rodada após rodada",
    "hist_sub": "Respostas corretas por rodada completa, com o intervalo de 95% · mais recente: v1.232.0 em 22/11/2026",
    "hist_all": "Todas as 500 perguntas", "hist_val": "Metade de validação (260 perguntas nunca lidas)",
    "types_title": "Acurácia por tipo de pergunta, rodada após rodada",
    "types_sub": "Cinco rodadas completas, de 20/10 a 22/11/2026 (v1.232.0) · cada painel vai de 80% a 100%",
    "questions": "%d perguntas",
    "cost_title": "Quanto custa uma pergunta, rodada após rodada",
    "cost_sub": "Médias sobre as 500 perguntas de cada rodada completa · mais recente: v1.232.0 em 22/11/2026",
    "m_cost": "Custo por pergunta (resposta + juiz)", "m_tools": "Chamadas de ferramenta por pergunta",
    "m_intok": "Tokens de entrada por pergunta", "m_secs": "Tempo mediano por pergunta",
    "f_cost": "US$ %.3f", "f_tools": "%.1f", "f_intok": "%.1f mil", "f_secs": "%.1f s",
    "stab_title": "As 500 perguntas em seis rodadas publicadas",
    "stab_sub": "Um quadrado por pergunta, agrupado por tipo · de 20/10 a 22/11/2026",
    "stab_row": "%d de %d em todas",
    "stab_always": "%d certas nas seis rodadas",
    "stab_flip": "%d mudaram entre rodadas (correções no produto e variação entre rodadas)",
    "stab_never": "%d erradas nas seis rodadas",
    "flip4": {"flip_title": "O que aconteceu com as 21 falhas da rodada de outubro",
              "flip_sub": "29 perguntas erraram em pelo menos uma das duas rodadas",
              "row1": "24/10/2026, busca de sessões: 21 falhas", "row2": "22/11/2026, v1.232.0: 19 falhas",
              "fixed": "10 acertam", "stayed": "11 continuam", "new": "8 novas",
              "legend": "Nenhuma mudança mirou essas perguntas: os dois sentidos são variação entre rodadas"},
})
# "Changed between runs" in the stability grid. Validated with the dataviz
# palette checker against each surface, next to teal and red.
THEME["light"]["flip"] = "#6d5fd0"
THEME["dark"]["flip"] = "#8b7fe8"


def pct(a, b, dec):
    return ("%.1f%%" % (100 * a / b)).replace(".", dec)


def wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * (p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5
    return 100 * (c - m) / d, 100 * (c + m) / d


def svg_open(W, H, title, sub, c):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'font-family="Inter, -apple-system, Segoe UI, sans-serif" role="img" aria-label="{title}">',
            f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>',
            f'<text x="24" y="34" font-size="18" font-weight="600" fill="{c["ink"]}">{title}</text>',
            f'<text x="24" y="56" font-size="13" fill="{c["sub"]}">{sub}</text>']


def history(lang, mode):
    """Every full run: all 500 and the validation half, each with its 95%
    interval. The axis starts at 84% because the marks are points with
    intervals, not bars; the labels carry the exact values."""
    t, c = TEXT[lang], THEME[mode]
    W, H, dec = 760, 336, t["dec"]
    out = svg_open(W, H, t["hist_title"], t["hist_sub"], c)
    lo_axis, hi_axis, ptop, ph = 84.0, 100.0, 118, 140

    def ypos(v):
        return ptop + (hi_axis - v) / (hi_axis - lo_axis) * ph

    for p, (label, field, n) in enumerate(((t["hist_all"], "total", 500), (t["hist_val"], "val", 260))):
        px = 24 + p * 372
        out.append(f'<text x="{px}" y="88" font-size="13" font-weight="600" fill="{c["ink"]}">{label}</text>')
        for g in (85, 90, 95, 100):
            out.append(f'<line x1="{px + 34}" y1="{ypos(g):.1f}" x2="{px + 340}" y2="{ypos(g):.1f}" stroke="{c["track"]}" stroke-width="1"/>')
            out.append(f'<text x="{px + 28}" y="{ypos(g) + 4:.1f}" font-size="11" text-anchor="end" fill="{c["mute"]}">{g}%</text>')
        xs = [px + 66 + i * 62 for i in range(len(RUNS))]
        vals = [100 * r[field] / n for r in RUNS]
        path = " ".join(f'{"M" if i == 0 else "L"}{x},{ypos(v):.1f}' for i, (x, v) in enumerate(zip(xs, vals)))
        out.append(f'<path d="{path}" fill="none" stroke="{c["second"]}" stroke-width="2" stroke-linejoin="round"/>')
        for i, (r, x, v) in enumerate(zip(RUNS, xs, vals)):
            last = i == len(RUNS) - 1
            lo, hi = wilson(r[field], n)
            tip = f'{t["run_date"][r["key"]]} {t["run_tag"][r["key"]]}: {pct(r[field], n, dec)} ({r[field]}/{n})'
            out.append(f'<line x1="{x}" y1="{ypos(lo):.1f}" x2="{x}" y2="{ypos(hi):.1f}" stroke="{c["mute"]}" stroke-width="2" stroke-linecap="round"/>')
            out.append(f'<circle cx="{x}" cy="{ypos(v):.1f}" r="{6 if last else 4.5}" fill="{c["teal"]}" stroke="{c["bg"]}" stroke-width="2"><title>{tip}</title></circle>')
            out.append(f'<text x="{x}" y="{ypos(hi) - 8:.1f}" font-size="11.5" text-anchor="middle" font-weight="{"600" if last else "400"}" '
                       f'fill="{c["ink"] if last else c["mute"]}">{pct(r[field], n, dec)}</text>')
            by = ptop + ph + 22
            out.append(f'<text x="{x}" y="{by}" font-size="11.5" text-anchor="middle" font-weight="{"600" if last else "400"}" fill="{c["ink"] if last else c["sub"]}">{t["run_date"][r["key"]]}</text>')
            out.append(f'<text x="{x}" y="{by + 15}" font-size="10.5" text-anchor="middle" fill="{c["mute"]}">{t["run_tag"][r["key"]]}</text>')
            out.append(f'<text x="{x}" y="{by + 30}" font-size="10.5" text-anchor="middle" fill="{c["mute"]}">{r[field]}/{n}</text>')
    out.append("</svg>")
    return "\n".join(out)


def types_history(lang, mode):
    """Small multiples: one panel per question type, the five full runs."""
    t, c = TEXT[lang], THEME[mode]
    W, rows_h, dec = 760, 152, t["dec"]
    H = 84 + 2 * rows_h + 4
    out = svg_open(W, H, t["types_title"], t["types_sub"], c)
    lo_axis, ph = 80.0, 70
    for k, key in enumerate(TYPE_ORDER):
        px, py = 24 + (k % 3) * 244, 84 + (k // 3) * rows_h
        n = TYPE_N[key]
        ptop = py + 40

        def ypos(v):
            return ptop + (100.0 - v) / (100.0 - lo_axis) * ph

        out.append(f'<text x="{px}" y="{py + 12}" font-size="13" font-weight="600" fill="{c["ink"]}">{t["labels"][key]}</text>')
        out.append(f'<text x="{px}" y="{py + 27}" font-size="11" fill="{c["mute"]}">{t["questions"] % n}</text>')
        for g in (80, 90, 100):
            out.append(f'<line x1="{px + 30}" y1="{ypos(g):.1f}" x2="{px + 176}" y2="{ypos(g):.1f}" stroke="{c["track"]}" stroke-width="1"/>')
            out.append(f'<text x="{px + 25}" y="{ypos(g) + 4:.1f}" font-size="10.5" text-anchor="end" fill="{c["mute"]}">{g}%</text>')
        xs = [px + 40 + i * 32 for i in range(len(RUNS))]
        vals = [100 * r["types"][key] / n for r in RUNS]
        path = " ".join(f'{"M" if i == 0 else "L"}{x},{ypos(v):.1f}' for i, (x, v) in enumerate(zip(xs, vals)))
        out.append(f'<path d="{path}" fill="none" stroke="{c["teal"]}" stroke-width="2" stroke-linejoin="round"/>')
        for i, (r, x, v) in enumerate(zip(RUNS, xs, vals)):
            last = i == len(RUNS) - 1
            tip = f'{t["run_date"][r["key"]]} {t["run_tag"][r["key"]]}: {pct(r["types"][key], n, dec)} ({r["types"][key]}/{n})'
            out.append(f'<circle cx="{x}" cy="{ypos(v):.1f}" r="{5 if last else 3.5}" fill="{c["teal"]}" stroke="{c["bg"]}" stroke-width="2"><title>{tip}</title></circle>')
        out.append(f'<text x="{xs[-1] + 11}" y="{ypos(vals[-1]) + 4:.1f}" font-size="12" font-weight="600" fill="{c["ink"]}">{pct(RUNS[-1]["types"][key], n, dec)}</text>')
        out.append(f'<text x="{xs[0]}" y="{ptop + ph + 20}" font-size="10.5" text-anchor="middle" fill="{c["mute"]}">{t["run_date"]["r1"]} · {pct(RUNS[0]["types"][key], n, dec)}</text>')
        out.append(f'<text x="{xs[-1]}" y="{ptop + ph + 20}" font-size="10.5" text-anchor="middle" fill="{c["mute"]}">{t["run_date"][RUNS[-1]["key"]]}</text>')
    out.append("</svg>")
    return "\n".join(out)


def cost_history(lang, mode):
    """Small multiples: four per-question averages over the full runs. Bars
    start at zero; one panel per measure, so no scale is shared."""
    t, c = TEXT[lang], THEME[mode]
    W, rows_h, dec = 760, 172, t["dec"]
    H = 84 + 2 * rows_h
    out = svg_open(W, H, t["cost_title"], t["cost_sub"], c)
    for k, field in enumerate(("cost", "tools", "intok", "secs")):
        px, py = 24 + (k % 2) * 372, 84 + (k // 2) * rows_h
        base, maxh = py + 124, 78
        top = max(r[field] for r in RUNS)
        out.append(f'<text x="{px}" y="{py + 12}" font-size="13" font-weight="600" fill="{c["ink"]}">{t["m_" + field]}</text>')
        out.append(f'<line x1="{px}" y1="{base}" x2="{px + 340}" y2="{base}" stroke="{c["track"]}" stroke-width="1"/>')
        for i, r in enumerate(RUNS):
            last = i == len(RUNS) - 1
            x, h = px + 18 + i * 64, maxh * r[field] / top
            label = (t["f_" + field] % r[field]).replace(".", dec)
            tip = f'{t["run_date"][r["key"]]} {t["run_tag"][r["key"]]}: {label}'
            out.append(f'<path d="M{x},{base} v{-(h - 4):.1f} q0,-4 4,-4 h28 q4,0 4,4 v{h - 4:.1f} z" fill="{c["teal"] if last else c["first"]}"><title>{tip}</title></path>')
            out.append(f'<text x="{x + 18}" y="{base - h - 7:.1f}" font-size="11.5" text-anchor="middle" font-weight="{"600" if last else "400"}" '
                       f'fill="{c["ink"] if last else c["mute"]}">{label}</text>')
            out.append(f'<text x="{x + 18}" y="{base + 15}" font-size="10.5" text-anchor="middle" fill="{c["ink"] if last else c["mute"]}">{t["run_date"][r["key"]]}</text>')
            out.append(f'<text x="{x + 18}" y="{base + 28}" font-size="10" text-anchor="middle" fill="{c["mute"]}">{t["run_tag"][r["key"]]}</text>')
    out.append("</svg>")
    return "\n".join(out)


def stability(lang, mode):
    """One square per question: right in every published run, changed, or
    wrong in every one. Identity is carried by the legend and its counts."""
    t, c = TEXT[lang], THEME[mode]
    W, per_line, pitch, cell, x0 = 760, 45, 11, 9, 232
    body, y = [], 84
    for key in TYPE_ORDER:
        always, flip, never = STABILITY[key]
        n = always + flip + never
        cols = [c["teal"]] * always + [c["flip"]] * flip + [c["red"]] * never
        for i, col in enumerate(cols):
            body.append(f'<rect x="{x0 + (i % per_line) * pitch}" y="{y + (i // per_line) * pitch}" width="{cell}" height="{cell}" rx="2" fill="{col}"/>')
        body.append(f'<text x="220" y="{y + 9}" font-size="13" text-anchor="end" fill="{c["ink"]}">{t["labels"][key]}</text>')
        body.append(f'<text x="220" y="{y + 24}" font-size="11" text-anchor="end" fill="{c["mute"]}">{t["stab_row"] % (always, n)}</text>')
        y += max(-(-n // per_line) * pitch, 28) + 12
    tot = [sum(v[j] for v in STABILITY.values()) for j in range(3)]
    for j, (col, label) in enumerate(((c["teal"], t["stab_always"] % tot[0]), (c["flip"], t["stab_flip"] % tot[1]),
                                      (c["red"], t["stab_never"] % tot[2]))):
        body.append(f'<rect x="24" y="{y + 6 + j * 22}" width="12" height="12" rx="3" fill="{col}"/>')
        body.append(f'<text x="44" y="{y + 16 + j * 22}" font-size="12" fill="{c["sub"]}">{label}</text>')
    H = y + 6 + 3 * 22 + 8
    return "\n".join(svg_open(W, H, t["stab_title"], t["stab_sub"], c) + body + ["</svg>"])


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


def flips(lang, mode, counts=None, round_text=None):
    """Misses of one round in the next. Defaults: the first round's misses in
    the second round; counts/round_text draw another pair of rounds."""
    t, c = TEXT[lang], THEME[mode]
    if round_text:
        t = {**t, **t[round_text]}
    FLIPS = counts or globals()["FLIPS"]
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


# ---------------------------------------------------------------------------
# Same model, another harness: Claude Code 2.1.330 against chatcli v1.232.0,
# both on 2026-11-22 (results/2026-11-22-claude-code and results/2026-11-22).
# Per DATA key: both right, only chatcli, only Claude Code, neither.
VERSUS = {"user": (69, 1, 0, 0), "assistant": (55, 0, 1, 0), "updates": (72, 5, 1, 0),
          "temporal": (118, 9, 2, 4), "preference": (27, 1, 1, 1), "multi": (115, 9, 2, 7)}
VERSUS_TOTAL = {"chatcli": 481, "claude": 463}
# Per question: cost (US$, answer + judge), median seconds, tool calls.
VERSUS_COST = {"chatcli": dict(cost=0.102, secs=19.1, tools=3.5), "claude": dict(cost=0.046, secs=8.1, tools=2.0)}

TEXT["en"].update({
    "vs_chatcli": "chatcli v1.232.0", "vs_claude": "Claude Code 2.1.330",
    "vs_acc_title": "Same model, two harnesses: accuracy by question type",
    "vs_acc_sub": "LongMemEval-S, 500 questions, Claude Sonnet 5.5 answering and judging on both sides · 2026-11-22",
    "vs_grid_title": "The same 500 questions, answered by both",
    "vs_grid_sub": "One square per question, grouped by type · same model, same judge",
    "vs_both": "%d both right", "vs_only_chatcli": "%d only chatcli right",
    "vs_only_claude": "%d only Claude Code right", "vs_neither": "%d neither right",
    "vs_row": "%d apart",
    "vs_cost_title": "What each harness spends per question",
    "vs_cost_sub": "Averages over the 500 questions · Claude Code answers from the search lines, chatcli opens the sessions",
    "vs_m_cost": "Cost per question", "vs_m_secs": "Median time per question", "vs_m_tools": "Tool calls per question",
})
TEXT["pt"].update({
    "vs_chatcli": "chatcli v1.232.0", "vs_claude": "Claude Code 2.1.330",
    "vs_acc_title": "Mesmo modelo, dois harnesses: acurácia por tipo de pergunta",
    "vs_acc_sub": "LongMemEval-S, 500 perguntas, Claude Sonnet 5.5 respondendo e julgando nos dois lados · 22/11/2026",
    "vs_grid_title": "As mesmas 500 perguntas, respondidas pelos dois",
    "vs_grid_sub": "Um quadrado por pergunta, agrupado por tipo · mesmo modelo, mesmo juiz",
    "vs_both": "%d os dois acertaram", "vs_only_chatcli": "%d só o chatcli acertou",
    "vs_only_claude": "%d só o Claude Code acertou", "vs_neither": "%d nenhum acertou",
    "vs_row": "%d de diferença",
    "vs_cost_title": "Quanto cada harness gasta por pergunta",
    "vs_cost_sub": "Médias sobre as 500 perguntas · o Claude Code responde pelas linhas da busca, o chatcli abre as sessões",
    "vs_m_cost": "Custo por pergunta", "vs_m_secs": "Tempo mediano por pergunta", "vs_m_tools": "Ferramentas por pergunta",
})


def versus_accuracy(lang, mode):
    """Accuracy by type, the two agents side by side. Identity is carried by
    the legend and by the order (chatcli first), not by color alone."""
    t, c = TEXT[lang], THEME[mode]
    W, top, rowh, dec = 760, 92, 50, t["dec"]
    H = top + len(TYPE_ORDER) * rowh + 62
    out = svg_open(W, H, t["vs_acc_title"], t["vs_acc_sub"], c)
    x0, bw = 232, 330
    for i, key in enumerate(TYPE_ORDER):
        both, only_h, only_c, _ = VERSUS[key]
        n, y = TYPE_N[key], top + i * rowh
        out.append(f'<text x="220" y="{y + 15}" font-size="13" text-anchor="end" fill="{c["ink"]}">{t["labels"][key]}</text>')
        for j, (v, col, name) in enumerate(((both + only_h, c["teal"], t["vs_chatcli"]), (both + only_c, c["flip"], t["vs_claude"]))):
            by = y + j * 15
            out.append(f'<rect x="{x0}" y="{by}" width="{bw}" height="11" rx="3" fill="{c["track"]}"/>')
            out.append(f'<rect x="{x0}" y="{by}" width="{bw * v / n:.1f}" height="11" rx="3" fill="{col}">'
                       f'<title>{name}, {t["labels"][key]}: {pct(v, n, dec)} ({v}/{n})</title></rect>')
            out.append(f'<text x="{x0 + bw + 12}" y="{by + 10}" font-size="12" font-weight="{"600" if j == 0 else "400"}" '
                       f'fill="{c["ink"] if j == 0 else c["sub"]}">{pct(v, n, dec)}  ·  {v}/{n}</text>')
    ly = top + len(TYPE_ORDER) * rowh + 18
    for j, (col, name, tot) in enumerate(((c["teal"], t["vs_chatcli"], VERSUS_TOTAL["chatcli"]), (c["flip"], t["vs_claude"], VERSUS_TOTAL["claude"]))):
        out.append(f'<rect x="24" y="{ly + j * 22}" width="12" height="12" rx="3" fill="{col}"/>')
        out.append(f'<text x="44" y="{ly + j * 22 + 10}" font-size="12" fill="{c["sub"]}">{name}: {tot}/500 = {pct(tot, 500, dec)}</text>')
    out.append("</svg>")
    return "\n".join(out)


def versus_grid(lang, mode):
    """One square per question: both right, only one of them, neither."""
    t, c = TEXT[lang], THEME[mode]
    W, per_line, pitch, cell, x0 = 760, 45, 11, 9, 232
    body, y = [], 84
    for key in TYPE_ORDER:
        both, only_h, only_c, neither = VERSUS[key]
        n = both + only_h + only_c + neither
        cols = [c["first"]] * both + [c["teal"]] * only_h + [c["flip"]] * only_c + [c["red"]] * neither
        for i, col in enumerate(cols):
            body.append(f'<rect x="{x0 + (i % per_line) * pitch}" y="{y + (i // per_line) * pitch}" width="{cell}" height="{cell}" rx="2" fill="{col}"/>')
        body.append(f'<text x="220" y="{y + 9}" font-size="13" text-anchor="end" fill="{c["ink"]}">{t["labels"][key]}</text>')
        body.append(f'<text x="220" y="{y + 24}" font-size="11" text-anchor="end" fill="{c["mute"]}">{t["vs_row"] % (only_h + only_c)}</text>')
        y += max(-(-n // per_line) * pitch, 28) + 12
    tot = [sum(v[j] for v in VERSUS.values()) for j in range(4)]
    legend = ((c["first"], t["vs_both"] % tot[0]), (c["teal"], t["vs_only_chatcli"] % tot[1]),
              (c["flip"], t["vs_only_claude"] % tot[2]), (c["red"], t["vs_neither"] % tot[3]))
    for j, (col, label) in enumerate(legend):
        lx, ly = 24 + (j % 2) * 300, y + 6 + (j // 2) * 22
        body.append(f'<rect x="{lx}" y="{ly}" width="12" height="12" rx="3" fill="{col}"/>')
        body.append(f'<text x="{lx + 20}" y="{ly + 10}" font-size="12" fill="{c["sub"]}">{label}</text>')
    H = y + 6 + 2 * 22 + 8
    return "\n".join(svg_open(W, H, t["vs_grid_title"], t["vs_grid_sub"], c) + body + ["</svg>"])


def versus_cost(lang, mode):
    """Three measures per question, one panel each, bars from zero."""
    t, c = TEXT[lang], THEME[mode]
    W, H, dec = 760, 262, t["dec"]
    out = svg_open(W, H, t["vs_cost_title"], t["vs_cost_sub"], c)
    fmts = {"cost": t["f_cost"], "secs": t["f_secs"], "tools": t["f_tools"]}
    for k, field in enumerate(("cost", "secs", "tools")):
        px, py = 24 + k * 244, 84
        base, maxh = py + 124, 78
        top = max(v[field] for v in VERSUS_COST.values())
        out.append(f'<text x="{px}" y="{py + 12}" font-size="13" font-weight="600" fill="{c["ink"]}">{t["vs_m_" + field]}</text>')
        out.append(f'<line x1="{px}" y1="{base}" x2="{px + 212}" y2="{base}" stroke="{c["track"]}" stroke-width="1"/>')
        for i, (who, col) in enumerate((("chatcli", c["teal"]), ("claude", c["flip"]))):
            v = VERSUS_COST[who][field]
            x, h = px + 26 + i * 96, maxh * v / top
            label = (fmts[field] % v).replace(".", dec)
            out.append(f'<path d="M{x},{base} v{-(h - 4):.1f} q0,-4 4,-4 h48 q4,0 4,4 v{h - 4:.1f} z" fill="{col}"><title>{t["vs_" + who]}: {label}</title></path>')
            out.append(f'<text x="{x + 28}" y="{base - h - 7:.1f}" font-size="12" text-anchor="middle" font-weight="600" fill="{c["ink"]}">{label}</text>')
            out.append(f'<text x="{x + 28}" y="{base + 16}" font-size="11" text-anchor="middle" fill="{c["sub"]}">{t["vs_" + who].split(" ")[0] if who == "chatcli" else "Claude Code"}</text>')
    out.append("</svg>")
    return "\n".join(out)


def main():
    for lang in TEXT:
        for mode in THEME:
            (OUT / f"vs-claude-code-accuracy-{lang}-{mode}.svg").write_text(versus_accuracy(lang, mode) + "\n")
            (OUT / f"vs-claude-code-questions-{lang}-{mode}.svg").write_text(versus_grid(lang, mode) + "\n")
            (OUT / f"vs-claude-code-cost-{lang}-{mode}.svg").write_text(versus_cost(lang, mode) + "\n")
    for lang in TEXT:
        for mode in THEME:
            (OUT / f"accuracy-r2-{lang}-{mode}.svg").write_text(accuracy(lang, mode) + "\n")
            (OUT / f"flips-{lang}-{mode}.svg").write_text(flips(lang, mode) + "\n")
            (OUT / f"accuracy-r3-{lang}-{mode}.svg").write_text(accuracy3(lang, mode) + "\n")
            (OUT / f"validation-{lang}-{mode}.svg").write_text(validation(lang, mode) + "\n")
            (OUT / f"flips-r3-{lang}-{mode}.svg").write_text(flips(lang, mode, FLIPS3, "flip3") + "\n")
            (OUT / f"history-{lang}-{mode}.svg").write_text(history(lang, mode) + "\n")
            (OUT / f"types-history-{lang}-{mode}.svg").write_text(types_history(lang, mode) + "\n")
            (OUT / f"cost-history-{lang}-{mode}.svg").write_text(cost_history(lang, mode) + "\n")
            (OUT / f"stability-{lang}-{mode}.svg").write_text(stability(lang, mode) + "\n")
            (OUT / f"flips-2026-11-{lang}-{mode}.svg").write_text(flips(lang, mode, FLIPS4, "flip4") + "\n")
    print("wrote", len(TEXT) * len(THEME) * 10, "charts to", OUT)


if __name__ == "__main__":
    main()
