import logging
import os
import time
from collections.abc import Awaitable, Callable

from wizardgram import Bot, Context, Next

logging.basicConfig(level=logging.INFO)
bot = Bot(token=os.environ["WIZARDGRAM_TOKEN"])
last_seen: dict[int, float] = {}


async def rate_limit(ctx: Context, next_: Next) -> None:
	if ctx.chat is not None:
		current = time.monotonic()
		previous = last_seen.get(ctx.chat["id"], 0.0)
		if current - previous < 1.0:
			return
		last_seen[ctx.chat["id"]] = current
	await next_()


@bot.middleware
async def log_updates(ctx: Context, next_: Next) -> None:
	logging.info("update=%s type=%s", ctx.update_id, ctx.update_type)
	await next_()


bot.use(rate_limit)


@bot.hears(r"^(.+)$")
async def echo(ctx: Context) -> None:
	if ctx.text is not None:
		await ctx.reply(ctx.text)


if __name__ == "__main__":
	bot.run()