#!/usr/bin/env python3
"""Infer the Open Laws Foundation contributor list from GitHub and write
data/contributors.json for Hugo to consume.

Rules:
  - Only the organization's OWN repositories count (forks and archived repos
    are excluded). Contributions are aggregated by login across them.
  - Organization MEMBERS are surfaced as the "core team" (shown big). Reading
    members needs a token with read:org; without it we fall back to the public
    members list, and the core-team section is simply smaller or empty.
  - Sipioteo and sirmmo are FORCED as founders, on top, regardless of the API.
  - Everyone else with commits in the owned repos is listed as a contributor.

Stdlib only. Never fails the build: on any API error it degrades gracefully and
still writes a valid file (founders are always present).
"""

import datetime
import json
import os
import sys
import urllib.error
import urllib.request

ORG = "OpenLawsFoundation"
# Forced founders, in display order. Matched case-insensitively against the API.
FOUNDERS = ["Sipioteo", "sirmmo"]
API = "https://api.github.com"
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""


def _get(url):
    if not url.startswith("http"):
        url = API + url
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("User-Agent", "olf-contributors-builder")
    if TOKEN:
        req.add_header("Authorization", "Bearer " + TOKEN)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r), r.headers.get("Link", "")
    except urllib.error.HTTPError as e:
        sys.stderr.write("warn: %s -> HTTP %s\n" % (url, e.code))
    except Exception as e:  # noqa: BLE001
        sys.stderr.write("warn: %s -> %s\n" % (url, e))
    return None, ""


def paginate(path):
    out, url = [], API + path
    while url:
        data, link = _get(url)
        if not isinstance(data, list):
            break
        out.extend(data)
        url = None
        for part in link.split(","):
            if 'rel="next"' in part:
                url = part[part.find("<") + 1:part.find(">")]
    return out


def owned_repos():
    repos = paginate("/orgs/%s/repos?per_page=100&type=all" % ORG)
    return sorted(
        r["name"] for r in repos
        if not r.get("fork") and not r.get("archived")
    )


def member_logins():
    m = paginate("/orgs/%s/members?per_page=100" % ORG)
    if not m:  # no token / no permission -> public members only
        m = paginate("/orgs/%s/public_members?per_page=100" % ORG)
    return [u["login"] for u in m]


def profile(login):
    data, _ = _get("/users/%s" % login)
    return data or {}


def main():
    repos = owned_repos()
    if not repos:
        sys.stderr.write("warn: no owned repos resolved; founders only\n")

    # Aggregate contributions across owned repos.
    agg = {}
    for repo in repos:
        for c in paginate(
            "/repos/%s/%s/contributors?per_page=100&anon=false" % (ORG, repo)
        ):
            login = c.get("login")
            if not login or c.get("type") == "Bot" or login.endswith("[bot]"):
                continue
            e = agg.setdefault(login, {
                "login": login,
                "contributions": 0,
                "avatar": c.get("avatar_url"),
                "url": c.get("html_url"),
            })
            e["contributions"] += int(c.get("contributions", 0))

    members = member_logins()
    low = str.lower
    founder_low = {low(f) for f in FOUNDERS}
    member_low = {low(m) for m in members}

    def enrich(login):
        p = profile(login)
        a = agg.get(login, {})
        # prefer canonical login casing from the profile when available
        canon = p.get("login", login)
        a = agg.get(canon, a)
        blog = (p.get("blog") or "").strip()
        if blog and not blog.startswith("http"):
            blog = "https://" + blog
        return {
            "login": canon,
            "name": p.get("name") or canon,
            "avatar": p.get("avatar_url") or a.get("avatar"),
            "url": p.get("html_url") or a.get("url") or "https://github.com/%s" % canon,
            "blog": blog,
            "location": p.get("location") or "",
            "bio": p.get("bio") or "",
            "contributions": int(a.get("contributions", 0)),
        }

    founders = [enrich(f) for f in FOUNDERS]

    team = [enrich(m) for m in members if low(m) not in founder_low]
    team.sort(key=lambda x: -x["contributions"])

    excluded = founder_low | member_low
    contributors = [
        {
            "login": e["login"],
            "name": e["login"],
            "avatar": e["avatar"],
            "url": e["url"],
            "contributions": e["contributions"],
        }
        for login, e in agg.items()
        if low(login) not in excluded
    ]
    contributors.sort(key=lambda x: -x["contributions"])

    out = {
        "generated_utc": datetime.datetime.now(datetime.timezone.utc)
        .strftime("%Y-%m-%dT%H:%M:%SZ"),
        "org": ORG,
        "owned_repos": repos,
        "founders": founders,
        "team": team,
        "contributors": contributors,
    }

    os.makedirs("data", exist_ok=True)
    with open("data/contributors.json", "w") as f:
        json.dump(out, f, indent=2)
        f.write("\n")

    sys.stderr.write(
        "wrote data/contributors.json: %d founders, %d team, %d contributors "
        "across %d owned repos %s\n"
        % (len(founders), len(team), len(contributors), len(repos), repos)
    )


if __name__ == "__main__":
    main()
