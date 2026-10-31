---
name: rodan-findings
description: Answer questions about the markets, companies and regulators a business follows, using cited Rodan findings. Use when the user asks what changed in a market, what a monitor found, or for evidence on a company, regulation or topic, and when explaining an OmniaScore.
---

# Use Rodan findings

Rodan gives you findings from the user's own account. A finding is a cited statement from
public sources or the user's private documents, with an OmniaScore. Answer only from what
the tools return.

## Find the right finding

1. To see what the user follows, call `omniagraph_list_monitors`, unless they named a monitor.
2. For "what changed", call `omniagraph_get_report` for that monitor. New and changed
   findings come first. If the reply gives `next_cursor`, ask for the next page only when
   the user needs more.
3. For a question about stored findings, call `omniagraph_ask`. It reads findings already
   held and costs nothing.
4. For a named company, regulation or topic, call `search`, then call `fetch` for each id
   you need to quote.
5. To check a research run, call `omniagraph_get_run`.

Rodan shows only the tools for the apps the user has connected. If a result says the
connection has expired, tell the user to reconnect at
https://platform.rodananalytics.com/connections and stop.

## Cite every finding

- Give the finding's statement as returned. Do not reword it so that it says more than it
  does.
- Give each finding's date and its sources. Link the source URL.
- Keep the finding apart from your own comment. Label your comment as yours.
- If a finding has no source, say so and do not present it as a finding.
- If the tools return nothing relevant, say that. Do not fill the gap from memory.

## Explain OmniaScore

OmniaScore is a number from 0 to 100 that measures how strong the evidence for a finding
is. Fixed rules calculate it. An AI model does not generate it.

- A high score means the evidence is strong. It does not prove the finding is true.
- A low score means the evidence is thin. It does not prove the finding is false.
- Do not turn a score into a probability or a recommendation.
- When the user needs to decide how far to trust a finding, give the score and the sources
  together, and say how the score changed since the previous run if the reply includes that.

## Ask before you change anything

Ask the user before you call `omniagraph_start_research`, `omniagraph_create_monitor`,
`omniagraph_add_to_watchlist` or `omniagraph_upload_document`. Also ask before you call
`omniagraph_ask` with `live=true`, because live research uses credits.

If a tool reports a rate limit, wait for the time it states before you call again.

Rodan results are research to inform a decision. They are not legal, financial or
investment advice, and you should not present them as such.
