from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from usu.config import OWNER_ID, PHOTO, USERNAME
from usu import OWNER_ID, bot, get_expired_date, get_two_factor, ubot
from usu import *
from usu.core.helpers.uptime import *


class MSG:     
    def EXP_MSG_UBOT(X):
        return f"""<i><b>Information!</b>
<b>Account:</b> <a href=tg://user?id={X.me.id}>{X.me.first_name} {X.me.last_name or ''}</a>
<b>ID:</b> {X.me.id}
<b>Reason:</b> Userbot anda telah habis! Order?PM @{USERNAME}</i>
"""

    async def PILIHAN():
        usu_time = await usu_alive()
        susers = await get_list_from_vars(bot.me.id, "SAVED_USERS")
        gc = len(list(chat for chat in susers if str(chat).startswith("-100")))
        return f"""<b><i>Halo,
Saya adalah [{bot.me.first_name}]({PHOTO})..!!

Bot Hidup:</i></b> {usu_time}
<i><b>Koneksi Userbot:</b> {len(ubot._ubot)}</i>
<i><b>Koneksi Group:</b> {gc}</i>
"""

    async def START():
        return f"""<b><i>Halo,
Anda sekarang berada di menu [Userbot]({PHOTO})..!!</i></b>
"""


    async def UBOT(count):
        return f"""<i><b>Userbot To</b> <code>{int(count) + 1}/{len(ubot._ubot)}</code>
<b>Account:</b> <a href=tg://user?id={ubot._ubot[tuple(ubot._ubot.keys())[int(count)]].me.id}>{ubot._ubot[tuple(ubot._ubot.keys())[int(count)]].me.first_name} {ubot._ubot[tuple(ubot._ubot.keys())[int(count)]].me.last_name or ''}</a> 
<b>ID:</b> <code>{ubot._ubot[tuple(ubot._ubot.keys())[int(count)]].me.id}</code></i>
"""
