# wizardgram

**Async Telegram bot framework for Python.**

Works with Python 3.10+. Tracks the current Bot API and documents what's verified.

[![PyPI](https://img.shields.io/pypi/v/wizardgram)](https://pypi.org/project/wizardgram/)
[![Python](https://img.shields.io/pypi/pyversions/wizardgram)](https://pypi.org/project/wizardgram/)
[![License](https://img.shields.io/pypi/l/wizardgram)](LICENSE)
[![CI](https://github.com/daddymaou/wizardgram/actions/workflows/test.yml/badge.svg)](https://github.com/daddymaou/wizardgram/actions/workflows/test.yml)
[![Ruff](https://img.shields.io/badge/lint-Ruff-d7ff64)](https://github.com/astral-sh/ruff)

Installation · [Quickstart](#quickstart) · [Features](#features) · [Examples](#examples) · [Docs](docs/index.md) · [Contributing](CONTRIBUTING.md)

## Installation

```bash
pip install wizardgram
```

## Quickstart

```python
import wizardgram

bot = wizardgram.Bot(token="YOUR_BOT_TOKEN")


@bot.command("start")
async def start(ctx: wizardgram.Context) -> None:
    await ctx.reply("Hello!")


if __name__ == "__main__":
    bot.run()
```

Set `WIZARDGRAM_TOKEN` before running your bot.

## Features

### Middleware

```python
async def logging_middleware(ctx, next_):
    print(ctx.update_type)
    await next_()


bot.use(logging_middleware)
```

### Bot API Coverage

```python
from wizardgram import status

print(status("sendMessage").value)
```

### FSM

```python
from wizardgram import Scene, Stage

stage = Stage([Scene("signup", [collect_name, collect_city])])
bot.use(stage.middleware())
```

### Keyboards

```python
from wizardgram import Keyboard

keyboard = Keyboard.inline().button("Confirm", callback_data="confirm").build()
```

### Webhooks

```python
async def telegram_webhook(request):
    return await bot.handle_webhook(request)
```

### File Uploads

```python
@bot.command("photo")
async def photo(ctx):
    await ctx.reply_with_photo("photo.jpg", caption="Attached")
```

## Examples

| File | Description | Run |
|---|---|---|
| `echo_bot.py` | Echoes incoming text. | `WIZARDGRAM_TOKEN=... python examples/echo_bot.py` |
| `menu_bot.py` | Inline Confirm/Cancel keyboard. | `WIZARDGRAM_TOKEN=... python examples/menu_bot.py` |
| `scene_bot.py` | Two-step signup scene. | `WIZARDGRAM_TOKEN=... python examples/scene_bot.py` |
| `middleware_bot.py` | Logging and rate limiting. | `WIZARDGRAM_TOKEN=... python examples/middleware_bot.py` |
| `webhook_bot.py` | FastAPI webhook endpoint. | `uvicorn examples.webhook_bot:app` |

## Coverage Confidence

| Area | Confidence | How it was verified |
|---|---|---|
| Core send methods | Verified | Included in the bundled method status table. |
| Update polling | Verified | Included in the bundled method status table. |
| Webhook methods | Verified | Included in the bundled method status table. |
| Callback queries | Verified | Included in the bundled method status table. |
| Chat administration | Verified | Included in the bundled method status table. |
| Multipart uploads | Inferred | Exercised with mocked HTTP requests. |

## Project Layout

```text
src/wizardgram/
    bot.py
    context.py
    coverage.py
    errors.py
    fsm.py
    keyboard.py
    middleware.py
    router.py
    testing.py
    transport.py
    types.py
examples/
    echo_bot.py
    menu_bot.py
    middleware_bot.py
    scene_bot.py
    webhook_bot.py
```

## Star History

<div align="center">

[![Star History Chart](https://api.star-history.com/svg?repos=daddymaou/wizardgram&type=Date)](https://star-history.com/#daddymaou/wizardgram&Date)

</div>

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and pull request guidance.

## License

Apache-2.0. See [LICENSE](LICENSE).