import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from aiogram.types import Update
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.bot import BotManager
from app.settings import settings
from app.webapp.manager import ConnectionManager

logger = logging.getLogger(__name__)

bot = BotManager()
manager = ConnectionManager()


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncGenerator:  # noqa: ARG001
    await bot.start_bot()
    await bot.bot.set_webhook(
        url=settings.webhook_url,
        allowed_updates=bot.dp.resolve_used_update_types(),
        drop_pending_updates=True,
    )
    yield
    await bot.bot.delete_webhook()


app = FastAPI(lifespan=_lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    logger.info(request)
    return HTMLResponse(
        content=Path("templates/index.html").read_text(encoding="utf-8"),
        status_code=200,
    )


@app.post("/webhook")
async def webhook(request: Request) -> None:
    logger.info("Received webhook request")
    await bot.dp.feed_update(
        bot.bot,
        Update.model_validate(await request.json(), context={"bot": bot.bot}),
    )
    logger.info("Update processed")


@app.websocket("/communicate")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            logger.warning(data)
            await manager.send_personal_message(f"Received:{data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


if __name__ == "__main__":
    uvicorn.run("app.__main__:app", host="127.0.0.1", port=5050, reload=True)
