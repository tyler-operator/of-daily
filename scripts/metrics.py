#!/usr/bin/env python3
"""
Pull per-post Instagram metrics into metrics.json.

Appends a dated snapshot per published post so the same post is measured
at day 1, day 7 and day 30. Carousels keep earning saves for weeks; a
single read at publish time tells you nothing.

The ranking metric is saves per 1,000 reach. For an operator audience a
save means "I want this later", which is the closest free proxy for
intent. Likes are noise.

Needs instagram_business_manage_insights on the app.

Env:
  IG_USER_ID, IG_ACCESS_TOKEN
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://graph.instagram.com/v23.0"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(ROOT, "queue.json")
METRICS = os.path.join(ROOT, "metrics.json")

IG_USER_ID = os.environ.get("IG_USER_ID", "")
TOKEN = os.environ.get("IG_ACCESS_TOKEN", "")

# Carousel-safe metrics. Meta rejects the whole call on an unsupported
# name, so keep this list conservative and widen only after testing.
POST_METRICS = "reach,saved,shares,comments,likes,profile_visits,follows,total_interactions"
ACCOUNT_METRICS = "reach,profile_views,follower_count,accounts_engaged"


def get(path, params=None):
    params = dict(params or {})
    params["access_token"] = TOKEN
    url = f"{API}/{path}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise RuntimeError(f"GET {path} -> HTTP {e.code}: {body}") from None


def insights(media_id):
    """Return {metric: value}. Missing metrics are skipped, not fatal."""
    out = {}
    try:
        r = get(f"{media_id}/insights", {"metric": POST_METRICS})
    except RuntimeError as e:
        print(f"  insights unavailable for {media_id}: {e}")
        return out
    for row in r.get("data", []):
        vals = row.get("values") or [{}]
        out[row["name"]] = vals[0].get("value")
    return out


def account_snapshot():
    try:
        r = get(f"{IG_USER_ID}/insights",
                {"metric": ACCOUNT_METRICS, "period": "day"})
        return {row["name"]: (row.get("values") or [{}])[0].get("value")
                for row in r.get("data", [])}
    except RuntimeError as e:
        print(f"account insights unavailable: {e}")
        return {}


def score(m):
    """Saves per 1,000 reach. The ranking number."""
    reach = m.get("reach") or 0
    saved = m.get("saved") or 0
    if not reach:
        return None
    return round(saved * 1000 / reach, 2)


def main():
    if not (IG_USER_ID and TOKEN):
        print("::error::IG_USER_ID and IG_ACCESS_TOKEN must be set")
        sys.exit(1)

    with open(QUEUE) as f:
        queue = json.load(f)

    history = {"account": [], "posts": {}}
    if os.path.exists(METRICS):
        with open(METRICS) as f:
            history = json.load(f)
    history.setdefault("account", [])
    history.setdefault("posts", {})

    today = time.strftime("%Y-%m-%d")

    acct = account_snapshot()
    if acct:
        acct["date"] = today
        history["account"] = [a for a in history["account"]
                              if a.get("date") != today] + [acct]
        print(f"account: {acct}")

    for e in queue["posts"]:
        mid = e.get("media_id")
        if e.get("status") != "published" or not mid:
            continue
        m = insights(mid)
        if not m:
            continue
        m["date"] = today
        m["saves_per_1k_reach"] = score(m)
        rows = [r for r in history["posts"].get(e["slug"], [])
                if r.get("date") != today]
        history["posts"][e["slug"]] = rows + [m]
        print(f"{e['slug']}: reach {m.get('reach')}, saved {m.get('saved')}, "
              f"score {m.get('saves_per_1k_reach')}")

    with open(METRICS, "w") as f:
        json.dump(history, f, indent=2)
        f.write("\n")
    print("metrics updated")


if __name__ == "__main__":
    main()
