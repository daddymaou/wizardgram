# wizardgram

**An async Telegram bot framework for Python.**

Build Telegram bots with async handlers, middleware, regex routing, inline keyboards,
and multi-step scenes. wizardgram supports Python 3.10 and newer. Its API coverage
page distinguishes methods verified by tests from methods currently inferred.

[![PyPI](https://img.shields.io/pypi/v/wizardgram)](https://pypi.org/project/wizardgram/)
[![Python](https://img.shields.io/pypi/pyversions/wizardgram)](https://pypi.org/project/wizardgram/)
[![License](https://img.shields.io/pypi/l/wizardgram)](LICENSE)
[![CI](https://github.com/daddymaou/wizardgram/actions/workflows/test.yml/badge.svg)](https://github.com/daddymaou/wizardgram/actions/workflows/test.yml)
[![Ruff](https://img.shields.io/badge/lint-Ruff-d7ff64)](https://github.com/astral-sh/ruff)

 [Quickstart](#quickstart) · [Features](#features) · [Examples](#examples) · [Documentation](docs/index.md) · [Contributing](CONTRIBUTING.md)

## Installation

```bash
pip install wizardgram
```

Requires Python 3.10 or newer. The package installs its runtime dependencies
automatically. See the [installation guide](docs/installation.md) for virtual
environment setup and development extras.

## Quickstart

Create a bot with your Telegram token supplied through an environment variable:

```python
import os

import wizardgram

bot = wizardgram.Bot(token=os.environ["WIZARDGRAM_TOKEN"])


@bot.command("start")
async def start(ctx: wizardgram.Context) -> None:
    await ctx.reply("Hello!")


if __name__ == "__main__":
    bot.run()
```

Set `WIZARDGRAM_TOKEN` before running your bot.
    Set `WIZARDGRAM_TOKEN` in your shell before running the script. In PowerShell:

    ```powershell
    $env:WIZARDGRAM_TOKEN = "your-telegram-bot-token"
    python bot.py
    ```

    On macOS or Linux:

    ```bash
    export WIZARDGRAM_TOKEN="your-telegram-bot-token"
    python bot.py
    ```

    Keep the token private; do not commit it to source control. The
    [quickstart guide](docs/quickstart.md) walks through a runnable bot.
## Features

### Middleware
    - **Polling:** run a bot using Telegram long polling with `bot.run()`.
    - **Routing:** register command, text-pattern, callback-data, and update handlers.
    - **Context helpers:** reply, edit messages, answer callback queries, and send media.
    - **Middleware:** compose async processing around each update.
    - **Keyboards:** build inline and reply keyboards with a fluent API.
    - **Scenes:** implement multi-step flows. The default state store is in-memory and
      does not persist when the process restarts.
    - **Webhooks:** integrate `handle_webhook()` with an async web framework.
    - **Testing:** simulate updates with `TestBot` and the `Updates` helpers.
## Examples

| File | Description | Run |
    Runnable scripts are in [`examples/`](examples/README.md):

    - `echo_bot.py` demonstrates command and text handlers.
    - `menu_bot.py` demonstrates inline keyboards and callback queries.
    - `scene_bot.py` demonstrates a multi-step flow.
    - `middleware_bot.py` demonstrates logging and rate limiting.
    - `webhook_bot.py` demonstrates a FastAPI webhook endpoint; install `fastapi` and
      `uvicorn` separately to run it.
## Coverage Confidence
    See [examples and run instructions](docs/examples.md). Set `WIZARDGRAM_TOKEN`
    before launching any bot example.

    ## Bot API Coverage
| Area | Confidence | How it was verified |
|---|---|---|
| Core send methods | Verified | Included in the bundled method status table. |
    | Core send methods | Verified | Listed in the bundled method status table. |
    | Update polling | Verified | Listed in the bundled method status table. |
    | Webhook methods | Verified | Listed in the bundled method status table. |
    | Callback queries | Verified | Listed in the bundled method status table. |
    | Chat administration | Verified | Listed in the bundled method status table. |
    | Multipart uploads | Inferred | Exercised with mocked HTTP requests. |

    Use the [`wizardgram check`](docs/guide/coverage.md) command or see the
    [coverage guide](docs/guide/coverage.md) for details.
## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and pull request guidance.

## License

Apache-2.0. See [LICENSE](LICENSE).