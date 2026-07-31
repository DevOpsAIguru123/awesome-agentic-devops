"""Deterministic Trivy tools for the container hardening copilot."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Literal

MAX_REPORT_BYTES = 10 * 1024 * 1024
MAX_FINDINGS = 200
DEFAULT_TIMEOUT_SECONDS = 120
SEVERITY_ORDER = {"UNKNOWN": 0, "LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}


class ScanInputError(ValueError):
    """Raised when a scan request violates the local safety boundary."""


def _scan_root() -> Path:
    configured = os.getenv("CONTAINER_HARDENING_SCAN_ROOT", os.getcwd())
    try:
        return Path(configured).expanduser().resolve(strict=True)
    except (FileNotFoundError, RuntimeError) as exc:
        raise ScanInputError(
            f"Configured scan root does not exist or cannot be resolved: {configured}"
        ) from exc


def _safe_path(user_path: str, *, must_be_file: bool | None = None) -> Path:
    if not user_path or "\x00" in user_path:
        raise ScanInputError("A non-empty local path is required.")

    root = _scan_root()
    candidate = Path(user_path).expanduser()
    if not candidate.is_absolute():
        candidate = root / candidate

    try:
        candidate = candidate.resolve(strict=True)
        candidate.relative_to(root)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        raise ScanInputError(
            f"Path must exist under the configured scan root: {root}"
        ) from exc

    if must_be_file is True and not candidate.is_file():
        raise ScanInputError("The report path must be a regular file.")
    if must_be_file is False and not (candidate.is_file() or candidate.is_dir()):
        raise ScanInputError("The scan target must be a regular file or directory.")
    return candidate


def _timeout_seconds() -> int:
    raw_value = os.getenv(
        "CONTAINER_HARDENING_TRIVY_TIMEOUT", str(DEFAULT_TIMEOUT_SECONDS)
    )
    try:
        return min(max(int(raw_value), 1), 600)
    except ValueError:
        return DEFAULT_TIMEOUT_SECONDS


def _trivy_environment() -> dict[str, str]:
    """Pass only runtime necessities, never cloud or model credentials."""
    allowed = (
        "HOME",
        "LANG",
        "LC_ALL",
        "PATH",
        "SSL_CERT_DIR",
        "SSL_CERT_FILE",
        "TMPDIR",
        "TRIVY_CACHE_DIR",
        "XDG_CACHE_HOME",
    )
    environment = {key: os.environ[key] for key in allowed if key in os.environ}
    environment["TRIVY_NO_PROGRESS"] = "true"
    return environment


def _compact_text(value: Any, limit: int = 1200) -> str:
    if value is None:
        return ""
    text = " ".join(str(value).split())
    return text if len(text) <= limit else f"{text[: limit - 3]}..."


def _line_description(start_line: Any, end_line: Any) -> str:
    if not start_line:
        return "line unavailable"
    if end_line and start_line != end_line:
        return f"lines {start_line}-{end_line}"
    return f"line {start_line}"


def _evidence_for(item: dict[str, Any], result: dict[str, Any]) -> str:
    cause = item.get("CauseMetadata") or {}
    start_line = cause.get("StartLine")
    end_line = cause.get("EndLine")
    lines = _line_description(start_line, end_line)
    code = cause.get("Code") or {}
    code_lines = code.get("Lines") or []
    rendered = " | ".join(
        _compact_text(line.get("Content"), 240)
        for line in code_lines
        if isinstance(line, dict) and line.get("Content")
    )
    target = result.get("Target") or "unknown target"
    return _compact_text(
        f"{target}, {lines}: {rendered}" if rendered else f"{target}, {lines}"
    )


def _normalize_misconfiguration(
    item: dict[str, Any], result: dict[str, Any]
) -> dict[str, Any]:
    return {
        "kind": "misconfiguration",
        "id": item.get("ID") or item.get("AVDID") or "unknown",
        "severity": str(item.get("Severity") or "UNKNOWN").upper(),
        "title": _compact_text(
            item.get("Title") or item.get("Message") or "Untitled finding"
        ),
        "description": _compact_text(item.get("Description") or item.get("Message")),
        "resolution": _compact_text(item.get("Resolution")),
        "status": item.get("Status") or "FAIL",
        "target": result.get("Target") or "",
        "evidence": _evidence_for(item, result),
        "primary_url": item.get("PrimaryURL") or "",
    }


def _normalize_vulnerability(
    item: dict[str, Any], result: dict[str, Any]
) -> dict[str, Any]:
    fixed_version = item.get("FixedVersion") or ""
    package = item.get("PkgName") or "unknown package"
    installed = item.get("InstalledVersion") or "unknown version"
    return {
        "kind": "vulnerability",
        "id": item.get("VulnerabilityID") or "unknown",
        "severity": str(item.get("Severity") or "UNKNOWN").upper(),
        "title": _compact_text(
            item.get("Title") or item.get("VulnerabilityID") or "Untitled vulnerability"
        ),
        "description": _compact_text(item.get("Description")),
        "resolution": (
            f"Upgrade {package} from {installed} to {fixed_version}."
            if fixed_version
            else f"No fixed version was reported for {package}; investigate or mitigate exposure."
        ),
        "status": item.get("Status") or "affected",
        "target": result.get("Target") or "",
        "package": package,
        "installed_version": installed,
        "fixed_version": fixed_version,
        "evidence": f"{result.get('Target') or 'unknown target'}: {package} {installed}",
        "primary_url": item.get("PrimaryURL") or "",
    }


def _correlate(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    # Use finding titles for category membership. Trivy evidence excerpts often
    # include an entire surrounding resource, so matching evidence would attach
    # unrelated finding IDs to every correlation for that resource.
    searchable = {
        finding["id"]: str(finding.get("title", "")).lower() for finding in findings
    }

    def matches(*terms: str) -> list[str]:
        return [
            finding_id
            for finding_id, text in searchable.items()
            if any(term in text for term in terms)
        ]

    root = matches(
        "run as root",
        "runs as root",
        "run as non-root",
        "user should not be 'root'",
        'user should not be "root"',
    )
    writable = matches(
        "read-only root",
        "readonlyrootfilesystem",
        "writable root",
        "not read-only",
    )
    exposed = matches("host network", "hostnetwork", "public", "0.0.0.0/0", "nodeport")
    privileged = matches("privileged", "elevate its own privileges")
    critical_cves = [
        finding["id"]
        for finding in findings
        if finding["kind"] == "vulnerability" and finding["severity"] == "CRITICAL"
    ]

    correlations: list[dict[str, Any]] = []
    if root and writable:
        correlations.append(
            {
                "risk": "root-and-writable-filesystem",
                "severity": "HIGH",
                "finding_ids": sorted(set(root + writable)),
                "explanation": "Code execution could gain root privileges in a writable container, increasing persistence and tampering impact.",
            }
        )
    if critical_cves and exposed:
        correlations.append(
            {
                "risk": "exposed-critical-vulnerability",
                "severity": "CRITICAL",
                "finding_ids": sorted(set(critical_cves + exposed)),
                "explanation": "A critical vulnerable component appears alongside a network-exposure finding, increasing likely exploitability.",
            }
        )
    if privileged and exposed:
        correlations.append(
            {
                "risk": "exposed-privileged-workload",
                "severity": "CRITICAL",
                "finding_ids": sorted(set(privileged + exposed)),
                "explanation": "Network exposure combined with privileged execution can turn an application compromise into a host-impacting event.",
            }
        )
    return correlations


def _normalized_misconfigurations(result: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        _normalize_misconfiguration(item, result)
        for item in result.get("Misconfigurations") or []
        if isinstance(item, dict) and str(item.get("Status", "FAIL")).upper() != "PASS"
    ]


def _normalized_vulnerabilities(result: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        _normalize_vulnerability(item, result)
        for item in result.get("Vulnerabilities") or []
        if isinstance(item, dict)
    ]


def _normalized_findings(results: list[Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for result in results:
        if isinstance(result, dict):
            findings.extend(_normalized_misconfigurations(result))
            findings.extend(_normalized_vulnerabilities(result))
    return findings


def normalize_trivy_report(report: dict[str, Any]) -> dict[str, Any]:
    """Normalize Trivy JSON without allowing the model to reinterpret evidence."""
    results = report.get("Results") or []
    if not isinstance(results, list):
        raise ScanInputError("Invalid Trivy report: Results must be a list.")
    findings = _normalized_findings(results)

    findings.sort(
        key=lambda finding: (
            -SEVERITY_ORDER.get(finding["severity"], 0),
            finding["id"],
            finding["target"],
        )
    )
    total_findings = len(findings)
    findings = findings[:MAX_FINDINGS]
    counts = {
        severity: sum(1 for finding in findings if finding["severity"] == severity)
        for severity in ("CRITICAL", "HIGH", "MEDIUM", "LOW", "UNKNOWN")
    }
    return {
        "status": "success",
        "scanner": "trivy",
        "schema_version": report.get("SchemaVersion"),
        "artifact_name": report.get("ArtifactName") or "",
        "policy_decision": "not_evaluated",
        "policy_note": "Trivy findings are preserved; no organization policy pack was evaluated.",
        "summary": {
            "total_findings": total_findings,
            "returned_findings": len(findings),
            "truncated": total_findings > len(findings),
            "severity_counts": counts,
        },
        "findings": findings,
        "correlations": _correlate(findings),
    }


def _parse_report_text(report_text: str) -> dict[str, Any]:
    if len(report_text.encode("utf-8")) > MAX_REPORT_BYTES:
        raise ScanInputError(f"Trivy report exceeds the {MAX_REPORT_BYTES}-byte limit.")
    try:
        report = json.loads(report_text)
    except json.JSONDecodeError as exc:
        raise ScanInputError(f"Trivy did not return valid JSON: {exc.msg}.") from exc
    if not isinstance(report, dict):
        raise ScanInputError(
            "Invalid Trivy report: the top-level value must be an object."
        )
    return normalize_trivy_report(report)


def scan_with_trivy(
    target_path: str, scan_type: Literal["config", "filesystem"] = "config"
) -> dict[str, Any]:
    """Scan a safe local path with Trivy and return normalized findings.

    Args:
        target_path: File or directory under CONTAINER_HARDENING_SCAN_ROOT.
        scan_type: "config" for Dockerfile/Kubernetes/IaC misconfigurations, or
            "filesystem" for dependency vulnerabilities and secrets.
    """
    try:
        target = _safe_path(target_path, must_be_file=False)
        with tempfile.TemporaryDirectory(prefix="container-hardening-") as temp_dir:
            report_path = Path(temp_dir) / "trivy-report.json"
            common = [
                "--format",
                "json",
                "--output",
                str(report_path),
                "--quiet",
            ]
            if scan_type == "config":
                command = ["trivy", "config", *common, str(target)]
            elif scan_type == "filesystem":
                command = [
                    "trivy",
                    "filesystem",
                    *common,
                    "--scanners",
                    "vuln,secret",
                    "--skip-db-update",
                    str(target),
                ]
            else:
                raise ScanInputError("scan_type must be 'config' or 'filesystem'.")

            completed = subprocess.run(
                command,
                capture_output=True,
                check=False,
                text=True,
                timeout=_timeout_seconds(),
                env=_trivy_environment(),
            )
            if completed.returncode != 0:
                return {
                    "status": "error",
                    "scanner": "trivy",
                    "policy_decision": "not_evaluated",
                    "error": _compact_text(completed.stderr or completed.stdout, 2000),
                }
            if not report_path.is_file():
                raise ScanInputError("Trivy completed without producing a JSON report.")
            if report_path.stat().st_size > MAX_REPORT_BYTES:
                raise ScanInputError(
                    f"Trivy report exceeds the {MAX_REPORT_BYTES}-byte limit."
                )
            normalized = _parse_report_text(report_path.read_text(encoding="utf-8"))
        normalized["scan_type"] = scan_type
        normalized["target"] = str(target)
        return normalized
    except FileNotFoundError:
        return {
            "status": "error",
            "scanner": "trivy",
            "error": "Trivy is not installed or is not on PATH.",
        }
    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "scanner": "trivy",
            "error": f"Trivy exceeded the {_timeout_seconds()}-second timeout.",
        }
    except (OSError, UnicodeError, ScanInputError) as exc:
        return {"status": "error", "scanner": "trivy", "error": str(exc)}


def analyze_trivy_report(report_path: str) -> dict[str, Any]:
    """Read and normalize an existing Trivy JSON report under the scan root."""
    try:
        path = _safe_path(report_path, must_be_file=True)
        if path.stat().st_size > MAX_REPORT_BYTES:
            raise ScanInputError(
                f"Trivy report exceeds the {MAX_REPORT_BYTES}-byte limit."
            )
        return _parse_report_text(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ScanInputError) as exc:
        return {"status": "error", "scanner": "trivy", "error": str(exc)}
