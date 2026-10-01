# Examples

Runnable bot templates. Each is a standalone script.

| File | What it shows |
|------|---------------|
| echo_bot.py | Simplest possible bot. |
| menu_bot.py | Inline keyboards and callback queries. |
| scene_bot.py | Multi-step signup flow with FSM. |
| middleware_bot.py | Logging and rate limiting. |
| webhook_bot.py | Webhook deployment with FastAPI. |

Run any example:

    export WIZARDGRAM_TOKEN="your_token_here"
    python examples/echo_bot.py