#!/usr/bin/env python3
"""
Refresh the long-lived Instagram token and write it back as a repo secret.

Meta's long-lived tokens last 60 days. Refreshing extends by another 60.
Miss the window and the token is dead, which means a manual browser login.
This runs weekly so there are eight chances to catch a failure before that.

Needs a GH_PAT with repo secrets write scope, because GITHUB_TOKEN cannot
update secrets.

Env:
  IG_ACCESS_TOKEN    current long-lived token
  GH_PAT             personal access token, scope: repo secrets write
  GITHUB_REPOSITORY  owner/repo
"""
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request

TOKEN = os.environ.get("IG_ACCESS_TOKEN", "")
GH_PAT = os.environ.get("GH_PAT", "")
REPO = os.environ.get("GITHUB_REPOSITORY", "")

WARN_DAYS = 10          # shout if the new token expires sooner than this


def fail(msg):
    print(f"::error::{msg}")
    sys.exit(1)


def main():
    if not TOKEN:
        fail("IG_ACCESS_TOKEN not set")

    url = ("https://graph.instagram.com/refresh_access_token?"
           + urllib.parse.urlencode({"grant_type": "ig_refresh_token",
                                     "access_token": TOKEN}))
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        fail(f"refresh failed HTTP {e.code}: {body}. "
             f"If the token is already expired you must re-authorise in a browser.")

    new_token = data.get("access_token")
    expires_in = int(data.get("expires_in", 0))
    days = expires_in // 86400
    print(f"refreshed. new token valid {days} days")

    if days < WARN_DAYS:
        print(f"::warning::token only has {days} days left, check the app config")

    if not new_token:
        fail("no access_token in refresh response")

    if new_token == TOKEN:
        print("token unchanged, nothing to write")
        return

    if not (GH_PAT and REPO):
        print("::warning::GH_PAT or GITHUB_REPOSITORY missing, "
              "cannot store the rotated token. Set it by hand.")
        return

    env = dict(os.environ, GH_TOKEN=GH_PAT)
    res = subprocess.run(
        ["gh", "secret", "set", "IG_ACCESS_TOKEN", "--repo", REPO, "--body", new_token],
        env=env, capture_output=True, text=True)
    if res.returncode != 0:
        fail(f"could not write secret: {res.stderr.strip()}")
    print("IG_ACCESS_TOKEN secret rotated")


if __name__ == "__main__":
    main()
