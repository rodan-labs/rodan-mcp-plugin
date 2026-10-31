# Reviewer instructions: template

Use this for the Claude "Test and launch" step, the OpenAI "Review details" form and the Google
test-account hand-off. Fill every placeholder in `{{double braces}}` before you paste it. Never
commit the filled-in version. The credentials live in your password manager, not in this
repository.

---

## About Rodan

Rodan connects an AI assistant to a Rodan account. Today the connected app is OmniaGraph, which
runs monitors: repeated research on markets, companies and regulators, with cited findings that
each carry an OmniaScore (a deterministic 0 to 100 measure of how strong the evidence is).

Server address: `https://mcp.rodananalytics.com/mcp`

## Review account

| Item | Value |
|---|---|
| Sign-in page | `https://platform.rodananalytics.com` |
| Email | {{REVIEWER_EMAIL}} |
| Password | {{REVIEWER_PASSWORD}} |
| Demo workspace | {{DEMO_WORKSPACE_NAME}} |
| Monitors in the workspace | {{DEMO_MONITOR_NAMES}} |
| Two-factor step | None. The account asks for no code, link or text message |
| Valid until | {{REVIEWER_VALID_UNTIL}} |

The account reaches only the demo workspace. It holds sample data, so you can run every tool.

## How to connect

1. In your assistant, add Rodan (or the custom connector at the server address above).
2. When the assistant opens the Rodan sign-in page, enter the email above. The page then asks
   for the password above. Enter it.
3. Rodan shows what the assistant is asking to do. Approve it.
4. Rodan then asks you to connect OmniaGraph. Approve that too. You return to your chat.

## What to try

| Try this | What you should see |
|---|---|
| "What changed in my monitors this week?" | The monitors listed, then new and changed findings, each with an OmniaScore, a date and source links |
| "Search my findings for new rules from regulators" | Search results, then the findings read in full, with sources |
| "Summarise my latest brief and list its sources" | A short summary and the sources as links |
| "What is the latest on battery storage rules? Do not run live research." | An answer from stored findings only, with sources |
| "Set up a monitor on European heat pump subsidies that runs every Monday" | A request to confirm first, then a new monitor |

The last row changes the demo workspace. It is safe to repeat. {{DEMO_RESET_NOTE}}

## Things that look unusual but are expected

- Rodan shows only the tools for apps the account has connected. If OmniaGraph is not
  connected, you will see no OmniaGraph tools.
- Calls that use credits are limited per minute and per day. If a call is refused, the
  message says when to try again.
- Results go to the assistant you are testing, and Rodan does not store them.

## Contact during review

{{SUPPORT_CONTACT_NAME}}, `support@rodananalytics.com`, {{SUPPORT_CHANNEL_AND_HOURS}}

Walkthrough video: {{VIDEO_URL}}
