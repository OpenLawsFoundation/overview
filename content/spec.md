---
title: "AKN4OLF: the profile"
eyebrow: "spec"
image: "/img/og/spec.png"
description: "The Open Laws Foundation profile of Akoma Ntoso, plus the conformance suite every adapter must pass."
lede: "AKN4OLF is a profile of Akoma Ntoso (OASIS LegalDocML) plus the conformance suite that every Open Laws Foundation adapter must pass. It is the entry point to the project. Read this before the other repositories."
repo: "spec"
---

## The core principle

**We normalize metadata, not content.**

Legal *content* is not normalizable across jurisdictions, and trying to do it is how
this kind of project dies. An Italian *comma*, a U.S. *section*, and a French *article*
are not three names for the same object: they differ in granularity, hierarchy, and
citation rules. Force them into one schema and you either lose everything that makes
each jurisdiction useful (lowest common denominator) or build an unmaintainable monster
with a field for every national exception (highest common multiple).

Akoma Ntoso already solved this the right way: a shared vocabulary (`act`, `body`,
`article`, `ref`, `lifecycle`) that each jurisdiction *instantiates* on its own terms.
That is exactly why AKN4EU, AKN4UN, and AKN4Africa are **profiles, not translations**.
AKN4OLF is one more profile in that family.

So:

- **Content** stays in native Akoma Ntoso, in the jurisdiction's own profile. We never
  flatten it into a neutral schema.
- **Metadata and relationships** are normalized by AKN4OLF, because *every* legal system
  has a "when", a "what is named what", and a "who cites whom".

<div class="callout rule"><span class="callout-label">The rule, on your monitor</span>
If two lawyers from two countries would <strong>argue</strong> about how to model it, it's
content, so leave it native. If they <strong>agree</strong> it exists in both systems, it's
metadata, so normalize it. <em>Entry into force?</em> Exists everywhere → normalize.
<em>comma vs section structure?</em> They'd argue → native.</div>

## What AKN4OLF normalizes

Exactly three things. Nothing about the substantive text.

### 1. Identity

A uniform way to name and address an act across jurisdictions, layered over Akoma Ntoso's
native FRBR/URI identifiers. The OLF identifier is a stable, resolvable key:

```
olf:<jurisdiction>/<type>/<year>/<number>[/<eId>]

olf:it/legge/2019/123              # an Italian act
olf:it/legge/2019/123/art_3        # an element inside that act
olf:fr/loi/2016/1321               # a French act
```

The identifier never carries content. It is an address: it tells you *which* act and
*which* element, not what the element says.

### 2. Time

Legislation is not a document; it is a sequence of states. AKN4OLF normalizes the
*temporal* metadata every system shares (enactment, publication, entry into force,
amendment, repeal) onto Akoma Ntoso's `lifecycle` and `temporalData`, so that "the law
as it stood on a given date" is a well-defined query in every jurisdiction.

### 3. Citations

Who cites whom, and what kind of relationship the citation expresses: amends, repeals,
implements, refers to. Normalizing the *graph* of references (not the prose around them)
is what turns a pile of acts into a navigable body of law.

## The conformance suite

A profile is only as real as its tests. The suite defines what "correct" means so that
independent contributors stay interoperable **without ever talking to each other**. An
adapter for a new jurisdiction is "done" when it passes the suite, not when a committee
says so.

This is the mechanism that lets the project scale across jurisdictions without a central
bottleneck: the spec is executable, and conformance is checkable.

## Where to go next

- [`pipeline`](/pipeline/): how official sources become validated Akoma Ntoso.
- [`diff`](/diff/): how change between two states is detected and classified.
- [`archive`](/archive/): the canonical corpus the pipeline produces.
- [The principles](/principles/): the design philosophy in full.
