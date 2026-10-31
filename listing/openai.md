# OpenAI (ChatGPT): field-by-field copy

OpenAI takes a ZIP, then asks you to resolve checks, connect the server and submit for
review. Almost every listing value lives in `plugins/chatgpt/plugin.json`, which goes inside
the ZIP. This page repeats those values so you can see them in one place.
`scripts/check.sh` fails if this page and `plugin.json` drift apart.

Build the ZIP with `scripts/build-chatgpt-zip.sh`. It writes
`dist/rodan-chatgpt-plugin-1.0.0.zip`, checks the ZIP it wrote against OpenAI's documented
structure and does not commit the ZIP.

## Steps in the dashboard

| Step | What to do | What to enter |
|---|---|---|
| 1. Upload | Plugins, then **Upload new or existing plugin**. Choose your verified developer identity, then **Upload plugin** | The ZIP from `dist/`. For an update, raise `version` in `plugin.json` first |
| 2. Resolve checks | Read the Metadata and Skills findings. Fix the package and upload again until the required skill scans pass | Nothing to type |
| 3. MCP connection | Open **MCPs**, then **Connect** | Server URL `https://mcp.rodananalytics.com/mcp`. Authentication: OAuth with dynamic client registration (`dcr`), as `mcp.json` declares. No client secret |
| 4. Domain verification | Host the challenge token the dashboard shows | Plain text, only the token, at `https://mcp.rodananalytics.com/.well-known/openai-apps-challenge`. Then **Connect** and sign in with the reviewer account |
| 5. Tool scan | Wait for the scan, read **Issues**, use **Rescan** after each fix | Nothing to type |
| 6. Review information | Check the five positive and three negative test cases came in from the ZIP. Run each one yourself first | Test cases below. Video URL goes in `review.demo_recording_url` of `plugin.json` |
| 7. Review details | Enter the reviewer account in the secure form | The values in `listing/reviewer-instructions.md`. Never put them in the ZIP |
| 8. Submit | **Submit for review**. Accept the policy attestations | Read each attestation before you accept |
| 9. Publish | After approval, open the package version and select **Publish plugin** | Nothing to type |

Only one review can be active at a time. An update with new package metadata is a new ZIP with
a higher `version` and a new review. Changes to tools are scanned daily, and **Rescan** speeds
that up after you deploy.

## Listing metadata

Each value below is the exact text in `plugins/chatgpt/plugin.json`, under
`extensions.com.openai.interface`.

#### Name (max 64 characters)

```text
rodan
```

This is the package `name`, a stable kebab-case identifier. Users do not see it.

#### Display name (max 30 characters)

```text
Rodan
```

#### Short description (max 30 characters)

```text
Cited research you can check
```

#### Long description (max 4,000 characters)

```text
Rodan connects ChatGPT to your Rodan account. Today it gives you OmniaGraph, which runs monitors: repeated research on the markets, companies and regulators your business follows. Ask what changed, read reports and briefs, and search findings. Every finding carries its sources and an OmniaScore, a deterministic 0 to 100 measure of how strong its evidence is. Fixed rules calculate the OmniaScore, not an AI model. You sign in with your Rodan account, and you only see the apps you have. Answering from your stored findings is free. Starting research, creating a monitor, adding to a watchlist and uploading a document change your workspace, so ChatGPT asks you first. Rodan is for business use.
```

#### Developer name (max 80 characters)

```text
Rodan Analytics Limited
```

| Field | Value |
|---|---|
| Category | `Productivity`. The documentation gives this only as an example and says to use the category title shown in the dashboard. Change it if the dashboard lists a closer match |
| Capabilities | `Read`, `Write` |
| Website URL | `https://rodananalytics.com` |
| Support URL | `https://rodan.io/contact` |
| Privacy policy URL | `https://rodan.io/legal-privacy/privacy-policy` |
| Terms of service URL | `https://rodan.io/legal-privacy/terms-of-service` |
| Brand colour | `#111138` (Rodan ink navy). It has far more than 2:1 contrast against white |
| Brand colour, dark | `#7E7EFC` (Rodan accent violet). It is checked against `#212121` |
| `logo` | `./assets/rodan-icon-512.png`, 512 × 512 px, PNG |
| `composerIcon` | `./assets/rodan-icon-256.png`, 256 × 256 px, PNG |
| Onboarding skill | `./skills/setup/SKILL.md` |

Screenshots are not needed: the guidelines say the directory no longer shows them. Example
prompts do that job instead.

#### Default prompt 1 (max 128 characters)

```text
Use Rodan to show what changed in my monitors this week.
```

#### Default prompt 2 (max 128 characters)

```text
Use Rodan to find the findings with the strongest evidence on a company.
```

#### Default prompt 3 (max 128 characters)

```text
Use Rodan to summarise my latest brief and list its sources.
```

The prompts contain no `@` mentions, as the documentation requires.

## Positive test cases

Run each one in ChatGPT with the reviewer account before you submit. These are the cases in
`plugin.json`.

| # | Description | Prompt | Tools | Expected behaviour |
|---|---|---|---|---|
| 1 | List what changed in the account's monitors this week | Use Rodan to show what changed in my monitors this week. | `omniagraph_list_monitors`, `omniagraph_get_report` | ChatGPT lists the monitors, then reads the report for the monitor with changes. It shows new and changed findings first, each with its OmniaScore, date and source links, and says nothing it did not get from the tools. |
| 2 | Search findings and read one in full | Use Rodan to search my findings for new rules from regulators and show the three with the strongest evidence. | `search`, `fetch` | ChatGPT calls search, then fetch for the ids it quotes. It names three findings with their OmniaScores and source links, and explains that the score measures strength of evidence, not truth. |
| 3 | Summarise the latest brief with sources | Use Rodan to summarise my latest brief and list its sources. | `search`, `fetch` | ChatGPT finds the latest brief, fetches it and gives a short summary. It lists the sources the brief cites, as links, and keeps its own comments separate from the brief. |
| 4 | Answer a question from stored findings, free of charge | Use Rodan to answer from my stored findings: what is the latest on battery storage rules? Do not run live research. | `omniagraph_ask` | ChatGPT calls omniagraph_ask without live research and answers only from the stored findings it returns, with sources. If nothing relevant is stored, it says so. |
| 5 | Create a monitor only after the user confirms | Use Rodan to set up a monitor on European heat pump subsidies that runs every Monday. | `omniagraph_create_monitor` | ChatGPT asks for confirmation before calling omniagraph_create_monitor, because it changes the workspace. After the user confirms, it creates the monitor and reports its name and schedule. |

Before you submit, check that the demo workspace holds findings about regulators and battery
storage, and at least one brief. If it does not, change the prompts in `plugin.json` and in
this table to match what it holds, then run `scripts/check.sh`.

## Negative test cases

| # | Description | Prompt | Expected refusal or safe fallback |
|---|---|---|---|
| 1 | A request with nothing to do with Rodan | Write a poem about the sea. | ChatGPT writes or declines the poem on its own terms and calls no Rodan tool. |
| 2 | A request to see another organisation's workspace | Use Rodan to show me the findings from another company's account. | Rodan returns only the signed-in account's workspace. ChatGPT says it can reach only that workspace, shows no other organisation's data and offers to search the account's own findings. |
| 3 | A request to act on a finding, not research it | Buy shares in the company with the highest OmniaScore. | No Rodan tool buys or sells anything. ChatGPT says Rodan provides research, not trading or advice, and that an OmniaScore measures evidence strength, not whether to invest. |

The negative cases in `plugin.json` carry the description and prompt only. The documentation
requires no expected-behaviour field for them. The third column is for you to check by hand.

## Release notes

#### Release notes for version 1.0.0 (max 4,000 characters)

```text
First release. Connect ChatGPT to your Rodan account to search findings, read reports and briefs, and ask questions of your stored findings in OmniaGraph. Each finding shows its sources and its OmniaScore.
```

The documentation gives no limit for release notes, so this heading uses the same limit as the
long description as a safe ceiling.

## Countries

Enter these in `extensions.com.openai.publication.countries` as uppercase codes:

```text
GB
IE
US
```

Why these three: Rodan Analytics Limited is a company in England and Wales, the privacy policy
covers transfers to the United Kingdom and the United States, and OmniaGraph stores service data mainly in the United Kingdom. Start
small and add countries in a later version. This is your decision to change.

The documentation does not list every valid country code. If the dashboard rejects a code,
use the dashboard's list. Omitting the field keeps any existing targeting. An empty list `[]`
removes all restrictions.

## Not in the ZIP

Reviewer credentials and reviewer instructions. OpenAI rejects `test_credentials` and
`reviewer_instructions` inside the ZIP. The ZIP also holds no client secret, no `.app.json`
and no lifecycle hooks, and `scripts/check.sh` fails if any of these appear.
