# Portable workflow and recovery

## Preflight

1. Snapshot approved product facts, description variants, contact fields, authorized identities, policies, and asset hashes.
2. Mark phone, address, region, city, and description approval as verified or unverified. Never derive them from country or rewrite phone formats without approval.
3. Normalize and deduplicate URLs while preserving supplied paths and parameters.
4. Assign sequence numbers and initialize `Phase: eligibility`, `Status: not attempted`, and `Verification preflight: not checked`.
5. Select an approved interactive browser backend and record its profile/session and current URL.

## Pass A — eligibility and verification sweep

Visit every target without entering product-listing fields.

1. Confirm the exact route and current URL.
2. Check availability, redirects, maintenance, region restrictions, eligibility, plan cost, reciprocal links, site changes, account requirements, terms, duplicate listings, and claim routes.
3. Record exact evidence for `paid-only`, `ineligible`, `unavailable`, and policy/site-modification blockers.
4. Reuse an authorized session or create an account only within the authorization matrix.
5. Expose the earliest native CAPTCHA, Turnstile, email/phone check, 2FA, or equivalent verification.
6. Attempt ordinary native automatic verification only when authorized. Never bypass or escalate anti-bot defenses.
7. Preserve interactive challenges in the original tab/session and add them to one manual queue.
8. Keep listing `Status: not attempted` throughout Pass A.

## Manual checkpoint

Provide site, URL, session/tab, challenge type, exact prompt, user action, timestamp, and expiry risk. Reinspect after user action and set only a canonical verification state. Resolve or explicitly defer every actionable item before Pass B. Split very large campaigns into smaller batches to reduce verification-token expiry.

## Pass B — fill and submit

1. Recheck verification and duplicate state before typing.
2. Enter `Phase: form` and `Status: form in progress` when listing fields begin.
3. Use the approved product name, canonical URL, facts, category, description variant, and assets.
4. Leave unknown optional fields and subscriptions blank. Stop on unknown required facts.
5. Reinspect after every navigation, modal, native menu, reload, or user action.
6. Review cost, brand, URL, contact, category, price, uploads, agreements, subscriptions, reciprocal links, duplicate state, and verification validity.
7. Complete only authorized actions. Record the final-action time and exact page response.

## Outcome and retry handling

- Server receipt: `submitted`.
- Email confirmation required: `awaiting email verification`.
- Editorial queue: `awaiting approval`.
- Public page verified: `published`.
- Explicit rejection/bounce/business error: `submission failed`.
- Final click with uncertain receipt: `submission outcome unknown`.

For an unknown outcome, query the site backend, authorized mailbox, site search, public page, and application history. Record results and a next review time. Retry only after confirming non-receipt.

Pre-submit loading or entry-discovery failures may be retried once in the current session and once in a fresh session. Do not retry after an ambiguous final submit action.

## Route-specific handling

- Request app: valid discovery route; require a reliable request acknowledgment.
- Claim: check existing listing and pending claims; obtain separate ownership authorization before DNS, HTML, website, corporate, or social verification.
- Blog/article: record `Artifact stage`; draft is `form in progress`, editorial submission is `awaiting approval`, public page is `published`.
- Email: draft is `form in progress`, confirmed sending is `submitted`, explicit bounce is `submission failed`.
- Account/profile: account creation alone is not a listing submission unless the public profile displays the intended product.

## Browser recovery

- Confirm full URL, not only tab title, before each action.
- Reacquire accessibility elements after state changes; never reuse stale indices.
- Prefer accessible controls, then deterministic keyboard navigation, then screenshot coordinates as a local fallback.
- Treat local browser/backend crashes as `blocked — execution backend failure`; use `unavailable` only for an observed target-site failure.
- Preserve exact errors and entered values before reloading.

## Closeout

Update the record immediately. Run the bundled auditor, fix all errors, reconcile browser/mailbox/public evidence, and report detailed statuses separately from presentation groups.
