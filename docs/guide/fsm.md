# FSM

`Scene` stores a sequence of handlers. `Stage` routes each chat to its
current step; handlers advance with `ctx.scene.next()` or leave with
`ctx.scene.leave()`.

```python
stage = Stage([Scene("signup", [ask_name, ask_city])])
bot.use(stage.middleware())
```