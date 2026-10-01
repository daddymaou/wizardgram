import os

from wizardgram import Bot, Context, Scene, Stage

bot = Bot(token=os.environ["WIZARDGRAM_TOKEN"])


async def ask_name(ctx: Context) -> None:
	if ctx.scene is None:
		return
	ctx.scene.state["name"] = ctx.text or ""
	await ctx.reply("What city are you from?")
	await ctx.scene.next()


async def finish_signup(ctx: Context) -> None:
	if ctx.scene is None:
		return
	name = ctx.scene.state.get("name", "friend")
	await ctx.reply(f"Thanks, {name}. Your signup is complete.")
	await ctx.scene.leave()


stage = Stage([Scene("signup", [ask_name, finish_signup])])
bot.use(stage.middleware())


@bot.command("signup")
async def signup(ctx: Context) -> None:
	if ctx.scene is not None:
		await ctx.scene.enter("signup")
	await ctx.reply("What is your name?")


if __name__ == "__main__":
	bot.run()