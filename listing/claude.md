# Claude: field-by-field copy

Claude takes two submissions at [claude.ai/directory/manage](https://claude.ai/directory/manage).
Anthropic asks for both when you run the server and publish a plugin that points at it:

1. **MCP connector**: the server at `https://mcp.rodananalytics.com/mcp`.
2. **Plugin bundle**: this repository's `plugins/claude` folder, which holds the same server
   address and one skill.

Both use the same server address, so people who have both see one set of tools, not two.
Submit the connector first. Then submit the plugin bundle and pair the two listings.

Every field below with a limit in its heading is checked by `scripts/check.sh`.

## 1. MCP connector

### Step 1: Connection

| Field | Enter |
|---|---|
| Server URL | `https://mcp.rodananalytics.com/mcp` |
| Users connect to different URLs | Leave off. Every user connects to this one address |

### Step 2: Tools

Nothing to type. The portal reads the tools from the server. Sign in as an OmniaGraph
member or owner, or the portal sees only the eleven tools that read. It should show 16 tools:

| Tools | Annotation |
|---|---|
| `search`, `fetch`, `omniagraph_list_monitors`, `omniagraph_get_report`, `omniagraph_ask`, `omniagraph_get_run`, `omniagraph_company_intelligence`, `omniagraph_get_dashboards`, `omniagraph_get_quarterly_brief`, `omniagraph_page_watch_entries`, `omniagraph_get_enrichment` | `readOnlyHint` true, `destructiveHint` false |
| `omniagraph_start_research`, `omniagraph_create_monitor`, `omniagraph_add_to_watchlist`, `omniagraph_upload_document`, `omniagraph_enrich_companies` | `readOnlyHint` false, `destructiveHint` true |

Before you submit, check that every tool has a `title` and both hints, and that each tool name
is 64 characters or fewer.

### Step 3: Listing

#### Server name (max 100 characters)

```text
Rodan
```

#### One-liner (max 200 characters)

```text
Cited findings on the markets, companies and regulators you follow, each scored with OmniaScore for the strength of its evidence.
```

#### Description (max 2,000 characters)

```text
Rodan connects Claude to your Rodan account. Today it gives you OmniaGraph, which runs monitors: repeated research on the markets, companies and regulators your business follows.

Each run collects public sources and any private documents you add, extracts cited findings and scores each one with OmniaScore. OmniaScore is a number from 0 to 100 that measures how strong the evidence for a finding is. Fixed rules calculate it, not an AI model. It measures the evidence, not whether a finding is true.

Ask Claude what changed this week, search findings, briefs and private documents, read a finding with its sources, or ask a question of your stored findings. Claude can also read your workspace's company map and cited company profiles, dashboard figures with their sources, quarterly briefs with their data gaps, and dated entries from the university and incubator pages your workspace watches.

Eleven tools only read. Five change your workspace, so Claude asks you first: starting research, creating a monitor, adding to a watchlist, uploading a document and enriching a list of companies. Answering from stored findings is free. Live answers and research runs use workspace credits. Enrichment researches each company on the web.

You sign in with your Rodan account and see only the apps your account has. Each app keeps its own users and roles, so you can do only what your role in the app allows, and you need an OmniaGraph account to see findings.

Results go to Claude and are handled under Anthropic's terms. Rodan stores your email address, name, client name and logo, which apps your account has and your connection tokens, which are encrypted. It does not store results. Rodan is for business use.
```

#### Categories (pick one to five from the portal's list)

The documentation does not list the category names, so this page could not check them.
Pick the closest of these descriptions from the list the portal shows:

- research and analysis
- business intelligence or data and analytics
- business and productivity
- compliance or regulation, if the list has it

#### Other listing fields

| Field | Enter |
|---|---|
| Documentation URL | `https://github.com/rodan-labs/rodan-mcp-plugin#readme` once the repository is public, or a page on `rodananalytics.com` if you publish one |
| Privacy policy URL | `https://rodan.io/legal-privacy/privacy-policy` |
| Support contact | `support@rodananalytics.com` |
| Icon | `assets/rodan-icon-512.png` |
| URL slug | `rodan`. It is permanent once published |

### Step 4: Use cases

#### Primary use cases (max 600 characters)

```text
Catch up on what changed in the markets, companies and regulators you follow. Check the evidence behind a finding and open its sources. Read the latest brief, with its sources, before a meeting. Search findings and private documents. Look up a company's cited profile, a dashboard figure or a quarterly brief. Set up a monitor, add to a watchlist or enrich a list of companies by chat, after you approve the change.
```

| Question | Answer |
|---|---|
| What users need before they connect | A Rodan account with access to OmniaGraph. Rodan is for business use. Reviewers: a ready-made account is in the reviewer instructions |
| Does the connector read data, write data or both | Both. Eleven tools only read. Five tools change the workspace: starting research, creating a monitor, adding to a watchlist, uploading a document and starting a company enrichment job |

### Step 5: Company

| Field | Enter |
|---|---|
| Company name | Rodan Analytics Limited |
| Website | `https://rodananalytics.com` |
| Primary contact | `support@rodananalytics.com` |

### Step 6: Authentication

| Field | Enter |
|---|---|
| Authentication requirement | Required |
| Authentication methods | OAuth 2.0, with dynamic client registration. Leave the OAuth client ID and secret blank so Anthropic does not hold a client for you |

Rodan accepts HTTPS, loopback and native-scheme redirect addresses at registration. Confirm on
the live server that Claude's registration is accepted (see `CHECKLIST.md`). The documentation
pages read for this task do not print Claude's callback address.

### Step 7: Data handling

| Question | Answer |
|---|---|
| Whose API sits behind the server | Our own. The Rodan server calls OmniaGraph, which Rodan Analytics Limited owns and runs. It does not proxy a third party's API |
| Personal health data | No |
| Sponsored content | No |

### Step 8: Test and launch

Paste `listing/reviewer-instructions.md` with the placeholders filled in. Then confirm you ran
every tool yourself, either in MCP Inspector or as a custom connector in Claude. That
confirmation is yours to give, so do not tick it until you have done it.

### Step 9: Compliance

The portal asks for seven acknowledgements and all seven are required. The documentation names
the topics but does not print the wording, so read the wording in the portal before you tick
each box. What each topic means for Rodan:

#### Acknowledgement 1: Directory guidelines

You agree to the Anthropic Software Directory Terms and Policy. For Rodan: the connector does
what its listing says, describes each tool accurately and holds no hidden features. Read both
documents once before you tick.

#### Acknowledgement 2: First-party API usage

The server calls your own APIs or ones you legitimately proxy. For Rodan: it calls OmniaGraph,
a product of Rodan Analytics Limited. The server domain, `mcp.rodananalytics.com`, is a Rodan
domain.

#### Acknowledgement 3: Financial transactions

The connector does not transfer money, cryptocurrency or other financial assets. For Rodan:
true. No tool takes a payment or moves money. Some calls use workspace credits, which are a
usage allowance inside OmniaGraph, not a payment made through the connector.

#### Acknowledgement 4: AI media generation

The connector does not generate images, video or audio with AI models. For Rodan: true. It
returns text: findings, briefs, company profiles, dashboard figures and links to sources.

#### Acknowledgement 5: Prompt injection

Tool descriptions say what a tool does and do not tell Claude how to behave, and the server
does not try to steer Claude. For Rodan: you must check this on the live server. Read every
tool description. Remove any sentence that tells Claude to call another tool, to ignore its
instructions or to promote a product.

#### Acknowledgement 6: Conversation data collection

The connector collects no conversation data beyond what a tool needs, and does not read
Claude's memory, chat history or files. For Rodan: the server receives only the arguments of
each tool call. Results pass through it and are not stored.

#### Acknowledgement 7: Public documentation

Public documentation exists by your publish date. A blog post or help-centre article is enough.
For Rodan: the repository README is documentation once the repository is public. A page on
`rodananalytics.com` is better and is your job.

## 2. Plugin bundle

Submit after the connector. The portal reads everything below from the repository, so you
change copy by editing the repository, not the form.

### Step 1: Source

| Field | Enter |
|---|---|
| Repository | `rodan-labs/rodan-mcp-plugin` |
| Plugin path | `plugins/claude` |
| Branch or tag | Leave empty to follow `main` |

Run **Validate**. Fix every finding marked Blocking and validate again. The result applies to
one commit, so re-validate after every push.

### Step 2: Listing details

Nothing to type. The portal reads the name (`rodan`), `displayName` (`Rodan`), description and
version from `plugins/claude/.claude-plugin/plugin.json`, and the listing text from
`plugins/claude/README.md`.

### Step 3: Data handling

#### Plugin data handling answers (max 800 characters)

```text
The plugin holds configuration and one skill and runs no code. It does not read or store personal data itself. It sends no data to any service except its one declared connector, the Rodan server at mcp.rodananalytics.com. Through that connector, Rodan handles your email address, name, client name and logo, which apps your account has and encrypted connection tokens. Results pass through to Claude without being stored. Rodan keeps data for as long as it needs it for the purpose it was collected, by criteria set out in its privacy policy. The plugin is for business use and is not intended for people under 18.
```

The portal asks four questions. Answer them like this:

| Question | Answer |
|---|---|
| Does the plugin read or store personal data | No, the plugin does not. The connector handles account data, as described above |
| Does it send data to services other than its declared connectors | No |
| How long does it keep data | The plugin keeps none. For the connector, by criteria, as the privacy policy sets out |
| Is it intended for people under 18 | No |

### Step 4: Compliance

Check that the contact email is `support@rodananalytics.com`, then tick all four
acknowledgements. The documentation says there are four but does not name them, so read
them in the portal.

### Step 5: Review and submit

Keep **GitHub push webhook** selected so new commits reach the directory. Setting it up needs
admin access to the repository on GitHub.

## Before you submit

- The repository must be public before the plugin listing goes live. It may stay private while
  you validate and submit, but then the portal needs the Claude GitHub App installed on it.
- You need a paid Claude plan, your GitHub account connected on claude.ai in the organisation you
  submit from, and push access to the repository.
- The directory holds a plugin name for the first organisation that submits it. Submit from the
  organisation that should own the listing for good.
- The name `rodan` is checked for clashes when you validate. If it is taken, the portal says
  so and you must choose another name in `plugin.json`.
