import wget

from gc import get_objects

from pykeyboard import InlineKeyboard
from pyrogram.types import (InlineKeyboardButton, InlineQueryResultArticle,
                            InlineQueryResultPhoto, InputTextMessageContent)

from usu import *



async def send_log(c, chat_id, message, message_text, msg):
    usu = InlineKeyboardMarkup([[InlineKeyboardButton(f"Message Link", url=f"{message.link}")]] if "LOGS_GROUP" in msg else [[InlineKeyboardButton(f"Message Link", url=f"tg://openmessage?user_id={message.from_user.id}&message_id={message.id}")]])
    try:
        if message.photo:
            hasil = await c.download_media(message)
            await bot.send_photo(chat_id, hasil, caption=message_text, reply_markup=usu)
            os.remove(hasil)
        elif message.video:
            hasil = await c.download_media(message)
            await bot.send_video(chat_id, hasil, caption=message_text, reply_markup=usu)
            os.remove(hasil)
        elif message.document:
            hasil = await c.download_media(message)
            await bot.send_document(chat_id, hasil, caption=message_text, reply_markup=usu)
            os.remove(hasil)
        elif message.audio:
            hasil = await c.download_media(message)
            await bot.send_audio(chat_id, hasil, caption=message_text, reply_markup=usu)
            os.remove(hasil)
        elif message.animation:
            hasil = await c.download_media(message)
            await bot.send_animation(chat_id, hasil, caption=message_text, reply_markup=usu)
            os.remove(hasil)
        elif message.sticker:
            hasil = await c.download_media(message)
            await bot.send_sticker(chat_id, hasil)
            await bot.send_message(chat_id, message_text, reply_markup=usu)
            os.remove(hasil)
        elif message.voice:
            hasil = await c.download_media(message)
            await bot.send_voice(chat_id, hasil)
            await bot.send_message(chat_id, message_text, reply_markup=usu)
            os.remove(hasil)
        else:
            await bot.send_message(chat_id, message_text, reply_markup=usu)
    except Exception as error:
        print(error)


@USU.UBOT("logger")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    if len(message.command) < 2:
        return await message.reply(
            f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>[on/off]</b></i>"
        )

    query = {"on": True, "off": False}
    command = message.command[1].lower()

    if command not in query:
        return await message.reply(f"<i><b>{ggl}Invalid!</b></i>")

    value = query[command]

    vars = await db.get_vars(client.me.id, "ID_LOGS")
    if not vars:
        await db.set_vars(client.me.id, "ID_LOGS", bot.me.id)
    await db.set_vars(client.me.id, "ON_LOGS", value)
    await message.reply(
        f"<i><b>{sks}Logger {value}</b></i>"
    )
    if command == "on":
        return await bot.send_message(client.me.id, f"<i><b>Logger on!</b></i>")
    else:
        return await bot.send_message(client.me.id, f"<i><b>Logger off!</b></i>")

data = {}

@USU.NO_CMD("LOGS_PRIVATE", ubot)
async def _(client, message):
    logs = await db.get_vars(client.me.id, "ID_LOGS")
    on_logs = await db.get_vars(client.me.id, "ON_LOGS")

    if logs and on_logs:
        user_link = f"{message.from_user.mention}" if message.from_user else f"{message.sender_chat.title}"
        user_id = f"{message.from_user.id}" if message.from_user else f"{message.sender_chat.id}"
        if message.photo or message.video or message.document or message.voice or message.audio or message.animation:
            message_text = f"""Information Users!
Name: {user_link}
ID: {user_id}

Chat Name: {message.chat.title}
Chat ID: {message.chat.id}
Chat Type: Private

Message ID: {message.id}
Message: {message.caption}"""
        else:
            message_text = f"""Information Users!
Name: {user_link}
ID: {user_id}

Chat Name: {message.chat.title}
Chat ID: {message.chat.id}
Chat Type: Private

Message ID: {message.id}
Message: {message.text}"""
        await send_log(client, client.me.id, message, f"<b><i>{message_text}</i></b>", "LOGS_PRIVATE")
        if client.me.id not in data:
            data[client.me.id] = []
        data[client.me.id].append({"chat_id": message.chat.id, "message_id": message.id, "message_text": message_text})

@USU.NO_CMD("LOGS_GROUP", ubot)
async def _(client, message):
    logs = await db.get_vars(client.me.id, "ID_LOGS")
    on_logs = await db.get_vars(client.me.id, "ON_LOGS")

    if logs and on_logs:
        user_link = f"{message.from_user.mention}" if message.from_user else f"{message.sender_chat.title}"
        user_id = f"{message.from_user.id}" if message.from_user else f"{message.sender_chat.id}"
        if message.photo or message.video or message.document or message.voice or message.audio or message.animation:
            message_text = f"""Information Users!
Name: {user_link}
ID: {user_id}

Chat Name: {message.chat.title}
Chat ID: {message.chat.id}
Chat Type: Group

Message ID: {message.id}
Message: {message.caption}"""
        else:
            message_text = f"""Information Users!
Name: {user_link}
ID: {user_id}

Chat Name: {message.chat.title}
Chat ID: {message.chat.id}
Chat Type: Group

Message ID: {message.id}
Message: {message.text}"""
        await send_log(client, client.me.id, message, f"<b><i>{message_text}</i></b>", "LOGS_GROUP")
        if client.me.id not in data:
            data[client.me.id] = []
        data[client.me.id].append({"chat_id": message.chat.id, "message_id": message.id, "message_text": message_text})




@USU.NO_CMD("REPLY", ubot)
async def _(client, message):
    logs = await db.get_vars(client.me.id, "ID_LOGS")
    on_logs = await db.get_vars(client.me.id, "ON_LOGS")
    if logs and on_logs and message.reply_to_message:
        if client.me.id in data:
            if data[client.me.id]:
                for item in data[client.me.id]:
                    item_text = re.sub(r"<.*?>", "", item["message_text"])
                    if message.reply_to_message.text:
                        text_m = re.sub(r"<.*?>", "", message.reply_to_message.text)
                        if text_m == item_text:
                            chat_id = item["chat_id"]
                            message_id = item["message_id"]
                            if chat_id and message_id:
                                try:
                                    if message.photo:
                                        if message.caption:
                                            await client.send_photo(chat_id, message.photo.file_id, caption=message.caption, reply_to_message_id=message_id)
                                        else:
                                            await client.send_photo(chat_id, message.photo.file_id, reply_to_message_id=message_id)
                                    elif message.video:
                                        if message.caption:
                                            await client.send_video(chat_id, message.video.file_id, caption=message.caption, reply_to_message_id=message_id)
                                        else:
                                            await client.send_video(chat_id, message.video.file_id, reply_to_message_id=message_id)
                                    else:
                                        await message.copy(chat_id, reply_to_message_id=message_id)
                                except Exception as e:
                                    print(e)
