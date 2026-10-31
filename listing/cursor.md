# Cursor: form values

Cursor lists plugins that are open source and reviewed by hand. Each update is reviewed again.
You submit at [cursor.com/marketplace/publish](https://cursor.com/marketplace/publish). That
page needs you to be signed in, so this task could not read the form itself. The values below
come from the form fields you named, plus what Cursor's plugin reference requires of the
repository. Compare them with the form when you open it, and add any field that is
not here.

## Form values

| Field | Enter |
|---|---|
| Organisation | Rodan |
| Handle | `rodan` |
| Contact | `support@rodananalytics.com` |
| Logo | `plugins/cursor/assets/rodan-icon-512.png` (512 × 512 px, PNG). The same file is at `assets/rodan-icon-512.png` |
| Repository | `https://github.com/rodan-labs/rodan-mcp-plugin` |
| Website | `https://rodananalytics.com` |

#### Description (max 300 characters)

```text
Cited findings on the markets, companies and regulators you follow, each scored by OmniaScore, a deterministic 0 to 100 measure of evidence strength. Sign in with your Rodan account.
```

Cursor documents no limit for the description. The 300-character ceiling above is a safe
choice, not a rule from Cursor.

## What Cursor reads from the repository

| Item | Where | Value |
|---|---|---|
| Marketplace file | `.cursor-plugin/marketplace.json` | One plugin, `rodan`, with source `./plugins/cursor` |
| Plugin manifest | `plugins/cursor/.cursor-plugin/plugin.json` | Name `rodan`, author Rodan Analytics Limited, licence MIT, logo `assets/rodan-icon-512.png` |
| Server | `plugins/cursor/mcp.json` | `https://mcp.rodananalytics.com/mcp`. No variables, so there is nothing to declare |
| Skill | `plugins/cursor/skills/rodan-findings/SKILL.md` | The same skill as the Claude plugin |
| README | `plugins/cursor/README.md` | Usage, configuration and privacy |

Cursor shows the server as `plugin-rodan-rodan` in its approval prompts.

## Before you submit

- The repository must be public and open source. It is MIT licensed.
- The plugin has been tested locally in Cursor. This is your job once the server is live.
- The marketplace checks in Cursor's `plugin-template` repository pass. They were run on this
  repository and the result is in the commit message.
