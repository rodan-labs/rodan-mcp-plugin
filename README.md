# Rodan for AI assistants

Connect Claude, ChatGPT, Cursor and Gemini to your Rodan account. Ask what changed in the
markets, companies and regulators your business follows, and get findings with a source for
every one.

Rodan is operated by [Rodan Analytics Limited](https://rodananalytics.com). You sign in with
your Rodan account, and you see only the apps your account has. The first app is
[OmniaGraph](https://omniagraph.com).

## What you can do

OmniaGraph runs monitors: repeated research on the markets, companies and regulators you
choose. Each run collects public sources and any private documents you add, extracts cited
findings, and scores each finding with OmniaScore.

OmniaScore is a number from 0 to 100 that measures how strong the evidence for a finding is.
Fixed rules calculate it. An AI model does not generate it. It measures the evidence, not
whether a finding is true.

Through your assistant you can:

- ask what changed in a monitor this week
- search findings, briefs and private documents, and read any of them in full
- ask a question of your stored findings
- start research, create a monitor, add to a watchlist and upload a document, after you
  approve each one

## Requirements

- A Rodan account with access to OmniaGraph. Rodan is for business use.
- An AI assistant that supports remote MCP servers with OAuth sign-in.

The server address is:

```text
https://mcp.rodananalytics.com/mcp
```

## Install

Rodan is being submitted to the Claude, ChatGPT, Cursor and Google directories. Until a
listing is live in your assistant, add the server by its address.

| Assistant | Now | From the directory, once listed |
|---|---|---|
| Claude | Customize, Connectors, Add custom connector, then paste the server address | Add Rodan from the Claude directory |
| Claude Code | `/plugin marketplace add rodan-labs/rodan-mcp-plugin`, then `/plugin install rodan@rodan` | The same |
| ChatGPT | Add the server address as a custom app, if your plan allows | Add Rodan from the ChatGPT directory |
| Cursor | Copy [`plugins/cursor/mcp.json`](plugins/cursor/mcp.json) into `.cursor/mcp.json` | Add Rodan from the Cursor marketplace |
| Gemini | Not available until Google lists Rodan | Type `@Rodan` in Gemini |

The first time a tool runs, your assistant opens the Rodan sign-in page. Sign in, approve the
access it asks for and return to your chat.

Use one route per assistant. If you add the plugin and also add the server by hand, you get
two copies of the same tools.

## Tools

Rodan shows only the tools for the apps you have connected. If a connection has expired, the
tool result tells you to reconnect at
[platform.rodananalytics.com/connections](https://platform.rodananalytics.com/connections).

| Tool | What it does | Changes your workspace |
|---|---|---|
| `search` | Finds findings, entities, briefs and private documents | No |
| `fetch` | Returns one item in full | No |
| `omniagraph_list_monitors` | Lists your monitors and their latest run | No |
| `omniagraph_get_report` | Reads a monitor's findings, new and changed first | No |
| `omniagraph_ask` | Answers from your stored findings. Live research uses credits | No |
| `omniagraph_get_run` | Checks the status of a research run | No |
| `omniagraph_start_research` | Starts a research run | Yes |
| `omniagraph_create_monitor` | Creates a scheduled monitor | Yes |
| `omniagraph_add_to_watchlist` | Adds an entity to your watchlist | Yes |
| `omniagraph_upload_document` | Uploads a private document | Yes |

Tools that change your workspace are marked as such, so your assistant asks you first.
Answering from stored findings is free. Live research and new runs use workspace credits.

## Privacy

This repository holds configuration files and one skill. It has no code that runs on your
machine and it collects nothing.

When you use Rodan through the server, we handle your data as follows. Our
[privacy policy](https://platform.rodananalytics.com/privacy) has the full detail.

- **What Rodan stores:** your email address and name, your client name and logo, which apps
  your account has, and your connection tokens, which are encrypted.
- **What passes through:** results from an app go through the Rodan server to your assistant.
  The server does not store them.
- **Where results go:** to the AI assistant you chose, such as Claude, ChatGPT, Cursor or
  Gemini, and then to its provider. They handle results under their own terms.
- **Each product has its own policy.** Read the
  [OmniaGraph privacy policy](https://omniagraph.com/privacy) for what OmniaGraph holds.
- **Disconnecting:** remove a connection at
  [platform.rodananalytics.com/connections](https://platform.rodananalytics.com/connections).
- **We do not use your content to train AI models.**

Our [terms of service](https://platform.rodananalytics.com/terms) apply to your use of Rodan.

## What is in this repository

| Path | What it is |
|---|---|
| `plugins/claude/` | Claude and Claude Code plugin: the server connection and one skill |
| `plugins/cursor/` | Cursor plugin: the server connection and one skill |
| `plugins/chatgpt/` | Source for the ChatGPT plugin ZIP |
| `shared/skills/` | The one skill, copied into each plugin |
| `assets/` | Rodan icons |
| `listing/` | Copy and instructions for the store submissions |
| `scripts/` | Checks and the ZIP build, all run in Docker |

## Develop

Everything runs in Docker. Nothing is installed on your machine.

```sh
scripts/sync.sh              # copy the shared skill, icons and licence into each plugin
scripts/check.sh             # validate manifests, listing limits and writing rules
scripts/build-chatgpt-zip.sh # build dist/rodan-chatgpt-plugin-<version>.zip
scripts/make-assets.sh       # rebuild the icons from assets/source
```

The ZIP is built on demand and is not committed.

## Support

Email [support@rodananalytics.com](mailto:support@rodananalytics.com).

## Licence

MIT. See [LICENSE](LICENSE). Copyright Rodan Analytics Limited.
