# Examples

Runnable bot templates. Run these scripts from the repository root after installing
wizardgram and setting the `WIZARDGRAM_TOKEN` environment variable.

| File | What it shows |
| --- | --- |
| `echo_bot.py` | Simplest possible bot |
| `menu_bot.py` | Inline keyboards and callback queries |
| `scene_bot.py` | Multi-step signup flow with FSM |
| `middleware_bot.py` | Logging and rate limiting |
| `webhook_bot.py` | Webhook deployment with FastAPI |

## Run an example

### Windows (PowerShell)

```powershell
$env:WIZARDGRAM_TOKEN = "your-telegram-bot-token"
python examples/echo_bot.py
```

### macOS and Linux

```bash
export WIZARDGRAM_TOKEN="your-telegram-bot-token"
python examples/echo_bot.py
```

## Webhook example

The webhook example additionally requires FastAPI and Uvicorn:

```bash
python -m pip install fastapi uvicorn
uvicorn examples.webhook_bot:app --host 0.0.0.0 --port 8000
```

The default FSM state store is in-memory. Scene state is lost when the bot process
restarts.