# Quickstart

Create a file named `bot.py` and define a minimal bot:

```python
import os

import wizardgram

bot = wizardgram.Bot(token=os.environ["WIZARDGRAM_TOKEN"])


@bot.command("start")
async def start(ctx: wizardgram.Context) -> None:
    await ctx.reply(f"Hello, {ctx.from_user.first_name}!")


@bot.hears(r"^ping$")
async def ping(ctx: wizardgram.Context) -> None:
    await ctx.reply("pong")


if __name__ == "__main__":
    bot.run()
```

Set `WIZARDGRAM_TOKEN` to the token from [@BotFather](https://t.me/BotFather).
Do not put the token directly in the source file or commit it to your repository.

## Run it

### Windows (PowerShell)

```powershell
$env:WIZARDGRAM_TOKEN = "your-telegram-bot-token"
python bot.py
```

### macOS and Linux

```bash
export WIZARDGRAM_TOKEN="your-telegram-bot-token"
python bot.py
```

The bot starts long polling when `bot.run()` is called. Send `/start` or `ping`
to your bot to exercise the handlers.

## Next steps

Continue with the guides for [routing](guide/routing.md), [middleware](guide/middleware.md),
[keyboards](guide/keyboards.md), and [scenes](guide/fsm.md).