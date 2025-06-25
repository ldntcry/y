import asyncio
from datetime import datetime

from pyrogram.types import InlineKeyboardMarkup
from pytz import timezone

from usu import *
from usu.core.helpers.text import MSG


async def expiredUserbots():
    while True:
        await asyncio.sleep(120)
        for X in tuple(ubot._ubot.values()):
            try:
                time_now = datetime.now(pytz.timezone("Asia/Jakarta"))
                exp_datetime = await db.get_expired_date(X.me.id)
                if exp_datetime is not None and time_now >= exp_datetime:
                    await X.unblock_user(bot.me.username)
                    await db.remove_ubot(X.me.id)
                    await db.remove_all_vars(X.me.id)
                    await db.rem_expired_date(X.me.id)
                    await bot.send_message(
                        X.me.id,
                        MSG.EXP_MSG_UBOT(X),
                    )
                    user_link = f"{X.me.first_name} {X.me.last_name or ''}" 
                    gbt = [
                        [
                            InlineKeyboardButton(
                            user_link,
                            url=f"tg://openmessage?user_id={X.me.id}",
                            ),
                        ],
                    ]
                    for asuu in DEVS:
                        await bot.send_message(
                            asuu,
                            f"<b><i>Information Expired!\nName: {X.me.mention}\nID: {X.me.id}</i></b>",
                            reply_markup=InlineKeyboardMarkup(gbt),
                        )
                    logger.info(f"Client - {X.me.id} - Expired end!")
                    await X.log_out()
                    del ubot._ubot[X.me.id]
            except Exception as e:
                if X.me.id not in DEVS:
                    logger.error(f"Error {e}")
