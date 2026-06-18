# 42Crunch Kiro Skills

The official [42Crunch](https://www.42crunch.com) skills for [Kiro](https://kiro.dev) — AI-powered API security capabilities directly in your Kiro workflow.

42Crunch skills give Kiro the ability to audit OpenAPI specs, scan live APIs for vulnerabilities, and apply fixes to ensure APIs meet security guardrails.

## Structure

```
.kiro/
  skills/
    42crunch-api-security-testing/   # Full audit + scan pipeline skill
    42crunch-audit/                  # Static OAS audit skill
    42crunch-scan/                   # Live conformance & authorization scan skill
    42crunch-setup/                  # One-time environment setup skill
    code-to-oas/                     # Generate OAS from API source code
    postman-to-oas/                  # Convert Postman collection to OAS
    42crunch-references/             # Shared reference docs loaded by skills at runtime
```

## Installation

Copy the `.kiro/skills/` directory into your project root:

```bash
git clone https://github.com/42Crunch-AI/kiro-plugins.git /tmp/42crunch-kiro
cp -r /tmp/42crunch-kiro/.kiro/skills .kiro/skills
```

To make the skills available across all workspaces instead, copy to your global Kiro directory:

```bash
git clone https://github.com/42Crunch-AI/kiro-plugins.git /tmp/42crunch-kiro
cp -r /tmp/42crunch-kiro/.kiro/skills/* ~/.kiro/skills/
```

## Prerequisites

- [Kiro](https://kiro.dev) IDE
- A 42Crunch account — [Free Trial](https://42crunch.com/freemium/?source=kiro) or paid (Platform API key)
- For `42crunch-scan`: a running API server reachable at the URL in `servers[0]` of your OAS (or via `SCAN42C_HOST`)

The `42c-ast` binary is downloaded and kept up to date automatically on first use.

## Available Skills

### `42crunch-setup`

Installs the `42c-ast` binary for your OS/architecture, verifies its checksum,
and walks you through credential configuration. Supports Platform (API key) and
Free Trial (token) modes. Credentials are stored in `~/.42crunch/conf/env` with
`600` permissions.

**Trigger:** "set up 42crunch", "configure 42crunch", "install 42c-ast", "42crunch not working"

---

### `42crunch-audit`

Runs a static analysis of an OpenAPI Specification and produces a 0–100 security
score. Findings are classified into three tiers (SQG-Blocking / Security / Data
Validation) with plain-English descriptions and AI-assisted fixes applied with
your approval.

**Trigger:** "run audit", "audit my API", "fix audit issues", "42crunch audit", "SQG"

---

### `42crunch-scan`

Runs a live conformance and authorization scan against a running API. Detects
BOLA (OWASP API1), BFLA (OWASP API5), and response-contract violations through
operation-by-operation classification, happy-path validation, and full fuzzing.

**Trigger:** "run scan", "conformance test", "BOLA test", "BFLA test", "42crunch scan"

---

### `42crunch-api-security-testing`

Full audit + scan pipeline in a single session. Runs both phases back-to-back
with a single pre-flight check.

**Trigger:** "run audit and scan", "full 42crunch pipeline", "full security check", "42crunch"

---

### `code-to-oas`

Analyzes an API codebase — regardless of language or framework — and generates
a complete, valid OpenAPI 3.0 specification file. Supports Express, FastAPI,
Flask, Django, NestJS, Spring Boot, Gin/Echo/Chi, Rails, and more.

**Trigger:** "generate OAS from code", "create OpenAPI spec", "document my API", "reverse-engineer spec"

---

### `postman-to-oas`

Converts a Postman collection (v2.0 or v2.1) into a complete OpenAPI 3.0
specification file. Reads the full collection and optional environment file to
extract paths, methods, parameters, request/response bodies, headers, and auth
schemes.

**Trigger:** "convert postman to openapi", "postman collection to OAS", "generate spec from postman"

---

## Quick Start

1. **Install the skills** — copy `.kiro/` into your workspace (see Installation above)
2. **Set up the environment** — say: *"set up 42crunch"*
3. **Audit your API** — say: *"run a 42Crunch audit"*
4. **Fix issues** — Kiro presents findings by severity and asks your consent before changing anything
5. **Scan your API** — say: *"run a conformance scan"* against your running server

## Links

- [42Crunch](https://42crunch.com/)
- [42Crunch Documentation](https://docs.42crunch.com)
- [42Crunch on GitHub](https://github.com/42Crunch)
- [Kiro IDE](https://kiro.dev)
- Support: support@42crunch.com
