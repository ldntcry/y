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
    data = set()
    while True:
        for usu in list(ubot._ubot.values()):
            try:
                if usu.me.id not in data:
                    data.add(usu.me.id)
            except (AuthKeyUnregistered, RPCError):
                if usu.me.id in data and usu.me.id in ubot._ubot:
                    try:
                        user = await bot.get_users(usu.me.id)
                        if not user.is_deleted:
                            await bot.send_message(usu.me.id, f"<b><i>Sesi userbot anda terlepas, silahkan membuat userbot kembali!</i></b>")
                    except Exception as e:
                        print(e)
                    await remove_ubot(usu.me.id)
                    exp = await get_expired_date(usu.me.id)
                    jakarta_timezone = timezone("Asia/Jakarta")
                    now = datetime.now(jakarta_timezone)
                    expire_date = now + timedelta(days=int(exp))
                    if usu.me.id not in await get_list_from_vars(bot.me.id, "AKSES"):
                        await add_to_vars(bot.me.id, "AKSES", usu.me.id)
                        await set_expired_date(usu.me.id, expire_date)
                    data.discard(usu.me.id)
                    await usu.log_out()
                    del ubot._ubot[usu.me.id]
        await asyncio.sleep(60)