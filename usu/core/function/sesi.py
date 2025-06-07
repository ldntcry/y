import asyncio
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from pytz import timezone
from pyrogram.errors import AuthKeyUnregistered, RPCError, InputUserDeactivated
from pyrogram.types import InlineKeyboardMarkup
from pyrogram import Client, errors
import pyrogram 
from usu import *


async def check_session():
    while True:
        await asyncio.sleep(60)
        for usu in list(ubot._ubot.values()):
            try:
                await usu.get_me()
            except (AuthKeyUnregistered, RPCError) as e:
                try:
                    user = await bot.get_users(usu.me.id)
                    if not user.is_deleted:
                        await bot.send_message(usu.me.id, f"<b><i>Sesi userbot anda terlepas, silahkan membuat userbot kembali!</i></b>")
                except Exception as e:
                    pass
                await db.remove_ubot(usu.me.id)
                if usu.me.id not in await db.get_list_from_vars(bot.me.id, "AKSES"):
                    await db.add_to_vars(bot.me.id, "AKSES", usu.me.id)
                await usu.log_out()
                del ubot._ubot[usu.me.id]