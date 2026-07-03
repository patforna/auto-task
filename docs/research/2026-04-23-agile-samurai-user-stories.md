# The Agile Samurai — How to Write Good User Stories

Extracted from Chapters 5–10 of *The Agile Samurai* (Jonathan Rasmusson, 2010). Primary chapter: **6 "Gathering User Stories"** (book pp. 94–113). Supporting material: Ch 5 (sizing/conditions of satisfaction), Ch 7 (estimation), Ch 8 (planning), Ch 9 (making work ready), Ch 10.2 (story-planning meeting).

Source PDF: `Google Drive/_archive/learning/books/work/The Agile Samurai/the-agile-samurai_p1_0.pdf`.

---

## 1. Why Stories Exist (The Argument Against Documentation)

The book's starting claim is not "docs vs. cards" but **"writing vs. talking."**

> *"The problem with gathering requirements as documentation isn't one of volume — it's one of communication."*

Four failure modes of doc-heavy requirements: (a) they can't handle change; (b) teams build to spec instead of to what the customer actually wants; (c) they bake in bad assumptions; (d) most of the work is wasted on features that never ship. Beck is quoted: the word *"requirement"* is *"just plain wrong"* — absolutist, hostile to change. Of thousands of pages of requirements, *"if you deliver the right 5, 10, or 20 percent, you will likely realize all of the business benefit."*

The agile principle invoked verbatim: *"The most efficient and effective method of conveying information to and within a development team is face-to-face conversation."*

So a story is **"a promise of a conversation"** — a placeholder small enough to plan with, descriptive enough to remind you what you're talking about, but never the requirement itself.

---

## 2. What a Good Story *Is*

**Definition:**
> *"Agile user stories are short descriptions of features our customer would like to one day see in their software."*

**Optional template** (use when who/what/why matters; skip when it adds verbiage):

```text
As a <type of user>
I want <some goal>
so that <some reason>.
```

Vivid personas over generic "as a user" — the book's examples are *"surfer who likes to sleep,"* *"land-locked Canadian hockey player,"* *"grommet looking for the latest surf wear."*

### The Two Traits That Come Before INVEST

Called out separately in §6.3, before the acronym:

- **Valuable to customers** — *"What's valuable? Something they would pay for."*
- **End-to-end / slices the cake** — *"a good user story goes end-to-end slicing through all the layers of the architecture and delivers something of value."* Not a horizontal slab (UI-only, DB-only).

### INVEST (Bill Wake, Credited)

| Letter          | Book's gloss                                                                                                            |
| --------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **I**ndependent | Intertwined stories kill trade-off flexibility. End-to-end slicing + feature-grouping makes most stories independent.   |
| **N**egotiable  | *"We could build the Ford Focus, Honda Accord, or Porsche 911 version of any given feature."* Wiggle room is the point. |
| **V**aluable    | Business-framed, not technical. Something the customer would pay for.                                                   |
| **E**stimable   | Small enough to size with confidence. Can't size → spike it.                                                            |
| **S**mall       | *"One to five days"* — fits inside one- to two-week iterations.                                                         |
| **T**estable    | *"We like our stories to be testable (as opposed to detestable)."* Tests give the team *"a stake in the ground."*       |

---

## 3. Writing Mechanics

- **Business language, not technical jargon.** The Ernie's Tech Diner vs. Sam's Business Pancake House joke: *"C++ / Connection pooling / Model-View-Presenter"* → customer tunes out; *"Create user account / Cancel subscription"* → customer is engaged.
- **Rewrite technical work in customer-value terms.** Canonical example: *"Add database connection pooling"* → **"Reduce page load time from 10 secs to 2 secs."**
- **A few key words only.** *"The initial goal … isn't to get into all the details. It's to write down a few key words to capture the spirit of the feature."*
- **Breadth, not depth.** *"We are shooting for breadth (not depth) here."* Aim for 10–40 high-level stories for 3–6 months. *"If your stories number in the hundreds, either you're planning too far ahead or you're going into too much detail."*
- **Customers provide content; someone on the team usually does the writing.** The "It's OK to Help Customers Write Stories" sidebar.
- **Short name on the front, long-form on the back** is an acceptable compromise when the full template adds noise.

---

## 4. Acceptance Criteria & Constraints

**Testable** is operationalised as a bullet list of acceptance checks **on the card itself** — not a separate artefact. Book example, *"Login with expired account"*:

- Allow regular logins
- Re-direct expired logins
- Display appropriate error message
- Handle nonexistent user account

**Constraints ≠ stories.** Vague phrases like *"Website must be super-fast!"* or *"Design should look really good"* are characteristics, not features. Translate to measurable form: *"All web pages must load in less than 2 sec."* Capture on **differently-coloured cards**; test for them periodically.

Definition of "done" at story level = **customer-agreed test criteria verified by working software at the iteration showcase** (§10.3): *"real live code deployed on a test server. It's not pretty pictures or best intentions."*

---

## 5. Sizing and Splitting

**Philosophy:** *"High-level estimates are guesses."* Humans are bad at absolutes, good at relatives. Size stories **relatively** against each other, in points (t-shirt S/M/L ≈ 1/3/5). *"1 relative day ≠ 1 calendar day."* Keep the deck tiny — *"avoid the false sense of precision and noise"* of commercial 8/13/20/40 decks.

**How to size — triangulation:**

1. Pick a small, medium, and large reference story.
2. Peg them at 1, 3, 5 points.
3. Size everything else by comparison.

Who sizes: the people doing the work — *"developers, but it could also include DBAs, designers, technical writers, or anyone else responsible for the delivery."*

**Splitting triggers:**

- **Won't fit in one iteration?** Split it. *"Just break it down so it fits within a single iteration, update the plan, and move on."*
- **Can't size it (never done it before)?** Run a **spike** — a time-boxed investigation, usually a couple of days, to get enough information to estimate. You don't actually do the story.
- **Epics** are fine during initial gathering; break them down *"as if and when they come up for development."*

**Planning poker** is the team technique — wisdom-of-the-crowd, decks of 1/3/5. *"It's powerful because of the discussion."* Planning poker is not voting by seniority.

**Forecasts, not commitments:**
> *"Under no conditions can you let your customer think the plans you are presenting here are hard commitments."*

---

## 6. Making Stories "Ready" — Just-in-Time Analysis (§9.4)

Two pillars:

- **Just-enough** — *"Start light and add weight only when necessary."* No single right level of detail; scale artefacts to team size/distribution.
- **Just-in-time** — deep analysis happens **the iteration before** a story is built, not up front.

| Stage                                | What's produced                                                                                      |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| Story-writing / inception            | Card + conversation, rough size, priority, business intent                                           |
| Just-in-time (iteration *n* → *n+1*) | Flowcharts, personas, paper prototypes, task breakdown, **acceptance tests on the back of the card** |

Why defer: analysis uses the latest information, room to learn and innovate, avoids rework. Vindicating anecdote from the book: the "Print work permit" story was dropped at the last moment because browser printing was enough — *"Good thing we didn't waste any time on the analysis!"*

**Story-Planning Meeting (§10.2)** is the ready-state checkpoint — review test criteria with the customer, review estimates with developers, make sure the next batch is good to go.

Per the author's own "Done Means Done": *"Delivering a story in agile means analysis, testing, design, and coding. The whole thing."*

---

## 7. The Story-Gathering Workshop (§6.4)

Goal is **breadth**, not commitment — *"cast your net wide and discover as many features as possible."* Five moves:

1. **Get a big open room** — wall space for pictures, table space for cards.
2. **Draw lots of pictures** — personas, flowcharts, scenarios, system maps, paper prototypes. *"Pictures are a treasure trove for discovering stories."*
3. **Write lots of stories** — walk the diagrams with the customer, mining one story per flowchart step / one per button on a mockup. Look for end-to-end, 1–5 day slices.
4. **Brainstorm everything else** — non-feature work pictures won't surface: data migration, load testing, compliance, training, UAT. *"If there is something you need to do (even if it's not software related), create a card for it."*
5. **Scrub the list** — dedupe, fill gaps, group logical stories into a plan.

---

## 8. Anti-Patterns (All Called Out Explicitly by the Author)

**Writing:**

- Technical-jargon stories ("Add connection pooling") instead of customer value.
- Stretching the card into a mini-spec.
- Vague untestable stories ("super-fast", "looks good") — those are constraints.
- Horizontal slices (UI-only, DB-only).
- Intertwined, dependent stories — kill tradeoff flexibility.
- Generic "as a user" personas.

**Scope & size:**

- Hundreds of stories up front — planning too far out or too fine-grained.
- Deep analysis on stories that may never be built (64% of features are seldom/never used).
- Carrying a master list beyond ~6 months.
- Epics that don't get broken down when pulled for development.

**Estimation:**

- Turning up-front guesses into hard commitments.
- Chasing precision with commercial decks (8/13/20/40/100).
- Re-scaling all estimates when velocity drifts (use points, adjust velocity, leave estimates).
- Estimators who don't do the work.
- Three juniors "outvoted" by one senior.

**Execution:**

- Starting an iteration with unanalysed stories.
- Pretending stories are done when testing or UAT isn't complete.
- Measuring individual velocity.
- Hiding bad news. *"Bad news early is the agile way."*

---

## 9. Mapping to the `*-task` Skills in This Repo

The TAD task workflow (`/define-task → /create-task → /clarify-task → /plan-task → /impl-task → /code-review → /review-task`) already embodies most of Rasmusson's user-story ethos, often with stricter guard-rails. Where it differs, the difference is intentional (single-engineer codebase, AI-implementer audience).

### Strong Alignment

| TAD rule                                                                             | Agile Samurai principle                                                                        |
| ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| *"Stay at the what, not the how"* (`define-task`)                                    | *"Agile user stories are short descriptions of features."* No mechanics.                       |
| *"No code references — symbol names, file paths, import lists"*                      | *"Simple business language, no technical mumbo-jumbo."*                                        |
| *"A task should read like a product manager wrote it: plain English, behavioural"*   | *"Create user account / Cancel subscription"* (Sam's Business Pancake House).                  |
| *"Right-size the task to the work"* — one-paragraph tasks when that's enough         | *"A few key words to capture the spirit."* Breadth over depth.                                 |
| *"Write for an implementer with zero context beyond this file and the repo"*         | *"A placeholder for a conversation."* The card is a reminder, not a spec.                      |
| `/clarify-task` exists as a separate step                                            | Just-in-time analysis (§9.4) — the iteration-before deep-dive.                                 |
| `/plan-task` owns symbol names, file paths, verification gates                       | *"Don't dive too deep and get lost in the weeds"* at story-writing time.                       |
| CLAUDE.md §Tasks: *type: feat/tech/bug/research/other*                               | Rasmusson's non-feature stories (compliance, migration, training) — different-colour cards.    |
| `review-task` against working software                                               | *"Showing real live code deployed on a test server... the stuff you could go to battle with."* |
| Feedback memory: *"tasks: plain English, no file paths/symbol names/code mechanics"* | Direct restatement of Rasmusson's customer-language rule.                                      |

### Gaps Worth Thinking About

Four places where the book offers heuristics the TAD task skills don't currently bake in:

1. **Acceptance criteria as a bullet list on the card itself.** `define-task`'s *"Acceptance criteria (when the deliverable is ambiguous)"* section captures this, but the book's formulation is more disciplined — *every* story carries a short testable bullet list as the definition of "Testable" in INVEST. TAD treats AC as optional; Rasmusson treats testability as non-negotiable. For ambiguous tasks the TAD rule is the right one (*skip entirely when body names the deliverable unambiguously*), but it's worth noting that Rasmusson would push back: if a story genuinely has *no* observable test, it's probably a constraint, not a feature.

2. **The "slices the cake" / end-to-end heuristic.** The TAD skills don't explicitly frame tasks as end-to-end user-observable slices. For a backend-heavy quant codebase this is often fine (a task can legitimately be "move signal code into a separate package"), but for product work, the cake-slicing rule is a useful reframe: *"If your task only changes one layer, is it delivering something a user/caller can observe?"*

3. **Splitting triggers.** Rasmusson's splitting rules are sharper than TAD's: *split when it doesn't fit in one iteration* and *spike when you can't size it*. The TAD equivalent is implicit — epics with sub-tasks (`012.01-`, `012.02-`, etc.) — but there's no explicit "if you can't plan it in one session, spike or split" rule in the skill docs. The `research` type covers the spike idea.

4. **Constraints as first-class, separate artefacts.** Rasmusson splits performance/security/compliance requirements out of the story list onto different-coloured cards. TAD has `tech` tasks for cross-cutting non-functional work, which roughly maps — but the framing ("these are *characteristics*, not features, and you test for them periodically") is a useful lens when an AC list starts to include things like "must be fast" or "must not break existing behaviour."

### Quotes Worth Lifting into a CLAUDE.md or Skill Doc

If you ever want a pithy line to cite when pushing back on over-specified tasks:

- *"The card is not the requirement — it's a placeholder for a conversation."*
- *"We are shooting for breadth (not depth) here."*
- *"We like our stories to be testable (as opposed to detestable)."*
- *"Simple business language, no technical mumbo-jumbo."*
- *"Start light and add weight only when necessary."*
- *"Bad news early is the agile way."*

---

## TL;DR

A good story, per Rasmusson: **short, valuable, end-to-end, negotiable, small (1–5 days), estimable, testable, in customer language, one-card-sized.** The card exists to provoke a conversation — not to replace one. Detail is deferred until just before the work is pulled. Constraints and tech-speak get called out and rewritten.

The TAD `*-task` skills already enforce most of this — sometimes more strictly (no code references, PM-voice, right-sized). The main deltas worth considering are (1) acceptance tests as the default rather than the exception, (2) explicit end-to-end framing for product work, (3) sharper splitting rules (can't size → spike; won't fit one session → split), and (4) constraints as a separate artefact type.
