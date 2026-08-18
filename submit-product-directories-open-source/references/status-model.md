# Status model

## Independent record layers

- `Phase` records workflow progress.
- `Status` records the current listing or artifact outcome.
- `Verification preflight` records authentication and human-verification readiness.
- `Artifact stage` records draft, review, public, sent, or bounced state for content and email routes.

Verification preflight is not a listing attempt. Keep `Status: not attempted` until listing fields are entered.

## Phases

```text
eligibility
verification
form
confirmation
follow-up
```

## Canonical statuses

```text
not attempted
form in progress
submitted
awaiting approval
awaiting email verification
published
submission outcome unknown
submission failed
blocked — user action
blocked — missing verified data
blocked — account or email policy
blocked — reciprocal link/site modification
blocked — execution backend failure
unavailable
paid-only
ineligible
terminated by user
```

Use exact values. Normalize whitespace and Unicode/ASCII dash variants only for validation, and report noncanonical input.

## Verification-preflight states

```text
not checked
automatic verification passed
awaiting manual verification
manual verification completed
verification unavailable before form
verification expired/reset
no verification presented
deferred by user
```

Do not use `still blocked` as a status. Keep `awaiting manual verification` and record the original prompt and follow-up.

## Truth rules

- `submitted`: reliable receipt acknowledgment or confirmed sent-email evidence exists.
- `awaiting email verification`: email confirmation is the current next action.
- `awaiting approval`: the site explicitly placed the item in review.
- `published`: a public, non-preview page is verified and recorded.
- `submission failed`: explicit rejection, bounce, or reliable business-failure evidence exists.
- `submission outcome unknown`: final action occurred but receipt is uncertain. Do not retry until non-receipt is established.
- `blocked — execution backend failure`: local browser or automation failed.
- `unavailable`: the target site itself produced an observed connection, certificate, HTTP, or availability failure.
- Account creation, a click, navigation, form clearing, or a disabled button does not prove submission.

## Unique presentation mapping

Use detailed statuses in records. If a browser group is needed, map each current status once:

| Status | Presentation group |
|---|---|
| `submitted` | success / submitted |
| `awaiting email verification` | awaiting verification |
| `awaiting approval` | awaiting review |
| `published` | success / published |
| `submission outcome unknown` | awaiting confirmation |
| `submission failed` | failed |
| retryable blocked states | retryable blockers |
| `paid-only`, `ineligible`, `unavailable` | failed / terminal |

If only four groups are available, map `awaiting approval` to `awaiting confirmation` and document that choice once. Never use an “or” mapping.

## Evidence requirements

- `submitted`, `awaiting approval`, and `awaiting email verification` require reliable text or evidence.
- `published` requires a public URL, check time, and evidence that the page is not a preview and identifies the intended product.
- `submission failed` requires explicit failure evidence.
- `submission outcome unknown` requires submit time, observed post-submit state, checks performed, and next review time.
- Every blocked state requires a follow-up or an explicit terminal reason.
