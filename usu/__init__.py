import uvloop

uvloop.install()

import io
from contextlib import redirect_stdout
import asyncio
import logging
import functools
import os
import re
from aiohttp import ClientSession
from pytgcalls import PyTgCalls
from pytgcalls import filters as fl
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.handlers import CallbackQueryHandler, MessageHandler
from pyrogram.types import Message
from pyromod import listen
from rich.logging import RichHandler
from usu.config import *
import sys



class ConnectionHandler(logging.Handler):
    def emit(self, record):
        for X in ["OSError", "TimeoutError"]:
            if X in record.getMessage():
                os.system(f"kill -9 {os.getpid()} && python3 -m usu")

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

formatter = logging.Formatter("[%(levelname)s] - %(name)s - %(message)s", "%d-%b %H:%M")
stream_handler = logging.StreamHandler()

stream_handler.setFormatter(formatter)
connection_handler = ConnectionHandler()

logger.addHandler(stream_handler)
logger.addHandler(connection_handler)
logging.getLogger("pytgcalls").setLevel(logging.WARNING)



class UsuInti(Client):
    _ubot = {}
    _prefix = {}
    _translate = {}
    peer = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def optimize(self, func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        return wrapper

    def set_prefix(self, user_id, prefix):
        self._prefix[user_id] = prefix

    async def get_prefix(self, user_id):
        return self._prefix.get(user_id, ["."])

    def cmd_prefix(self, cmd):
        command_re = re.compile(r"([\"'])(.*?)(?<!\\)\1|(\S+)")

        async def func(_, client, message):
            if message.text:
                text = message.text.strip().encode("utf-8").decode("utf-8")
                username = client.me.username or ""
                prefixes = await self.get_prefix(client.me.id)

                if not text:
                    return False

                for prefix in prefixes:
                    if not text.startswith(prefix):
                        continue

                    without_prefix = text[len(prefix):]

                    for command in cmd.split("|"):
                        if not re.match(
                            rf"^(?:{command}(?:@?{username})?)(?:\s|$)",
                            without_prefix,
                            flags=re.IGNORECASE | re.UNICODE,
                        ):
                            continue

                        without_command = re.sub(
                            rf"{command}(?:@?{username})?\s?",
                            "",
                            without_prefix,
                            count=1,
                            flags=re.IGNORECASE | re.UNICODE,
                        )
                        message.command = [command] + [
                            re.sub(r"\\([\"'])", r"\1", m.group(2) or m.group(3) or "")
                            for m in command_re.finditer(without_command)
                        ]

                        return True

                return False

        return filters.create(func)


class Bot(UsuInti):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.usu = Client(name="assistant", in_memory=True, api_id=API_ID, api_hash=API_HASH, session_string=str(STRING))
        self.assistant = PyTgCalls(
            self.usu
        )
        self.device_model = DEVICE_NAME
        self.app_version = DEVICE_VERSION

    def on_message(self, filters=None, group=-1):
        def decorator(func):
            optimized_func = self.optimize(func)
            self.add_handler(MessageHandler(optimized_func, filters), group)
            return optimized_func
        return decorator

    def on_callback_query(self, filters=None, group=-1):
        def decorator(func):
            self.add_handler(CallbackQueryHandler(func, filters), group)
            return func

        return decorator

    def usu_stream(self):
        def decorator(func):
            self.assistant.on_update(fl.stream_end)(func)
            return func
        return decorator

    async def start(self):
        await super().start()
        try:
            with redirect_stdout(io.StringIO()):
                await self.assistant.start()
        except Exception as e:
            print(f"Error: {e}")
        if STRING:
            try:
                await self.send_message(LOGS_CHAT, f"<b><i>Bot music aktif!</i></b>")
                await self.usu.send_message(LOGS_CHAT, f"<b><i>Assistant started!</i></b>")
                print(f"Assistant started!")
            except FloodWait as e:
                await asyncio.sleep(e.value)
                try:
                    await self.send_message(LOGS_CHAT, f"<b><i>Bot music aktif!</i></b>")
                    await self.usu.send_message(LOGS_CHAT, f"<b><i>Assistant started!</i></b>")
                    print(f"Assistant started!")
                except:
                    print(
                        f"Silahkan tambahkan assistant dan bot nya ke chat logs dan jangan lupa di adminkan "
                    )
            except:
                print(
                    f"Silahkan tambahkan assistant dan bot nya ke chat logs dan jangan lupa di adminkan "
                )
                sys.exit()
        try:
            await self.set_bot_commands(
                [
                    BotCommand(
                        "start",
                        "mulai bot.",
                    ),
                    BotCommand(
                        "restart",
                        "restart jika bot error.",
                    ),
                    BotCommand(
                        "akses",
                        "menambahkan akses bot (Only Seller).",
                    ),
                    BotCommand(
                        "delakses",
                        "menghapus akses bot (Only Seller).",
                    ),
                    BotCommand(
                        "ping",
                        "cek bot hidup/mati",
                    ),
                    BotCommand(
                        "play",
                        "mainkan audio music",
                    ),
                    BotCommand(
                        "vplay",
                        "mainkan video music",
                    ),
                    BotCommand(
                        "playlist",
                        "daftar music yang di mainkan",
                    ),
                    BotCommand(
                        "end",
                        "hentikan music",
                    ),
                    BotCommand(
                        "skip",
                        "memutar antrian music",
                    ),
                    BotCommand(
                        "resume",
                        "lanjutkan music",
                    ),
                    BotCommand(
                        "pause",
                        "jeda music",
                    ),
                    BotCommand(
                        "all",
                        "mention semua pengguna",
                    ),
                    BotCommand(
                        "stop",
                        "mention semua pengguna",
                    ),
                    BotCommand(
                        "ankes",
                        "on/off",
                    ),
                    BotCommand(
                        "bl",
                        "blacklist kata",
                    ),
                    BotCommand(
                        "unbl",
                        "unblacklist kata",
                    ),
                    BotCommand(
                        "listbl",
                        "melihat daftar kata yang di blacklist",
                    ),
                    BotCommand(
                        "addwl",
                        "tambahkan pengguna ke dalam daftar whitelist",
                    ),
                    BotCommand(
                        "delwl",
                        "hapus pengguna dari daftar whitelist",
                    ),
                    BotCommand(
                        "listwl",
                        "melihat daftar whitelist",
                    ),

                ]
            )
        except Exception as er:
            logger.error(str(er))



class Ubot(UsuInti):
    __module__ = "pyrogram.client"
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.call_py = PyTgCalls(self)
        self.device_model = DEVICE_NAME
        self.app_version = DEVICE_VERSION

    def on_message(self, filters=None, group=-1):
        def decorator(func):
            optimized_func = self.optimize(func)
            for ub in self._ubot.values():
                ub.add_handler(MessageHandler(optimized_func, filters), group)
            return optimized_func
        return decorator

    def usu_stream(self):
        def decorator(func):
            for ub in self._ubot.values():
                ub.call_py.on_update(fl.stream_end)(func)
            return func
        return decorator

    async def start(self):
        await super().start()
        try:
            with redirect_stdout(io.StringIO()):
                await self.call_py.start()
        except Exception as e:
            print(f"Error: {e}")
        handler = await get_pref(self.me.id)
        if handler:
            self._prefix[self.me.id] = handler
        else:
            self._prefix[self.me.id] = ["."]
        self._ubot[self.me.id] = self
        self._translate[self.me.id] = "id"
        print(f"Client - {self.me.id} Started!")



bot = Bot(
    name="bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
    in_memory=True,
    workdir="./usu/",
    plugins=dict(root="usu.core")
)

ubot = Ubot(name="ubot")



from usu.core.database import *
from usu.core.function import *
from usu.core.helpers import *