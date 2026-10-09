---
name: "of-daily-deck"
description: "Build one Operators Fund daily eight-slide Instagram carousel on a machine, component, material, origin story or Canadian builder. Use for daily deck, market warm up, content deck, or the daily content series."
---

# OF Daily Deck

One eight-slide carousel a day on the physical guts of industry. Modelled on the Market Warm Up format but rebuilt so every slide carries a number.

## Output, named before work starts

Eight JPEGs, 1080x1350, Brand v3 case-study system, OF mark on every slide. Published to @operatorsfund as an Instagram carousel by the `of-daily` repo. See the `of-instagram-publish` skill for the pipeline.

All figures CAD. Every slide footer says so.

## THE FIREWALL, read this first

The deck carries the spine, the specs and the odd facts. It **never** carries:
- Penetration percentages
- Adoption share or how few firms own the thing
- Any build-vs-service verdict
- Anything about what Operators Fund is buying or looking at

Those four are the thesis and they stay internal. A deck on robot arms publishes payload, reach, repeatability, landed cost by origin and serviceability in Canada. It does not publish how few Canadian manufacturers own one. That number is the business.

If a slide would make a reader think "somebody is about to roll this up", cut it.

## The five-type rotation

One per weekday, so the series reads as curiosity rather than a sector pitch.

- **Monday, machine.** Press brakes, fiber lasers, waterjets, machining centres, powder coat lines
- **Tuesday, component.** Arms, conveyors, VFDs, bearings, linear rails, dock levellers, gearboxes
- **Wednesday, material.** 304 vs 316, A36 vs A572, 6061 vs 7075, tool steels, coatings. Live pricing, so it refreshes itself
- **Thursday, origin.** Who invented the wrench. Why Robertson is Canadian and Phillips won anyway. The adjustable wrench patent fight
- **Friday, Canadian builder.** Massey, Bombardier's first snowmobile, Magna's first stamping plant, Clearpath out of a Waterloo garage, Kinova and Robotiq in Quebec

Thursday and Friday cost almost nothing to research, give the series personality, and buy cover for the equipment decks.

## Eight-slide arc, machine and component

Carousels are read in order and most readers quit by slide 3. Front-load the hook, back-load the payoff.

1. **Hook.** One counterintuitive number or claim, big serif type, mint highlighter behind the turn. No setup, no throat-clearing.
2. **What it is.** Plain words a ten-year-old follows, plus a vector drawing of the thing. What it makes or moves.
3. **The spine.** One part walked through the machine: input, setup, cycle, output, scrap. Sequence drawing, four frames.
4. **Versions.** Two or three eras or variants side by side, drawn. What changed and in what year.
5. **What it costs.** New price range, used range, typical hours or age at resale. Lead time new versus used; the lead time is often the whole story.
6. **Cost to run.** Shop rate billed per hour against cost per hour (power, consumables, tooling, labour). Zebra-row table, labour in violet, serif figures.
7. **The operator's cut.** Utilisation to break even, depreciation from real auction comps, who can run it and how scarce they are.
8. **The turn.** The one line worth repeating, plus the handle. Where the margin is actually hiding.

Material decks: 1 hook, 2 what it is, 3 ore to bar, 4 grades compared, 5 price today and the move, 6 strength and machinability, 7 where it wins and loses, 8 the turn.

Origin and Canadian builder decks: 1 hook, 2 the thing and why it exists, 3-5 dated timeline to the breakthrough, 6 what happened to the invention, 7 what happened to the inventor, 8 the turn.

## Render system

Rendering is local, never in CI. Pure SVG to JPEG, no pptx.

Source lives in the `of-daily` repo under `render/`:
- `social.py` — page frame, type scale, chrome, eight `slideN()` functions, `save()`
- `art*.py` — vector illustrations per subject

Rules that cost time when forgotten:
- Embedded PNGs need base64 data URIs. `href="file.png"` and `file://` both render nothing.
- Give every `<image>` an explicit width AND height plus `preserveAspectRatio`, or it mis-sizes.
- Pass `background_color="#FAFAFA"` to cairosvg or art sits on a white block.
- Export JPEG quality 92. Target under 300KB a slide; Meta's ceiling is 8MB.
- Every slide identical at 1080x1350. Instagram crops the whole carousel to slide 1's ratio.

Brand v3 case-study system:
- `#0F2920` ink, `#52F5A0` mint, `#FAFAFA` ground, `#7366E0` violet as the second data colour
- Inter for everything structural, Lora for headline and figures
- Headline pattern: serif line, then a mint highlighter rect behind the second line
- Section label pattern: short mint dash, then all-caps grey 21px with letter-spacing
- Chrome: OF mark top left, `n/8` top right, rule under both, handle bottom left, ALL FIGURES CAD bottom right

Open every rendered JPEG and look at it before shipping. Overflow and collision are the normal failure, not the exception.

## The comparison variant

For components with several origins, run origin versus origin instead of one product. Japanese, European, Chinese, Korean, Canadian. Compare on what decides a purchase, not on sticker:
- Spec (payload, reach, repeatability)
- Sticker price
- Landed cost including tariff and freight. Nobody publishes this
- Spare part lead time and whether a Canadian depot exists
- Controller lock-in
- Integrator availability in Ontario
- Payback at a real Ontario wage

The finding is almost always that sticker price is the wrong comparison and cost per year of uptime is the right one. That is defensible, contrarian and numbers-backed. It is also the single most useful thing the series produces.

## Serviceability score

On machines and components, score serviceability in Canada out of 5, on the same scale every time: Canadian depot, spares stocked in Canada, spare lead time, third-party service access, controller still supported. Published next to the price. Across fifty decks this becomes a ranked table nobody else has.

## Caption

Max 2,200 characters. Structure:
- The hook line again, one sentence
- Three or four short paragraphs, one number each, blank line between
- The turn
- `Sources:` named, comma separated. Say which figures are modeled. End with `All figures CAD.`
- 8 to 12 hashtags, lowercase, mixing trade and general

## Research sources

- Specs: OEM spec sheets, scraped per manufacturer. Published, structured, authoritative, and the odd fact is already on the page
- New price: dealer listings, municipal tender awards (Canadian municipalities publish real paid prices)
- Used price and depreciation: Ritchie Bros and IronPlanet auction results, Surplus Record, Machinio, Kitmondo
- Materials pricing: LME, SteelBenchmarker, service centre published sheets
- Tariff: CBSA customs tariff schedule by HS code
- Service network: OEM dealer locator pages filtered to Canada, parts distributor stock pages, end-of-life notices
- History: patent records are usually the unlock date

Tag every number confirmed, modeled or single-source. Never build a depreciation curve across machine classes; same class only, or the curve is noise.

## Quality bar

A deck ships only if it has:
- A number on the constraint, not just the market
- One margin, rate or cost-per-hour line
- A date where cost fell
- One fact that survives retelling at a dinner table

Day 40 is where series like this die, when the cost line quietly disappears and it becomes specs and trivia. The cost-per-hour line is the gate.

## Voice

Plain words. Short punchy lines. Whitespace. One idea at a time. Curious, not salesy. No dismissive "just". No certainty-theater. No em dashes. Compliance check before anything ships: no IRR, no raise size, no LP names.
