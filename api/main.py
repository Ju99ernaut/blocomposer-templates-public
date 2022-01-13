import os
import uvicorn

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from routes import templates, assets, users, blocks, bookmarks, comments, newsletter

import config
import data

from constants import API_TAGS_METADATA

config.parse_args()
app = FastAPI(
    title="Blocomposer API",
    description="Public API for blocomposer templates",
    version="1.0.0",
    openapi_tags=API_TAGS_METADATA,
)

if os.getenv("WHITELIST_ORIGINS"):
    allow_origins = os.getenv("WHITELIST_ORIGINS").split(",")
else:
    allow_origins = [
        "http://localhost:8080/",
        "http://localhost:8080",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(templates.router)
app.include_router(assets.router)
app.include_router(blocks.router)
app.include_router(bookmarks.router)
app.include_router(comments.router)
app.include_router(newsletter.router)


@app.get("/")
async def root():
    return {
        "docs": "api documentation at /docs or /redoc",
    }


@app.websocket("/live")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        await websocket.send_json(data)


if __name__ == "__main__":
    data.setup()
    uvicorn.run(
        "main:app",
        host=config.CONFIG.host,
        port=int(config.CONFIG.port),
        reload=bool(config.CONFIG.reload),
    )
