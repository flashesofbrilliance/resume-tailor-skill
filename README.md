# resume-tailor

Tailor a resume — and a matching cover letter — to a **specific role**, built from your
**real evidence** (LinkedIn export, repo/portfolio, the job description), not from vibes.

Most AI resume tools optimize for *impressive*. This one optimizes for **defensibly true**.
The core is a **falsifier**: it decomposes every claim into hard / soft / tacit, attaches the
evidence and a verifiability grade, and **refuses to state what it can't defend**. Then it
projects lead-with-strengths for the target JD, renders a print-safe PDF plus an ATS-plain
companion, and runs an adversarial **pre-send gauntlet** before anything ships.

## Why it's different

- **Honesty-graded SSOT** — one source of truth. Every claim carries `evidence` + a
  `verifiability` grade (`documented` / `self-reported` / `unverifiable`). Proficiency scores are
  *provisional hypotheses the falsifier exists to confirm*, never asserted facts.
- **Refuses to overclaim** — a claim it can't ground is flagged, not printed. Handles NDA /
  confidentiality boundaries explicitly (say the public fact, cut the nature-of-the-work).
- **Lead-with-strengths** — ranks the competency model by JD-relevance and projects the top.
- **Print-safe by construction** — standard `@page` margins, per-page frame, flattens cleanly
  for ATS; a matching cover letter; an ATS-plain single-column companion.
- **Adversarial pre-send gauntlet** — simulates the hiring panel across facets at high burden of
  proof and verifies every flag against your evidence before you send.

## What you get

- `SKILL.md` — the workflow Claude runs.
- `assets/competency-ssot.schema.json` — the honesty-graded competency model schema.
- `assets/resume-template.html` — the print-safe, framed, Exec→Surgical HTML resume template.
- `assets/cover-letter-template.html` — the matching cover-letter template.
- `assets/render.sh` — headless-Chrome HTML→PDF + rasterize-and-eyeball print check.

## Use

Ask Claude to *"tailor my resume for `<job posting URL>`"* (with your LinkedIn export handy).
The pre-send gauntlet uses the [`counterpart-gauntlet`](https://github.com/flashesofbrilliance/arcs-v9)
workflow when available.

MIT.
