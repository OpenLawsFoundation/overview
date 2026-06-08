---
title: "Diff — semantic, type-aware"
eyebrow: "diff"
description: "An Akoma Ntoso–aware semantic differ and changeset model. It tells you what kind of change happened, not just that some bytes moved."
lede: "A text diff tells you that bytes moved. For legislation that is almost useless. The OLF differ is Akoma Ntoso–aware: it tells you what kind of change happened — a substantive amendment, a change to entry into force, or a cosmetic fix."
repo: "diff"
---

## Why a normal diff is not enough

Run `diff` on two versions of an act and you get added and removed lines. But a lawyer,
a journalist, or a downstream system does not care that line 412 changed. They care
*which kind* of change it was:

- Did the **substantive text** of an article change?
- Did the **entry into force** move?
- Was it a **cosmetic** fix — a typo, a renumbering, a formatting normalization?

These have completely different consequences, and a line-based diff flattens them into one
undifferentiated pile of "changes". The OLF differ does not.

## Type-aware change classification

Because the differ operates on Akoma Ntoso structure rather than raw text, it knows what
each node *is*. A change is classified by the kind of element it touches and the kind of
edit it represents:

- **Text amendment** — the normative content of a provision changed.
- **Temporal change** — a date in the [`lifecycle`](/spec/#2-time) changed (enactment,
  entry into force, repeal).
- **Structural change** — an article was inserted, moved, or renumbered.
- **Citation change** — a [reference](/spec/#3-citations) was added, removed, or
  re-targeted.
- **Cosmetic** — a change with no normative effect.

The output is a **changeset**: a structured, machine-readable description of *what kind* of
change happened between two states, addressed by [OLF identifier](/spec/#1-identity) down
to the element level.

## The changeset model

A changeset is a first-class object, not a rendering. It can be stored, queried, and
reasoned about: "show me every substantive amendment to this act since 2019", or "flag
temporal changes, ignore cosmetic ones". Because it speaks in OLF identifiers, a changeset
in one jurisdiction has the same shape as a changeset in another.

This is the piece that turns the [archive](/archive/) from a snapshot into a history you
can interrogate.

## Status

Early — the changeset model and classifier are being built alongside the first two
jurisdictions in the [pipeline](/pipeline/), so the diff is exercised against real
legislative change from day one rather than synthetic examples.
