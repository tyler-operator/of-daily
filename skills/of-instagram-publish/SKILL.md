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
| Meta app | OF Daily Publisher, app ID `897158953423545` |
| Auth path | Unified Login, system-user token (never expires) |
| Graph host | `graph.facebook.com`, override with `IG_API_BASE` |
| Publish cron | `12 11 * * 1-5`, weekdays 11:12 UTC |
| Secrets | `IG_USER_ID`, `IG_ACCESS_TOKEN` |

Rebuilt 2026-11-17 after the original app (`1086663147312668`) vanished.
There is no token refresh job any more; the old one is deleted.

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
- **`API access blocked`, subcode 5258005** — the app itself is gone or restricted. Not transient. Check developers.facebook.com/apps; if it is not listed, rebuild. This happened on 2026-10-11 and went unnoticed for five weeks.
- **`Cannot parse access token`, code 190** — right token, wrong host. A Unified Login system-user token only works against `graph.facebook.com`. An Instagram Login token only works against `graph.instagram.com`. Set `IG_API_BASE` to match the token.
- **`Tried accessing nonexisting field (error_message)`** — `graph.facebook.com` does not expose that field on a container node. `wait_ready` already falls back; if it resurfaces, trim the field list further.
- **401 or other OAuth errors** — regenerate the token in the app dashboard and replace the secret.

Turn on Settings, Notifications, **Actions: send notifications for failed workflows only**.

The failure mode to design against is not a dead token, it is a familiar alarm. The old refresh job went red every Sunday for six weeks and nobody looked, because it had always looked like that. Meanwhile the publish job stayed green by doing nothing, because the queue was empty. Green that means idle and red that means nothing add up to a pipeline that is dead and silent. Every alarm in here should mean something, and an empty queue should be visible.

## Limits

- 10 images per carousel, 2 minimum
- JPEG only, no PNG or WebP, under 8MB
- Caption 2,200 characters, 30 hashtags
- Publishing quota read at runtime from `content_publishing_limit` rather than trusting the docs, which contradict themselves (50 in one place, 100 in another)

## Rebuilding from scratch

The order matters; several steps have non-obvious prerequisites.

1. **Facebook account.** Required to create any Meta app, even on the Instagram Login path. An Instagram-only Business Suite login is not enough. The user creates this.
2. **Meta for Developers registration.** Four screens, includes phone verification. The user does this.
3. **Create app.** Use case **Manage messaging & content on Instagram**. No business portfolio needed. No App Review, no Business Verification for an account you own; the dashboard says as much on the App Review step.
4. **Permissions.** Instagram, then Customize. New apps arrive with these pre-attached, so there may be nothing to action. Confirm `instagram_business_content_publish` reads "Ready for testing".
5. **Login path. Choose Unified, not Facebook Login.** Facebook Login needs a Page linked to the account. Meta retired the standalone Instagram Login setup during 2026.
6. **Tester role.** Roles tab, Instagram Testers, add the handle. Then accept at instagram.com/accounts/manage_access/ under **Tester Invites**. The user accepts; it agrees to Meta's terms.
7. **Configuration.** API setup step 1, Create new configuration: General, **system-user access token**, the Instagram account as business asset, `instagram_content_publish` in permissions. Ignore Redirect URL and Login URL, they are for third-party login flows. Step 2 stays locked until a configuration exists.
8. **Generate token.** Step 2, Add account. The user copies it.
9. **Repo secret.** Replace `IG_ACCESS_TOKEN`. `IG_USER_ID` survives a rebuild unchanged. No `GH_PAT` needed.
10. **Check the host.** A system-user token needs `graph.facebook.com`. The publisher defaults there.

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
