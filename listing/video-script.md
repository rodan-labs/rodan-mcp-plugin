# Walkthrough video script

About two minutes. OpenAI requires a reviewer-accessible video for an MCP plugin. Claude and
Google reviewers can use the same video. This version is recorded in ChatGPT. To record it for
another assistant, change only the words in square brackets in scene 2.

Read the narration word for word at an even pace, about 130 words a minute. The narration is
244 words, about 1 minute 53 seconds of speech. The pauses for screen actions bring the video
to about two minutes.

## Before you record

- Use the demo workspace and the review account, never a real client's.
- Set the browser to a clean profile with no other tabs, bookmarks or notifications.
- Blur or crop the password field. Never show the password.
- Run each prompt once off camera so you know the result and the timing.
- Have the heat pump monitor ready to delete after the take.
- Record at 1080p or higher, with a voice-over after the screen capture if you prefer.

## Script

| Time | On screen | Narration |
|---|---|---|
| 0:00 | Rodan icon, then an empty ChatGPT chat | This is Rodan, from Rodan Analytics Limited. Rodan connects your AI assistant to your Rodan account. Today it gives you OmniaGraph: cited research on the markets, companies and regulators your business follows. |
| 0:18 | Add Rodan in [ChatGPT]. The Rodan sign-in page opens. Enter the review email. The password field appears, with the text hidden | I'll add Rodan in [ChatGPT]. It sends me to the Rodan sign-in page. I sign in with the review account. |
| 0:32 | The approval page. Click approve. Return to the chat. The tool list shows Rodan's 16 tools | Rodan shows me what the assistant is asking to do. I approve it, and I'm back in my chat. Rodan shows only the tools for the apps this account has. Eleven only read. Five change the workspace, so the assistant asks me first. |
| 0:45 | Type: Use Rodan to show what changed in my monitors this week. The tools run and the answer appears. Scroll to one finding, then its OmniaScore and source link | First, I ask what changed in my monitors this week. The assistant lists my monitors and reads the report. Each finding has a source and an OmniaScore. The OmniaScore is a number from zero to one hundred that measures how strong the evidence is. Fixed rules calculate it, not an AI model. |
| 1:15 | Type: Use Rodan to search my findings for new rules from regulators and show the ones with the strongest evidence first. The answer appears with links | Now I search my findings for new rules from regulators. The assistant searches, reads the findings in full, and puts the strongest evidence first, with links to every source. |
| 1:35 | Type: Use Rodan to set up a monitor on European heat pump subsidies that runs every Monday. The confirmation prompt appears. Click confirm. The result appears | Next, I ask Rodan to set up a monitor on European heat pump subsidies that runs every Monday. This changes my workspace, so the assistant asks me to confirm first. I confirm, and the monitor is created. |
| 1:52 | Open `platform.rodananalytics.com/connections`. Show the connection, then remove it | Last, I open Connections on the Rodan platform. I can see what is connected and remove it at any time. |
| 2:02 | Rodan icon and `support@rodananalytics.com` | That is Rodan. For help, email support at rodananalytics dot com. |

## After you record

- Upload it where a reviewer can open it without signing in. Check the link in a private window.
- Put the link in `extensions.com.openai.review.demo_recording_url` in
  `plugins/chatgpt/plugin.json`, rebuild the ZIP and fill `{{VIDEO_URL}}` in the reviewer
  instructions.
- Delete the heat pump monitor from the demo workspace.
