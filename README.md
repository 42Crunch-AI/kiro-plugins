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

The plugin's skills, references, `RECIPES.md`, and `plugin.json` are generated from the [GitHub Copilot port](https://github.com/42Crunch-AI/copilot-plugins), whose skills are already host-neutral. Only `README.md` and `LICENSE` under the plugin folder are maintained here by hand. To pull in an upstream release:

```bash
git clone https://github.com/42Crunch-AI/copilot-plugins.git ../copilot-plugins
python3 tools/sync_from_upstream.py --upstream ../copilot-plugins
```

The script:

- copies every reference file a skill needs into that skill's own `references/` folder;
- rewrites paths, product names, and Free Trial attribution for Kiro;
- writes `plugin.json` with the upstream version and a Kiro-specific description and keywords (Kiro chooses a power by these, so they must name OpenAPI and GraphQL);
- fails if any other host's wording (tool names, product names, attribution) remains.

The `upstream-sync` workflow runs it with `--check` on pull requests, on pushes to `main`, and weekly, and fails when this repo falls behind the Copilot plugin. Merge an upstream release in `copilot-plugins` first, then sync here.

## License

MIT — see [LICENSE](./LICENSE) for details.
