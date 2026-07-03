# Reviewing Design/UI Changes with AI Coding Agents Against a Spec — SOTA 2025–2026

Research date: 2026-06-03. Method: 6 parallel research agents (objective verification · spec-into-loop · browser MCPs · Tailwind tokens · best-practices/pitfalls · contrarian/ROI), synthesised, then reviewed. Sources cited inline; full per-agent findings archived in the review log.

## Problem Anchor (Verbatim)

State of the art for reviewing/verifying DESIGN and UI changes when working with AI coding agents — especially Claude Code — against a design spec. Cover, with concrete tools, workflows, and trade-offs:

1. How agents verify a UI change objectively matches design intent (not eyeballing): DOM geometry / computed-style measurement, visual regression / screenshot diffing (Playwright toHaveScreenshot, Chromatic, Percy, Argos, Lost Pixel, reg-suit), pixel vs perceptual vs DOM-level comparison, and how AI/LLM "visual judge" approaches compare to deterministic diffs.
2. Pulling the design spec INTO the agent loop: Figma Dev Mode + the official Figma MCP server, figma-to-code, design-token extraction (Figma variables → CSS/Tailwind tokens, Style Dictionary, Tokens Studio), and "Claude Design"/Anthropic design tooling if it exists. How specs are represented so an agent can check against them.
3. Browser-automation/MCP options for driving the running app during review: chrome-devtools MCP, Playwright MCP, claude-in-chrome, computer-use — strengths for measurement, real-input interaction, and screenshots.
4. Tailwind / design-token specific review: enforcing token usage (no magic values), linting (eslint-plugin-tailwindcss, biome), and checking computed styles resolve to the right token values.
5. Established best practices and pitfalls: where visual-regression flakiness comes from, when to gate in CI vs local, the role of Storybook, accessibility/contrast checks, and what leading teams / Anthropic guidance recommend for agentic design review in 2025-2026.

Prioritise concrete, current (2025-2026) tools and workflows over generic advice. Note maturity/adoption and cost/complexity of each so the findings can be weighed for a small solo-dev local-first setup.

### Resolution Criteria (Pre-Committed)

A strong answer: (a) names concrete, current tools with maturity/cost, not generic advice; (b) resolves the central tension — heavy automated visual verification vs lightweight assertion-based checking — with evidence, not preference; (c) is honest about what each tier does *not* catch; (d) is weighable for a solo, local-first, token-based stack with no design-team handoff. Evidence that would change the conclusion: independent (non-vendor) data showing pixel-VRT false-positive rates are low and maintenance is cheap; or evidence that DOM/computed-style assertions miss a large class of real design regressions.

---

## Bottom Line

For a solo-dev, local-first, token-based stack (Vite + React + Tailwind v4 + shadcn/Base UI, Playwright e2e, a browser MCP), the evidence points consistently — though without any controlled solo-dev ROI study (see §Synthesis) — to a **layered loop, lightweight by default**:

1. **Deterministic assertions are the gate.** Computed-style + semantic assertions (`toHaveCSS`, `boundingBox`, `toMatchAriaSnapshot`, `toHaveRole`/`toHaveAccessibleName`, axe-core) are fast, near-zero-flake, and capture *most* design invariants that an agent can regress in a token-based system. This is the highest-ROI tier and the one to invest in. **One structural caveat that matters precisely because the spec is token-based:** `toHaveCSS` asserts the *resolved* value (`16px`, `oklch(...)`), not *which token was applied* — `getComputedStyle` collapses custom properties. To assert token identity you need `el.evaluate(n => getComputedStyle(n).getPropertyValue('--token'))` or CSSOM inspection, not `toHaveCSS`. In practice, assert the resolved value (which is what users see) and rely on lint (§4) for token-identity discipline.
2. **AI/vision is the triage + intent layer, not the gate.** An agent screenshotting the running app and comparing to the spec — ideally a *separate evaluator* agent — interprets intent and explains diffs. It is non-deterministic and misses sub-pixel/colour drift, so it never becomes the pass/fail authority. This is exactly Anthropic's own published guidance.
3. **Pixel visual-regression (VRT) is optional and earns its place only under specific conditions** (pixel-precise brand work, stable design, a diff dashboard someone actually reviews). Its dominant failure mode is environmental flakiness → review fatigue → shelfware. If adopted: run in a pinned Docker/CI environment, never locally-baselined, never auto-updated.
4. **Figma tooling is irrelevant when Figma isn't the source of truth.** The official Figma Dev Mode MCP is real but rate-limited behind paid Dev seats; for a design-in-browser / spec-as-artifact workflow, a committed `tokens.json` + Tailwind v4 `@theme` is the checkable ground truth, with no subscription or sync burden. "Claude Design" (Apr 2026) is a prompt-to-prototype creator, **not** a verification tool.

The strongest, most independently-corroborated finding: **the "minimal loop" — measure load-bearing invariants + one screenshot read + promote anything that bites to a permanent e2e assertion — captures the bulk of the value of heavy VRT tooling at near-zero maintenance cost.** It was reached from *opposite evaluative stances* — the pro-tooling best-practices track (citing Anthropic + Tweag + Connsulting) and the anti-tooling contrarian track (citing the snapshot-test backlash and VRT-abandonment literature) — and it matches both Anthropic's guidance and the workflow this repo already uses. (Both tracks were briefed from the same anchor, so read this as robustness across stances, not fully independent discovery.)

---

## 1. Verifying a Change Objectively (Not Eyeballing)

Three comparison modalities, in increasing flakiness and decreasing determinism:

**DOM / computed-style assertions — the deterministic floor.** Playwright `toHaveCSS('gap', '16px')` asserts the *computed* value (post-cascade, auto-retried); `locator.boundingBox()` gives `{x,y,width,height}` in CSS pixels; `page.evaluate(() => getComputedStyle(el)...)` runs any measurement in-browser; `toMatchAriaSnapshot()` (Playwright 1.49, late 2024) is a "textual screenshot" of the a11y tree — robust to layout/pixel noise. These have near-zero environmental flakiness and are ideal for token-level conformance (spacing, colour, typography, structure). They cannot judge gestalt. **Known limitation (corroborated by 3 agents): `toHaveCSS` cannot read CSS custom properties** — it collapses to resolved values; assert the *resolved* value (`oklch(...)`/`16px`), not the token name. Asserting which *variable* was used requires brittle CSSOM inspection ([Playwright #12629](https://github.com/microsoft/playwright/issues/12629), [#20321](https://github.com/microsoft/playwright/issues/20321)) — still unfixed as of Playwright v1.60 (Apr 2026), which added a `pseudo` option but not custom-property reads.

**Pixel / perceptual screenshot diffing — the gestalt layer, environmentally fragile.** Playwright's built-in `toHaveScreenshot()` uses pixelmatch with `threshold`/`maxDiffPixels`/`mask`/animation-disable options ([docs](https://playwright.dev/docs/test-snapshots)). Algorithm choice (pixelmatch vs odiff vs SSIM vs pHash) matters less than environmental determinism: "Environmental determinism beats algorithm choice" — most false positives trace to OS font rendering, GPU anti-aliasing, and DPI, not the differ ([Wopee.io](https://wopee.io/blog/screenshot-comparison-algorithms-visual-testing/)). SSIM is forgiving of anti-aliasing (a font-hinting change scoring 0.998 looks identical) but is a targeted fix, not a global replacement.

**AI/LLM "visual judge" — intent interpretation, non-deterministic.** Vision LLMs grade a screenshot against a reference. The Oct-2025 *MLLM as UI Judge* benchmark (9,296 human ratings) found ≥75% within ±1 Likert point, Claude highest exact-match at 38% (vs GPT-4o 37% — a 1-point margin), pairwise preference ~60% overall (90–93% only for clearly dissimilar UIs) — authors conclude "supplement, not replace" ([arXiv 2510.08783](https://arxiv.org/html/2510.08783v1)). LLM judges reliably flag large structural changes and explain them in English but **miss subtle per-pixel/colour regressions** unless given explicit rubrics, and are non-deterministic by construction. Production AI-triage layers (Percy Visual Review Agent, Oct 2025; Applitools Eyes) reduce diff noise (~40% claimed) but publish no independent accuracy data.

**Consensus across all three facet agents:** these are complementary layers, not competitors. *Deterministic checks are the gate; AI reduces the build/maintenance cost around it* ([Bug0](https://bug0.com/knowledge-base/visual-regression-testing-tools)).

### Tool Landscape (Visual Regression)

| Tool                                                       | Type                     | Local/Hosted       | Solo-dev cost          | Flakiness                   | Maturity                     | Note                                                                                |
| ---------------------------------------------------------- | ------------------------ | ------------------ | ---------------------- | --------------------------- | ---------------------------- | ----------------------------------------------------------------------------------- |
| Playwright `toHaveCSS`/`boundingBox`/`toMatchAriaSnapshot` | DOM/semantic assertion   | Local              | Free                   | Near-zero                   | First-party, excellent       | Highest ROI; no baseline to maintain                                                |
| Playwright `toHaveScreenshot`                              | Pixel diff (pixelmatch)  | Local or CI-Docker | Free                   | High locally; low in Docker | First-party, excellent       | Must baseline in the same Docker image as CI                                        |
| Argos                                                      | Pixel diff, hosted       | SaaS               | Free ≤5k; $100/mo·35k  | Low (cloud-rendered)        | Active                       | Best hosted fit; no Storybook needed (but a pricing change drove Ant Design off it) |
| Percy                                                      | Pixel diff + AI triage   | SaaS               | Free ≤5k; paid $399/mo | Low; AI cuts review noise   | Active                       | Visual Review Agent is the 2025 differentiator                                      |
| Chromatic                                                  | Pixel diff, hosted       | SaaS               | Free ≤5k; $149/mo+     | Low                         | Excellent                    | **Requires Storybook**                                                              |
| reg-suit                                                   | Pixel diff (BYO capture) | Local + S3/GCS     | Free + storage         | = your capture tool         | Active (Feb 2026)            | Composable, more ops glue                                                           |
| BackstopJS                                                 | Pixel diff               | Local              | Free                   | High without Docker         | Declining (last release ~2y) | Mature but stagnant                                                                 |
| Applitools Eyes                                            | AI visual diff           | SaaS               | ~$969/mo+              | Low (opaque)                | Enterprise                   | Overkill solo; no published accuracy                                                |
| Lost Pixel                                                 | Pixel diff               | —                  | —                      | —                           | **Archived Apr 2026**        | Team joined Figma — do not adopt                                                    |

---

## 2. Pulling the Spec into the Loop

**Official Figma Dev Mode MCP (GA-ish beta since Jun 2025):** 18 tools incl. `get_variable_defs` (tokens), `get_metadata` (positions/sizes), `get_design_context` (React+Tailwind scaffold), `get_screenshot` (base64 PNG), `get_code_connect_map`. **The rate limits are the killer for agentic use: 6 tool calls/month on Starter/View seats; ~200/day needs a paid Dev/Full seat** ([rate-limit docs](https://developers.figma.com/docs/figma-mcp-server/plans-access-and-permissions/)). **Code Connect** is the amplifier — without it the MCP returns generic scaffold; with it the agent gets real import paths/components (but mapping is non-trivial for shadcn/Base UI copy-in components). Crucially, the MCP is a *read/generation* integration — **it does not verify implementation against design; the agent must do that reasoning.**

**Framelink "Figma Context" MCP (third-party, Feb 2025):** ~11k★ (some sources cite ~15k), ~105k weekly downloads; raw descriptive JSON, ~25% smaller payloads, **free, no seat requirement** — the practical alternative without a Dev seat. No Code Connect. Keep it current — an RCE (CVE-2025-53967) was patched in v0.6.3, Sep 2025.

**figma-to-code reliability:** good for auto-layout/flex/variables; weak on corner radii, responsive, deep nesting. Developer review still required. Neither MCP closes the fidelity gap alone.

**Tokens as the checkable spec (the no-Figma path):** `Figma Variables → Tokens Studio (Git sync, W3C DTCG) → tokens.json in repo → Style Dictionary → CSS vars`, consumed natively by Tailwind v4 `@theme`. A committed `tokens.json` (DTCG reached its first stable version Oct 2025) is machine-readable ground truth an agent can diff computed styles against — **portable, git-tracked, no Figma subscription**. The naming convention (`color/primary/600` ↔ `--color-primary-600`) is the load-bearing coupling.

**"Claude Design" (Anthropic Labs, 17 Apr 2026):** a conversational prompt-to-prototype creation tool (research preview). It is **not** an MCP, not a spec-ingestion layer, not a verification agent. Exhaustive search of anthropic.com/news, research, the cookbook, and Claude docs found **no Anthropic product or guide for "agentic design review" / "spec checking."** The closest published guidance is the general agentic-coding feedback-loop advice (§5).

**Spec representations for an agent, lowest→highest friction:** (1) committed `tokens.json` + generated CSS — static, CI-friendly, no Figma dependency at verify time; (2) reference screenshot + pixel/vision diff; (3) Figma MCP `get_variable_defs`/`get_design_context` — live, needs a seat; (4) Code Connect — highest precision, most setup.

---

## 3. Browser MCPs for Driving the Running App

| Tool                             | Measure DOM (getBoundingClientRect/ComputedStyle)         | Real input (hover/focus/click)             | Screenshot   | a11y tree                     | Perf                                 | Maturity                         |
| -------------------------------- | --------------------------------------------------------- | ------------------------------------------ | ------------ | ----------------------------- | ------------------------------------ | -------------------------------- |
| **chrome-devtools MCP** (Google) | Yes — `evaluate_script` (unrestricted JS)                 | Yes (10 input tools)                       | Yes          | Yes (`take_snapshot`)         | Full (LCP/INP/CLS, Lighthouse, heap) | v1.1.1, ~42k★, post-1.0          |
| **Playwright MCP** (Microsoft)   | Yes — `browser_evaluate` (pass JS *string*, not TS arrow) | Yes (real events)                          | Yes          | Yes (default mode, low-token) | Tracing (opt-in)                     | v0.0.75, ~33k★                   |
| **claude-in-chrome** (Anthropic) | Via injected JS (no named eval tool)                      | Yes (CDP)                                  | Yes (+ GIF)  | No                            | No                                   | Beta, all paid plans             |
| **computer-use** (Anthropic)     | No (pixel-level only)                                     | Native apps only; **browsers = read-only** | Desktop only | No                            | No                                   | Research preview, Pro/Max, macOS |

Takeaways: **chrome-devtools MCP and Playwright MCP are equivalent for the core review job** (geometry via `evaluate`, real input, element screenshots). chrome-devtools adds DevTools/perf/Lighthouse depth; Playwright MCP adds a low-token a11y-tree snapshot mode (~200–400 tokens vs ~3–5k for a screenshot), opt-in `toHaveScreenshot`, and codegen. **claude-in-chrome** does real input via CDP but lacks an ergonomic named `evaluate`, so geometry measurement is clunkier. **computer-use is the wrong tool for a localhost web app** (browsers are read-tier — it can see but not click). Notable gotcha: the Playwright **CLI** is community-benchmarked at ~4× fewer tokens than its MCP (~27k vs ~114k per task) — at some latency cost from file round-trips; Microsoft frames the CLI as the more token-efficient path and the MCP as best for interactive/human-in-the-loop review.

---

## 4. Tailwind / Design-Token Review

**Token-usage enforcement (ban magic values), best→adequate:**

- **`oxlint-tailwindcss`** (Mar 2026, v0.1.x) — strongest: reads your `@theme` tokens directly via `@tailwindcss/node`, rules `no-hardcoded-colors`, `no-arbitrary-value`, `prefer-theme-tokens` (rewrites `bg-[var(--primary)]`→named utility), autofix, CI-safe. v4-only by design; young.
- **`@poupe/eslint-plugin-tailwindcss`** — full v4 (`@theme`/`@apply`/etc.), `prefer-theme-tokens` + `no-arbitrary-value-overuse`. ESLint 9+ only.
- **`eslint-plugin-tailwindcss`** (francoismassart) — has `no-arbitrary-value` but **v4 support is partial/beta** with false positives.
- **`eslint-plugin-better-tailwindcss`** (schoero) — actively maintained, v3+v4; strong on correctness (unknown/conflicting/duplicate classes), shorthand, logical properties — but **no magic-value/token-enforcement rule**, so it complements rather than replaces the above for token discipline.
- **Biome** — `useSortedClasses` sorts only; v2.3 parses `@theme` syntax but has **no token-enforcement rule**. (Relevant: this repo lints with Biome, which covers class *order*, not magic-value bans.)
- **Deslint** — commercial; ships an **MCP server** so an agent can query token-scale violations in-context; imports scales from Figma/Style Dictionary.

**Checking computed styles resolve to the right token:** `toHaveCSS('background-color', 'oklch(...)')` asserts the *resolved* value; the custom-property *name* is not assertable via `getComputedStyle` (collapses to value). Pattern: `el.evaluate(n => getComputedStyle(n).getPropertyValue('--color-primary'))` for presence.

**The `@theme inline` trap (high-value, specific):** standard `@theme` emits `var(--token)` (cascade-overridable); **`@theme inline` resolves the value into the utility, breaking surface/dark-mode overrides** — a documented case had `@theme inline` hide a 2.06:1 contrast failure from a 200-scan axe matrix until reverted ([case study](https://dev.to/forrestmiller/tailwind-v4-dark-mode-the-theme-vs-theme-inline-gotcha-that-broke-my-contrast-tests-3p3o)). **shadcn/ui uses `@theme inline` deliberately** (two-layer `--background` → `--color-background`), trading cascade-overridability for predictability — worth knowing for any shadcn-based repo doing contrast/theming review. **This repo is one** (`frontend/src/styles.css` uses `@theme inline`), so the trap is live here: dark/light surface overrides that go through a wrapper class may not take effect, and an axe contrast matrix can miss it — verify theme overrides with a resolved-value check, not just the lint.

---

## 5. Best Practices, Pitfalls, and What Anthropic Recommends

**VRT flakiness root causes (ranked):** font rendering across OS/headless (#1), animation race conditions, dynamic content, DPI/device-pixel-ratio, third-party resources, async font load. **~80% of false positives are killed by:** `document.fonts.ready` wait + animation disable + masking dynamic regions + fixed viewport + `--force-device-scale-factor=1` + `--font-render-hinting=none`, and — for cross-platform — **generating baselines inside the official Playwright Docker image in CI, never locally**.

**Where to gate (solo dev):** local = fast functional + axe spot-checks; CI (PR/main only, not every commit) = authoritative VRT + axe WCAG AA. **Never auto-update baselines in CI** (Playwright's own guidance) — that recreates the `jest --updateSnapshot` antipattern. Hosted review (Chromatic/Percy free tiers) adds value *only if someone actually reviews the dashboard* — "if Chromatic sits unreviewed, it becomes useless."

**Storybook:** skip for a solo Vite/React app — Playwright e2e already covers the surface, and the Storybook Test Runner is now superseded by the Vitest addon. Add it only for component isolation or a design-team catalogue (and Chromatic *requires* it).

**Accessibility:** `@axe-core/playwright` auto-catches ~30–57% of WCAG issues (~30% per WebAIM; 57% self-reported by Deque for axe) — structural + static-text contrast; it **misses** hover/focus contrast, keyboard-nav quality, dynamic `aria-live`, and meaningful label text. Gate axe AA in CI; supplement with a manual keyboard pass on new interactive components.

**Anthropic's explicit guidance** ([Claude Code best practices](https://code.claude.com/docs/en/best-practices), [harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)):

- "Verify UI changes visually: [paste screenshot] … Take a screenshot of the result and compare it to the original. List differences and fix them." A browser screenshot is treated as a verification signal *on par with test output*.
- Hardening ladder: in-prompt screenshot → `/goal` re-check each turn → stop-hook deterministic gate → **verification subagent** ("the agent doing the work isn't the one grading it").
- For subjective design quality, give a *separate evaluator* the browser (Playwright MCP) to navigate/screenshot the live page before scoring against gradable criteria.

Practitioner corroboration: Tweag (annotated, *specific* screenshot critique beats vague), Connsulting ("if the agent cannot run the app, drive the browser, inspect, fix, and re-test, you don't have a closed loop"; deterministic gates accelerate, judgment gates stay human), and Tal Rotbart's "Giving Claude Code Eyes" round-trip loop.

---

## 6. The Contrarian Thesis (And Why It Largely Holds)

The strongest critical finding, well-sourced and consistent across years (HN 2019→qtrl 2026): **VRT fails operationally, not technically — review fatigue from false positives is the dominant abandonment cause.** "Just update the baseline" is isomorphic to `jest --updateSnapshot`; the snapshot-test backlash (Sapegin, Gard) is the same lesson one layer down. Screenshot VRT sits at the apex of the test pyramid (full browser + font + GPU + OS stack), so its false-positive "cone of influence" is enormous (Fowler's pyramid / ice-cream-cone antipattern). Concrete datapoint: Ant Design abandoned hosted VRT after ~6,000 screenshots/PR became cost-prohibitive and built a self-hosted replacement.

For a solo dev whose design system *is* tokens (Tailwind classes/CSS vars), `toHaveCSS`/`toMatchAriaSnapshot` give deterministic, zero-baseline assertions on the invariants that matter; Figma integration is "irrelevant infrastructure" when there's no maintained Figma source of truth. The **minimal viable loop**: measure load-bearing invariants in the existing Playwright suite → one `shot-scraper`/MCP screenshot read per changed route → **promote anything that bites to a permanent assertion (don't keep the screenshot as a baseline)**.

---

## Synthesis: Agreements, Tensions, Emergent Patterns

**Independent agreements (high confidence — different agents, different source domains):**

- Deterministic-gate + AI-triage layering (all five non-contrarian facets converge; Anthropic states it explicitly).
- DOM/computed-style assertions are the highest-ROI tier for token-based systems (objective-verification, best-practices, contrarian all independently).
- VRT flakiness is environmental, not algorithmic; Docker/CI baselining is the fix (objective-verification + best-practices, separate source sets).
- `toHaveCSS` can't read custom-property *names* (objective-verification, tailwind-tokens, contrarian — three independent hits on the same Playwright issue).

**Tensions:**

- *Is pixel VRT worth it at all for solo dev?* Best-practices says "yes, in CI/Docker, PR-only"; contrarian says "usually no — assertions + one screenshot read suffice." Resolution: it's conditional on pixel-fidelity stakes and whether a diff dashboard is actually reviewed. Substituting *this* stack's facts into that conditional — token-based Tailwind v4, no brand-pixel-precise surfaces, no designer/Figma handoff, a single reviewer — every "yes" trigger is absent, so it resolves concretely to: **skip pixel VRT and Figma tooling; invest in the assertion + screenshot-read loop.** Revisit only if a brand-pixel-precise surface or a designer handoff appears.
- *Figma MCP value:* spec-into-loop is positive-but-qualified (powerful with Code Connect + paid seat); contrarian is negative when Figma isn't the source of truth. Both agree it's a *generation/read* aid, not a verification loop.

**Emergent (no single agent owns it):** the "minimal loop" is the same artifact reached from opposite directions — Anthropic's feedback-loop guidance, the best-practices deterministic-gate-with-AI-triage pipeline, and the contrarian anti-VRT case all land on *measure-invariants + screenshot-read + promote-to-e2e*. Robustness across opposite evaluative stances (pro- and anti-tooling), rather than full independence (both were briefed from the same anchor), is the strongest signal in this report.

**Claim strength:** Tool capabilities/pricing — strong (vendor docs, dated). VRT-abandonment dynamics — strong (many independent practitioners over years). AI-judge accuracy — moderate (one good benchmark; vendor triage claims unaudited). "Minimal loop is sufficient" — moderate-to-strong (consistent practitioner + Anthropic signal; no controlled solo-dev ROI study exists).

**Uncertainties / not found:** no independent benchmark of AI-diff false-positive rates; no controlled solo-dev VRT ROI study; exact post-beta Figma MCP pricing; whether `toHaveCSS` on computed Tailwind values stays stable across Chrome/Tailwind upgrades.

### Pre-Mortem — If the Bottom Line Is Wrong, Why?

The recommendation ("lightweight assertion + screenshot-read loop; skip heavy VRT/Figma") fails if its assumptions break:

- **Pixel fidelity is actually load-bearing** (brand/marketing surfaces, charts where a 2px shift is a real bug) → assertions miss it; targeted pixel VRT on those few surfaces pays off.
- **A real Figma source of truth + designer handoff appears** → the tokens-in-repo path under-uses available structure; Figma MCP + Code Connect + token sync becomes worth the seat cost.
- **The project grows past solo** (many components/contributors) → a component catalogue (Storybook) and a reviewed VRT dashboard start catching cross-cutting regressions that ad-hoc reads miss.
- **AI-judge non-determinism bites** — if the screenshot-read step rubber-stamps a regression it didn't "see," the loop gives false confidence; mitigate with a *separate* evaluator and by promoting load-bearing invariants to deterministic assertions (which the loop already prescribes).

---

## Review Process

Two independent reviewers (accuracy/gaps + synthesis-quality), one round. Both judged the doc well-sourced with no material errors and the core recommendation sound; convergence reached after incorporating the findings below.

| #   | Reviewer finding                                                                                                      | Response                                                                                    | Outcome                                                                                                                  |
| --- | --------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| 1   | (synth, major) `toHaveCSS` token-identity limitation never reaches the bottom line, though tokens are the stated spec | Added the caveat to Bottom-line item 1                                                      | accepted                                                                                                                 |
| 2   | (synth, major) "evidence converges hard" overclaims vs §Synthesis's own "moderate-to-strong, no controlled study"     | Softened to "points consistently — though without controlled ROI data"                      | accepted                                                                                                                 |
| 3   | (synth, minor) Synthesis names the pixel-VRT tension but doesn't resolve it for *this* stack                          | Added the concrete substitution → "skip pixel VRT and Figma tooling" for this stack's facts | accepted                                                                                                                 |
| 4   | (synth, minor) `@theme inline` trap flagged without saying if it applies here                                         | Verified `frontend/src/styles.css` uses `@theme inline`; marked the trap live + mitigation  | accepted                                                                                                                 |
| 5   | (synth, minor) / (accuracy) Framelink CVE disproportionate; star count ~11k not 15k                                   | Trimmed CVE to "keep current"; corrected to "~11k (some cite ~15k)"                         | accepted                                                                                                                 |
| 6   | (synth, minor) / (accuracy) Playwright-CLI "4× / Microsoft recommends" loosely attributed; omits latency              | Reframed as community-benchmarked ~4×, added latency-cost caveat                            | accepted                                                                                                                 |
| 7   | (synth, minor) "minimal loop arrived at independently" overstates — same anchor seeded both tracks                    | Reframed as robustness across opposite stances, not full independence (twice)               | accepted                                                                                                                 |
| 8   | (synth, minor) GUISpector is a dangling reference                                                                     | Dropped from references                                                                     | accepted                                                                                                                 |
| 9   | (accuracy, minor) MLLM "Claude highest exact-match" is a 1-point margin                                               | Added "(vs GPT-4o 37% — a 1-point margin)"                                                  | accepted                                                                                                                 |
| 10  | (accuracy, minor) axe 30–57% figure uncited                                                                           | Added WebAIM (~30%) / Deque (57%) attribution                                               | accepted                                                                                                                 |
| 11  | (accuracy, minor) `eslint-plugin-better-tailwindcss` omitted from the Tailwind landscape                              | Added it to §4 (correctness-focused, no token-enforcement rule)                             | accepted                                                                                                                 |
| 12  | (accuracy, minor) note `toHaveCSS` CSS-var limit still unfixed in current Playwright                                  | Added "still unfixed as of v1.60 (Apr 2026)"                                                | accepted                                                                                                                 |
| 13  | (accuracy, minor) computer-use: terminals/IDEs are click-tier, not just browsers read-tier                            | Not added                                                                                   | rejected: disproportionate — tangential to localhost-web-app review; the browser read-tier point is the load-bearing one |
| 14  | (accuracy, minor) claude-in-chrome "no named eval tool" not primary-source verified                                   | No change                                                                                   | accepted: already hedged in text ("via injected JS (no named eval tool)")                                                |

## References

Objective verification: [Playwright assertions](https://playwright.dev/docs/test-assertions) · [Playwright visual comparisons](https://playwright.dev/docs/test-snapshots) · [#12629 custom-property limitation](https://github.com/microsoft/playwright/issues/12629) · [Wopee.io diff algorithms](https://wopee.io/blog/screenshot-comparison-algorithms-visual-testing/) · [Chromatic pricing](https://www.chromatic.com/pricing) · [Percy plans](https://www.browserstack.com/docs/percy/overview/plans-and-billing) · [Percy Visual Review Agent](https://www.browserstack.com/release-notes/en/introducing-percys-visual-review-agent-iqB3J3UT) · [Argos pricing](https://argos-ci.com/pricing) · [reg-suit](https://github.com/reg-viz/reg-suit) · [Lost Pixel (archived)](https://github.com/lost-pixel/lost-pixel) · [Applitools Visual AI](https://applitools.com/platform/validate/visual-ai/) · [MLLM-as-UI-Judge, arXiv 2510.08783](https://arxiv.org/html/2510.08783v1) · [Docker baselining](https://adequatica.medium.com/operating-system-independent-screenshot-testing-with-playwright-and-docker-6e2251a9eb32)

Spec into loop: [Figma MCP intro](https://www.figma.com/blog/introducing-figma-mcp-server/) · [Figma MCP tools](https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/) · [Figma MCP rate limits](https://developers.figma.com/docs/figma-mcp-server/plans-access-and-permissions/) · [Code Connect](https://developers.figma.com/docs/figma-mcp-server/code-connect-integration/) · [Framelink](https://github.com/GLips/Figma-Context-MCP) · [CVE-2025-53967](https://www.endorlabs.com/learn/cve-2025-53967-remote-code-execution-in-framelink-figma-mcp-server) · [Tokens Studio → Style Dictionary](https://docs.tokens.studio/transform-tokens/style-dictionary) · [DTCG stable](https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/) · [Claude Design announcement](https://www.anthropic.com/news/claude-design-anthropic-labs)

Browser MCPs: [chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) · [chrome-devtools-mcp blog](https://developer.chrome.com/blog/chrome-devtools-mcp) · [Playwright MCP](https://github.com/microsoft/playwright-mcp) · [Playwright MCP snapshots](https://playwright.dev/mcp/snapshots) · [pixel-perfect Playwright+Figma](https://vadim.blog/pixel-perfect-playwright-figma-mcp) · [Claude Code Chrome](https://code.claude.com/docs/en/chrome) · [Claude Code computer use](https://code.claude.com/docs/en/computer-use)

Tailwind tokens: [oxlint-tailwindcss](https://github.com/sergioazoc/oxlint-tailwindcss) · [@poupe/eslint-plugin-tailwindcss](https://github.com/poupe-ui/eslint-plugin-tailwindcss) · [eslint-plugin-tailwindcss](https://github.com/francoismassart/eslint-plugin-tailwindcss) · [Biome useSortedClasses](https://biomejs.dev/linter/rules/use-sorted-classes/) · [Tailwind v4 theme](https://tailwindcss.com/docs/theme) · [@theme inline contrast trap](https://dev.to/forrestmiller/tailwind-v4-dark-mode-the-theme-vs-theme-inline-gotcha-that-broke-my-contrast-tests-3p3o) · [shadcn Tailwind v4](https://ui.shadcn.com/docs/tailwind-v4) · [sd-tailwindv4](https://github.com/tokens-studio/sd-tailwindv4)

Best practices / pitfalls: [Claude Code best practices](https://code.claude.com/docs/en/best-practices) · [Anthropic harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps) · [Playwright a11y](https://playwright.dev/docs/accessibility-testing) · [Playwright ARIA snapshots](https://playwright.dev/docs/aria-snapshots) · [Desplega VRT hardening](https://www.desplega.ai/blog/deep-dive-3-visual-regression-testing-production-hardening) · [Playwright+Docker](https://noraweisser.com/2026/02/01/visual-testing-with-playwright-and-docker/) · [Tweag visual feedback](https://tweag.github.io/agentic-coding-handbook/WORKFLOW_VISUAL_FEEDBACK/) · [Connsulting concentric loops](https://www.connsulting.io/blog/concentric-feedback-loops)

Contrarian / ROI: [VRT is Stupid — Lamping](https://dev.to/klamping/visual-regression-testing-is-stupid-3cfn) · [What's wrong with snapshot tests — Sapegin](https://medium.com/@sapegin/whats-wrong-with-snapshot-tests-37fbe20dfe8e) · [Ant Design VRT](https://ant.design/docs/blog/visual-regression/) · [It's time to disrupt VRT — Ward](https://www.tonyward.dev/articles/visual-regression-testing-disruption) · [Giving Claude Code Eyes — Rotbart](https://medium.com/@rotbart/giving-claude-code-eyes-round-trip-screenshot-testing-ce52f7dcc563) · [Ministry of Testing: false positives](https://club.ministryoftesting.com/t/false-positives-in-visual-regression-testing/35145) · [Test Pyramid — Fowler](https://martinfowler.com/bliki/TestPyramid.html) · [Ice cream cone antipattern](https://bugbug.io/blog/software-testing/ice-cream-cone-anti-pattern/)
