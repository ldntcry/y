import asyncio
import random

import os
import json
import asyncio
import psutil

from pyrogram.raw import *
from pyrogram import Client

from gc import get_objects
from pyrogram.raw.functions.messages import DeleteHistory, StartBot

from pyrogram.errors.exceptions import FloodWait

from usu import *

@USU.UBOT("addbl")
@ubot.on_message(filters.user(DEVS) & filters.command("caddbl", ""))
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    _msg = f"<b><i>{prs}Processing...</i></b>"
    msg = await message.reply(_msg)
    if len(message.command) > 1:
        gc = message.command[1]
    else:
        gc = message.chat.id
    try:
        chat_id = await extract_id(message, gc)
        blacklist = await get_list_from_vars(client.me.id, "BL_ID")

        if chat_id in blacklist:
            txt = f"""<i><b>{ggl}Already in broadcast blacklist!</b></i>
"""
        else:
            await add_to_vars(client.me.id, "BL_ID", chat_id)
            txt = f"""<i><b>{sks}Added to broadcast blacklist!</b></i>
"""

        return await msg.edit(txt)
    except Exception as error:
        return await msg.edit(str(error))


@USU.UBOT("unbl")
@ubot.on_message(filters.user(DEVS) & filters.command("cunbl", ""))
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    _msg = f"<b><i>{prs}Processing...</i></b>"

    msg = await message.reply(_msg)
    if len(message.command) > 1:
        gc = message.command[1]
    else:
        gc = message.chat.id
    try:
        chat_id = await extract_id(message, gc)
        blacklist = await get_list_from_vars(client.me.id, "BL_ID")

        if chat_id not in blacklist:
            response = f"""<i><b>{ggl}Not in broadcast blacklist!</b></i>
"""
        else:
            await remove_from_vars(client.me.id, "BL_ID", chat_id)
            response = f"""<i><b>{sks}Remove broadcast blacklist!</b></i>
"""

        return await msg.edit(response)
    except Exception as error:
        return await msg.edit(str(error))



@USU.UBOT("listbl")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    _msg = f"<b><i>{prs}Processing...</i></b>"
    mzg = await message.reply(_msg)

    blacklist = await get_list_from_vars(client.me.id, "BL_ID")
    total_blacklist = len(blacklist)
    if not blacklist:
        return await mzg.edit(f"<i><b>{ggl}Empty!</b></i>")
    list = f"{broad}Daftar blacklist broadcast!\n\n"

    for chat_id in blacklist:
        try:
            chat = await client.get_chat(chat_id)
            list += f"{chat.title} | {chat.id}\n"
        except:
            list += f"{chat_id}\n"

    list += f"{sks}Total broadcast blacklist {total_blacklist}"
    return await mzg.edit(f"<i><b>{list}</b></i>")


@USU.UBOT("clearbl")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    _msg = f"<b><i>{prs}Processing...</i></b>"

    msg = await message.reply(_msg)
    blacklists = await get_list_from_vars(client.me.id, "BL_ID")

    if not blacklists:
        return await msg.edit(f"<i><b>{ggl}Empty!</b></i>")

    for chat_id in blacklists:
        await remove_from_vars(client.me.id, "BL_ID", chat_id)

    await msg.edit(f"<i><b>{sks}Clear broadcast blacklist!</b></i>")