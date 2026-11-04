# 42Crunch API Security Plugin

Automate API security directly in Kiro with 42Crunch: audit OpenAPI specs and GraphQL schemas, scan running REST and GraphQL APIs for vulnerabilities aligned with the OWASP API Security Top 10 (including BOLA/BFLA), and apply AI-assisted fixes.

## Overview

The `42crunch-api-security-testing` plugin is built for AI-assisted development. It runs an **audit → scan → remediate → validate** loop, so APIs meet your security standards before they are deployed, and it asks your consent before changing any file.

The plugin uses the [Agent Plugins](https://agent-plugins.org) format, so Kiro installs it as a power. Each skill is self-contained (`SKILL.md` plus its own `references/` folder), so the skills can also be installed on their own.

## Skills

| Skill | Description |
|---|---|
| [`42crunch-setup`](#42crunch-setup) | Install the `42c-ast` binary and configure credentials (one-time) |
| [`42crunch-audit`](#42crunch-audit) | Static security audit of an OpenAPI Specification file or GraphQL schema with scored findings and AI-assisted fixes |
| [`42crunch-scan`](#42crunch-scan) | Live conformance and authorization scan (BOLA/BFLA) against a running REST or GraphQL API |
| [`42crunch-api-security-testing`](#42crunch-api-security-testing) | Full audit + scan pipeline in a single session (OAS or GraphQL) |
| [`generate-oas`](#generate-oas) | Generate a complete `openapi.json` from your API source code, a Postman/Insomnia collection, or both |

Kiro activates a skill when your request matches it ("run a 42Crunch audit"), or you can call one directly by typing `/` and its name, for example `/42crunch-audit`.

## Prerequisites

- [Kiro](https://kiro.dev): the IDE or Kiro CLI. Installing as a power needs a Kiro IDE release that supports Agent Plugins powers; older 0.x releases only load legacy `POWER.md` powers, so update Kiro or install the skills directly.
- A 42Crunch account: [Starter (Free Trial)](https://42crunch.com/freemium/?source=kiro), a paid token-based plan (Individual or Individual Pro), or a Platform account with an API key (Team 10, Team 25, or Enterprise).
- On macOS and Linux: `curl` or `wget`, `shasum` or `sha256sum`, and `python3` (used to verify the binary download and to read audit and scan reports). On Windows, the built-in PowerShell commands are used instead.
- For scans: a running API reachable from your machine, at the URL in `servers[0]` of your OAS, your GraphQL endpoint URL, or the URL in `SCAN42C_HOST`.

The `42c-ast` binary is downloaded, checksum-verified, and kept up to date automatically on first use.

## Installation

### As a power (recommended)

In the Kiro IDE, open the **Powers** panel, choose **Add Custom Power → Import power from GitHub**, and enter the plugin folder URL:

```
https://github.com/42Crunch-AI/kiro-plugins/tree/main/plugins/42crunch-api-security-testing
```

Use the folder URL, not the repository root: the power's `plugin.json` manifest lives in that folder. If the import does not accept the URL, clone the repository and choose **Add Custom Power → Import power from a folder** instead, selecting `plugins/42crunch-api-security-testing`.

To update, select the power in the Powers panel and choose **Check for updates**. To remove it, choose **Uninstall**.

**Kiro CLI:** install from a local clone, then start chat with the V3 agent. The V2 agent, which is still the CLI's default for non-interactive runs, does not load skills from installed powers.

```bash
git clone --depth 1 https://github.com/42Crunch-AI/kiro-plugins.git /tmp/42crunch-kiro
kiro-cli powers install /tmp/42crunch-kiro/plugins/42crunch-api-security-testing
kiro-cli chat --v3
```

To remove it from the CLI: `kiro-cli powers uninstall 42crunch-api-security-testing` (or `/powers uninstall 42crunch-api-security-testing` in chat). If you use the V2 agent, install the skills into your project instead (below).

### As skills

Copy the skills into your project to use them in the Kiro IDE, Kiro CLI, Kiro Web, and Kiro Mobile:

```bash
git clone --depth 1 https://github.com/42Crunch-AI/kiro-plugins.git /tmp/42crunch-kiro

# From your project root
mkdir -p .kiro/skills
cp -R /tmp/42crunch-kiro/plugins/42crunch-api-security-testing/skills/* .kiro/skills/
```

To make them available in every project in the Kiro IDE, copy them to `~/.kiro/skills/` instead. Kiro loads global skills in the IDE only; use the project folder for the CLI, Web, and Mobile.

You can also import a single skill in the IDE: in the Kiro panel, open **Agent Steering & Skills**, click **+**, choose **Import a skill**, and paste the URL of a skill folder, for example `https://github.com/42Crunch-AI/kiro-plugins/tree/main/plugins/42crunch-api-security-testing/skills/42crunch-audit`.

Custom agents don't load skills automatically. Add them to the agent's `resources`, for example `skill://.kiro/skills/*/SKILL.md`.

### Upgrading from the earlier `.kiro/` layout

Earlier releases were installed by copying a `.kiro/` folder into the project. Before installing this version, remove the files it left behind:

```bash
rm -rf .kiro/steering/references
rm -rf .kiro/skills/code-to-oas .kiro/skills/postman-to-oas   # replaced by generate-oas
```

## Quick Start

1. **Install the plugin** as a power, or copy the skills (see Installation above).
2. **Set up the environment**: say *"set up 42crunch"* or type `/42crunch-setup`.
3. **Audit your API**: say *"run a 42Crunch audit"*. If you don't have an OpenAPI file yet, Kiro offers to generate one from your source code.
4. **Fix issues**: Kiro presents findings by severity and asks your consent before changing anything.
5. **Scan your API**: say *"run a conformance scan"* against your running server.

## Common Scenarios

See [RECIPES.md](./RECIPES.md) for step-by-step guides covering the most common workflows, including:

- Running a **fix-only audit** from an existing report (skip re-running the audit)
- **Review-only mode**: see findings without applying any fixes
- **Full pipeline** (audit + scan) in a single session
- **Scan only** when the audit is already passing
- **Generating an OAS** from source code and/or a Postman/Insomnia collection, then auditing it immediately
- **GraphQL**: auditing a schema, scanning a live endpoint, or both in one session

## Skill Details

### `42crunch-setup`

Installs the `42c-ast` binary for your OS/architecture, verifies its checksum, and walks you through credential configuration. Supports Platform (Team 10, Team 25, Enterprise) and Token (Starter (Free Trial), Individual, Individual Pro) modes. Credentials are stored in `~/.42crunch/conf/env` with `600` permissions.

> **Invoke:** `/42crunch-setup`, or say "set up 42crunch", "configure 42crunch", "install 42c-ast", "update 42c-ast", "set api key", "42crunch not working", "binary not found"

---

### `42crunch-audit`

Runs a static analysis of an OpenAPI Specification **or GraphQL schema** and produces a 0–100 security score.

OAS findings are classified into four tiers:

- **SQG-Blocking**: must fix to pass the Security Quality Gate
- **Security**: recommended fixes
- **Data Validation**: informational
- **Spec Conformance**: OAS format defects outside the score/SQG

GraphQL findings are classified into two tiers:

- **Resource Limiting**: missing query-cost and list-size restrictions (the DoS surface)
- **Data Validation**: built-in scalars and custom scalars missing value constraints

GraphQL fixes annotate the schema with constraint and cost directives (`@stringValue`, `@numberValue`, `@list`, `@cost`); Kiro declares the directive definitions in the SDL and notes that server-side enforcement is a separate step.

Kiro asks your explicit consent before applying any changes, then re-runs the audit to confirm passage.

**Platform mode:** SQG threshold enforced from your platform policy, including tag-based SQGs (GraphQL SQGs are configured on the platform like OAS SQGs).  
**Token mode:** No SQG gate; you set the target score (and, for OAS, blocking severity) for the session.

> **Invoke:** `/42crunch-audit`, or say "run audit", "42crunch audit", "fix audit issues", "SQG audit", "audit score", "audit my graphql schema"

Kiro asks for:
1. OpenAPI Specification file or GraphQL schema

---

### `42crunch-scan`

Runs a live conformance and authorization test against a running API server (**REST or GraphQL**). Kiro confirms the target URL, checks reachability, analyses the API definition (operations, auth schemes, dependency chains, BOLA/BFLA candidates), and presents a scan preview before any configuration begins. After a happy-path validation run, Kiro asks your consent before starting the full fuzzing scan.

OAS findings are classified into three tiers:

- **Authorization failures**: BOLA/BFLA confirmed
- **SQG-Blocking conformance**: must fix to pass the Security Quality Gate
- **Informational conformance**: surfaced for review

GraphQL scans use the same three tiers. A GraphQL schema declares no auth, so Kiro asks how your API authenticates (a login mutation, a bearer token, or an API-key header) and for a second user (BOLA) or an admin (BFLA) when the schema has candidates. Because GraphQL servers often refuse with HTTP 200 and an error in the body, each authorization finding is confirmed against the response data before it is reported.

Kiro asks your consent before applying any fixes, both contract updates (OAS or SDL) and server-side code/resolver changes.

**Platform mode:** SQG enforced from platform policy.  
**Token mode:** All findings presented informally; you decide what to fix.

> **Invoke:** `/42crunch-scan`, or say "run scan", "scan only", "conformance test", "BOLA test", "BFLA test", "42crunch scan", "scan config", "scan my graphql api"

Kiro asks for:
1. OpenAPI Specification file or GraphQL schema
2. API host endpoint

---

### `42crunch-api-security-testing`

Orchestrates Audit (Phase 1) and Scan (Phase 2) in sequence for a REST or GraphQL API. Resolves the API definition and confirms the scan target URL up front. Each phase requires separate user consent. Produces a combined summary covering both phases.

> **Invoke:** `/42crunch-api-security-testing`, or say "run audit and scan", "full 42crunch pipeline", "full security check", "audit then scan", "SQG"

Kiro asks for:
1. OpenAPI Specification file or GraphQL schema
2. API host endpoint

---

### `generate-oas`

Generates a complete `openapi.json` from an API codebase, a Postman or Insomnia collection, or both. Kiro asks which sources are available and uses whichever you provide:

- **Codebase only**: detects routes, parameters, request/response schemas, auth middleware, data models, and server config from the source.
- **Postman collection only**: extracts paths, methods, parameters, request/response bodies, headers, and auth schemes from a v2.0/v2.1 collection (and optional environment file), resolving `{{variableName}}` placeholders.
- **Insomnia collection only**: extracts the same contract details from a v4 (JSON) or v5 (JSON or YAML) export, resolving `{{ variableName }}`/`{{ _.variableName }}` templating. Insomnia exports carry no saved example responses, so response shapes are best-effort placeholders unless a codebase is also provided.
- **Codebase + collection**: the codebase is treated as the structural source of truth; the collection enriches the result with real example values and surfaces any endpoint the codebase analysis missed.

Deduplicates schemas into `components/schemas` and performs a self-review pass before writing the file.

Supported frameworks: Express, Fastify, Koa, Hapi, NestJS, FastAPI, Flask, Django, Starlette, Spring Boot, Quarkus, Micronaut, Gin, Echo, Chi, Gorilla/mux, Rails, Sinatra, Grape, ASP.NET Core, and more.

> **Invoke:** `/generate-oas`, or say "generate OAS", "create OpenAPI spec", "document my API", "reverse-engineer spec", "write openapi.json from my codebase", "convert postman to openapi", "convert insomnia to openapi", "postman collection to OAS", "insomnia collection to OAS", "generate spec from postman", "generate spec from insomnia"

Kiro asks for:
1. Whether you have an API codebase, and if so, its location
2. Whether you have a Postman or Insomnia collection, and if so, its file path (and an optional environment file path)
3. Output file path (default: `openapi.json` at the codebase root, or next to the collection file)

---

## Configuration

Credentials are read from `~/.42crunch/conf/env` (macOS/Linux) or `%APPDATA%\42Crunch\conf\env` (Windows), written by `42crunch-setup`. Never edit this file manually while a skill is running.

| Variable | Description | Mode |
|---|---|---|
| `API_KEY` | Platform token (`api_*` or `ide_*`) | Platform |
| `PLATFORM_HOST` | 42Crunch platform base URL (e.g. `https://us.42crunch.cloud`) | Platform |
| `TRIAL_TOKEN` | Access token (Base64) for Starter (Free Trial), Individual, or Individual Pro (the variable name is kept for backward compatibility) | Token |
| `SCAN42C_HOST` | Scan target URL, overriding `servers[0]` in the OAS or the GraphQL endpoint in the scan config | Both |

Credentials are never printed in plaintext after entry.

## Network access

The skills run `42c-ast` from Kiro's shell, which needs to reach:

| Host | Used for |
|---|---|
| `repo.42crunch.com` | Downloading and updating the `42c-ast` binary |
| Your platform host (e.g. `us.42crunch.cloud`, `eu.42crunch.cloud`) | Audits, scan configuration, and SQGs in Platform mode |
| `stateless.42crunch.com` | Audits and scans in Token mode |
| The API you scan | Scan requests |

Kiro's shell sandbox is off by default. If you turn it on, allow these hosts with `sandbox_network` rules in `~/.kiro/settings/permissions.yaml`, listing specific hosts before wildcards:

```yaml
rules:
  - capability: sandbox_network
    match: ['repo.42crunch.com', 'stateless.42crunch.com', '*.42crunch.cloud']
    effect: allow
```

Add a rule for the host of the API you scan as well.

## Privacy and data handling

- The plugin itself sends nothing: it is a set of instructions for Kiro. All 42Crunch traffic comes from the `42c-ast` binary.
- **Audit:** your OpenAPI file or GraphQL schema is sent to 42Crunch for analysis: to your 42Crunch platform in Platform mode, or to 42Crunch's Token-mode service in Token mode.
- **Scan:** test requests go from your machine to the API you target. `42c-ast` also contacts 42Crunch to authorize the run and apply your platform's settings.
- **Credentials** stay on your machine, in `~/.42crunch/conf/env` (permissions `600`). Scan configurations under `.42c/scan/` can contain the test-user credentials you provide, so use dedicated test accounts, and keep those files out of version control if they hold real secrets.

See the [42Crunch Privacy Policy](https://42crunch.com/privacy-policy.html).

## Support

- Email: [support@42crunch.com](mailto:support@42crunch.com)
- Issues: [github.com/42Crunch-AI/kiro-plugins/issues](https://github.com/42Crunch-AI/kiro-plugins/issues)
- Documentation: [docs.42crunch.com](https://docs.42crunch.com)

## Links

- [42Crunch](https://42crunch.com/)
- [42Crunch on GitHub](https://github.com/42Crunch)
- [Kiro](https://kiro.dev)

## License

MIT — see [LICENSE](./LICENSE) for details.
