"""FastAPI webhook example.

Install the optional server packages with `pip install fastapi uvicorn`, then
run `uvicorn examples.webhook_bot:app --host 0.0.0.0 --port 8000`.
"""

import os
from typing import Any

from fastapi import FastAPI, Request

from wizardgram import Bot

bot = Bot(token=os.environ["WIZARDGRAM_TOKEN"])
app = FastAPI()


@app.post("/telegram/webhook")
async def telegram_webhook(request: Request) -> dict[str, bool]:
	return await bot.handle_webhook(request)


@app.on_event("shutdown")
async def shutdown() -> None:
	await bot.close()