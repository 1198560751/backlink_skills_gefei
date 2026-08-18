# Open-Source Backlink & Product Directory Submission Skill

> Created by [Flaq.ai](https://flaq.ai/) for AI coding agents such as Codex and Claude Code.

An evidence-backed, recoverable workflow for submitting products, software, startups, apps, and websites to product directories and other public discovery channels. The skill helps an agent research eligible routes, avoid duplicates, respect authorization boundaries, preserve manual verification steps, submit truthful information, and record outcomes that another operator can audit or resume.

Directory listings may create citations, referral traffic, or backlinks, but this project does **not** promise link placement, follow attributes, approval, indexing, traffic, or ranking improvements.

**Languages:** [English](README.md) · [简体中文](README_zh.md) · [繁體中文](README_tw.md) · [日本語](README_ja.md) · [한국어](README_ko.md) · [ไทย](README_th.md) · [Tiếng Việt](README_vi.md) · [Bahasa Indonesia](README_id.md) · [Español](README_es.md) · [Français](README_fr.md) · [Deutsch](README_de.md) · [Italiano](README_it.md) · [Português](README_pt.md) · [Русский](README_ru.md) · [العربية](README_ar.md) · [हिन्दी](README_hi.md) · [Türkçe](README_tr.md) · [Nederlands](README_nl.md) · [Polski](README_pl.md)

## What the skill supports

- Product, software, AI-tool, startup, company, app, and website listings
- `Request app` and recommendation routes
- Claim-listing and vendor applications
- Free account or public profile creation when authorized
- Blog, article, news, community, email, and contact-form submissions
- Resource pages, partner directories, and similar public discovery routes
- Eligibility, pricing, reciprocal-link, account, duplicate, and verification checks
- Evidence-backed status tracking and resumable campaign records

## Core safeguards

- Use only verified product, company, founder, pricing, contact, ownership, and legal facts.
- Never bypass CAPTCHA, Turnstile, 2FA, passkeys, email verification, or other safeguards.
- Never use CAPTCHA-solving services, stealth techniques, proxy rotation, or fingerprint evasion.
- Do not pay, enable renewal, add reciprocal links, change a website or DNS, upload verification files, or claim ownership without separate authorization.
- Do not treat account creation, a saved draft, a button click, or navigation as a published listing.
- Do not retry a final submission when the outcome is ambiguous; investigate first to prevent duplicates.

## Workflow

1. Load the approved product profile, description variants, URLs, assets, authorization rules, and any existing campaign record.
2. Normalize and deduplicate target URLs.
3. Run an eligibility sweep: check availability, fit, cost, reciprocal-link requirements, accounts, terms, duplicates, and claim-vs-new-listing conditions.
4. Surface CAPTCHA, email, phone, 2FA, and other manual verification in a single ordered queue.
5. After verification, fill forms only with approved facts and assets.
6. Recheck cost, brand, canonical URL, category, uploads, agreements, duplicate risk, and authorization before the final action.
7. Capture the exact response, timestamp, resulting URL, and evidence immediately.
8. Audit the campaign record and report each status separately.

## Repository structure

```text
submit-product-directories-open-source/
├── SKILL.md
├── agents/openai.yaml
├── assets/submission-record-template.md
├── references/
│   ├── authorization.md
│   ├── status-model.md
│   └── workflow.md
├── scripts/audit_submission_record.py
└── tests/test_audit_submission_record.py
```

## Use the skill

Copy `submit-product-directories-open-source/` into the skills directory supported by your agent, or reference the folder directly from your project. Then ask the agent to use the skill:

```text
Use $submit-product-directories-open-source to review these directory URLs
and prepare a submission campaign for our product.

First run the eligibility and verification sweep. Do not publish, create an
account, accept agreements, or pay without the authorization recorded in the
campaign matrix. Save an auditable submission record and collect all manual
verification steps into one queue.
```

The agent should read `SKILL.md` first and load only the required references. If no campaign record exists, copy `assets/submission-record-template.md` instead of inventing a new format.

## Status and evidence model

- `submitted`: reliable receipt acknowledgment or confirmed sent-email evidence exists.
- `awaiting email verification`: email confirmation is the current next action.
- `awaiting approval`: the site explicitly placed the submission in review.
- `published`: a public, non-preview page contains the intended product identity.
- `submission outcome unknown`: a final action occurred, but receipt is uncertain; investigate before retrying.
- `submission failed`: explicit rejection, bounce, or reliable business-failure evidence exists.
- `blocked — execution backend failure`: the local browser or automation failed; it does not mean the target site is unavailable.

Never infer success from a click, redirect, cleared form, disabled button, or absence of an error.

## Audit a campaign record

```bash
python3 submit-product-directories-open-source/scripts/audit_submission_record.py path/to/record.md
python3 submit-product-directories-open-source/scripts/audit_submission_record.py path/to/record.md --json
python3 -m unittest discover -s submit-product-directories-open-source/tests
```

The auditor returns a nonzero exit code for invalid statuses, missing required evidence, duplicate submission URLs, unresolved placeholders, invalid timestamps, and other record errors.

## About Flaq.ai

[Flaq.ai](https://flaq.ai/) provides unified access to image, video, music, and language models for AI agents and production applications. The Flaq AI team maintains this repository as an open-source, reusable workflow for careful product discovery submissions.

Related collections: [Awesome Codex Skills](https://github.com/flaqai/awesome_codex_skills) · [Awesome Claude Code Skills](https://github.com/flaqai/awesome_claude_code_skills)

## License

See [LICENSE](LICENSE).
