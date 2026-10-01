# Quickstart

```python
import wizardgram

bot = wizardgram.Bot(token="YOUR_BOT_TOKEN")


@bot.command("start")
async def start(ctx: wizardgram.Context):
    await ctx.reply(f"Hello, {ctx.from_user.first_name}!")


@bot.hears(r"^ping$")
async def ping(ctx: wizardgram.Context):
    await ctx.reply("pong")


if __name__ == "__main__":
    bot.run()
```

Set `WIZARDGRAM_TOKEN` and run.