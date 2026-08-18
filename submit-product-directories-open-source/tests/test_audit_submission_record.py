from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


SCRIPT = Path(__file__).parents[1] / "scripts" / "audit_submission_record.py"
SPEC = importlib.util.spec_from_file_location("spd_audit", SCRIPT)
assert SPEC and SPEC.loader
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


def record(status: str = "not attempted", *, name: str = "Example", url: str = "https://example.com/submit", exact: str = "none", evidence: str = "none", target: str = "not applicable", follow_up: str = "none") -> str:
    if status in {"submitted", "awaiting approval", "awaiting email verification", "submission failed", "unavailable"} and exact == "none":
        exact = "Reliable server response captured"
    if status == "published":
        evidence = "Public page verified while logged out"
        target = "https://example.com/products/example"
    if status == "submission outcome unknown":
        exact = "Timed out after final submit; receipt unknown"
    if status.startswith("blocked") and follow_up == "none":
        follow_up = "Retry after the blocker is resolved"
    form_started = "2026-08-18T10:04:00+08:00" if status == "form in progress" else "not started"
    submitted_at = "2026-08-18T10:05:00+08:00" if status in {
        "submitted", "awaiting approval", "awaiting email verification", "submission failed", "submission outcome unknown"
    } else "not submitted"
    review = "2026-08-18T11:05:00+08:00" if status == "submission outcome unknown" else "not applicable"
    return f"""## {name}

- Website: Example
- Submission URL: {url}
- Route: public form
- Phase: eligibility
- Status: **{status}**
- Listing plan/cost: free
- Execution backend/session: test / profile
- Account/login: none
- Credential source: not applicable
- Verification preflight: no verification presented
- Manual-verification queue: not queued
- Duplicate check: clear
- Fields entered: none
- Fields omitted: none
- Category: not applicable
- Asset path: none
- Asset SHA-256: not applicable
- Agreements: none
- Subscriptions: none
- CAPTCHA/authentication: not presented
- Artifact stage: not applicable
- First opened: 2026-08-18T10:00:00+08:00
- Eligibility checked at: 2026-08-18T10:01:00+08:00
- Verification checked at: 2026-08-18T10:02:00+08:00
- Form started at: {form_started}
- Submit action timestamp: {submitted_at}
- Last checked: 2026-08-18T10:06:00+08:00
- Result summary: test
- Exact result: {exact}
- Target URL: {target}
- Evidence: {evidence}
- Backend checked: not applicable
- Mailbox checked: not applicable
- Public search checked: not applicable
- Next review time: {review}
- Follow-up: {follow_up}
- Owner: test
- Deadline: not applicable
"""


class AuditTests(unittest.TestCase):
    def test_canonical_statuses_are_exact(self) -> None:
        for status, category in AUDIT.STATUS_CATEGORIES.items():
            with self.subTest(status=status):
                report = AUDIT.audit_text(record(status))
                self.assertTrue(report["valid"], report["errors"])
                self.assertEqual(report["sites"][0]["category"], category)
                self.assertFalse(report["sites"][0]["status_inferred"])

    def test_failed_and_unknown_are_distinct(self) -> None:
        report = AUDIT.audit_text(record("submission failed") + record(
            "submission outcome unknown", name="Unknown", url="https://example.org/submit"
        ))
        self.assertTrue(report["valid"], report["errors"])
        self.assertEqual(report["counts"]["submission_failed"], 1)
        self.assertEqual(report["counts"]["outcome_unknown"], 1)

    def test_valid_status_wins_over_conflicting_evidence(self) -> None:
        report = AUDIT.audit_text(record(
            "submission failed",
            exact="Earlier page said submission received; final response rejected it",
        ))
        self.assertEqual(report["sites"][0]["category"], "submission_failed")
        self.assertTrue(report["warnings"])

    def test_invalid_status_is_not_silently_accepted(self) -> None:
        report = AUDIT.audit_text(record("submitted successfully", exact="Submission received"))
        self.assertFalse(report["valid"])
        self.assertTrue(report["sites"][0]["status_inferred"])

    def test_duplicate_urls_fail(self) -> None:
        report = AUDIT.audit_text(record() + record(name="Duplicate", url="https://EXAMPLE.com/submit/"))
        self.assertFalse(report["valid"])
        self.assertTrue(any("duplicate submission URL" in error for error in report["errors"]))


if __name__ == "__main__":
    unittest.main()
