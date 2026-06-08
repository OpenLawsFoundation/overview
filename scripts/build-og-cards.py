#!/usr/bin/env python3
"""Generate per-page Open Graph share cards (1200x630) for the OLF site.

Run from the repo root. Writes static/img/og-card.png (home/default) and
static/img/og/<slug>.png for each content page. Static brand assets: regenerate
only when the page titles/taglines change. macOS system fonts.
"""
from PIL import Image, ImageDraw, ImageFont

NAVY = (27, 58, 94)
PAPER = (251, 250, 246)
MUTED = (173, 193, 217)
EYE = (139, 167, 201)
SER = "/System/Library/Fonts/Supplemental/Georgia.ttf"
SERB = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
MONO = "/System/Library/Fonts/Menlo.ttc"
W, H = 1200, 630
PAD = 90

# (output path, eyebrow, title, subtitle)
CARDS = [
    ("static/img/og-card.png", "",
     "An interoperability and provenance layer for the world's legislation.",
     "A profile of Akoma Ntoso, per-jurisdiction adapters, a semantic legal diff, and a conformance suite."),
    ("static/img/og/spec.png", "SPEC",
     "AKN4OLF: the profile",
     "A profile of Akoma Ntoso, plus the conformance suite every adapter must pass."),
    ("static/img/og/pipeline.png", "PIPELINE",
     "Adapters & ingest",
     "Turn official sources into validated Akoma Ntoso. Pass the suite, get published."),
    ("static/img/og/diff.png", "DIFF",
     "Semantic, type-aware diff",
     "What kind of change happened, not just that some bytes moved."),
    ("static/img/og/archive.png", "ARCHIVE",
     "The canonical corpus",
     "Legislation in Akoma Ntoso. Generated, not hand-edited. Public domain."),
    ("static/img/og/principles.png", "DESIGN PHILOSOPHY",
     "Principles",
     "Normalize metadata, never content. Profile, don't replace. Conformance over coordination."),
    ("static/img/og/contributors.png", "THE PEOPLE",
     "Contributors",
     "Who builds and maintains the Open Laws Foundation."),
]


def wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def tracked(draw, xy, text, font, fill, spacing):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + spacing


def make(out, eyebrow, title, subtitle):
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    d.rectangle([0, H - 10, W, H], fill=(15, 34, 58))

    mark = Image.open("static/img/olf-mark-light.webp").convert("RGBA").resize((92, 92), Image.LANCZOS)
    img.paste(mark, (PAD, 70), mark)
    d.text((PAD + 114, 82), "Open Laws Foundation", font=ImageFont.truetype(SERB, 33), fill=PAPER)
    d.text((PAD + 116, 125), "interoperability & provenance for legislation",
           font=ImageFont.truetype(SER, 20), fill=MUTED)

    y = 232
    if eyebrow:
        tracked(d, (PAD, y), eyebrow, ImageFont.truetype(SERB, 22), EYE, 3)
        y += 50

    fh = ImageFont.truetype(SER, 58 if len(title) > 22 else 66)
    for ln in wrap(d, title, fh, W - 2 * PAD):
        d.text((PAD, y), ln, font=fh, fill=PAPER)
        y += fh.size + 12

    if subtitle:
        y += 14
        fs = ImageFont.truetype(SER, 28)
        for ln in wrap(d, subtitle, fs, W - 2 * PAD)[:2]:
            d.text((PAD, y), ln, font=fs, fill=MUTED)
            y += 40

    fm = ImageFont.truetype(MONO, 26)
    d.text((PAD, H - 76), "openlawsfoundation.org", font=fm, fill=PAPER)
    fid = ImageFont.truetype(MONO, 22)
    idtxt = "olf:it/legge/2019/123"
    d.text((W - PAD - d.textlength(idtxt, font=fid), H - 72), idtxt, font=fid, fill=MUTED)

    img.save(out, optimize=True)
    print("wrote", out)


if __name__ == "__main__":
    import os
    os.makedirs("static/img/og", exist_ok=True)
    for c in CARDS:
        make(*c)
