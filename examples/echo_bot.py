import os

from wizardgram import Bot, Context

bot = Bot(token=os.environ["WIZARDGRAM_TOKEN"])


@bot.command("start")
async def start(ctx: Context) -> None:
	await ctx.reply("Send me a message and I will echo it.")


@bot.hears(r"^(.+)$")
async def echo(ctx: Context) -> None:
	if ctx.text is not None:
		await ctx.reply(ctx.text)


if __name__ == "__main__":
	bot.run()