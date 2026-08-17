# resume-tailor eval rubric

Outputs are subjective (writing + design) — grade qualitatively. A run passes only if **every HARD
check passes**; SOFT checks weigh quality; anti-signals dock it.

## HARD — the honesty floor (any failure = fail, regardless of polish)

- **Defensibly-true.** Every claim traces to `documented` or `self-reported` evidence in the SSOT.
  Nothing the applicant couldn't defend in a reference check.
- **No unbacked term-of-art.** Every load-bearing technical term (OpenTelemetry, RAG, fine-tuning,
  "evaluation" when the target means LLM-evals, zero-knowledge) was verified against the artifact,
  in-repo AND live. Cut or narrowed if unverified. Extra scrutiny when the *target ships the real
  thing*.
- **No category-error equivalence.** An orthogonal-echo may claim *same domain / independently
  converged*, never *same problem* when the two solve it from different sides (e.g. reduction vs
  observability). State the distinction; it's stronger than a false identity.
- **No fabricated PII.** Contact details are real or stripped, never invented.
- **Proof-links resolve.** Every linked URL is public/READY (checked), and the linked artifact's own
  README doesn't contradict the resume's description of it (a "mock scan" prototype is not a
  "working intelligence engine").
- **Facts reconciled.** Titles/dates checked against the LinkedIn export, not prior resumes.
- **Print-eval.** The PDF was rasterized and LOOKED at — 1–2 pages, no orphans/widows, glass
  flattened, clean margins. ATS-plain companion in sync on facts.

## SOFT — quality (weigh, don't gate)

- **Voice-match** — the letter reads like the applicant's own writing, not generic.
- **Register-fit** — tuned to the hiring manager's seat/voice; one honest domain nod, no pandering.
- **Lead-with-strengths** — the literal JD match leads; differentiators support, don't headline.
- **Orthogonal-echo present** when a real one exists — and used ONCE at full strength (repetition
  converts confidence into effort; a skeptical reader reads 3× as "doesn't trust me to remember").
- **Soft metrics stay subordinate** — self-reported/internal figures are labeled and don't sit so
  prominently that they invite an audit of the hard, documented numbers next to them.
- **Layout discipline** — uniform glyph-per-tier, incrementing section dots, sub-bullet indents,
  clickable link-outs.

## Anti-signals (presence = quality hit)

Self-grading ("world-class", "bank-grade"); inflated single engagements; implied adoption/
distribution; a hook repeated 2–3× instead of landed once; coined-metaphor pile-up; hashtags/emoji
in the letter; a credential double-counted as two issuers; a round-number seniority claim ("two
decades") that a dated roster invites auditing.
