# 42Crunch Kiro Plugins

The official [42Crunch](https://www.42crunch.com) plugins for [Kiro](https://kiro.dev) — AI-powered API security capabilities directly in your Kiro workflow.

| Plugin | Description |
|---|---|
| [`42crunch-api-security-testing`](./plugins/42crunch-api-security-testing) | Audit OpenAPI specs, scan live APIs for vulnerabilities (including BOLA/BFLA), and apply fixes that meet your security quality gates. |

Plugins use the [Agent Plugins](https://agent-plugins.org) format and install in Kiro as powers. See the [plugin README](./plugins/42crunch-api-security-testing/README.md) for installation and usage.

## Maintainers

The plugin content is generated from the [GitHub Copilot port](https://github.com/42Crunch-AI/copilot-plugins), whose skills are already host-neutral. Only `README.md` and `LICENSE` under the plugin folder are maintained here by hand. To pull in an upstream release:

```bash
git clone https://github.com/42Crunch-AI/copilot-plugins.git ../copilot-plugins
python3 tools/sync_from_upstream.py --upstream ../copilot-plugins
```

The script copies every reference file a skill needs into that skill's own `references/` folder, rewrites paths and product names for Kiro, and fails if any host-specific wording (other hosts' tool names, product names, Free Trial attribution) remains. The `upstream-sync` workflow runs it with `--check` and fails when this repo falls behind the Copilot plugin.

## Links

- [42Crunch Documentation](https://docs.42crunch.com)
- [Kiro](https://kiro.dev)
- Support: support@42crunch.com
