import json
import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from aiogram.types import Update
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.bot import BotManager
from app.settings import settings
from app.webapp.api import (
    SNewChat,
    create_new_chat,
    get_ai_models,
    get_app_chats,
    get_chat,
    gpt_request,
    remove_chat,
)
from app.webapp.manager import ConnectionManager
from app.webapp.md_format import format_code

logger = logging.getLogger(__name__)

bot = BotManager()
manager = ConnectionManager()
templates = Jinja2Templates(directory="templates")


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
    logger.info(await request.body())
    return HTMLResponse(
        content=Path("templates/index.html").read_text(encoding="utf-8"),
        status_code=200,
    )


@app.get("/chats")
async def chats(request: Request, user_id: int) -> JSONResponse:  # noqa: ARG001
    return JSONResponse(
        [chat.model_dump(by_alias=True) for chat in await get_app_chats(user_id)]
    )


@app.get("/chats/{chat_id}")
async def chat_request(request: Request, chat_id: int) -> JSONResponse:  # noqa: ARG001
    chat = await get_chat(chat_id)
    for message in chat.messages:
        message.content = format_code(message.content)
    return JSONResponse(chat.model_dump(by_alias=True))


@app.delete("/chats/{chat_id}")
async def delete_chat(request: Request, chat_id: int) -> JSONResponse:  # noqa: ARG001
    await remove_chat(chat_id)
    return JSONResponse({"success": True})


@app.get("/ai_models")
async def ai_models(request: Request) -> JSONResponse:  # noqa: ARG001
    return JSONResponse([ai_model.model_dump() for ai_model in await get_ai_models()])


@app.post("/new_chat")
async def new_chat(request: Request, new_chat: SNewChat) -> JSONResponse:
    logger.info(await request.body())
    chat = await create_new_chat(new_chat)
    return JSONResponse(chat.model_dump(by_alias=True))


@app.post("/webhook")
async def webhook(request: Request) -> None:
    logger.info("Received webhook request")
    await bot.dp.feed_update(
        bot.bot,
        Update.model_validate(await request.json(), context={"bot": bot.bot}),
    )
    logger.info("Update processed")


@app.websocket("/communicate/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: int):
    logger.info(chat_id)
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            logger.warning(data)
            resp = await gpt_request(chat_id, json.loads(data)["text"])
            await manager.send_personal_message(
                json.dumps({"text": format_code(resp)}), websocket
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket)


if __name__ == "__main__":
    uvicorn.run("app.__main__:app", host="127.0.0.1", port=5050, reload=True)
