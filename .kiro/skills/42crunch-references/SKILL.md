---
name: 42crunch-references
description: >
  Shared reference library for 42Crunch skills. This is NOT an invocable skill.
  It contains procedural reference documents (pre-flight, binary setup,
  credential setup, audit workflow, scan workflow, tag detection, reachability
  check, audit rule translations, and scanconf templates) that are read by the
  other 42Crunch skills during execution. Do not invoke this skill directly.
---

# 42Crunch Shared References

This directory contains reference documents used internally by the 42Crunch
skills. They are not intended to be invoked as a standalone skill.

| File | Used by |
|---|---|
| `pre-flight.md` | All skills — binary check, credential check, OAS resolution, tag detection |
| `binary-setup.md` | `42crunch-setup`, `pre-flight` |
| `credential-setup.md` | `42crunch-setup`, `pre-flight` |
| `audit-workflow.md` | `42crunch-audit`, `42crunch-api-security-testing` |
| `audit-rule-translations.md` | `42crunch-audit`, `42crunch-api-security-testing` |
| `scan-workflow.md` | `42crunch-scan`, `42crunch-api-security-testing` |
| `scanconf-templates.md` | `42crunch-scan`, `42crunch-api-security-testing` |
| `tag-detection.md` | `pre-flight` (platform mode only) |
| `reachability-check.md` | `42crunch-scan`, `42crunch-api-security-testing` |
