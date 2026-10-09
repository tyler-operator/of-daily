---
name: "of-instagram-growth"
description: "Run the weekly Operators Fund Instagram growth loop: read the numbers, rank posts by saves per reach, set next week's topics, and file the operators who engaged. Use for social growth, follower growth, content performance, or the weekly social review."
---

# OF Instagram Growth

Runs Friday, after the week's five decks have posted. Related skills: `of-daily-deck` builds the carousels, `of-instagram-publish` ships them.

## Who we are actually trying to reach

Owner-operators of Canadian B2B service, industrial and transportation businesses. Shop owners, GMs, plant managers, trades principals. $1-6M EBITDA range or the people who run businesses that size.

Three reasons they matter, in order: they become sellers, they become bench operators, they refer other owners.

**Follower count is not the goal and never gets reported as the headline.** A fabrication shop owner in Cambridge who saved the press brake deck is worth more than 200 anonymous accounts. The scoreboard is named operators who raised a hand.

## The metric

**Saves per 1,000 reach.** For this audience a save means "I want this later", which is the closest free proxy for intent. Likes are noise and follower count is lagging.

Secondary, in order: shares per 1,000 reach (an operator sending it to another operator is the strongest signal on the platform), profile visits, follows from post.

Carousels keep earning saves for weeks, so every published post is re-measured daily, not read once at publish. Compare posts at the same age: day 7 against day 7.

`scripts/metrics.py` in the `of-daily` repo pulls this into `metrics.json` on a daily cron. Needs `instagram_business_manage_insights` on the Meta app, added from the Permissions and features table. No review required.

## The weekly loop

**1. Read the numbers.** Pull `metrics.json`. Rank the week's five posts by saves per 1k reach at matched age. Note the account line: reach, profile views, follower delta.

**2. Name one rule.** What did the top post do that the bottom one did not? Force it into a sentence that constrains next week, not an observation. "Decks that open with a dollar figure beat decks that open with a date" is a rule. "Engagement was higher" is not.

Write the rule into the Lessons Log. After eight weeks the rules are the content strategy, and nobody else in this market has them.

**3. Set next week's five.** Pick against the standing rotation (machine, component, material, origin, Canadian builder) filtered by every rule learned so far. Keep the rotation; it is what stops the feed reading as a sector pitch.

**4. Sweep the engagers.** Everyone who commented, shared or followed this week. Keep the ones whose profile reads as a Canadian operator: shop, trade, plant, fleet, fabrication, contracting. Enrich what is findable, file to Attio with the post that caught them and the date.

This is the output that compounds. One name a week is 50 warm Canadian operators a year, each with a known interest.

**5. Report.** One screen. Numbers, the rule, next week's five, who showed up. No recap of what was posted; Ty saw it.

## Hooks, where most of the gain is

Slide 1 decides reach. Everything after it decides saves.

What works on operators:
- A real dollar figure they can check against their own shop
- A cost nobody prices (the ten minutes nobody pays for)
- A number that contradicts what the trade assumes
- A Canadian specific: a town, a tender, a plant

What does not:
- "Did you know"
- Market size
- Anything that sounds like a consultant wrote it
- A question with an obvious answer

When a hook underperforms, the deck is usually fine. Rewrite slide 1 and repost in six weeks under a different hook. Testing hooks against the same body is the cheapest experiment available.

## Growth levers that are real

- **Consistency.** Five a week beats a good week and a dead one. The publishing cron already handles this; protect it.
- **Reply to every comment, in Ty's voice, within a day.** Replies pull the post back into the feed and an operator who gets a real answer remembers it.
- **Answer with a number.** A commenter asking what a used one costs gets the figure, not a hedge. That is the whole brand in one reply.
- **Hashtags are a minor lever.** 8 to 12, mixing trade-specific and general. Do not spend an hour on them.
- **Post timing.** Operators read early. Test 6-8am ET against lunch, one change at a time, four weeks per test.

## What is not available, and is not worth building

Meta's API has no follow, no unfollow, no liking, no commenting on other accounts, no cold DMs. Every classic growth hack is either browser automation that gets the account actioned or a third-party tool doing the same thing with the account's credentials.

Not worth the brand. Do not propose engagement pods, follow-for-follow, comment bots, or buying anything. If asked for faster growth, the honest answer is better hooks and a second channel.

## The channel question, raise it once a quarter

Instagram is a decent fit for the machine series and a weak fit for the audience. Brokers, owners considering a sale, and investors live on LinkedIn.

The same eight slides repost there as a document carousel with no extra work, from Ty's personal profile rather than a company page. LinkedIn's API does not allow automated posting without partner access, so that one is manual or browser-driven.

When Instagram saves per 1k reach plateaus for three consecutive weeks, that is the signal to put the effort into LinkedIn instead of into more Instagram.

## Quality bar

The weekly report ships only if it has:
- A ranked list with the actual numbers, not adjectives
- One rule stated as a constraint on next week
- Five named topics
- The engager list, even when it is empty

A week with no rule is a week the loop did not run. Say so rather than padding it.
