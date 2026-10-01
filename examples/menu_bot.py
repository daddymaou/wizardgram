import os

from wizardgram import Bot, Context, Keyboard

bot = Bot(token=os.environ["WIZARDGRAM_TOKEN"])


@bot.command("start")
async def start(ctx: Context) -> None:
	keyboard = (
		Keyboard.inline()
		.button("Confirm", callback_data="confirm")
		.button("Cancel", callback_data="cancel")
		.build()
	)
	await ctx.reply("Choose an option:", reply_markup=keyboard)


@bot.action(r"^(confirm|cancel)$")
async def choose(ctx: Context) -> None:
	if ctx.match is not None:
		await ctx.answer_callback_query(ctx.match.group(1).title())
		await ctx.edit_text(f"{ctx.match.group(1).title()}ed")


if __name__ == "__main__":
	bot.run()