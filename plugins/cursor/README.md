# Rodan for Cursor

Connect Cursor to your Rodan account. Ask what changed in the markets, companies and
regulators you follow, and get findings with a source for every one, each scored with
OmniaScore.

## What is in this plugin

- The Rodan server connection at `https://mcp.rodananalytics.com/mcp`. Cursor opens the Rodan
  sign-in page the first time a tool runs. Cursor names the server `plugin-rodan-rodan` in its
  approval prompts.
- One skill, `rodan-findings`. It tells the assistant how to find findings, cite their
  sources and explain what OmniaScore means. OmniaScore is a number from 0 to 100 that measures
  how strong the evidence for a finding is. Fixed rules calculate it, not an AI model.

The plugin has no scripts, rules or hooks, and runs no code on your machine.

## Configuration

There is nothing to configure and no key to enter. Sign in with your Rodan account when
Cursor asks. If you add the server by hand as well, you get two copies of the same tools, so
use one route.

## Requirements

A Rodan account with access to OmniaGraph. Rodan is for business use.

## Privacy

Rodan stores your email address and name, your client name and logo, which apps your account
has, and your connection tokens, which are encrypted. Results from an app pass through the
Rodan server to your assistant and are not stored by it. Read the
[privacy policy](https://platform.rodananalytics.com/privacy) and the
[OmniaGraph privacy policy](https://omniagraph.com/privacy). We do not use your content to
train AI models.

## Support

Email support@rodananalytics.com. Licence: MIT.
