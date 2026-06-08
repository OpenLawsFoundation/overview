#!/usr/bin/env python3
"""Validate SEO metadata in the built site. Fails (exit 1) if any HTML page is
missing required tags, or if an og:image points at a file that isn't there.

Usage: python3 scripts/check-seo.py [public_dir]   (default: public)
"""
import os
import sys
from html.parser import HTMLParser

PUBLIC = sys.argv[1] if len(sys.argv) > 1 else "public"

# Required on every HTML page.
REQUIRED_META_NAME = {"description", "twitter:card"}
REQUIRED_META_PROP = {"og:title", "og:description", "og:url", "og:image", "og:type"}


class Head(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self._in_title = False
        self.meta_name = {}
        self.meta_prop = {}
        self.canonical = None
        self.ld_json = False
        self._in_ld = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            c = (a.get("content") or "").strip()
            if a.get("name"):
                self.meta_name[a["name"]] = c
            if a.get("property"):
                self.meta_prop[a["property"]] = c
        elif tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._in_ld = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "script" and self._in_ld:
            self._in_ld = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_ld and data.strip():
            self.ld_json = True


def rel_from_url(url):
    for base in ("https://openlawsfoundation.org", "http://openlawsfoundation.org",
                 "https://localhost", "http://localhost"):
        if url.startswith(base):
            return url[len(base):].split("?")[0]
    if url.startswith("/"):
        return url.split("?")[0]
    return None


def check(path, is_home):
    errors = []
    with open(path, encoding="utf-8") as f:
        html = f.read()
    p = Head()
    p.feed(html)

    if not p.title.strip():
        errors.append("missing <title>")
    for n in REQUIRED_META_NAME:
        if not p.meta_name.get(n):
            errors.append(f"missing meta name={n}")
    for n in REQUIRED_META_PROP:
        if not p.meta_prop.get(n):
            errors.append(f"missing meta property={n}")
    if not p.canonical:
        errors.append("missing canonical link")

    og_img = p.meta_prop.get("og:image")
    if og_img:
        rel = rel_from_url(og_img)
        if not rel:
            errors.append(f"og:image not absolute/resolvable: {og_img}")
        else:
            fp = os.path.join(PUBLIC, rel.lstrip("/"))
            if not os.path.isfile(fp):
                errors.append(f"og:image file missing on disk: {rel}")
            elif os.path.getsize(fp) < 1024:
                errors.append(f"og:image suspiciously small: {rel}")

    if is_home and not p.ld_json:
        errors.append("home page missing JSON-LD structured data")
    return errors


def main():
    if not os.path.isdir(PUBLIC):
        print(f"ERROR: '{PUBLIC}' not found. Build the site first.", file=sys.stderr)
        sys.exit(2)

    home = os.path.normpath(os.path.join(PUBLIC, "index.html"))
    pages, failures = 0, 0
    for root, _, files in os.walk(PUBLIC):
        for fn in files:
            if not fn.endswith(".html"):
                continue
            path = os.path.join(root, fn)
            pages += 1
            errs = check(path, is_home=(os.path.normpath(path) == home))
            if errs:
                failures += 1
                rel = os.path.relpath(path, PUBLIC)
                print(f"FAIL  {rel}")
                for e in errs:
                    print(f"        - {e}")

    if failures:
        print(f"\nSEO check failed: {failures}/{pages} page(s) with issues.", file=sys.stderr)
        sys.exit(1)
    print(f"SEO check passed: {pages} page(s), all required metadata present.")


if __name__ == "__main__":
    main()
