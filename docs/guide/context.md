# Context

`Context` wraps one Telegram update. It exposes the update type, message,
user, chat, text, and a mutable `state` dictionary for per-update data.

```python
@bot.hears(r"^hello$")
async def hello(ctx):
	await ctx.reply(f"Hello, {ctx.from_user['first_name']}!")
```