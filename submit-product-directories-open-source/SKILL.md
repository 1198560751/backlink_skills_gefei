---
name: submit-product-directories-open-source
description: Portable, evidence-backed workflow for submitting products, software, startups, apps, and websites to directories and other public discovery channels. Use when planning, filling, submitting, auditing, or resuming directory forms, Request app routes, claims, account applications, blogs, articles, email submissions, or contact forms.
---

# Open-source product directory submissions

Run directory campaigns as a recoverable state machine. Keep product data truthful, preserve site rules and authorization boundaries, prevent duplicate submissions, and record evidence strong enough for another operator to resume the work.

## Load only the required context

1. Read the campaign's approved product profile, description variants, asset list, URL list, authorization rules, and existing record.
2. Read [references/workflow.md](references/workflow.md) before browser work.
3. Read [references/status-model.md](references/status-model.md) before creating or auditing records.
4. Read [references/authorization.md](references/authorization.md) before account creation, sign-in, agreement acceptance, publication, claims, or other consequential actions.
5. Copy [assets/submission-record-template.md](assets/submission-record-template.md) when a campaign record does not exist.

Never invent company, founder, pricing, address, launch, user-count, social, legal, ownership, or contact facts. Leave optional unknowns blank and mark required unknowns `blocked — missing verified data`.

## Supported routes

Treat every route that can create a truthful public presence as an eligible route for review:

- product, software, AI-tool, startup, or company listing;
- `Request app` or recommendation request;
- claim-listing or vendor application;
- free account or profile creation;
- blog, article, news, or community submission;
- email or contact-form submission;
- resource-page or partner-directory submission.

Do not assume that account creation, a saved draft, or a claim request is a published listing.

## Operating workflow

Use two strict passes for each manageable batch:

### Pass A — eligibility and verification sweep

1. Normalize and deduplicate URLs while preserving supplied paths and relevant parameters.
2. Assign stable sequence numbers and initialize each site with `Phase: eligibility` and `Status: not attempted`.
3. Check availability, redirects, eligibility, cost, reciprocal-link requirements, site modifications, account requirements, terms, duplicates, and claim-vs-new-listing conditions.
4. Record terminal exclusions immediately: `paid-only`, `ineligible`, or `unavailable`.
5. Reuse an authorized account or create one only within the authorization matrix.
6. Expose the earliest native CAPTCHA, Turnstile, email/phone check, 2FA, or equivalent verification and record `Verification preflight`.
7. Preserve interactive challenges in the original session and collect them in one manual queue.
8. Do not enter product-listing fields during Pass A. Keep listing `Status: not attempted`.

### Manual checkpoint

Present one ordered queue with the site, full URL, session/tab, verification type, exact prompt, required user action, timestamp, and expiry risk. Reinspect each preserved page after the user acts. Resolve or explicitly defer every actionable item before Pass B.

### Pass B — form execution and confirmation

1. Recheck verification validity and duplicate risk before typing.
2. Set `Phase: form` and `Status: form in progress` when listing fields are first entered.
3. Fill only approved facts and the description variant that matches the field limit.
4. Leave optional subscriptions unchecked unless specifically authorized. Stop on unknown required data.
5. Use only approved assets and record their path, hash, and modification state.
6. Reinspect after navigation, modal changes, native-menu expansion, reloads, and user interactions.
7. Before the final action, verify plan, cost, brand, canonical URL, contact, category, price, uploads, agreements, duplicate state, and verification validity.
8. Submit only within the authorization matrix. Capture the action time, exact response, resulting URL, and evidence immediately.

## Safety boundaries

- Never bypass CAPTCHA, Turnstile, 2FA, Passkey, security keys, email verification, or other safeguards.
- Use only the site's native registration-email verification flow when the mailbox and action are authorized.
- Do not use external CAPTCHA solvers, proxy or fingerprint rotation, stealth modes, or anti-detection escalation.
- Do not pay, enable auto-renewal, add reciprocal links, modify a website, change DNS, upload verification files, or claim ownership without separate authorization.
- Treat Terms/Privacy and other legal agreements according to the host environment's action-time confirmation policy.
- Do not store plaintext passwords or recovery codes in campaign records.
- If a user only pastes form text, return field values; operate a browser only when explicitly requested.

## Outcome rules

Use the canonical statuses in [references/status-model.md](references/status-model.md). In particular:

- `submitted` requires a reliable receipt acknowledgment or confirmed sent-email evidence;
- `awaiting email verification` means email confirmation is the current next action;
- `awaiting approval` means the site explicitly placed the item in review;
- `published` requires a public, non-preview page containing the intended product identity;
- `submission failed` requires explicit rejection, bounce, or reliable business-failure evidence;
- `submission outcome unknown` means a final action occurred but receipt is uncertain; check the backend, mailbox, site search, and public page before any retry;
- `blocked — execution backend failure` describes a local browser/automation failure, not target-site unavailability.

Never infer success from a click, navigation, form clearing, disabled button, or lack of an error.

## Recovery and audit

Reacquire page state and accessible elements after every page change. Retry only pre-submit loading or entry-discovery failures once in the current session and once in a fresh session. Never apply that retry rule after an ambiguous final submission.

Update the record immediately after each site. Run:

```bash
python3 scripts/audit_submission_record.py path/to/record.md
python3 scripts/audit_submission_record.py path/to/record.md --json
```

The auditor must return a nonzero exit code for invalid statuses, missing required evidence, duplicate submission URLs, unresolved placeholders, invalid timestamps, or other record errors.

Report detailed statuses separately from presentation groups: submitted, email verification, approval, published, outcome unknown, submission failed, retryable blockers, terminal exclusions, manual verification, and not attempted.

## Bundled resources

- [references/workflow.md](references/workflow.md): portable browser and recovery procedure.
- [references/status-model.md](references/status-model.md): phases, statuses, verification states, evidence rules, and group mapping.
- [references/authorization.md](references/authorization.md): campaign authorization matrix and safety boundaries.
- [assets/submission-record-template.md](assets/submission-record-template.md): neutral record template with no private campaign data.
- `scripts/audit_submission_record.py`: standalone Markdown-record auditor.
