# Middleware

Middleware receives a `Context` and an asynchronous `next_` function. Calling
`next_()` continues the chain; returning without calling it stops processing.

```python
async def log_updates(ctx, next_):
	print(ctx.update_id)
	await next_()

bot.use(log_updates)
```