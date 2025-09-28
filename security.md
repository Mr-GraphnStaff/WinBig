# SECURITY.md

# WinBig / WAMECU — Security Policy

This repository (`Mr-GraphnStaff/WinBig`) is an experimental research project. Security and responsible disclosure matter — we want people to explore, reproduce, and critique this work safely. This document explains how to report security issues and what to expect.

---

## Supported Versions

This project is early-stage and uses a rolling `main` branch. Supported releases for security fixes are listed here:

| Version | Supported |
|--------:|:---------:|
| `main` (latest) | :white_check_mark: |
| `v0.x` (experimental snapshots) | :white_check_mark: |
| older snapshots | :x: |

If you depend on a tagged release, please include the tag name in your report so we can prioritize appropriately.

---

## Reporting a Vulnerability

If you discover a security issue, please **do not** open a public issue. Instead follow one of these private paths:

1. **GitHub Security Advisory** (preferred)
   - If you're a repo collaborator or can create an advisory, please open a private GitHub Security Advisory for `Mr-GraphnStaff/WinBig` and include the details requested below.

2. **Email** (alternative)
   - Send a report to: `security@winbig.org` (placeholder — replace with your project or org security contact).
   - If you prefer encryption, provide a PGP key request and we will publish our key or share one back.

Please include the following information in your report:
- A clear summary of the issue and impact.
- Steps to reproduce (preferably a minimal test case or notebook).
- The affected commit hash / tag / branch and any environment specifics.
- Your contact email and preferred disclosure timeline.
- Any suggested remediation if you have one.

We treat all reports as sensitive. Do **not** publish details until the issue is addressed or you have explicit permission from the maintainers.

---

## Response and Triage Process

We aim to respond promptly and transparently:

- **Acknowledgment:** within 72 hours (business days) of receiving the report.
- **Initial triage:** within 7 calendar days to determine severity and next steps.
- **Fix & disclosure timeline:** depends on severity; we will propose a remediation timeline in the triage response and keep you updated.

If a fix requires coordination across ecosystems (dependency or infra), we will provide status updates and reasonable timelines.

---

## Severity Levels (guidance)

We use a pragmatic set of severity levels to prioritize work:

- **Critical:** Remote code execution, secret exfiltration, or vulnerabilities that allow full compromise of systems or data. Urgent handling.
- **High:** Privilege escalation, persistent compromise, supply-chain risk affecting many users.
- **Medium:** Information disclosure of non-sensitive data, significant denial-of-service on this repo's infrastructure or CI.
- **Low:** Minor issues, documentation errors, or stylistic problems that do not expose systems or data.

Final severity is determined by the maintainers after triage.

---

## Coordinated Disclosure

We prefer coordinated disclosure:
- Maintain the report privately until a patch or mitigation is available.
- If you want to coordinate public disclosure, tell us your preferred embargo period; we will propose a disclosure timeline and work with you.

If you publicly disclose a vulnerability without coordination we may still respond, but coordinated disclosure helps protect users.

---

## Safe Harbor / Good Faith Research

Researchers acting in good faith to improve security will not be penalized. If you follow the reporting guidance above and avoid activities that materially harm systems or data, we welcome your findings.

Specifically:
- Do not exfiltrate or publish sensitive user data.
- Do not attempt denial-of-service attacks against production infrastructure.
- Avoid social-engineering attacks against individuals.

If you're unsure whether a test crosses a line, contact us privately and we'll advise.

---

## What We Will Not Fix

- We will not implement or support work intended to facilitate cheating, exploitation of regulated systems, or wrongdoing. If a vulnerability report suggests misuse to break laws or enable fraud (for example, enabling operational exploitation of a regulated lottery), we will treat it as a safety issue and may refuse to act on exploit-oriented remediation requests. We *will* accept reports that help detect, audit, and harden systems against misuse.

---

## Third-Party Dependencies and Supply-Chain

If you discover an issue in a third-party dependency used by this project, please:
- Report it to the dependency maintainer and to us (link to advisory or email).
- Include the affected versions and any reproducible tests.
We will coordinate remediation and update pinned dependencies in `requirements.txt` or via a follow-up PR.

---

## Contact & Escalation

- Preferred: GitHub Security Advisory for this repository.
- Alternative: `security@winbig.org` (replace with your real contact).
- If you do not get a response within the acknowledgment window, please escalate to the project owner (open a direct message to the repo owner on GitHub or email the maintainer contact listed on the repo).

---

## Privacy & Handling of Human Data

This project may, by design, record human or procedural metadata (operator IDs, session notes, optional mood tags, etc.) for research purposes. If you discover a vulnerability that exposes personal data:
- Report it privately as described above.
- We will triage it as high/critical and follow data breach best practices (containment, notification, remediation) consistent with applicable law.

---

## Non-Security Support & Abuse

This policy is for security vulnerability reporting only. For general support, feature requests, or to report abuse, please open a normal GitHub Issue (public) or use the contact information listed in the README.

---

## Changelog

- 2025-09-28 — Initial SECURITY.md added by project maintainers.

---

Thank you for helping keep WinBig / WAMECU safe and responsible.
