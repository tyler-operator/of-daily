#!/usr/bin/env python3
"""
Publish the next ready carousel to Instagram.

Reads queue.json, finds the first entry that is ready and due, uploads its
slides as a carousel, marks it published and writes the queue back.

Images are served from raw.githubusercontent.com, which is what Meta fetches.
Nothing here renders anything: the JPEGs are committed ahead of time.

Env:
  IG_USER_ID        Instagram professional account id
  IG_ACCESS_TOKEN   long-lived token
  GITHUB_REPOSITORY owner/repo   (set automatically by Actions)
  GITHUB_REF_NAME   branch name  (set automatically by Actions)
  DRY_RUN           "1" to do everything except the final publish
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

API = "https://graph.instagram.com/v23.0"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(ROOT, "queue.json")

IG_USER_ID = os.environ.get("IG_USER_ID", "")
TOKEN = os.environ.get("IG_ACCESS_TOKEN", "")
REPO = os.environ.get("GITHUB_REPOSITORY", "")
BRANCH = os.environ.get("GITHUB_REF_NAME", "main")
DRY_RUN = os.environ.get("DRY_RUN") == "1"

MAX_SLIDES = 10


def fail(msg, code=1):
    print(f"::error::{msg}")
    sys.exit(code)


def post(path, params):
    """POST to the Graph API. Returns parsed JSON or raises."""
    params = dict(params)
    params["access_token"] = TOKEN
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(f"{API}/{path}", data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise RuntimeError(f"POST {path} -> HTTP {e.code}: {body}") from None


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


def raw_url(rel_path):
    return (f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/"
            + urllib.parse.quote(rel_path))


def wait_ready(container_id, label, timeout=300):
    """Poll a container until FINISHED. Meta fetches the image during this."""
    start = time.time()
    while time.time() - start < timeout:
        info = get(container_id, {"fields": "status_code,status"})
        code = info.get("status_code")
        if code == "FINISHED":
            return
        if code == "ERROR":
            fail(f"{label} container errored: {info.get('status')}")
        time.sleep(5)
    fail(f"{label} container timed out after {timeout}s")


def check_quota():
    try:
        q = get(f"{IG_USER_ID}/content_publishing_limit",
                {"fields": "quota_usage,config"})
        d = (q.get("data") or [{}])[0]
        used = d.get("quota_usage", 0)
        cap = (d.get("config") or {}).get("quota_total", "unknown")
        print(f"publishing quota: {used} used of {cap} in the last 24h")
        if isinstance(cap, int) and used >= cap:
            fail("publishing quota exhausted, skipping this run")
    except Exception as e:                       # non-fatal, keep going
        print(f"note: could not read quota ({e})")


def pick_entry(queue):
    now = time.strftime("%Y-%m-%d")
    for e in queue["posts"]:
        if e.get("status") != "ready":
            continue
        if e.get("publish_at") and e["publish_at"] > now:
            continue
        return e
    return None


def main():
    if not (IG_USER_ID and TOKEN):
        fail("IG_USER_ID and IG_ACCESS_TOKEN must be set")
    if not REPO:
        fail("GITHUB_REPOSITORY not set, cannot build public image URLs")

    with open(QUEUE) as f:
        queue = json.load(f)

    entry = pick_entry(queue)
    if not entry:
        print("nothing ready to publish. done.")
        return

    slides = entry["slides"]
    if not 2 <= len(slides) <= MAX_SLIDES:
        fail(f"{entry['slug']}: carousel needs 2 to {MAX_SLIDES} slides, got {len(slides)}")

    for rel in slides:
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            fail(f"missing slide file: {rel}")
        size_mb = os.path.getsize(p) / 1e6
        if size_mb > 8:
            fail(f"{rel} is {size_mb:.1f}MB, over Meta's 8MB limit")

    caption_path = os.path.join(ROOT, entry["caption"])
    with open(caption_path) as f:
        caption = f.read().strip()
    if len(caption) > 2200:
        fail(f"caption is {len(caption)} chars, over the 2200 limit")

    print(f"publishing {entry['slug']}: {len(slides)} slides, "
          f"{len(caption)} char caption")
    check_quota()

    # 1. one container per slide
    children = []
    for i, rel in enumerate(slides, 1):
        url = raw_url(rel)
        print(f"  [{i}/{len(slides)}] container for {url}")
        if DRY_RUN:
            children.append(f"dry-{i}")
            continue
        r = post(f"{IG_USER_ID}/media",
                 {"image_url": url, "is_carousel_item": "true"})
        cid = r["id"]
        wait_ready(cid, f"slide {i}")
        children.append(cid)

    # 2. the carousel parent, caption lives here
    if DRY_RUN:
        print("DRY_RUN: stopping before carousel creation")
        print("---- caption ----")
        print(caption)
        return

    parent = post(f"{IG_USER_ID}/media",
                  {"media_type": "CAROUSEL",
                   "children": ",".join(children),
                   "caption": caption})["id"]
    wait_ready(parent, "carousel")

    # 3. publish
    published = post(f"{IG_USER_ID}/media_publish", {"creation_id": parent})
    media_id = published.get("id")
    print(f"published {entry['slug']} as media {media_id}")

    entry["status"] = "published"
    entry["published_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    entry["media_id"] = media_id
    with open(QUEUE, "w") as f:
        json.dump(queue, f, indent=2)
        f.write("\n")
    print("queue updated")


if __name__ == "__main__":
    main()
