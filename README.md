# of-daily

Headless Instagram publishing for the Operators Fund machine series.

Slides are rendered ahead of time and committed as JPEGs. A scheduled GitHub
Action posts the next one as a carousel. Nothing renders in CI, so a broken
font or a missing library can never cost you a post.

Cost: $0. Public repo, so Actions minutes are unmetered and
raw.githubusercontent.com serves the images Meta needs to fetch.

---

## One-time setup

### 1. Instagram account

Convert the account to **Business** or **Creator** (Settings, Account type and
tools). A personal account cannot publish via API.

### 2. Meta app

1. developers.facebook.com, **Create App**, use case
   **Manage messaging & content on Instagram**.
2. Left menu, **Instagram**, then **Customize**. Permissions arrive
   pre-attached on new apps; confirm `instagram_business_content_publish`
   reads "Ready for testing".
3. Login path: **Unified Login**. Not Facebook Login, which would need a
   Facebook Page linked to the account.

   Meta retired the standalone "Instagram API with Instagram Login" setup
   during 2026. Unified is what exists now, and it changes which Graph host
   the token works against. See step 3.
4. **Roles** tab, **Instagram Testers**, add the account. Then accept the
   invite at instagram.com/accounts/manage_access/ under **Tester Invites**.

No App Review and no Business Verification. The dashboard says so itself:
skippable if you only build for your own Instagram business.

### 3. Get a token

In **API setup**, step 1, click **Create new configuration**:

- Login variation: General
- Access token: **System-user access token (SUAT)**
- Business assets: the Instagram account
- Permissions: include `instagram_content_publish`

Ignore the Redirect URL and Login URL fields. Those exist to send other
people through a login flow, which you are not doing. Step 2 stays greyed
out until a configuration exists.

Then step 2, **Add account**, and generate the token.

**This token never expires.** That is the main reason to prefer this path:
there is no renewal job to fail quietly.

**It is a Facebook token, not an Instagram one.** It works against
`graph.facebook.com` and `graph.instagram.com` cannot parse it at all. The
publisher defaults to the Facebook host; override with `IG_API_BASE` if you
ever move back to an Instagram-Login token.

Note your Instagram user id from the same screen.

### 4. Repo secrets

Settings, Secrets and variables, Actions:

| Secret | What |
|---|---|
| `IG_USER_ID` | Instagram professional account id |
| `IG_ACCESS_TOKEN` | the system-user token from step 3 |

`GH_PAT` is no longer needed. It existed only to rotate the old 60-day
token.

### 5. Test before trusting it

Actions tab, **publish**, Run workflow, tick **dry run**. It builds every
image URL, checks file sizes and the caption length, prints the caption, and
stops before anything goes live.

Then run it again without dry run.

---

## Adding a post

1. Drop eight to ten JPEGs in `posts/<nnn>-<slug>/`.
   - **1080 x 1350**, every slide identical. Instagram crops the whole
     carousel to the first slide's ratio.
   - JPEG only. No PNG, no WebP. Under 8MB.
2. Write `posts/<nnn>-<slug>/caption.txt`. Max 2,200 characters. Meta allows
   30 hashtags; Instagram now surfaces about five, so use ten at most.
3. Add an entry to `queue.json` with `"status": "ready"` and a `publish_at`
   date.
4. Commit. The next scheduled run picks it up.

Use `"status": "draft"` to park something. The publisher skips it.

---

## Schedule

| Workflow | When | Does |
|---|---|---|
| `publish` | Weekdays 11:12 UTC | Posts the next ready entry |
| `metrics` | Daily | Records reach and saves |

Both run on `workflow_dispatch` too.

There is no token refresh job. System-user tokens do not expire, so the
weekly renewal that used to live here was deleted in November 2026.

Times are UTC, so they shift an hour against Toronto when DST changes. The
minutes are deliberately off the hour: cron jobs scheduled at :00 queue behind
everyone else's.

---

## The thing that will actually break

**The Meta app.** It can disappear. This one did, around 11 October 2026, and
nothing surfaced it for five weeks: the publish job kept going green because
the queue was empty, and the only signal was a weekly red run on a renewal
job that everybody had learned to ignore.

Symptom: `API access blocked`, OAuthException, subcode 5258005, on every
call. Not transient. Re-running will not help. Check
developers.facebook.com/apps and see whether the app is still listed.

The lesson is about alarms, not tokens. A red run that fires every week
trains you to stop reading them, and then a real failure arrives wearing the
same colour. Every alarm in here should mean something.

Turn this on: Settings, Notifications, **Actions: send notifications for
failed workflows only**. With the renewal job gone, a red run now means a
real failure.

**Recovery** is a rebuild: new app, new configuration, new token, replace
`IG_ACCESS_TOKEN`. About 20 minutes. `IG_USER_ID` does not change.

## Limits worth knowing

- 10 images per carousel.
- Meta's docs say 50 published posts per 24h in one place and 100 in another.
  The script reads `content_publishing_limit` at runtime rather than trusting
  either.
- Images are fetched by Meta from the raw URL at container-creation time. The
  repo must stay public, or the fetch fails.
