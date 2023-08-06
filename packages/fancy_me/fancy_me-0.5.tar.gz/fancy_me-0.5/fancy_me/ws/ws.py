import json
import logging

from fancy_me.helpers import Message
from fancy_me.middleware import async_middle_ware
from websockets.server import WebSocketServerProtocol

logging.basicConfig()

# 用户目录
user_client = dict()


async def register(user: str, websocket):
    user_client[user] = websocket


async def unregister(user):
    del user_client[user]


async def send(user, data):
    if isinstance(data, Message):
        data = data.message

    await user_client[user].send(data)


class MetaMessage:
    def __init__(self, typed, data):
        self._type = typed
        self._origin_data = data

    @property
    def data(self) -> dict:
        return json.loads(self._origin_data)

    @property
    def user(self) -> str:
        return self.data.get('user')

    @property
    def type(self):
        return self._type


async def parse_protocol(message: str):
    if ">" not in message:
        raise ValueError("格式出错")
    typed, data = message.split(">")
    return MetaMessage(typed=typed, data=data)


async def counter(websocket: WebSocketServerProtocol, path):
    async for message in websocket:
        message = await parse_protocol(message=message)
        await register(message.user, websocket)
        try:
            await async_middle_ware(event_type=message.type, data=message.data)
        finally:
            # await unregister(message.user)
            pass
