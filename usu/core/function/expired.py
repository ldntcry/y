import asyncio
from datetime import datetime

from pyrogram.types import InlineKeyboardMarkup
from pytz import timezone

from usu import *


async def expiredUserbots():
    while True:
        for X in tuple(ubot._ubot.values()):
            try:
                time_now = datetime.now(timezone("Asia/Jakarta"))
                time = time_now.strftime("%d %B %Y")
                exp_datetime = await get_expired_date(X.me.id)
                if exp_datetime:
                    exp = exp_datetime.astimezone(timezone("Asia/Jakarta")).strftime("%d %B %Y")
                if time == exp:
                    await X.unblock_user(bot.me.username)
                    await remove_ubot(X.me.id)
                    await remove_all_vars(X.me.id)
                    await rem_expired_date(X.me.id)
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
                    await X.log_out()
                    del ubot._ubot[X.me.id]
            except Exception as e:
                print(f"[Client]: {X.me.id} - Expired end!")
        await asyncio.sleep(60)
