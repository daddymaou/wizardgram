# Routing

Register handlers with decorators or direct calls. Commands match at the
beginning of a message, while `hears` and `action` expose a regex match on
`ctx.match`.

```python
@bot.command("start")
async def start(ctx):
	await ctx.reply("Welcome")

@bot.action(r"^item:(\d+)$")
async def item(ctx):
	await ctx.answer_callback_query(ctx.match.group(1))
```