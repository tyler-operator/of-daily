---
name: "of-instagram-publish"
description: "Publish, queue or troubleshoot an Operators Fund Instagram carousel through the of-daily repo, or rebuild the headless publishing pipeline from scratch."
---

# OF Instagram Publish

Headless publishing for @operatorsfund. Slides are rendered locally and committed as JPEGs; a scheduled GitHub Action posts them. Nothing renders in CI, so a broken font or a missing library can never cost a post. Cost: $0.

## The live system

| Thing | Value |
|---|---|
| Repo | `tyler-operator/of-daily`, public |
| Account | @operatorsfund, Instagram professional |
| IG user id | `17841422442383715` |
| Meta app | OF Daily Publisher, app ID `1086663147312668` |
| Auth path | Instagram API with Instagram Login (no Facebook Page needed) |
| Publish cron | `12 11 * * 1-5`, weekdays 11:12 UTC |
| Token refresh cron | `7 13 * * 0`, Sundays |
| Secrets | `IG_USER_ID`, `IG_ACCESS_TOKEN`, `GH_PAT` |

Public repo is load-bearing twice over: Actions minutes are unmetered, and Meta fetches the images from `raw.githubusercontent.com` at container-creation time. Make it private and posting stops.

## Adding a post

1. Render eight JPEGs into `posts/<nnn>-<slug>/` at 1080x1350. See `of-daily-deck`.
2. Write `posts/<nnn>-<slug>/caption.txt`, max 2,200 characters.
3. Add an entry to `queue.json`: `slug`, `title`, `status: "ready"`, `publish_at` (YYYY-MM-DD), `caption` path, `slides` array.
4. Commit and push. The next scheduled run takes the first `ready` entry whose `publish_at` is today or earlier.

`status: "draft"` parks one. The publisher rewrites the entry to `published` with `published_at` and `media_id`, then commits that back itself.

## Running it by hand

Actions tab, **publish**, Run workflow.

Always dry run first. It builds every image URL, checks file sizes and caption length, reads the live publishing quota from Meta, prints the caption, and stops before anything goes public. A clean dry run proves the token, the URLs and the quota in one pass.

Then run again with dry run unticked.

The GitHub UI panel is fiddly to drive by browser automation. Open the panel, then set the checkbox and submit through the DOM:

```js
const cb = document.querySelector('input[type=checkbox][name="inputs[dry_run]"]');
const b = [...document.querySelectorAll('button')]
  .find(x => x.type === 'submit' && /Run workflow/.test(x.innerText));
if (cb.checked) cb.click();
b.click();
```

If `cb` comes back null the panel did not open. Click the green Run workflow button again and retry.

## Reading the result

`gh run list --repo tyler-operator/of-daily --limit 1`. Logs are not downloadable through the API proxy; read them in the browser instead, expanding the "Publish next carousel" step.

Success looks like `published <slug> as media <id>` followed by a `published:` commit on main.

## Failures and what they mean

- **`carousel container errored`** — Meta's parent container failed. Often transient; re-run before investigating. The script prints the whole status payload including `error_message`.
- **`nothing ready to publish`** — no entry is both `ready` and due. Check `publish_at` against today.
- **Child container errors** — Meta could not fetch an image. Confirm the repo is still public and the raw URL resolves.
- **401 or OAuth errors** — the token died. Regenerate in the app dashboard and replace the secret.
- **Red refresh-token run** — the warning shot. Tokens last 60 days and the weekly job gets eight attempts, so one red run is not urgent but three is.

Turn on Settings, Notifications, **Actions: send notifications for failed workflows only**. That red run is the only thing standing between a working pipeline and silent death.

## Limits

- 10 images per carousel, 2 minimum
- JPEG only, no PNG or WebP, under 8MB
- Caption 2,200 characters, 30 hashtags
- Publishing quota read at runtime from `content_publishing_limit` rather than trusting the docs, which contradict themselves (50 in one place, 100 in another)

## Rebuilding from scratch

The order matters; several steps have non-obvious prerequisites.

1. **Facebook account.** Required to create any Meta app, even on the Instagram Login path. An Instagram-only Business Suite login is not enough. The user creates this.
2. **Meta for Developers registration.** Four screens, includes phone verification. The user does this.
3. **Create app.** Use case **Manage messaging & content on Instagram**. No business portfolio needed. No requirements, no App Review, no Business Verification for an account you own.
4. **Permissions.** Add all required, then add `instagram_business_content_publish` by hand from the Permissions and features table. It is not in the required set. Each should read "Ready for testing".
5. **Connect the account.** Section 2, Add account, role **Instagram Tester**, type the handle. Then accept the invite at instagram.com/accounts/manage_access/ under **Tester Invites**. The user accepts; it agrees to Meta's terms.
6. **Generate token.** Section 2 next to the account. The user copies it.
7. **Repo secrets.** `IG_USER_ID` (shown under the handle in section 2), `IG_ACCESS_TOKEN`, and `GH_PAT` (fine-grained, this repo only, Secrets: read and write, used solely to rotate the token).

## What Claude cannot do here, and must not try

These are not obstacles to route around. State them plainly and hand the step over.

- Create accounts of any kind
- Type passwords, tokens, API keys or PATs into any field, including GitHub's secret value box
- Accept terms of service or authorize an app on the user's behalf
- Copy a live token out of a page

If the user pastes a token into chat, do not use it. Tell them to rotate it, and that it is now sitting in plaintext in the conversation.

Also structural, worth knowing before promising anything:
- The container cannot reach graph.instagram.com, graph.facebook.com, S3 or Cloudflare. It can reach GitHub. That is why publishing lives in the Action.
- `gh api -X POST /user/repos` and secret writes are blocked by the proxy. Create repos through the browser.
- Pushing needs the Claude GitHub App installed on the account for that repo. Without it, `add_repo` attaches read-only and the push 403s.
