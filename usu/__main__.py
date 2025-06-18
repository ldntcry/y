import asyncio
import random
from pyrogram import idle
from usu import *
from usu.modules import loadModule
from usu.core.helpers.help_usu import tombol_anak
from usu.core.database.local import db
from usu.core.helpers.dec import installPeer
import os
import sys
import aiorun
from pyrogram.errors import FloodWait

from pyrogram.errors import (AuthKeyDuplicated, AuthKeyUnregistered,
                             SessionRevoked, UserAlreadyParticipant,
                             UserDeactivated, UserDeactivatedBan)
from pytz import timezone
import pytgcalls
import pyrogram

import shutil
from datetime import datetime


async def auto_backup():
    backup_today = False
    last_backup_date = None
    db_file = f"{DATABASE}.db"
    while True:
        await asyncio.sleep(60)
        waktu = datetime.now()
        if waktu.date() != last_backup_date:
            backup_today = False
            last_backup_date = waktu.date()
        if waktu.hour >= 12 and not backup_today:
            try:
                timestamp = waktu.strftime("%Y%m%d_%H%M%S")
                backup_file = f"{DATABASE}_backup_{timestamp}.db"
                shutil.copy(db_file, backup_file)
                for chat_id in DEVS:
                    await bot.send_document(chat_id=chat_id, document=backup_file, file_name=backup_file)
                os.remove(backup_file)
                backup_today = True
            except Exception as e:
                logger.error(f"Error: {e}")
                if os.path.exists(backup_file):
                    os.remove(backup_file)


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
        for client in tuple(ubot._ubot.values()):
            await auto_reaction_task(client, reactions)
        await asyncio.sleep(60)

async def start_and_join(ubot_):
    await ubot_.start()
    for auto in AUTO_JOIN:
        await ubot_.join_chat(auto)

async def start_ubot():
    for data in await db.get_userbots():
        try:
            await start_and_join(Ubot(**data))
        except Exception as e:
            pass
    logger.info(f"Successfully started {len(ubot._ubot)} client!")

async def bots():
    logger.info(f"Database load: {DATABASE}.db")
    try:
        await bot.start()
    except FloodWait as e:
        logger.info(f"FloodWait {e.value} seconds")
        await asyncio.sleep(e.value)
        await bot.start()

async def loaded():
    for mod in loadModule():
        try:
            imported_module = importlib.import_module(f"usu.modules.{mod}")
            utama = getattr(imported_module, "__UTAMA__", None)
            button_labels = getattr(imported_module, "__BUTTON__", None)
            text = getattr(imported_module, "__TEXT__", None)
            hasil = getattr(imported_module, "__HASIL__", None)

            if utama and button_labels and text and hasil:
                if utama not in tombol_utama:
                    tombol_utama[utama] = {"text": utama, "callback_data": f"usu {utama}", "__TEXT__": text, "HASIL": hasil}
                if utama not in tombol_anak:
                    tombol_anak[utama] = []

                buttons = []
                for label, hasil_labels in zip(button_labels, hasil):
                    callback_data = f"tousu {utama.lower()}_{label.replace(' ', '_').lower()}"
                    buttons.append({"text": label, "teks": hasil_labels, "callback_data": callback_data})

                tombol_anak[utama].extend(buttons)
        except Exception as e:
            logger.error(f"Client - Error loading module {mod}: {e}")
    task = [installPeer(), auto_reaction(), expiredUserbots(), check_session(), auto_backup()]
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
    await bots()
    await start_ubot()
    await loaded()
    await bash("rm -rf *session*")


if __name__ == "__main__":
    aiorun.run(main(), loop=bot.loop, shutdown_callback=stopped())
