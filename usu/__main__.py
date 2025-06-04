import asyncio
import random
from pyrogram import idle
from usu import *
from usu.core.helpers.help_usu import tombol_anak
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


async def start_ubot():
    for data in await get_userbots():
        try:
            ubot_ = Ubot(**data)
            await ubot_.start()
            try:
                for auto in AUTO_JOIN:
                    await ubot_.join_chat(auto)
            except Exception as e:
                pass
        except Exception as e:
            pass
    print(f"Successfully started {len(ubot._ubot)} client!")
    await asyncio.sleep(2)

async def bots():
    print(f"Database load: {DATABASE}.db")
    print(f"------------------------------")
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
            print(f"Silahkan /start @{bot.me.username} terlebih dahulu di semua akun DEVS!")
            sys.exit()
    print(f"------------------------------")
    print(f"Bot - Running!")


async def stopped():
    await bot.stop()

async def main():
    await bots()
    await start_ubot()
    await loaded()


if __name__ == "__main__":
    aiorun.run(main(), loop=bot.loop, shutdown_callback=stopped())