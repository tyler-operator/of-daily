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

1. developers.facebook.com, **Create App**, type **Business**.
2. Add the **Instagram** product.
3. Choose **Instagram API with Instagram Login**. This path needs no Facebook
   Page, which removes a whole class of problems.
4. Under API setup with Instagram login, add your Instagram account.
5. Permissions needed: `instagram_business_basic`,
   `instagram_business_content_publish`.

No App Review and no Business Verification. Standard Access covers apps that
only serve accounts you own.

### 3. Get a long-lived token

In the app dashboard, generate a token for your account. Then exchange it:

```bash
# short-lived -> long-lived (60 days)
curl -s "https://graph.instagram.com/access_token\
?grant_type=ig_exchange_token\
&client_secret=APP_SECRET\
&access_token=SHORT_LIVED_TOKEN"
```

Note your Instagram user id from the same dashboard.

### 4. Repo secrets

Settings, Secrets and variables, Actions:

| Secret | What |
|---|---|
| `IG_USER_ID` | Instagram professional account id |
| `IG_ACCESS_TOKEN` | the long-lived token from step 3 |
| `GH_PAT` | fine-grained PAT, this repo, **Secrets: read and write**. Only used to rotate the token above. |

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
2. Write `posts/<nnn>-<slug>/caption.txt`. Max 2,200 characters, 30 hashtags.
3. Add an entry to `queue.json` with `"status": "ready"` and a `publish_at`
   date.
4. Commit. The next scheduled run picks it up.

Use `"status": "draft"` to park something. The publisher skips it.

---

## Schedule

| Workflow | When | Does |
|---|---|---|
| `publish` | Weekdays 11:12 UTC | Posts the next ready entry |
| `refresh-token` | Sundays 13:07 UTC | Extends the token another 60 days |

Both run on `workflow_dispatch` too.

Times are UTC, so they shift an hour against Toronto when DST changes. The
minutes are deliberately off the hour: cron jobs scheduled at :00 queue behind
everyone else's.

---

## The thing that will actually break

**The token.** Long-lived tokens last 60 days. The weekly refresh extends them,
so in steady state it runs forever. But if the refresh fails eight weeks
running and nobody looks, the token dies and recovery needs a manual browser
login.

Watch for it: Settings, Notifications, tick **Actions: send notifications for
failed workflows only**. A red refresh-token run is the warning, and you get
eight of them.

## Limits worth knowing

- 10 images per carousel.
- Meta's docs say 50 published posts per 24h in one place and 100 in another.
  The script reads `content_publishing_limit` at runtime rather than trusting
  either.
- Images are fetched by Meta from the raw URL at container-creation time. The
  repo must stay public, or the fetch fails.
