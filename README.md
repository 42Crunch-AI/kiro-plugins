# 42Crunch Kiro Plugins

The official [42Crunch](https://42crunch.com) plugins for [Kiro](https://kiro.dev): AI-powered API security directly in your Kiro workflow.

| Plugin | Description |
|---|---|
| [`42crunch-api-security-testing`](./plugins/42crunch-api-security-testing) | Audit OpenAPI specs and GraphQL schemas, scan running REST and GraphQL APIs for vulnerabilities (including BOLA/BFLA), and apply fixes that meet your security quality gates. |

Plugins use the [Agent Plugins](https://agent-plugins.org) format and install in Kiro as powers; the skills can also be installed on their own. See the [plugin README](./plugins/42crunch-api-security-testing/README.md) for installation, usage, network requirements, and data handling.

## Support

- Email: [support@42crunch.com](mailto:support@42crunch.com)
- Issues: [github.com/42Crunch-AI/kiro-plugins/issues](https://github.com/42Crunch-AI/kiro-plugins/issues)
- [42Crunch Privacy Policy](https://42crunch.com/privacy-policy.html)

## Maintainers

Each skill ships its own copy of the reference documents it uses (`skills/<skill>/references/`), because a skill imported on its own only receives its own folder. To keep those copies identical, the reference documents are edited in one place:

| Edit this | To change |
|---|---|
| `shared/references/*.md` | Workflow reference documents used by the skills |
| `plugins/42crunch-api-security-testing/skills/*/SKILL.md` | A skill's entry point and frontmatter |
| `plugins/42crunch-api-security-testing/README.md`, `RECIPES.md` | User-facing documentation |
| `plugins/42crunch-api-security-testing/plugin.json` | Version, description, and activation keywords (Kiro chooses a power by its description and keywords, so they must name what the plugin covers) |

Never edit `skills/*/references/` directly. After changing anything, run:

```bash
python3 tools/build.py
```

It copies each skill's references from `shared/references/` (only the documents that skill mentions, directly or through another reference) and checks the plugin:

- every skill's references match `shared/references/` and nothing it mentions is missing;
- no wording from other AI assistants (tool names, product names, Free Trial attribution) has crept in;
- `SKILL.md` frontmatter follows Kiro's rules;
- `plugin.json` has the Agent Plugins 1.0.0 shape.

The `check` workflow runs `python3 tools/build.py --check` on pull requests and pushes to `main`, and fails if the skills are stale or the plugin is invalid. Bump `version` in `plugin.json` for each release.

## License

MIT — see [LICENSE](./LICENSE) for details.
