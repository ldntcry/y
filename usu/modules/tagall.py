import asyncio
import random
from random import shuffle


from usu import *





tagallgcid = []

emoji_categories = {
    "smileys": [
        "😀",
        "😃",
        "😄",
        "😁",
        "😆",
        "😅",
        "😂",
        "🤣",
        "😊",
        "😍",
        "🥰",
        "😘",
        "😎",
        "🥳",
        "😇",
        "🙃",
        "😋",
        "😛",
        "🤪",
    ],
    "animals": [
        "🐶",
        "🐱",
        "🐰",
        "🐻",
        "🐼",
        "🦁",
        "🐸",
        "🦊",
        "🦔",
        "🦄",
        "🐢",
        "🐠",
        "🐦",
        "🦜",
        "🦢",
        "🦚",
        "🦓",
        "🐅",
        "🦔",
    ],
    "food": [
        "🍎",
        "🍕",
        "🍔",
        "🍟",
        "🍩",
        "🍦",
        "🍓",
        "🥪",
        "🍣",
        "🍔",
        "🍕",
        "🍝",
        "🍤",
        "🥗",
        "🥐",
        "🍪",
        "🍰",
        "🍫",
        "🥤",
    ],
    "nature": [
        "🌲",
        "🌺",
        "🌞",
        "🌈",
        "🌊",
        "🌍",
        "🍁",
        "🌻",
        "🌸",
        "🌴",
        "🌵",
        "🍃",
        "🍂",
        "🌼",
        "🌱",
        "🌾",
        "🍄",
        "🌿",
        "🌳",
    ],
    "travel": [
        "✈️",
        "🚀",
        "🚲",
        "🚗",
        "⛵",
        "🏔️",
        "🚁",
        "🚂",
        "🏍️",
        "🚢",
        "🚆",
        "🛴",
        "🛸",
        "🛶",
        "🚟",
        "🚈",
        "🛵",
        "🛎️",
        "🚔",
    ],
    "sports": [
        "⚽",
        "🏀",
        "🎾",
        "🏈",
        "🎱",
        "🏓",
        "🥊",
        "⛳",
        "🏋️",
        "🏄",
        "🤸",
        "🏹",
        "🥋",
        "🛹",
        "🥏",
        "🎯",
        "🥇",
        "🏆",
        "🥅",
    ],
    "music": ["🎵", "🎶", "🎤", "🎧", "🎼", "🎸", "🥁", "🎷", "🎺", "🎻", "🪕", "🎹", "🔊"],
    "celebration": ["🎉", "🎊", "🥳", "🎈", "🎁", "🍰", "🧁", "🥂", "🍾", "🎆", "🎇"],
    "work": ["💼", "👔", "👓", "📚", "✏️", "📆", "🖥️", "🖊️", "📂", "📌", "📎"],
    "emotions": ["❤️", "💔", "😢", "😭", "😠", "😡", "😊", "😃", "🙄", "😳", "😇", "😍"],
}


def emoji_random():
    random_category = random.choice(tuple(emoji_categories.keys()))
    return random.choice(emoji_categories[random_category])


@USU.UBOT("tagall|all")
@USU.GROUP
async def _(client, message):
    if message.chat.id in tagallgcid:
        return
    susers = await db.get_list_from_vars(bot.me.id, "SAVED_USERS")
    if message.chat.id not in susers:
        if message.chat.type in [ChatType.SUPERGROUP, ChatType.GROUP]:
            await db.add_to_vars(bot.me.id, "SAVED_USERS", message.chat.id)
    tagallgcid.append(message.chat.id)
    text = message.text.split(None, 1)[1] if len(message.text.split()) != 1 else (message.reply_to_message.text if message.reply_to_message else "")
    m = message.reply_to_message if message.reply_to_message else message
    users = []
    async for member in client.get_chat_members(message.chat.id):
        if not (member.user.is_bot or member.user.is_deleted):
            if message.chat.id not in tagallgcid:
                break
            targetnya = f"• <a href=tg://user?id={member.user.id}>{member.user.first_name} {member.user.last_name or ' '}</a>"
            users.append(targetnya)
            if len(users) == 5:
                shuffle(users)
                anu = "\n".join(users)
                try:
                    await asyncio.sleep(2)
                    await m.reply_text(f"<blockquote>{text}</blockquote>\n<blockquote><b>{anu}</b></blockquote>\n<b><blockquote>🛒 @{CHANNEL}</blockquote></b>", quote=False)
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    await asyncio.sleep(2)
                    await m.reply_text(f"<blockquote>{text}</blockquote>\n<blockquote><b>{anu}</b></blockquote>\n<b><blockquote>🛒 @{CHANNEL}</blockquote></b>", quote=False)
                users = []
    if users:
        shuffle(users)
        anu = "\n".join(users)
        try:
            await asyncio.sleep(2)
            await m.reply_text(f"<blockquote>{text}</blockquote>\n<blockquote><b>{anu}</b></blockquote>\n<b><blockquote>🛒 @{CHANNEL}</blockquote></b>", quote=False)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await asyncio.sleep(2)
            await m.reply_text(f"<blockquote>{text}</blockquote>\n<blockquote><b>{anu}</b></blockquote>\n<b><blockquote>🛒 @{CHANNEL}</blockquote></b>", quote=False)
    try:
        tagallgcid.remove(message.chat.id)
    except Exception:
        pass


@USU.UBOT("cancel")
@USU.GROUP
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    if message.chat.id not in tagallgcid:
        return await message.reply_text(
            f"<i><b>{ggl}No tags all!</b></i>"
        )
    try:
        tagallgcid.remove(message.chat.id)
    except Exception:
        pass
    await message.reply_text(f"<i><b>{sks}Successfully canceled!</b></i>")


@USU.BOT("all|tagall")
@USU.GROUP
@USU.ADMIN
async def _(client, message):
    if message.chat.id in tagallgcid:
        return
    susers = await db.get_list_from_vars(bot.me.id, "SAVED_USERS")
    if message.chat.id not in susers:
        if message.chat.type in [ChatType.SUPERGROUP, ChatType.GROUP]:
            await db.add_to_vars(bot.me.id, "SAVED_USERS", message.chat.id)
    tagallgcid.append(message.chat.id)
    text = message.text.split(None, 1)[1] if len(message.text.split()) != 1 else (message.reply_to_message.text if message.reply_to_message else "")
    m = message.reply_to_message if message.reply_to_message else message
    users = []
    async for member in client.get_chat_members(message.chat.id):
        if not (member.user.is_bot or member.user.is_deleted):
            if message.chat.id not in tagallgcid:
                break
            targetnya = f"• <a href=tg://user?id={member.user.id}>{member.user.first_name} {member.user.last_name or ' '}</a>"
            users.append(targetnya)
            if len(users) == 5:
                shuffle(users)
                anu = "\n".join(users)
                try:
                    await asyncio.sleep(2)
                    await m.reply_text(f"<blockquote>{text}</blockquote>\n<blockquote><b>{anu}</b></blockquote>\n<b><blockquote>🛒 @{CHANNEL}</blockquote></b>", quote=False)
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    await asyncio.sleep(2)
                    await m.reply_text(f"<blockquote>{text}</blockquote>\n<blockquote><b>{anu}</b></blockquote>\n<b><blockquote>🛒 @{CHANNEL}</blockquote></b>", quote=False)
                users = []
    if users:
        shuffle(users)
        anu = "\n".join(users)
        try:
            await asyncio.sleep(2)
            await m.reply_text(f"<blockquote>{text}</blockquote>\n<blockquote><b>{anu}</b></blockquote>\n<b><blockquote>🛒 @{CHANNEL}</blockquote></b>", quote=False)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await asyncio.sleep(2)
            await m.reply_text(f"<blockquote>{text}</blockquote>\n<blockquote><b>{anu}</b></blockquote>\n<b><blockquote>🛒 @{CHANNEL}</blockquote></b>", quote=False)
    try:
        tagallgcid.remove(message.chat.id)
    except Exception:
        pass


@USU.BOT("cancel|stop")
@USU.GROUP
@USU.ADMIN
async def _(client, message):
    admin = await list_admins(message)
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    if message.chat.id not in tagallgcid:
        return await message.reply_text(
            f"<i><b>{ggl}No tags all!</b></i>"
        )
    try:
        tagallgcid.remove(message.chat.id)
    except Exception:
        pass
    await message.reply_text(f"<i><b>{sks}Successfully canceled!</b></i>")
