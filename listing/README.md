# Listing copy

One folder per store, with the exact text to enter in each field. Start with `CHECKLIST.md`.

| File | What it holds |
|---|---|
| `CHECKLIST.md` | What must be true before each submission, and which items are yours |
| `claude.md` | Claude connector and plugin bundle: every field, categories, use cases, data handling and the seven acknowledgements |
| `openai.md` | ChatGPT: metadata, five positive and three negative test cases, release notes, countries and each dashboard step |
| `cursor.md` | Cursor: the form values |
| `google.md` | Google: description, capabilities, example prompts, locale tags and the recommended category |
| `reviewer-instructions.md` | A template with placeholders. Fill it in privately and never commit it filled in |
| `video-script.md` | A word-for-word script for a walkthrough of about two minutes |

A heading such as `(max 200 characters)` over a code block marks a field with a limit.
`scripts/check.sh` counts each one and fails if a field is over its limit.
