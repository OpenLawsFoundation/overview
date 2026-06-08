---
title: "Pipeline — adapters & ingest"
eyebrow: "pipeline"
description: "Per-jurisdiction adapters and the ingest → validate → publish workflow that turns official sources into validated Akoma Ntoso."
lede: "The pipeline is where official, already-published legal data becomes validated Akoma Ntoso. One adapter per jurisdiction, one shared workflow, one definition of done: pass the conformance suite."
repo: "pipeline"
---

## What the pipeline does

The Open Laws Foundation does not invent a corpus. It defines the machinery that lets
anyone turn their own jurisdiction's *already-published* legal data into a common,
verifiable, interoperable form — and keep it that way over time.

The pipeline is that machinery. For each jurisdiction it runs three stages:

### 1. Ingest

An **adapter** reads the jurisdiction's official source — a national gazette feed, an open
data portal, a bulk export — in whatever format that source happens to publish. Adapters
are deliberately thin and jurisdiction-specific: they know one source's quirks and nothing
else.

### 2. Validate

The adapter emits Akoma Ntoso conforming to [AKN4OLF](/spec/). The pipeline validates that
output against the [conformance suite](/spec/#the-conformance-suite). Output that does not
pass is not published — there is no "mostly correct" tier. This is what keeps adapters
written by people who have never met each other interoperable.

### 3. Publish

Validated documents flow into the [`archive`](/archive/), addressed by their stable
[OLF identifier](/spec/#1-identity) and carrying their normalized
[temporal metadata](/spec/#2-time) and [citation graph](/spec/#3-citations).

## Provenance, not scraping

Every document the pipeline publishes records where it came from and how it was produced.
The point is not to have *a* copy of the law — it is to have a copy whose lineage back to
the official source is explicit and reproducible. Re-run the pipeline, get the same result.

That is the difference between a scraped dump and a provenance layer.

## Adding a jurisdiction

An adapter is a contained piece of work: read one official source, emit AKN4OLF, pass the
suite. You do not need to coordinate with other jurisdictions, and you do not need
permission — the conformance suite is the gatekeeper, not a committee.

If you maintain legal data for a jurisdiction and want it represented here, open an issue
in [`pipeline`](https://github.com/OpenLawsFoundation/pipeline/issues).

## Status

Early. The first adapters under construction are **Italy** and **France** — two civil-law
systems with different gazettes — chosen to prove the model holds across more than one
legal tradition before it claims to be general.
