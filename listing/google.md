# Google (Connected Apps Platform): field-by-field copy

Google lists the app in the Gemini app and in Search. You build it in Connected Console, test
it with Gmail testers, then send it for review. The documentation is at
[developers.google.com/connected-apps](https://developers.google.com/connected-apps).

Users find the app by typing `@Rodan`, so the name matters. Capabilities and example prompts
are shown to users, and the description is not used as model instructions.

## Step 1: Create the connected app

| Field | Enter |
|---|---|
| Name | Rodan |
| Category | See the recommendation below. It cannot be changed later |
| Connection type | MCP server. It cannot be changed later |

### Recommended category: the broadest business and productivity category

The documentation says a category cannot be changed after you create the app, and that each
category comes with default capabilities the app should support. The pages this task could read
did not list the categories, and the list page returned an error. So this recommendation is a
rule for choosing, not a named category:

1. Choose the broadest business-use category, such as business, productivity or work. Press
   coverage names productivity as one that exists, but that is not Google's documentation.
2. Avoid a narrow category such as health, commerce or ticketing, and avoid a finance category
   that comes with default capabilities for payments or accounts.

Reason: the category is permanent and sets default capabilities, and Rodan is meant to carry
more than one product. Research and monitoring today, and a later analytics product, both fit
a broad business category. A narrow category would force default capabilities that a later
product may not support. Before you create the app, open the category list in Connected
Console and check each default capability. Choose the broadest category whose defaults every
Rodan product can honestly support.

## Step 2: App details

The description must be one sentence under 30 words. Each capability is one entry, with no
leading number. At least two example prompts start with `@Rodan` and at least one mentions
Rodan inside the sentence. No prompt is numbered or in quotation marks.

#### Description, en-GB (under 30 words)

```text
Rodan gives you cited findings on the markets, companies and regulators you follow, each scored for the strength of its evidence.
```

### Capabilities (en-GB)

```text
Find out what changed in the markets, companies and regulators you follow
Search findings, briefs and private documents, with the sources behind each one
Check how strong the evidence is for a finding with its OmniaScore
Ask questions of your stored findings and get answers with sources
Start research and create monitors, after you approve each change
```

### Example prompts (en-GB)

```text
@Rodan what changed in my markets this week?
@Rodan show me the findings on a company with the strongest evidence
@Rodan summarise my latest brief and list its sources
Ask Rodan if my stored findings cover new rules on battery storage
```

### Example prompts (en-US)

```text
@Rodan what changed in my markets this week?
@Rodan show me the findings on a company with the strongest evidence
@Rodan summarize my latest brief and list its sources
Ask Rodan if my stored findings cover new rules on battery storage
```

### Locale tags

Connected Console reads a language tag around each locale's text and lists the locales it
detects under each field. Paste the text for each field as below. The two locales differ only
where spelling differs.

#### Description, tagged (paste into Description)

```text
<en-GB>Rodan gives you cited findings on the markets, companies and regulators you follow, each scored for the strength of its evidence.</en-GB>
<en-US>Rodan gives you cited findings on the markets, companies and regulators you follow, each scored for the strength of its evidence.</en-US>
```

#### Capabilities, tagged (paste into Capabilities)

```text
<en-GB>Find out what changed in the markets, companies and regulators you follow</en-GB><en-US>Find out what changed in the markets, companies and regulators you follow</en-US>
<en-GB>Search findings, briefs and private documents, with the sources behind each one</en-GB><en-US>Search findings, briefs and private documents, with the sources behind each one</en-US>
<en-GB>Check how strong the evidence is for a finding with its OmniaScore</en-GB><en-US>Check how strong the evidence is for a finding with its OmniaScore</en-US>
<en-GB>Ask questions of your stored findings and get answers with sources</en-GB><en-US>Ask questions of your stored findings and get answers with sources</en-US>
<en-GB>Start research and create monitors, after you approve each change</en-GB><en-US>Start research and create monitors, after you approve each change</en-US>
```

#### Example prompts, tagged (paste into Example prompts)

```text
<en-GB>@Rodan what changed in my markets this week?</en-GB><en-US>@Rodan what changed in my markets this week?</en-US>
<en-GB>@Rodan show me the findings on a company with the strongest evidence</en-GB><en-US>@Rodan show me the findings on a company with the strongest evidence</en-US>
<en-GB>@Rodan summarise my latest brief and list its sources</en-GB><en-US>@Rodan summarize my latest brief and list its sources</en-US>
<en-GB>Ask Rodan if my stored findings cover new rules on battery storage</en-GB><en-US>Ask Rodan if my stored findings cover new rules on battery storage</en-US>
```

The documentation does not show how a multi-entry field takes two locales. If Connected Console
rejects the combined lines, enter the en-GB lines only, one entry per line, and add en-US once
you see how it lists the locales. The checker reads the en-GB blocks above.

### Other app details

| Field | Enter |
|---|---|
| Icon | `assets/rodan-icon-512.png`. JPG or PNG, up to 1 MB, 512 × 512 px. The file is 512 × 512 px and well under 1 MB |
| Terms of service URL | `https://rodan.io/legal-privacy/terms-of-service` |
| Policy URL | `https://rodan.io/legal-privacy/privacy-policy` |
| Website URL | `https://rodananalytics.com` |

## Step 3: MCP endpoint and domain verification

| Field | Enter |
|---|---|
| MCP endpoint | `https://mcp.rodananalytics.com/mcp` |
| Verification file | Download `google-connected-apps.json` from the console and host it at `https://mcp.rodananalytics.com/.well-known/google-connected-apps`. It must return HTTP 200 directly, with no redirect, and include your token |

Google needs a publicly reachable HTTPS endpoint using the Streamable HTTP transport. If the
server restricts access by source address, allow Google's ranges. The documentation gives
the ranges and says to refresh them from Google's published lists, so read them from there at
the time.

## Step 4: Access credentials

| Question | Answer |
|---|---|
| Does your server require authorization | Yes |
| Authorization model | User-delegated (Authorization Code) |
| Allowlist Google's redirect addresses | Add the six `googleusercontent.com` patterns the console shows in its banner to the Rodan sign-in service |
| Client registration | Client ID metadata or dynamic client registration. Google checks metadata documents first and falls back to dynamic registration. Its OAuth guide says the discovery document must still list a `registration_endpoint` |
| Authenticate with your developer credentials | Pop up. Use Redirect if the Rodan sign-in page sends frame headers that block the pop-up |

## Step 5: Test accounts

Give your Google representative the reviewer account from `listing/reviewer-instructions.md`.
Google needs seeded data and no two-factor step.

## Step 6 and 7: Sync tools, availability and tool settings

| Setting | Enter |
|---|---|
| Sync tools | Sign in with a developer account that can reach every tool. Tools it cannot reach do not sync |
| Countries and regions | United Kingdom and United States. Your decision to change |
| Languages | English |
| Products | Gemini app and Search, as the console offers |
| User confirmation | Leave on for the four tools that change the workspace. The console selects it when a tool's annotations set `destructiveHint` to true |
| Additional context (locale, location) | Request none. Rodan needs none, and over-asking can fail review |

## Step 8 and 9: Test and review

Add testers on **Manage testers**. Only `@gmail.com` accounts can be added, and they may need
up to 10 minutes to see the app. Try every example prompt, both with `@Rodan` and in plain
sentences, and the full sign-in flow. Then **Send for review** on the Releases card. After
approval, **Publish**.

## What Google's policy means for the copy

- Descriptions must not claim more than the app does. Every capability above is a tool that
  exists.
- A tool description must not mention other tools or set rules for when to use them.
- The app must not wrap APIs it does not own. OmniaGraph is a Rodan Analytics Limited product.
- The app needs a privacy policy that says how data is collected, used, stored and shared, and
  help that explains how users manage and delete their data.
