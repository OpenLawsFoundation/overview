---
title: "Pipeline — adapters & ingest"
eyebrow: "pipeline"
description: "Per-jurisdiction adapters and the ingest → validate → publish workflow that turns official sources into validated Akoma Ntoso."
lede: "The pipeline is where official, already-published legal data becomes validated Akoma Ntoso. One adapter per jurisdiction, one shared workflow, one definition of done: pass the conformance suite."
repo: "pipeline"
---

## What the pipeline does

We don't invent a corpus. We build the machinery that lets anyone take their own
jurisdiction's *already-published* legal data and turn it into a common, verifiable,
interoperable form, then keep it that way as the law changes.

The pipeline is that machinery. Three stages, one per jurisdiction.

### 1. Ingest

An **adapter** reads the official source: a national gazette feed, an open-data portal, a
bulk export, whatever that country actually publishes. Adapters are thin on purpose. Each
one knows the quirks of exactly one source and nothing else.

### 2. Validate

The adapter emits Akoma Ntoso that conforms to [AKN4OLF](/spec/), and the pipeline runs it
against the [conformance suite](/spec/#the-conformance-suite). Output that fails doesn't get
published. There is no "mostly correct" tier. That single rule is what keeps adapters
written by people who have never met interoperable.

### 3. Publish

What passes flows into the [`archive`](/archive/), addressed by its stable
[OLF identifier](/spec/#1-identity) and carrying its normalized
[temporal metadata](/spec/#2-time) and [citation graph](/spec/#3-citations).

## Provenance, not scraping

Every document the pipeline emits records where it came from and how it was built. The goal
isn't to own *a* copy of the law. It's to produce a copy whose lineage back to the official
source is explicit, and reproducible: re-run the pipeline, get the same bytes. That is the
whole difference between a scraped dump and a provenance layer.

## Adding a jurisdiction

An adapter is a self-contained piece of work. Read one official source, emit AKN4OLF, pass
the suite. You don't coordinate with other jurisdictions and you don't ask permission. The
suite is the gatekeeper, not a committee.

Maintain legal data for a jurisdiction and want it here? Open an issue in
[`pipeline`](https://github.com/OpenLawsFoundation/pipeline/issues).

## Status

Early. The first two adapters are **Italy** and **France**: two civil-law systems, two very
different gazettes. We picked them to find out whether one model really holds across more
than one legal tradition before we claim it's general.
