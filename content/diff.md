---
title: "Diff: semantic and type-aware"
eyebrow: "diff"
description: "A semantic differ and changeset model that understands Akoma Ntoso. It tells you what kind of change happened, not just that some bytes moved."
lede: "A text diff tells you that bytes moved. For legislation that is almost useless. The OLF differ understands Akoma Ntoso structure, so it tells you what kind of change happened: a substantive amendment, a change to entry into force, or a cosmetic fix."
repo: "diff"
---

## Why a normal diff isn't enough

Run `diff` on two versions of an act and you get added and removed lines. A lawyer, a
journalist, or a downstream system does not care that line 412 moved. They care what kind
of change it was. Did the substantive text of an article change? Did the entry into force
shift? Or was it just a typo fix, a renumbering, a formatting cleanup?

Those three things have nothing in common except that the bytes are different. A line-based
diff throws them all in the same pile. Ours doesn't.

## Type-aware change classification

Because the differ works on Akoma Ntoso structure instead of raw text, it knows what each
node *is*. So it classifies a change by the element it touches and the edit it represents:

- **Text amendment.** The normative content of a provision changed.
- **Temporal change.** A date in the [`lifecycle`](/spec/#2-time) moved: enactment, entry
  into force, repeal.
- **Structural change.** An article was inserted, moved, or renumbered.
- **Citation change.** A [reference](/spec/#3-citations) was added, removed, or re-targeted.
- **Cosmetic.** No normative effect at all.

The output is a **changeset**: a machine-readable account of what kind of change happened
between two states, addressed by [OLF identifier](/spec/#1-identity) right down to the
element.

## The changeset model

A changeset is a first-class object, not a rendering you read once and throw away. Store it,
query it, reason over it. "Every substantive amendment to this act since 2019." "Flag
temporal changes, ignore cosmetic ones." And because it speaks in OLF identifiers, a
changeset in Italy has the same shape as a changeset in France.

This is what turns the [archive](/archive/) from a snapshot into a history you can actually
interrogate.

## Status

Early. The classifier and the changeset model are being built next to the first two
jurisdictions in the [pipeline](/pipeline/), so the differ runs against real legislative
change from the start, not toy examples.
