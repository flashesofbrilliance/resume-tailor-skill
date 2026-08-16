---
name: resume-tailor
description: Tailor a resume and matching cover letter to a specific role from the user's REAL evidence — their LinkedIn export, repo/portfolio, and the job description. Build an honesty-graded competency model (every claim carries its evidence + a verifiability grade), refuse to state what can't be defended, project lead-with-strengths for the target JD, and render a print-safe framed PDF plus an ATS-plain companion, then run an adversarial pre-send gauntlet before anything ships. Use when the user wants to tailor, rewrite, or build a resume/cover letter for a specific job or company, says "make a resume for this role", pastes a job posting, or asks for an honest/defensible/ATS-safe resume. The differentiator is the falsifier core: optimize for defensibly-true over impressive.
---

# resume-tailor

Build a role-tailored resume the user can defend in a reference check — not one that sounds good.
The moat is the **falsifier**: every claim is graded against real evidence, and anything that
can't be grounded is flagged, not printed. Impressive-but-false is a ruin vector, not a rounding
error — a resume goes through background and reference checks.

## The one rule

**Never state what the evidence can't defend.** A claim that sounds good but is false is worse
than a weaker true claim. When unsure whether something is grounded, ask the user or flag it —
do not print it.

## Inputs to gather first

1. **The job description** — URL or pasted text. If it's a JS-rendered ATS page (Oracle/Taleo/
   Workday), a plain fetch returns nothing; render it in a browser and extract the text. Pull:
   title, team, core duties, required + preferred quals, and the exact keywords.
2. **The user's LinkedIn export** — the authoritative record for titles, dates, employers, and
   certs. Full export is a zip of CSVs (`Positions.csv`, `Education.csv`, `Certifications.csv`,
   `Recommendations_Received.csv`, `Skills.csv`); the profile PDF works too. Parse it — do not
   trust prior resumes over the export for titles/dates.
3. **Any repo / portfolio / prior resume** — for substance and metrics. Prior resumes are a
   source of *self-reported* claims, not ground truth; the export overrides them on facts.

## Stage 1 — Build the honesty-graded competency SSOT

Write `competency-model.json` (schema in `assets/competency-ssot.schema.json`). This is the single
source every render reads from. Decompose the user's experience into domains, each with:

- **competencies**, each tagged `hard` / `soft` / `tacit`, with:
  - `evidence` — the specific engagement/artifact it rests on.
  - `verifiability` — `documented` (public/inspectable: repo, commit count, live URL, cert badge),
    `self-reported` (their figure; plausible, not independently verified), or `unverifiable`
    (tacit/subjective).
  - `proficiency_provisional` (0–5) + `confirmed:false` — a HYPOTHESIS for the falsifier to
    confirm, never an asserted fact. You cannot grade the user's competence on your own authority.
  - `disclosure` — `when` (lead / support / hold), `why`, `how`.
  - `practice_gap` + `gap_note` — where proficiency < the claim the role wants.
- **levels** — Exec → Strategic → Operational → Tactical → Surgical (the depth ladder: the
  executive claim at top, the surgical receipt at bottom).
- **jd_relevance** (0–100) for this specific role.

Record known honesty tension points explicitly: single engagements inflated into specialties,
borrowed terms-of-art, self-graded scores, adoption claims a click refutes.

## Stage 2 — Falsifier pass

For each competency: is proficiency defensible against the evidence? Flag `practice_gap`s (real,
citable, but thin — e.g. one study ≠ a standing specialty). Flag `unverifiable` claims that read as
fact. Flag anything a background/reference check or a public lookup (Credly, npm, GitHub) would
contradict. **These flags are the user's interview-prep list and the resume's honesty guardrail.**

### Confidentiality / NDA boundary
If the user has an NDA, separate **public facts** (employer AUM, product count — often public) from
**nature-of-the-work** (specific systems built, internal metrics, architecture) — the latter stays
out. Mirror what their own public LinkedIn already discloses; do not overshoot past it. Confirm the
scope with the user; it's their legal call.

## Stage 3 — Lead-with-strengths projection

Rank domains by `jd_relevance`. The literal JD match leads; a strong differentiator supports, it
does not headline (leading with the lowest-relevance domain triggers the wrong screen). Order the
resume's experience reverse-chronologically; order the *framing* by relevance.

## Stage 4 — Render (see `assets/`)

- **Print-safe resume** — `assets/resume-template.html`. Standard `@page` margins (NOT full-bleed),
  a per-page bordering frame via a `position:fixed` element that repeats on each page, an Exec→
  Surgical depth-ladder spine, and any dark data-viz band converted to **light** to match the sheet.
  Screen may carry glassmorphism/tint; print flattens to a clean framed document.
- **Matching cover letter** — `assets/cover-letter-template.html`. Same identity header. Bank/formal
  register when the target is conservative. **No em-dashes in prose** (a common house rule — use
  comma/colon/period; the `—` in a Re: line or an official job title is fine).
- **ATS-plain companion** — a single-column version with standard section headers (EXPERIENCE,
  SKILLS, EDUCATION), no multi-column grids, no decorative glyphs baked into company-name text
  (set glyphs as CSS `::before`, not literal characters), plain ASCII phone punctuation. This is
  the file the user *uploads*; the designed one is the leave-behind.

### Print-eval discipline (mandatory)
A resume is a print deliverable. **Page-count is not a pass — look at the pixels.** Render with
`assets/render.sh` (headless Chrome → PDF), rasterize both pages (`pdftoppm`), and actually view
them. Verify: 1–2 pages, no orphaned section headers, no widows, glass flattened, margins clean.

## Stage 5 — Pre-send gauntlet (the gate)

Before anything is called done or published, run an adversarial gauntlet: simulate the hiring panel
across facets (recruiter/ATS, hiring-manager, technical peer, HR/compliance reference-check, rival
candidate, ruthless copy editor) at high burden of proof. **Every flag must be verified against the
evidence** (LinkedIn export, repo, the SSOT) — reject over-flags. Apply the survivors; they are
subtractive or scope-anchoring, never inflating. If the ARCS `counterpart-gauntlet` workflow is
available, use it with a ground-truth doc; otherwise run the facets inline.

## Stage 6 — Publish (gated)

Submittable PDF is what goes into the ATS. A hosted/interactive version is outward-facing — get
explicit user confirmation before any deploy, and re-run the NDA scrub against the live target
first. Verify the deploy reaches READY (canceled ≠ deployed).

## Anti-goals

Do not: assert proficiency numbers as fact; imply distribution (npm/Homebrew) or adoption you can't
show; borrow a term-of-art (zero-knowledge, OpenTelemetry) the artifact doesn't back; self-grade
("bank-grade", "world-class"); inflate one engagement into a specialty; or declare "shipped" off a
page-count. The quality floor is defensibly-true; the falsifier enforces it.
