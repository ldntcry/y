from usu import *
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup



@USU.BOT("setgoodbye")
@USU.GROUP
@USU.ADMIN
async def set_goodbye(c, m):
    user_id = m.from_user.id
    chat_id = m.chat.id
    pesan = await m.reply(f"<b><i>Processing...</i></b>")
    file = None
    if m.reply_to_message:
        if m.reply_to_message.photo or m.reply_to_message.video or m.reply_to_message.voice or m.reply_to_message.audio:
            value = m.reply_to_message.media.value
            file = getattr(getattr(m.reply_to_message, f"{value}"), "file_id")
        teks = m.reply_to_message.caption or " ".join(m.text.split()[1:]) or m.reply_to_message.text
    elif len(m.text.split()) > 1:
        teks = " ".join(m.text.split()[1:])
    else:
        return await pesan.edit(f"<b><i>Reply/text</i></b>")
    hasil = {"text": teks, "file": file} if file else {"text": teks}
    await set_vars(chat_id, "GOODBYE", hasil)
    return await pesan.edit(f"<b><i>Pesan selamat tinggal berhasil di settings!</i></b>")


@USU.BOT("delgoodbye")
@USU.GROUP
@USU.ADMIN
async def del_goodbye(c, m):
    user_id = m.from_user.id
    chat_id = m.chat.id
    vars = await get_vars(chat_id, "GOODBYE")
    pesan = await m.reply(f"<b><i>Processing...</i></b>")
    if vars:
        await remove_vars(chat_id, "GOODBYE")
        return await pesan.edit(f"<b><i>Pesan selamat tinggal berhasil di hapus!</i></b>")
    else:
        return await pesan.edit(f"<b><i>Tidak ada pesan selamat tinggal!</i></b>")


