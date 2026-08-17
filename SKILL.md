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

1. **The job description** — URL or pasted text. If it's a JS-rendered ATS page (Greenhouse/
   Oracle/Taleo/Workday), a plain fetch returns the shell only. Fast paths: a Greenhouse
   `?gh_jid=NNN` careers page has clean JSON at
   `https://boards-api.greenhouse.io/v1/boards/<token>/jobs/NNN?content=true` (try the company
   slug as `<token>`); otherwise render it in a browser and extract. Pull: title, team, core
   duties, required + preferred quals, the exact keywords, AND who it reports to — find the hiring
   manager and read their public profile; it sets the register (see Voice-extract).
2. **The user's LinkedIn export** — the authoritative record for titles, dates, employers, certs.
   Full export is a zip of CSVs (`Positions.csv`, `Education.csv`, `Certifications.csv`,
   `Recommendations_Received.csv`, `Recommendations_Given.csv`, `Shares.csv`, `Comments.csv`,
   `Skills.csv`); the profile PDF works too. Parse it — do not trust prior resumes over the export
   for titles/dates. `Shares`/`Comments`/`Recommendations_Given` are the applicant's own **voice**;
   `Recommendations_Received` is **social proof**; scan `Certifications` for same-provider
   duplicates (e.g. an "Emeritus" cert that is really the MIT xPRO program — one issuer, not two).
3. **Any repo / portfolio / prior resume** — for substance, metrics, and shipped-artifact proof.
   Prior resumes are *self-reported* claims, not ground truth; the export overrides them on facts.
   A live portfolio (a public-goods page, a build-in-public dashboard) is `documented` evidence and
   a proof-link (see Proof-link) — but verify it's live and public first.

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

## Parameters (set these per run — they change structure, never the honesty floor)

- `structure` — `narrative` (prose letter) | `value-receipts-90` (Day-0 value → receipts → a
  30/60/90 plan → close). The second reads as a confident value brief; reach for it when the
  counterpart is GTM/ops-minded. The 30/60/90 is framed as *approach*, never as promises.
- `pii_mode` — `full` | `github-only` (contact stripped to a portfolio/GitHub link; use when the
  applicant is routed through a third-party recruiter) | `recruiter-routed`. Never fabricate a
  contact detail you don't have — strip rather than invent. (Trade-off: a github-only resume with
  no email/LinkedIn parses with blank ATS contact fields and can read as agency-represented; when
  the applicant is applying *direct*, prefer a real email. Confirm the routing with them.)
- `register` — the hiring manager's, derived from their public writing when you have it (see
  Voice-extract); else tuned to their seat and flagged as such.
- `voice_source` — path to the applicant's LinkedIn export (their voice, not a generic one).
- `proof_links[]` — live, inspectable URLs that back a claim. Verify each is public/READY before
  linking (a 404 from a recruiter's click is worse than no link).

## Components (field-tested; compose as needed)

**Voice-extract (applicant).** The applicant's own writing is the best source for register. From a
LinkedIn export, parse `Shares.csv` (posts — openers, rhythm, coined metaphors, punctuation),
`Comments.csv` (casual voice), and `Recommendations_Given.csv` (their warm-professional voice).
Build a short voice profile: signature openers (aphoristic? paradox/reframe?), sentence rhythm,
punctuation habits (an em-dash lover, when the house style bans em-dashes, is honored with spaced
en-dashes), coinage density. A *flat* letter is usually missing exactly this: the sharp standalone
opener, one reframe of *what the job even is*, and a human/slightly-vulnerable beat. Use ONE vivid
line, not a pile-up — a cover letter is not a LinkedIn post (drop hashtags/emoji).

**Voice-extract (counterpart / register).** If you have the hiring manager's profile, read their
career arc for register (a GTM/demand-gen leader ≠ a brand purist ≠ a PMM purist). Nod once to
their domain from *real* facts, never a creepy employer recital. Without their actual writing, tune
to their seat, say so, and offer to match precisely from a pasted sample — don't invent a persona.

**Orthogonal-echo (the strongest proof).** Search the applicant's SHIPPED artifacts for one that
independently solves the same problem as the target's actual product/feature. That convergence
(arrived at independently, before reading the JD) is proof of fit that can't be reverse-engineered
from a posting. Frame as "converged independently," never "built it first" (you usually can't prove
precedence, and independence is the stronger claim). Must be real and public. Reference run: the
applicant's open-source `token-savings-bank` (LLM token budgeting) ↔ the employer's "AI Spend
Tracker" feature.

**Proof-link.** Attach a live URL at the claim it backs. Verify PUBLIC/READY first
(`gh api repos/<org>/<repo> --jq .visibility`, or fetch the page). Under `github-only` PII mode, a
portfolio/repo link is the one contact channel that stays.

**Term-of-art gate (verify before claiming).** Before writing any load-bearing technical term
(OpenTelemetry, zero-knowledge, RAG, fine-tuning) verify the artifact backs it — in the repo AND
live. In the reference run the applicant floated an "OTel observatory"; a check showed the live site
was a GitHub-API status page and the "Observatory" was a decision-replay demo — NOT OpenTelemetry.
It was cut. This matters most when the *target ships the real thing* (Opik has OTel integration): a
technical peer probes it in the first five minutes. Verify, or don't claim.

**Social-proof interleave (use with restraint).** Received recommendations are strong, named,
verifiable proof. If used, interleave a one-line pull-quote *at the exact company it came from*, not
as a floating band — placement integrity keeps it honest. But quotes crowd an experience section
fast; often the metrics + framing carry more signal clean, so default to sparing or none, and let
the applicant veto. Never list LinkedIn skill-endorsement *counts* — weak, gameable signal that
lowers the register.

**Layout / print discipline (the designed resume).** One glyph shape per tier (e.g. filled ◆ for
full-time, open ◇ for advisory), not a confusing mix. Number the depth-ladder sections and give each
a dot indicator that increments (01→1 dot … 05→5 dots); off-ladder sections (Education, showcases)
carry no number/dots. Indent sub-bullets under their headers. A page-2 whitespace budget is an
opportunity: a "public goods, positioned" card (each shipped tool = a linked H2 name + a positioning
lede) is itself proof of the craft. Make link-outs clickable (contact, repos, portfolio). Always
render → rasterize → LOOK (page-count is not a pass). Note: an ATS-plain companion still ships
alongside — the designed one is the leave-behind; keep the two in sync on facts.

## Exemplar — Comet Technical PMM (reference run)

A builder-who-markets applicant; target = Technical Product Marketing Manager at an OSS-LLM-tooling
company (Opik). What worked: (1) headline framing "builder who markets," NOT "engineer applying to
marketing" — an FDE/applied-AI frame pointed at the wrong req and strained the honesty gate;
(2) the orthogonal echo (token-savings-bank ↔ AI Spend Tracker) as centerpiece; (3) `value-receipts-90`
once the counterpart was a GTM VP; (4) voice tuned from the applicant's own LinkedIn posts;
(5) `github-only` PII for third-party-recruiter routing; (6) a genuine cultural-fit close (real
family/work ties), specific not pandering; (7) merged a same-provider cert dupe (MIT xPRO ≡ Emeritus).
Honesty holds that saved it: no "LLM engineering" (app-layer only), no PyTorch/TF (unbacked), no OTel
(unverified), no adoption claims. Tried-and-cut: interleaved recommendation quotes (crowded the
section; removed).

## Anti-goals

Do not: assert proficiency numbers as fact; imply distribution (npm/Homebrew) or adoption you can't
show; borrow a term-of-art (zero-knowledge, OpenTelemetry, RAG) the artifact doesn't back — *verify
in-repo AND live first, especially when the target ships the real thing*; self-grade ("bank-grade",
"world-class"); inflate one engagement into a specialty; double-count one credential as two issuers;
or declare "shipped" off a page-count. The quality floor is defensibly-true; the falsifier enforces it.
