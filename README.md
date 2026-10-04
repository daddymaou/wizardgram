<h1 align="center">wizardgram</h1>

<p align="center">
  <strong>Async Telegram bot framework for Python.</strong><br>
  Routing, middleware, scenes, keyboards, webhooks, and a built-in test harness,<br>
  with a public record of which Bot API methods are verified.
</p>

<p align="center">
  <a href="https://pypi.org/project/wizardgram/"><img alt="PyPI" src="https://img.shields.io/pypi/v/wizardgram"></a>
  <a href="https://pypi.org/project/wizardgram/"><img alt="Python versions" src="https://img.shields.io/pypi/pyversions/wizardgram"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/pypi/l/wizardgram"></a>
  <a href="https://github.com/daddymaou/wizardgram/actions/workflows/test.yml"><img alt="CI" src="https://github.com/daddymaou/wizardgram/actions/workflows/test.yml/badge.svg"></a>
  <a href="https://github.com/astral-sh/ruff"><img alt="Ruff" src="https://img.shields.io/badge/lint-Ruff-d7ff64"></a>
  <a href="https://github.com/daddymaou/wizardgram/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/daddymaou/wizardgram?style=flat&logo=github"></a>
</p>

<p align="center">
  <a href="#installation">Installation</a> ·
  <a href="#quickstart">Quickstart</a> ·
  <a href="#features">Features</a> ·
  <a href="#testing-your-bot">Testing</a> ·
  <a href="#examples">Examples</a> ·
  <a href="docs/index.md">Docs</a> ·
  <a href="CONTRIBUTING.md">Contributing</a>
</p>

---

## Why wizardgram

- **Async handlers.** Every handler is a plain `async def` that receives a `Context`.
- **Middleware at the core.** Routing, scenes, logging, and rate limiting are all middleware, so they compose the same way.
- **Typed.** The package ships type hints (`py.typed`) and is checked with `mypy --strict`.
- **Testable.** `TestBot` and `Updates` let you simulate updates and assert on replies without touching the network.
- **Honest about coverage.** A bundled table records the verification status of each tracked Bot API method.
- **Light.** The only runtime dependencies are `httpx` and `typing-extensions`.

> **Status:** alpha (`0.1.0`). The API may change between minor versions. See the [changelog](CHANGELOG.md).

## Installation

```bash
pip install wizardgram
```

Requires Python 3.10 or newer. See the [installation guide](docs/installation.md) for virtual environments and development extras.

## Quickstart

1. Create a bot with [@BotFather](https://t.me/BotFather) (send `/newbot`) and copy the token.
2. Export the token. Keep it out of source control.

   ```bash
   # macOS / Linux
   export WIZARDGRAM_TOKEN="123456:ABC-your-token"
   ```

   ```powershell
   # Windows PowerShell
   $env:WIZARDGRAM_TOKEN = "123456:ABC-your-token"
   ```

3. Save this as `bot.py` and run `python bot.py`:

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

4. Open your bot in Telegram and send `/start`.

`bot.run()` uses long polling. It keeps polling after network or Telegram errors and backs off between retries, up to 30 seconds.

## Features

### Routing

Four decorators cover the common cases. Each one is also available as a direct call: `bot.command("help", handler)`.

```python
@bot.command("help")              # /help
async def help_(ctx): ...

@bot.hears(r"(?i)^ping$")         # text matching a regex; ctx.match holds the match
async def ping(ctx): await ctx.reply("pong")

@bot.action(r"^vote:(\d+)$")      # callback data matching a regex
async def vote(ctx): ...

@bot.on("edited_message")         # any Telegram update type
async def edited(ctx): ...
```

Handlers run in registration order. The first one that matches handles the update.

### Context

A `Context` wraps each update and exposes what you usually need: `ctx.text`, `ctx.chat`, `ctx.from_user`, `ctx.match`, `ctx.callback_query`, `ctx.update_type`, and `ctx.scene`.

| Helper | What it does |
| --- | --- |
| `reply(text, **kwargs)` | Send a message to the current chat |
| `reply_with_keyboard(text, keyboard)` | Send a message with a keyboard attached |
| `reply_with_photo(...)`, `reply_with_document(...)` | Upload media (file path, bytes, or file object) |
| `edit_text(...)`, `edit_caption(...)`, `edit_reply_markup(...)` | Edit the message that triggered the update |
| `delete_message()` | Delete a message |
| `answer_callback_query(text)` | Acknowledge an inline button press |
| `send_chat_action("typing")` | Show a typing or upload indicator |

### Middleware

Middleware wraps every update. Do work before and after `await next_()`, or skip it to stop the update.

```python
import logging
from wizardgram import Context, Next

@bot.middleware
async def log_updates(ctx: Context, next_: Next) -> None:
    logging.info("update=%s type=%s", ctx.update_id, ctx.update_type)
    await next_()
```

You can also register with `bot.use(fn)`, which returns the bot so calls can be chained. An exception raised inside middleware is logged and the chain continues, so one faulty middleware does not take the bot down.

### Keyboards

```python
from wizardgram import Keyboard

# Inline keyboard
keyboard = (
    Keyboard.inline()
    .button("Confirm", callback_data="confirm")
    .button("Cancel", callback_data="cancel")
    .row()
    .button("Docs", url="https://github.com/daddymaou/wizardgram")
    .build()
)
await ctx.reply("Choose:", reply_markup=keyboard)

# Reply keyboard
keyboard = Keyboard.reply().button("Share contact", request_contact=True).resize().one_time().build()
```

### Scenes (multi-step flows)

A `Scene` is an ordered list of step handlers. A `Stage` keeps track of which step each chat is on. Steps share data through `ctx.scene.state`.

```python
from wizardgram import Context, Scene, Stage


async def ask_name(ctx: Context) -> None:
    ctx.scene.state["name"] = ctx.text or ""
    await ctx.reply("What city are you from?")
    await ctx.scene.next()


async def finish(ctx: Context) -> None:
    await ctx.reply(f"Thanks, {ctx.scene.state['name']}. You're signed up.")
    await ctx.scene.leave()


bot.use(Stage([Scene("signup", [ask_name, finish])]).middleware())


@bot.command("signup")
async def signup(ctx: Context) -> None:
    await ctx.scene.enter("signup")
    await ctx.reply("What is your name?")
```

> **Note:** scene state is held by `MemoryStateStore`, so it is **not persistent**. Progress is lost when the process restarts.

### Webhooks

`handle_webhook` accepts any request object with an async `json()` method. Here it is with FastAPI:

```python
import os
from fastapi import FastAPI, Request
from wizardgram import Bot

bot = Bot(token=os.environ["WIZARDGRAM_TOKEN"])
app = FastAPI()


@app.post("/telegram/webhook")
async def telegram_webhook(request: Request) -> dict[str, bool]:
    return await bot.handle_webhook(request)
```

Register the URL once with `await bot.set_webhook("https://example.com/telegram/webhook")`, and remove it with `await bot.delete_webhook()`. Call `await bot.close()` on shutdown. Run the full example with `uvicorn examples.webhook_bot:app` (install `fastapi` and `uvicorn` separately).

### File uploads

```python
@bot.command("photo")
async def photo(ctx: Context) -> None:
    await ctx.reply_with_photo("photo.jpg", caption="Attached")
```

Files can be a path, raw `bytes`, a `(filename, bytes)` tuple, or an open binary file.

### Reliability

- **Flood control.** On HTTP 429 the transport waits for the `retry_after` Telegram sends and retries, up to `max_retries` (default 3).
- **Per-chat throttling.** `Bot(token, min_interval_ms=1000)` enforces a minimum gap between API calls to the same chat.
- **Timeouts.** `Bot(token, timeout=30.0)` sets the request timeout.
- **Clear errors.** `TelegramError` (with `error_code`, `description`, `retry_after`) and `NetworkError` both inherit from `WizardgramError`.

```python
from wizardgram import TelegramError

try:
    await ctx.reply("hi")
except TelegramError as exc:
    print(exc.error_code, exc.description)
```

## Testing your bot

`TestBot` records outgoing API calls and never opens a network connection, so handler tests run fast and offline.

```python
from wizardgram import Context, TestBot, Updates


async def test_hello() -> None:
    bot = TestBot()

    @bot.command("hello")
    async def hello(ctx: Context) -> None:
        await ctx.reply("world")

    reply = await bot.simulate(Updates.command("hello"))

    assert reply is not None
    assert reply.text == "world"
```

`Updates.text(...)`, `Updates.command(...)`, `Updates.callback(...)`, and `Updates.photo(...)` build realistic updates. `bot.calls` lists every API method your handler invoked, along with its parameters.

## Bot API coverage

wizardgram keeps a table of the Bot API methods it tracks and how each was checked. At `0.1.0` it holds 34 methods, all marked **verified**, including `sendMessage`, `sendPhoto`, `editMessageText`, `setWebhook`, `banChatMember`, and `answerCallbackQuery`. Unknown method names report `unverified`.

```python
from wizardgram import status

print(status("sendMessage").value)   # "verified"
```

Print the whole table from the command line:

```bash
wizardgram
```

| Area | Confidence | How it was verified |
| --- | --- | --- |
| Core send methods | Verified | Listed in the bundled method status table |
| Update polling | Verified | Listed in the bundled method status table |
| Webhook methods | Verified | Listed in the bundled method status table |
| Callback queries | Verified | Listed in the bundled method status table |
| Chat administration | Verified | Listed in the bundled method status table |
| Multipart uploads | Inferred | Exercised with mocked HTTP requests |

See the [coverage guide](docs/guide/coverage.md) for details.

## Examples

Set `WIZARDGRAM_TOKEN`, then run any example.

| File | What it shows | Run |
| --- | --- | --- |
| [`echo_bot.py`](examples/echo_bot.py) | Command and text handlers | `python examples/echo_bot.py` |
| [`menu_bot.py`](examples/menu_bot.py) | Inline keyboard and callback queries | `python examples/menu_bot.py` |
| [`scene_bot.py`](examples/scene_bot.py) | Two-step signup scene | `python examples/scene_bot.py` |
| [`middleware_bot.py`](examples/middleware_bot.py) | Logging and rate limiting | `python examples/middleware_bot.py` |
| [`webhook_bot.py`](examples/webhook_bot.py) | FastAPI webhook endpoint | `uvicorn examples.webhook_bot:app` |

## Project layout

```
src/wizardgram/
    bot.py          Bot: polling, webhooks, handler registration
    context.py      Context: per-update reply and edit helpers
    router.py       command / hears / action / on routing
    middleware.py   Middleware chain
    fsm.py          Scene, Stage, MemoryStateStore
    keyboard.py     Inline and reply keyboard builders
    transport.py    httpx transport: retries, flood control, uploads
    coverage.py     Bot API verification table and CLI
    testing.py      TestBot, Updates, MockMessage
    errors.py       WizardgramError, TelegramError, NetworkError
    types.py        Telegram TypedDicts
examples/           Runnable example bots
tests/              pytest suite
docs/               MkDocs documentation
```

## Documentation

Guides live in [`docs/`](docs/index.md): [installation](docs/installation.md), [quickstart](docs/quickstart.md), and guides for [routing](docs/guide/routing.md), [context](docs/guide/context.md), [middleware](docs/guide/middleware.md), [keyboards](docs/guide/keyboards.md), [scenes](docs/guide/fsm.md), and [coverage](docs/guide/coverage.md).

## Contributing

Contributions are welcome. Open a branch, make your change, and send a pull request.

```bash
git clone https://github.com/daddymaou/wizardgram.git
cd wizardgram
pip install -e ".[dev]"

ruff check . && ruff format --check . && mypy src/wizardgram && pytest
```

Read [CONTRIBUTING.md](CONTRIBUTING.md) and the [Code of Conduct](CODE_OF_CONDUCT.md) first. To report a security issue, see [SECURITY.md](SECURITY.md).

## Support the project

If wizardgram saves you time, **a star helps other developers find it**.

<p align="center">
  <a href="https://github.com/daddymaou/wizardgram/stargazers">⭐ Star wizardgram on GitHub</a>
</p>

### Star history

<a href="https://star-history.com/#daddymaou/wizardgram&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=daddymaou/wizardgram&type=Date&theme=dark">
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=daddymaou/wizardgram&type=Date">
    <img alt="Star history chart for wizardgram" src="https://api.star-history.com/svg?repos=daddymaou/wizardgram&type=Date">
  </picture>
</a>

## Citation

If you use wizardgram in research, cite it using [`CITATION.cff`](CITATION.cff).

## License

Apache-2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).