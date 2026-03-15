# `open-prs`

[![CI](https://github.com/logfoxai/open-prs/actions/workflows/ci.yml/badge.svg)](https://github.com/logfoxai/open-prs/actions)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A pretty CLI dashboard for all open PRs across a GitHub org. Includes CI status badges, post-merge deploy tracking, responsive 2-column layout, and clickable PR titles.

**One-shot mode** — quick glance at all open PRs:

```
open-prs myorg
```

**Watch mode** — full-screen dashboard that polls every 5 minutes:

```
open-prs myorg --watch
```

## Features

- **CI status badges** — pass, fail, running, or no CI — at a glance for every PR
- **Post-merge deploy tracking** — merged PRs stay on screen while workflows run; failures persist, successes fade after 15 min
- **Clickable PR titles** — OSC 8 hyperlinks work in iTerm2, VS Code terminal, Ghostty, etc.
- **Responsive 2-column layout** — automatically switches when content overflows the terminal height
- **Watch mode** — full-screen alternate buffer with keyboard controls (`r` refresh, `c` clear merged, `q` quit)
- **Grouped by repo** — PRs organized by repository name

## Requirements

- Python 3.9+
- [GitHub CLI](https://cli.github.com/) (`gh`) — installed and authenticated

## Installation

Copy the script somewhere in your `$PATH`:

```bash
curl -o ~/.local/bin/open-prs https://raw.githubusercontent.com/logfoxai/open-prs/main/open-prs
chmod +x ~/.local/bin/open-prs
```

Or clone and symlink:

```bash
git clone https://github.com/logfoxai/open-prs.git
ln -s "$(pwd)/open-prs/open-prs" ~/.local/bin/open-prs
```

## Usage

```
open-prs <org> [--watch]
```

| Argument   | Description                                              |
|------------|----------------------------------------------------------|
| `<org>`    | GitHub organization name (required)                      |
| `--watch`  | Full-screen polling mode (every 5 min), alias `-w`       |

### Watch mode keyboard shortcuts

| Key | Action                                         |
|-----|------------------------------------------------|
| `r` | Refresh immediately                            |
| `c` | Clear successfully merged/deployed PRs         |
| `q` | Quit (also `Ctrl+C`)                           |

## CI Status Badges

| Badge        | Meaning                                |
|--------------|----------------------------------------|
| `✓ pass`     | All CI checks passed                   |
| `✗ fail`     | One or more checks failed              |
| `● running`  | Checks are in progress                 |
| `no ci`      | No status checks configured            |

## Deploy Status Badges

After a PR is merged, if there are GitHub Actions workflows triggered by the merge:

| Badge          | Meaning                                |
|----------------|----------------------------------------|
| `✓ deployed`   | All workflows completed successfully   |
| `✗ failed`     | One or more workflows failed           |
| `● deploying`  | Workflows are in progress              |
| `◦ queued`     | Workflows are queued/waiting           |

Failed deploys persist on screen indefinitely (until resolved). Successful deploys fade after 15 minutes.

## How It Works

1. Fetches open and recently merged PRs via a single GitHub GraphQL API call
2. For each merged PR, checks workflow run status via the REST API
3. Renders everything with ANSI colors, OSC 8 hyperlinks, and responsive column layout
4. In watch mode, uses the terminal's alternate screen buffer for a clean full-screen experience

## Configuration

All configuration is via constants at the top of the script:

| Constant               | Default   | Description                                      |
|------------------------|-----------|--------------------------------------------------|
| `POLL_SECONDS`         | `300`     | Polling interval in watch mode (seconds)          |
| `DEPLOY_FADE_SECONDS`  | `900`     | How long successful deploys stay visible (seconds) |
| `MERGED_LOOKBACK_HOURS`| `4`       | How far back to search for merged PRs (hours)     |
| `TWO_COL_MIN_WIDTH`    | `100`     | Minimum terminal width for 2-column layout        |

## Contributing

- Star this repo if you like it!
- Submit an [issue](https://github.com/logfoxai/open-prs/issues) for bugs or feature requests
- PRs welcome against `main`

## License

[MIT](LICENSE)

---

<div align="center">

### Built by the team behind [LogFox.ai](https://logfox.ai)

**Stop digging through logs. Start finding bugs.**<br>
AI-powered log monitoring that detects issues before your users do.

[**Try the free beta →**](https://app.logfox.ai)

</div>
