import asyncio
import random
from pyrogram import idle
from usu import *
from usu.core.helpers.help_usu import tombol_anak
from usu.core.database.local import db
from usu.core.helpers.dec import installPeer
import os
import sys
import aiorun

from pyrogram.errors import (AuthKeyDuplicated, AuthKeyUnregistered,
                             SessionRevoked, UserAlreadyParticipant,
                             UserDeactivated, UserDeactivatedBan)
from pytz import timezone
import pytgcalls
import pyrogram




async def auto_reaction_task(client, reactions):
    random_emoji = random.choice(reactions)
    reacted = set()
    try:
        try:
            peer = await client.get_chat(AUTO_REACTION)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            peer = await client.get_chat(AUTO_REACTION)
        except Exception as e:
            pass
        async for message in client.get_chat_history(peer.id, limit=1):
            if client.me.id in reacted:
                continue
            try:
                await message.react(random_emoji)
                reacted.add(client.me.id)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                try:
                    await message.react(random_emoji)
                    reacted.add(client.me.id)
                except Exception as e:
                    pass
            except Exception as e:
                pass
    except Exception as e:
        pass


async def auto_reaction():
    reactions = ["👍", "🤩", "🎉", "😍", "👏", "🔥", "🙈", "💯", "🌚", "😎", "🍓", "🏆", "❤️‍🔥", "⚡", "🙉", "🙊", "👻", "🌭"]
    while True:
        task = []
        for client in ubot._ubot.values():
            task.append(asyncio.create_task(auto_reaction_task(client, reactions)))
        await asyncio.gather(*task)
        await asyncio.sleep(60)

async def start_and_join(ubot_):
    await ubot_.start()
    for auto in AUTO_JOIN:
        await ubot_.join_chat(auto)

async def start_ubot():
    logger.info(f"Database load: {DATABASE}.db")
    for data in await db.get_userbots():
        try:
            ubot_ = Ubot(**data)
            await start_and_join(ubot_)
        except Exception as e:
            pass
    logger.info(f"Successfully started {len(ubot._ubot)} client!")

async def bots():
    try:
        await bot.start()
    except FloodWait as e:
        logger.info(f"FloodWait {e.value} seconds")
        await asyncio.sleep(e.value)
        await bot.start()

async def loaded():
    task = [installPeer(), auto_reaction(), expiredUserbots(), check_session()]
    for tasks in task:
        asyncio.create_task(tasks)
    jumlah_button_usu = sum(len(buttons) for buttons in tombol_anak.values())
    for anjay in DEVS:
        try:
            await bot.send_message(
                anjay,
                f"""<b><i>Userbot Active!</i></b>

<i><b>Module:</b> {jumlah_button_usu}</i>
<i><b>Jumlah Pengguna:</b> {len(ubot._ubot)}</i>
<i><b>Pyrogram:</b> {pyrogram.__version__}</i>
<i><b>Pytgcalls:</b> {pytgcalls.__version__}</i>""")
        except Exception as e:
            logger.info(f"Silahkan /start @{bot.me.username} terlebih dahulu di semua akun DEVS!")
            sys.exit()
    logger.info(f"Bot - Running!")


async def stopped():
    db.close_connection()
    await bot.stop()

async def main():
    await start_ubot()
    await bots()
    await loaded()


if __name__ == "__main__":
    aiorun.run(main(), loop=bot.loop, shutdown_callback=stopped())