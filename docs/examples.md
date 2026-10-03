# Examples

The repository's [`examples/` directory](https://github.com/daddymaou/wizardgram/tree/main/examples)
contains runnable bot scripts:

| Script | Demonstrates |
|---|---|
| `echo_bot.py` | Commands and text-pattern handlers |
| `menu_bot.py` | Inline keyboards and callback queries |
| `scene_bot.py` | A multi-step signup scene |
| `middleware_bot.py` | Logging and rate limiting middleware |
| `webhook_bot.py` | A webhook endpoint using FastAPI |

Run commands from the repository root. Set `WIZARDGRAM_TOKEN` first.

=== "Windows (PowerShell)"

	```powershell
	$env:WIZARDGRAM_TOKEN = "your-telegram-bot-token"
	python examples/echo_bot.py
	```

=== "macOS and Linux"

	```bash
	export WIZARDGRAM_TOKEN="your-telegram-bot-token"
	python examples/echo_bot.py
	```

Replace `echo_bot.py` with another polling example as needed. The webhook example
requires additional packages and an externally reachable HTTPS webhook URL:

```bash
python -m pip install fastapi uvicorn
uvicorn examples.webhook_bot:app --host 0.0.0.0 --port 8000
```

See [`examples/README.md`](https://github.com/daddymaou/wizardgram/blob/main/examples/README.md)
for the example list.