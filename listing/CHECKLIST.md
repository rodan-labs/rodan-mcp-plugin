# Submission checklist

Work down each list before you submit to that store. **You** means a person at Rodan has to do
it: it cannot be done from this repository. **Repo** means this repository already does it and
`scripts/check.sh` tests it.

Nothing here has been submitted yet. The server has been live since November 2026.

## Before any submission

| # | Must be true | Who |
|---|---|---|
| 1 | The Rodan MCP server answers at `https://mcp.rodananalytics.com/mcp` over HTTPS with the Streamable HTTP transport, and works with clients that speak the 2025 protocol versions | You |
| 2 | OAuth discovery works: protected-resource metadata at `/.well-known/oauth-protected-resource/mcp`, authorisation-server metadata that lists `authorization_endpoint`, `token_endpoint`, `response_types_supported`, `code_challenge_methods_supported` (including `S256`) and a `registration_endpoint`, and every discovery URL returns HTTP 200 | You |
| 3 | Dynamic client registration accepts each assistant's redirect address: Claude, ChatGPT, Cursor and Google's `googleusercontent.com` addresses. Try each one on the live server | You |
| 4 | The server lists 16 tools to an OmniaGraph member or owner (a viewer sees the eleven that read). Every tool has a `title` and explicit `readOnlyHint`, `destructiveHint` and `openWorldHint`. The five tools that change the workspace, `omniagraph_start_research`, `omniagraph_create_monitor`, `omniagraph_add_to_watchlist`, `omniagraph_upload_document` and `omniagraph_enrich_companies`, have `destructiveHint` true. Names are 64 characters or fewer and unique. Descriptions say what the tool does and do not tell the assistant how to behave | You |
| 5 | The tool names match the skill, the README and the test cases: `search`, `fetch` and `omniagraph_<tool>`. If any name differs on the live server, or a tool is added or removed, change `README.md`, `shared/skills`, `plugins/chatgpt/plugin.json` and the `listing/` files, then run `scripts/sync.sh` and `scripts/check.sh` | You |
| 6 | The privacy policy and terms of service are public at `https://rodan.io/legal-privacy/privacy-policy` and `https://rodan.io/legal-privacy/terms-of-service`. Drafts are in the legal notes folder, outside this repository | You |
| 7 | The GitHub repository `rodan-labs/rodan-mcp-plugin` exists, is public, and has this branch pushed as `main`. Done on 19 November 2026 | You |
| 8 | A reviewer account and a seeded demo workspace exist, with findings, a brief and a monitor, an OmniaGraph user that matches the account, and no two-factor step. The account is an OmniaGraph owner or member, so it sees all 16 tools. The account's password is kept privately and nowhere in this repository. The demo workspace has no dashboards, quarterly briefs or page watches, and private documents are turned off, so those tools return an empty list or a refusal. Seed them, or accept that and keep the note in `listing/reviewer-instructions.md` | You |
| 9 | Each prompt in `listing/openai.md` has been run end to end with the reviewer account and gives the expected result | You |
| 10 | The domain verification files are served with HTTP 200 and no redirect: OpenAI's token at `https://mcp.rodananalytics.com/.well-known/openai-apps-challenge` and Google's at `https://mcp.rodananalytics.com/.well-known/google-connected-apps`. Each store shows its token only when you start its submission | You |
| 11 | The walkthrough video is recorded from `listing/video-script.md`, uploaded where a reviewer can open it without signing in, and its link is in `plugins/chatgpt/plugin.json` | You |
| 12 | A documentation page exists on `rodananalytics.com` or the README is public. Claude needs public documentation by your publish date | You |
| 13 | `support@rodananalytics.com` is monitored. Every store emails review feedback there | You |
| 14 | `scripts/check.sh` and `scripts/build-chatgpt-zip.sh` pass | Repo |
| 15 | After the first listing goes live, edit the sentence in `README.md` that says Rodan is being submitted | You |

## Claude

Two submissions: the connector, then the plugin bundle. Details in `listing/claude.md`.

| # | Must be true | Who |
|---|---|---|
| C1 | You have a paid Claude plan, and on Team or Enterprise you are an Owner or hold the Directory permission | You |
| C2 | Your GitHub account is connected on claude.ai in the organisation you submit from, and it can push to the repository | You |
| C3 | You submit from the organisation that should own the listing for good. The first organisation to submit a folder holds it | You |
| C4 | The connector is submitted first, with every tool run through MCP Inspector or as a custom connector in Claude | You |
| C5 | You have read the wording of all seven acknowledgements in the portal and agree with each. The wording is not in the documentation | You |
| C6 | The plugin passes **Validate** in the portal with no Blocking finding. Re-validate after every push | You |
| C7 | The plugin name `rodan` is not reported as taken or confusable | You |
| C8 | The plugin folder meets the file rules: README over 40 words, a licence, text and PNG files only, no file over 256 KiB, no more than 512 files, no symbolic links | Repo |
| C9 | The plugin points at the same server address as the connector, so people get one set of tools | Repo |
| C10 | The GitHub push webhook is set up, which needs admin access to the repository | You |
| C11 | The portal's four plugin acknowledgements are read and ticked. The documentation does not name them | You |

## OpenAI (ChatGPT)

Details in `listing/openai.md`.

| # | Must be true | Who |
|---|---|---|
| O1 | Rodan Analytics Limited is verified as a business in the OpenAI Platform Dashboard general settings, and you are an organisation owner or hold Apps Management Write | You |
| O2 | The ZIP is built with `scripts/build-chatgpt-zip.sh` and uploaded. It holds no credentials | Repo, then You |
| O3 | The category in `plugin.json` matches a category title shown in the dashboard. `Productivity` is only the documentation's example | You |
| O4 | The country list is the one you want. The draft is `GB`, `IE` and `US` | You |
| O5 | The five positive and three negative test cases are complete, and the video link is set in `review.demo_recording_url` | You |
| O6 | The server is connected in the dashboard, the domain is verified and the tool scan shows no issue. Rescan after any fix | You |
| O7 | Reviewer credentials are in the secure **Review details** form. The account needs no multi-factor step, email or text-message code, magic link or private network | You |
| O8 | The privacy, terms, support and website URLs are public and name Rodan Analytics Limited as the publisher | You |
| O9 | You have read the policy attestations in the dashboard before you accept them | You |

## Cursor

Details in `listing/cursor.md`.

| # | Must be true | Who |
|---|---|---|
| U1 | The repository is public and open source | You |
| U2 | `.cursor-plugin/marketplace.json` and `plugins/cursor/.cursor-plugin/plugin.json` are valid, and the skill has a name and description | Repo |
| U3 | You have installed the plugin in Cursor, signed in and used a tool against the live server | You |
| U4 | You have opened the form at `cursor.com/marketplace/publish` and compared its fields with `listing/cursor.md` | You |

## Google

Details in `listing/google.md`.

| # | Must be true | Who |
|---|---|---|
| G1 | You have applied for the Connected Apps preview and been accepted. One press report says the preview is open only to US-based developers. Google's documentation does not say so, so confirm it with Google before you build | You |
| G2 | A Connected Console account exists, and an owner or administrator has accepted the Connected Apps terms | You |
| G3 | You have opened the category list in the console and chosen the broadest business category whose default capabilities every Rodan product can support. The choice is permanent | You |
| G4 | The authorisation server's discovery document lists a `registration_endpoint`. Google does not accept a metadata document alone | You |
| G5 | Refresh tokens are not rotated for Google, or Google's persistent linking is not affected. Google's guide says to return the same refresh token and extend its life. Rodan's authorisation server must be checked against this | You |
| G6 | The sign-in pop-up works. If the Rodan sign-in page sends headers that block framing, choose the redirect option instead | You |
| G7 | If the server limits access by source address, Google's published address ranges are allowed | You |
| G8 | Testers have Gmail addresses and have tried every example prompt, with and without `@Rodan` | You |
| G9 | The reviewer account is with your Google representative, with seeded data and no two-factor step | You |
| G10 | The description is one sentence under 30 words, there are at least three capabilities and three example prompts, and the prompts meet Google's rules | Repo |
| G11 | The 512 × 512 px icon is a PNG under 1 MB | Repo |
