import random
import re

from datetime import datetime
from time import time

from pyrogram.raw.functions import Ping
from pyrogram.types import *
import os
import platform
import subprocess
import sys
import traceback
from datetime import datetime
from io import BytesIO, StringIO
from usu.config import OWNER_ID
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from pytz import timezone

from usu import *





@USU.UBOT("help")
async def user_help(client, message):
    if not get_arg(message):
        try:
            x = await client.get_inline_bot_results(bot.me.username, f"user_help {client.me.id}")
            await message.reply_inline_bot_result(x.query_id, x.results[0].id)
        except Exception as error:
            await message.reply(error)
    else:
        module = (get_arg(message))
        for utama, buttons in tombol_anak.items():
            for button in buttons:
                if button["text"].lower() == module.lower():
                    try:
                        x = await client.get_inline_bot_results(bot.me.username, f"user_help {client.me.id} {module}")
                        await message.reply_inline_bot_result(x.query_id, x.results[0].id)
                    except Exception as error:
                        await message.reply(error)
                    return
        await message.reply(
            f"<b><i>Module <code>{module}</code> not found!</i></b>"
        )

usu_back = {}


@USU.INLINE("^user_help")
async def user_help_inline(client, inline_query):
    query = inline_query.query
    user_id = query.split()[1]
    try:
        asu = await client.get_users(user_id)
    except Exception as e:
        print(e)
        return
    if len(query.split()) == 3:
        module = " ".join(query.split()[2:]).lower()
        for utama, buttons in tombol_anak.items():
            for button in buttons:
                if button["text"].lower() == module:
                    prefix = await ubot.get_prefix(client.me.id)
                    hsl = button["teks"].format(next((usu) for usu in prefix))
                    text = hsl + f"\n\n<i><b>@{CHANNEL}</b></i>"
                    if user_id not in usu_back:
                        usu_back[user_id] = 0
                    back = [[InlineKeyboardButton(text="Kembali", callback_data=f"back_{utama}"), InlineKeyboardButton(text="Home", callback_data="kembali")]]
                    results = [InlineQueryResultArticle(
                        title=button["text"],
                        reply_markup=InlineKeyboardMarkup(back),
                        input_message_content=InputTextMessageContent(text),
                    )]
                    await client.answer_inline_query(inline_query.id, cache_time=60, results=results)
                    return
    else:
        if user_id not in usu_back:
            usu_back[user_id] = 0
        text = f"<b><i>Halo {asu.mention},\nPerkenalkan saya adalah menu bantuan anda!</i></b>"
        markup = BTN.UTAMA()
        results = [InlineQueryResultArticle(
            title="Help Menu!",
            reply_markup=InlineKeyboardMarkup(markup),
            input_message_content=InputTextMessageContent(text),
        )]
        await client.answer_inline_query(inline_query.id, cache_time=60, results=results)


@USU.CALLBACK("^tousu")
async def tosub_callback(client, callback_query):
    usu = await ubot.get_prefix(callback_query.from_user.id)
    data = callback_query.data.split()
    id_button = data[1]
    for utama, buttons in tombol_anak.items():
        for button in buttons:
            if button["callback_data"] == callback_query.data:
                hsl = button["teks"].format(next((usu) for usu in usu))
                teks = hsl + f"\n\n<i><b>@{CHANNEL}</b></i>"
                if callback_query.from_user.id not in usu_back:
                    usu_back[callback_query.from_user.id] = 0
                back = [[InlineKeyboardButton(text="Kembali", callback_data=f"back_{utama}"), InlineKeyboardButton(text="Home", callback_data="kembali")]]
                await callback_query.edit_message_text(text=teks, reply_markup=InlineKeyboardMarkup(back))
                break


@USU.CALLBACK("^usu (.*?)")
async def help_callback(client, callback_query):
    utama = callback_query.data.split(" ")[1]
    if utama in tombol_anak:
        text_usu = tombol_utama[utama].get("__TEXT__")
        if callback_query.from_user.id not in usu_back:
            usu_back[callback_query.from_user.id] = 0
        for user in ubot._ubot.values():
            if callback_query.from_user.id == user.me.id:
                markup = await tombol_anak_usu_gbt(utama, usu_back[user.me.id])
            else:
                markup = await tombol_anak_usu_gbt(utama, usu_back[callback_query.from_user.id])
        await callback_query.edit_message_text(
            text=f"<i><b>{text_usu}</b></i>",
            reply_markup=markup,
            disable_web_page_preview=True
        )
    else:
        await callback_query.answer(text="Error! Tombol tidak ditemukan!", show_alert=True)



@USU.CALLBACK("^back_(.*?)")
async def back_callback(client, callback_query):
    utama = callback_query.data.split("_")[1]
    if callback_query.from_user.id not in usu_back:
        usu_back[callback_query.from_user.id] = 0
    for user in ubot._ubot.values():
        if callback_query.from_user.id == user.me.id:
            page = usu_back[user.me.id]
        else:
            page = usu_back[callback_query.from_user.id]
    markup = await tombol_anak_usu_gbt(utama, page)
    teks = tombol_utama[utama].get("__TEXT__")
    await callback_query.edit_message_text(text=f"<i><b>{teks}</b></i>", reply_markup=markup)



@USU.CALLBACK("^kembali")
async def kembali_callback(client, callback_query):
    data = callback_query.data.split()
    try:
        user = await bot.get_users(callback_query.from_user.id)
    except Exception as e:
        print(e)
        return
    text = f"<b><i>Wow {user.mention},\nSekarang kamu berada di menu fitur!</i></b>"
    markup = await tombol_usu()
    await callback_query.edit_message_text(text=text, reply_markup=markup)

@USU.CALLBACK("^ignore")
async def ignore(client, callback_query):
    start = datetime.now()
    await client.invoke(Ping(ping_id=0))
    end = datetime.now()
    delta_ping = (end - start).microseconds / 1000
    delta_ping_formatted = round(delta_ping)
    uptime = await get_time((time() - start_time))
    jumlah_button_usu = sum(len(buttons) for buttons in tombol_anak.values())
    alive = await usu_alive()
    await callback_query.answer(f"""Module: {jumlah_button_usu}
Pong: {str(delta_ping)} ms
Jumlah Pengguna: {len(ubot._ubot)}
Pyrogram: {pyrogram.__version__}
Pytgcalls: {pytgcalls.__version__}""", True)
        


@USU.CALLBACK("^next_(.*?)_(.*?)")
async def handle_next_callback(client, callback_query):
    data = callback_query.data.split("_")
    utama = data[1]
    page = int(data[2])
    for user_id in ubot._ubot.values():
        if callback_query.from_user.id == user_id.me.id:
            usu_back[callback_query.from_user.id] = page
    markup = await tombol_anak_usu_gbt(utama, page)
    await callback_query.edit_message_reply_markup(markup)


@USU.CALLBACK("^prev_(.*?)_(.*?)")
async def handle_prev_callback(client, callback_query):
    data = callback_query.data.split("_")
    utama = data[1]
    page = int(data[2])
    for user_id in ubot._ubot.values():
        if callback_query.from_user.id == user_id.me.id:
            usu_back[callback_query.from_user.id] = page
    markup = await tombol_anak_usu_gbt(utama, page)
    await callback_query.edit_message_reply_markup(markup)


@USU.CALLBACK("alive")
async def alive_cb(client, callback_query):
    data = callback_query.data.split()
    try:
        user = await bot.get_users(callback_query.from_user.id)
    except Exception as e:
        print(e)
        return
    for my in ubot._ubot.values():
        button = BTN.ALIVE()
        time_usu = await usu_alive()
        if user.id == my.me.id:
            try:
                peer = my.peer[my.me.id]
                users = len(peer["pm"])
                group = len(peer["gc"])
            except Exception:
                users = random.randrange(await my.get_dialogs_count())
                group = random.randrange(await my.get_dialogs_count())
            get_exp = await get_expired_date(my.me.id)
            exp = get_exp.strftime("%d %B %Y") if get_exp else "None"
            if my.me.id in DEVS:
                status = f"<i>Active! [Owner]</i>"
            elif my.me.id in await get_list_from_vars(client.me.id, "SELER_USERS") and my.me.id not in DEVS:
                status = f"<i>Active! [Seller]</i>"
            else:
                status = f"<i>Active!</i>"
            start = datetime.now()
            await my.invoke(Ping(ping_id=0))
            ping = (datetime.now() - start).microseconds / 1000
            uptime = await get_time((time() - start_time))
            msg = f"""<b><i>{bot.me.first_name}</i></b>
  <b><i>• Status:</i></b> {status} 
    <b><i>• Expired:</i></b> <i>{exp}</i>
    <b><i>• Name:</i></b> <i>{my.me.mention}</i>
    <b><i>• ID:</i></b> <i>{my.me.id}</i>
    <b><i>• Peer-User:</i></b> <i>{users}</i>
    <b><i>• Peer-Group:</i></b> <i>{group}</i>
    <b><i>• Alive:</i></b> {time_usu}
"""
            break
        else:
            msg = f"""<b><i>{bot.me.first_name}</i></b>
  <b><i>• Status:</i></b> <i>None</i>
    <b><i>• Expired:</i></b> <i>None</i>
    <b><i>• Name:</i></b> <i>{user.mention}</i>
    <b><i>• ID:</i></b> <i>{callback_query.from_user.id}</i>
    <b><i>• Peer-User:</i></b> <i>None</i>
    <b><i>• Peer-Group:</i></b> <i>None</i>
    <b><i>• Alive:</i></b> {time_usu}
"""
    return await callback_query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(button))


@USU.CALLBACK("menu_utama")
async def menu_utama(client, callback_query):
    if callback_query.from_user.id not in usu_back:
        for utama, buttons in tombol_anak.items():
            usu_back[callback_query.from_user.id] = 0
    try:
        asu = await bot.get_users(callback_query.from_user.id)
    except Exception as e:
        print(e)
        return
    data = callback_query.data.split()
    teks = f"<b><i>Halo {asu.mention},\nPerkenalkan saya adalah menu bantuan anda!</i></b>"
    button = BTN.UTAMA()
    return await callback_query.edit_message_text(teks, reply_markup=InlineKeyboardMarkup(button))



@USU.CALLBACK("saldo_userbot")
async def saldo_userbot(client, callback_query):
    data = callback_query.data.split()
    try:
        asu = await bot.get_users(callback_query.from_user.id)
    except Exception as e:
        print(e)
        return
    for user in ubot._ubot.values():
        if asu == user.me.id:
            vars = await get_vars(user.me.id, "SALDO")
            break
        else:
            vars = await get_vars(callback_query.from_user.id, "SALDO")
    btn = BTN.BACK_SALDO()
    saldo = vars if vars else 0
    teks = f"{saldo:,}".replace(",", ".")
    text = f"<i><b>Wow {asu.mention},\nSaldo Userbot anda saat ini:\n</b>Rp {teks}</i>"            
    return await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(btn))