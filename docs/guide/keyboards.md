# Keyboards

Use fluent builders to produce Telegram reply markup dictionaries.

```python
keyboard = (
	wizardgram.Keyboard.inline()
	.button("Confirm", callback_data="confirm")
	.button("Cancel", callback_data="cancel")
	.build()
)
await ctx.reply("Continue?", reply_markup=keyboard)
```