---
title: "Principles"
eyebrow: "design philosophy"
description: "The design philosophy of the Open Laws Foundation: normalize metadata, never content; profile, don't replace; conformance over coordination."
lede: "A few load-bearing decisions hold this whole project up. They're deliberately conservative. The usual way these projects die is too much ambition, not too little."
---

## 1. Normalize metadata, never content

This is the rule everything else follows from. Legal content does not normalize across
jurisdictions, and the projects that try to force it either collapse into a useless lowest
common denominator or balloon into an unmaintainable schema with a field for every national
exception.

So we draw a hard line. **Identity, time, and citations** are normalized, because every
legal system has a *when*, a *what-is-named-what*, and a *who-cites-whom*. Everything else,
the substantive structure and the text, stays native, in the jurisdiction's own
[Akoma Ntoso](https://www.oasis-open.org/standard/akn-v1-0/) profile.

<div class="callout rule"><span class="callout-label">The test</span>
If two lawyers from two countries would <strong>argue</strong> about how to model it, it's
content, so leave it native. If they <strong>agree</strong> it exists in both systems, it's
metadata, so normalize it.</div>

## 2. A profile, not a replacement

We're not inventing a format. AKN4OLF is a *profile* of Akoma Ntoso, the OASIS standard, in
exactly the sense that AKN4EU, AKN4UN, and AKN4Africa are profiles. We speak the language the
EU, the UN, and national gazettes already speak. We don't try to replace Akoma Ntoso, ELI, or
any national system.

A new format asks the whole world to come to you. A profile lets you meet the world where it
already is.

## 3. Conformance over coordination

The [conformance suite](/spec/#the-conformance-suite) is the project's coordination
mechanism. An adapter is correct when it passes the suite, not when a committee approves
it. This is what lets contributors who have never met, working on jurisdictions that share
nothing, produce interoperable output.

The spec is executable. Interoperability is checkable. That is the only way this scales.

## 4. Provenance over possession

The goal is not to own *a* copy of the law. It is to produce copies whose lineage back to
the official source is explicit and reproducible. Re-run the [pipeline](/pipeline/), get the
same [archive](/archive/). Nothing is hand-edited; corrections go into the adapter, never
the output.

## 5. Honest about what we are

This is an open-source project. It is **not** an incorporated legal entity. We don't solicit
or accept donations on behalf of a "foundation" that doesn't exist as a legal body. The name
describes the work, not a fundraising vehicle.

And we're early. Italy and France exist to *prove* the model across two legal traditions
before anyone claims it's general. We'd rather say "early" out loud than oversell coverage we
don't have yet.

---

If these principles describe a project you want to exist, the best contribution is an
adapter. Start at the [spec](/spec/), then open an issue in
[`pipeline`](https://github.com/OpenLawsFoundation/pipeline/issues).
