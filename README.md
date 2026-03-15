# open-prs

[![CI](https://github.com/logfoxai/open-prs/actions/workflows/ci.yml/badge.svg)](https://github.com/logfoxai/open-prs/actions)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

**Your entire org's PRs. One terminal. Zero dependencies.**

`open-prs` is a single-file CLI dashboard that shows every open pull request across a GitHub organization — with live CI status, post-merge deploy tracking, clickable links, and a responsive layout that just works.

No config files. No Docker. No Node modules. Just one Python script and `gh`.

<p align="center">
  <img src="assets/screenshot.png" alt="open-prs watch mode" width="800" />
</p>

## Quick Start

```bash
# Install
curl -o ~/.local/bin/open-prs https://raw.githubusercontent.com/logfoxai/open-prs/main/open-prs
chmod +x ~/.local/bin/open-prs

# Run
open-prs myorg          # one-shot
open-prs myorg --watch  # full-screen live dashboard
```

## Features

- **Live CI badges** — instantly see pass, fail, running, or no CI for every PR
- **Post-merge deploy tracking** — merged PRs stay visible while deploy workflows run; failures stick around, successes fade after 15 min
- **Clickable PR titles** — real hyperlinks (OSC 8) in iTerm2, VS Code terminal, Ghostty, Kitty, and more
- **Responsive 2-column layout** — auto-switches when your PRs overflow the terminal height
- **Watch mode** — full-screen alternate buffer, auto-refreshes every 60s, keyboard shortcuts for refresh (`r`), clear merged (`c`), and quit (`q`)
- **Grouped by repo** — clean visual hierarchy, sorted alphabetically
- **Single file, zero deps** — runs on any machine with Python 3.9+ and `gh`

## Requirements

- Python 3.9+
- [GitHub CLI](https://cli.github.com/) (`gh`) — installed and authenticated

## Installation

**curl** (recommended):

```bash
curl -o ~/.local/bin/open-prs https://raw.githubusercontent.com/logfoxai/open-prs/main/open-prs
chmod +x ~/.local/bin/open-prs
```

**Clone and symlink:**

```bash
git clone https://github.com/logfoxai/open-prs.git
ln -s "$(pwd)/open-prs/open-prs" ~/.local/bin/open-prs
```

## Usage

```
open-prs <org> [--watch]
```

- `<org>` — GitHub organization name (required)
- `--watch` / `-w` — full-screen polling mode (every 60s)

### Watch mode keyboard shortcuts

- `r` — Refresh immediately
- `c` — Clear successfully merged/deployed PRs
- `q` — Quit (also `Ctrl+C`)

## Status Badges

### CI (on open PRs)

- `✓ pass` — All checks passed
- `✗ fail` — One or more checks failed
- `● running` — Checks in progress
- `no ci` — No status checks configured

### Deploy (on merged PRs)

After merge, if GitHub Actions workflows are triggered:

- `✓ deployed` — All workflows completed successfully
- `✗ failed` — One or more workflows failed
- `● deploying` — Workflows in progress
- `◦ queued` — Workflows are queued/waiting

Failed deploys persist until resolved. Successful deploys fade after 15 minutes.

## How It Works

1. A single GitHub GraphQL call fetches all open + recently merged PRs across the org
2. For each merged PR, a REST call checks workflow run status
3. Everything renders with ANSI colors, OSC 8 hyperlinks, and responsive column layout
4. Watch mode uses the terminal's alternate screen buffer for a clean full-screen experience

## Configuration

All tunables are constants at the top of the script — no config files needed:

- `POLL_SECONDS` — Polling interval in watch mode (default: `60`)
- `DEPLOY_FADE_SECONDS` — How long successful deploys stay visible (default: `900`)
- `MERGED_LOOKBACK_HOURS` — How far back to search for merged PRs (default: `4`)
- `TWO_COL_MIN_WIDTH` — Minimum terminal width for 2-column layout (default: `100`)

## Contributing

- Star this repo if you find it useful!
- [Open an issue](https://github.com/logfoxai/open-prs/issues) for bugs or feature requests
- PRs welcome against `main`

## License

[MIT](LICENSE)

---

<div align="center">

### Built by the team behind [Logfox](https://aeroview.io)

**Stop digging through logs. Start finding bugs.**<br>
AI-powered log monitoring that detects issues before your users do.

[**Try the free beta →**](https://app.aeroview.io)

</div>
