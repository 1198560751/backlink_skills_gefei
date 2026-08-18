#!/usr/bin/env python3
"""Audit an open-source SPD Markdown submission record."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import re
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


STATUS_CATEGORIES = {
    "not attempted": "not_attempted",
    "form in progress": "in_progress",
    "submitted": "submitted",
    "awaiting approval": "awaiting_approval",
    "awaiting email verification": "awaiting_email_verification",
    "published": "published",
    "submission outcome unknown": "outcome_unknown",
    "submission failed": "submission_failed",
    "blocked — user action": "blocked_user_action",
    "blocked — missing verified data": "blocked_missing_data",
    "blocked — account or email policy": "blocked_account_policy",
    "blocked — reciprocal link/site modification": "blocked_reciprocal_link",
    "blocked — execution backend failure": "blocked_execution_backend",
    "unavailable": "unavailable",
    "paid-only": "paid_only",
    "ineligible": "ineligible",
    "terminated by user": "terminated",
}

PHASES = {"eligibility", "verification", "form", "confirmation", "follow-up"}

VERIFICATION_STATES = {
    "not checked": "not_checked",
    "automatic verification passed": "automatic_passed",
    "awaiting manual verification": "awaiting_manual",
    "manual verification completed": "manual_completed",
    "verification unavailable before form": "unavailable_before_form",
    "verification expired/reset": "expired_or_reset",
    "no verification presented": "not_presented",
    "deferred by user": "deferred",
}

EVIDENCE_PATTERNS = [
    ("published", ("public page verified", "public listing verified", "published successfully")),
    ("submission_failed", ("submission failed", "delivery failed", "message bounced", "application rejected")),
    ("outcome_unknown", ("outcome unknown", "receipt unknown", "no clear response", "timed out after submit")),
    ("awaiting_email_verification", ("email confirmation required", "verify your email", "email verification required")),
    ("awaiting_approval", ("awaiting approval", "pending review", "submitted for review")),
    ("submitted", ("submitted successfully", "submission received", "application received", "email sent successfully")),
    ("unavailable", ("site unavailable", "certificate error", "connection refused", "error code 520")),
    ("paid_only", ("paid only", "payment required", "credit card required")),
    ("ineligible", ("not eligible", "does not meet the requirements")),
]

REQUIRED_FIELDS = {
    "website", "submission url", "route", "phase", "status", "listing plan/cost",
    "execution backend/session", "account/login", "credential source",
    "verification preflight", "manual-verification queue", "duplicate check",
    "fields entered", "fields omitted", "category", "asset path", "asset sha-256",
    "agreements", "subscriptions", "captcha/authentication", "artifact stage",
    "first opened", "eligibility checked at", "verification checked at",
    "form started at", "submit action timestamp", "last checked", "result summary",
    "exact result", "target url", "evidence", "backend checked", "mailbox checked",
    "public search checked", "next review time", "follow-up", "owner", "deadline",
}

TIMESTAMP_FIELDS = {
    "first opened", "eligibility checked at", "verification checked at",
    "form started at", "submit action timestamp", "last checked", "next review time", "deadline",
}

SENTINELS = {
    "none", "not applicable", "n/a", "unknown", "not attempted", "not checked",
    "not started", "not submitted", "not queued",
}

CAMPAIGN_HEADINGS = {"permanent operating rules", "source list"}


def compact(value: str) -> str:
    value = re.sub(r"[*]", "", value).replace("`", "")
    return re.sub(r"\s+", " ", value).strip()


def normalize_token(value: str) -> str:
    value = compact(value).lower()
    value = value.replace("–", "—").replace("−", "—")
    value = re.sub(r"^blocked\s*-\s*", "blocked — ", value)
    return re.sub(r"\s*—\s*", " — ", value)


def infer_category(value: str) -> str | None:
    lowered = compact(value).lower()
    for category, phrases in EVIDENCE_PATTERNS:
        if any(phrase in lowered for phrase in phrases):
            return category
    return None


def is_placeholder(value: str) -> bool:
    cleaned = compact(value)
    return not cleaned or bool(re.fullmatch(r"\[.*\]", cleaned))


def is_meaningful(value: str) -> bool:
    cleaned = compact(value).lower()
    return not is_placeholder(value) and cleaned not in SENTINELS


def is_iso_timestamp(value: str) -> bool:
    cleaned = compact(value)
    if cleaned.lower() in SENTINELS or is_placeholder(cleaned):
        return True
    try:
        parsed = datetime.fromisoformat(cleaned.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def normalized_url(value: str) -> str:
    cleaned = compact(value)
    parts = urlsplit(cleaned)
    if not parts.scheme or not parts.netloc:
        return cleaned.lower()
    path = parts.path.rstrip("/") or "/"
    query = urlencode(sorted(parse_qsl(parts.query, keep_blank_values=True)))
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, query, ""))


def parse_fields(body: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for match in re.finditer(r"^- ([^:\n]+):\s*(.*)$", body, re.MULTILINE):
        fields[compact(match.group(1)).lower()] = compact(match.group(2))
    return fields


def parse_record(text: str) -> list[dict[str, object]]:
    sections: list[dict[str, object]] = []
    headers = list(re.finditer(r"^## (.+)$", text, re.MULTILINE))
    for index, header in enumerate(headers):
        name = compact(header.group(1))
        if name.lower() in CAMPAIGN_HEADINGS:
            continue
        end = headers[index + 1].start() if index + 1 < len(headers) else len(text)
        fields = parse_fields(text[header.end():end])
        raw_status = fields.get("status", "missing")
        normalized = normalize_token(raw_status)
        exact_category = STATUS_CATEGORIES.get(normalized)
        evidence_text = f"{fields.get('exact result', '')} {fields.get('evidence', '')}"
        inferred = infer_category(evidence_text) if exact_category is None else None
        verification = normalize_token(fields.get("verification preflight", "missing"))
        sections.append({
            "name": name,
            "website": fields.get("website", ""),
            "submission_url": fields.get("submission url", ""),
            "status": compact(raw_status),
            "normalized_status": normalized,
            "category": exact_category or inferred or "unknown",
            "status_inferred": exact_category is None and inferred is not None,
            "verification_preflight": verification,
            "verification_category": VERIFICATION_STATES.get(verification, "unknown"),
            "phase": compact(fields.get("phase", "")),
            "fields": fields,
            "errors": [],
            "warnings": [],
        })
    return sections


def validate_site(site: dict[str, object]) -> None:
    fields = site["fields"]
    errors = site["errors"]
    warnings = site["warnings"]
    assert isinstance(fields, dict) and isinstance(errors, list) and isinstance(warnings, list)

    missing = sorted(REQUIRED_FIELDS - fields.keys())
    if missing:
        errors.append("missing fields: " + ", ".join(missing))
    unresolved = sorted(field for field in REQUIRED_FIELDS & fields.keys() if is_placeholder(fields[field]))
    if unresolved:
        errors.append("unresolved placeholders: " + ", ".join(unresolved))

    normalized = str(site["normalized_status"])
    exact_category = STATUS_CATEGORIES.get(normalized)
    if exact_category is None:
        errors.append(f"invalid canonical status: {site['status']}")
        if site["status_inferred"]:
            warnings.append(f"status inferred from evidence as {site['category']}")
    elif compact(str(site["status"])).lower() != normalized:
        warnings.append(f"noncanonical status formatting; use: {normalized}")

    phase = compact(str(site["phase"])).lower()
    if phase not in PHASES:
        errors.append(f"invalid phase: {site['phase'] or 'missing'}")

    verification = str(site["verification_preflight"])
    if verification not in VERIFICATION_STATES:
        errors.append(f"invalid verification preflight: {fields.get('verification preflight', 'missing')}")

    for field in sorted(TIMESTAMP_FIELDS & fields.keys()):
        if not is_iso_timestamp(fields[field]):
            errors.append(f"{field} must be ISO 8601 with timezone or an approved sentinel")
    if not is_iso_timestamp(fields.get("last checked", "")) or not is_meaningful(fields.get("last checked", "")):
        errors.append("last checked requires an ISO 8601 timestamp")

    evidence_text = f"{fields.get('exact result', '')} {fields.get('evidence', '')}"
    evidence_category = infer_category(evidence_text)
    if exact_category and evidence_category and evidence_category != exact_category:
        warnings.append(f"evidence suggests {evidence_category}; canonical Status remains {normalized}")

    category = str(site["category"])
    exact_result = fields.get("exact result", "")
    evidence = fields.get("evidence", "")
    has_evidence = is_meaningful(exact_result) or is_meaningful(evidence)
    if category in {"submitted", "awaiting_approval", "awaiting_email_verification", "submission_failed", "unavailable"} and not has_evidence:
        errors.append(f"{category} requires an exact result or evidence")

    if category == "published":
        target_url = fields.get("target url", "")
        if not has_evidence:
            errors.append("published requires evidence")
        if not is_meaningful(target_url) or not target_url.lower().startswith(("http://", "https://")):
            errors.append("published requires a public target URL")

    if category == "outcome_unknown":
        for field in ("submit action timestamp", "exact result", "next review time"):
            if not is_meaningful(fields.get(field, "")):
                errors.append(f"outcome_unknown requires {field}")

    if category in {"submitted", "awaiting_approval", "awaiting_email_verification", "submission_failed", "outcome_unknown"} and not is_meaningful(fields.get("submit action timestamp", "")):
        errors.append(f"{category} requires submit action timestamp")

    if category == "in_progress" and not is_meaningful(fields.get("form started at", "")):
        errors.append("in_progress requires form started at")

    if category.startswith("blocked_") and not is_meaningful(fields.get("follow-up", "")):
        errors.append(f"{category} requires follow-up")

    if site["verification_category"] in {"awaiting_manual", "unavailable_before_form", "expired_or_reset"} and not is_meaningful(fields.get("manual-verification queue", "")):
        errors.append("unresolved verification requires a manual-verification queue entry")

    site["errors"] = [f"{site['name']}: {message}" for message in errors]
    site["warnings"] = [f"{site['name']}: {message}" for message in warnings]
    site["valid"] = not site["errors"]


def audit_text(text: str) -> dict[str, object]:
    sites = parse_record(text)
    for site in sites:
        validate_site(site)

    errors = [message for site in sites for message in site["errors"]]
    warnings = [message for site in sites for message in site["warnings"]]
    if not sites:
        errors.append("record contains no website sections")

    seen_urls: dict[str, str] = {}
    for site in sites:
        url = str(site["submission_url"])
        if not url or is_placeholder(url):
            continue
        key = normalized_url(url)
        if key in seen_urls:
            message = f"{site['name']}: duplicate submission URL also used by {seen_urls[key]}: {url}"
            errors.append(message)
            site["errors"].append(message)
            site["valid"] = False
        else:
            seen_urls[key] = str(site["name"])

    counts: dict[str, int] = {}
    verification_counts: dict[str, int] = {}
    for site in sites:
        category = str(site["category"])
        counts[category] = counts.get(category, 0) + 1
        verification = str(site["verification_category"])
        verification_counts[verification] = verification_counts.get(verification, 0) + 1

    queue = [site for site in sites if site["verification_category"] in {"awaiting_manual", "unavailable_before_form", "expired_or_reset"}]
    return {
        "valid": not errors,
        "total": len(sites),
        "counts": counts,
        "verification_counts": verification_counts,
        "manual_verification_queue": queue,
        "errors": errors,
        "warnings": warnings,
        "sites": sites,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = audit_text(args.record.read_text(encoding="utf-8"))
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Valid: {'yes' if report['valid'] else 'no'}")
        print(f"Total sites: {report['total']}")
        for key in sorted(report["counts"]):
            print(f"{key}: {report['counts'][key]}")
        for warning in report["warnings"]:
            print(f"WARNING: {warning}")
        for error in report["errors"]:
            print(f"ERROR: {error}")
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
