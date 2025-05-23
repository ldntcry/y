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


@USU.UBOT("tagall")
@USU.GROUP
async def _(client, message):
    if message.chat.id in tagallgcid:
        return
    tagallgcid.append(message.chat.id)
    text = message.text.split(None, 1)[1] if len(message.text.split()) != 1 else (message.reply_to_message.text if message.reply_to_message else "")
    m = message.reply_to_message if message.reply_to_message else message
    users = [
        f"• <a href=tg://user?id={member.user.id}>{member.user.first_name} {member.user.last_name or ' '}</a>"
        async for member in message.chat.get_members()
        if not (member.user.is_bot or member.user.is_deleted)
    ]
    shuffle(users)
    for output in [users[i : i + 5] for i in range(0, len(users), 5)]:
        if message.chat.id not in tagallgcid:
            break
        anu = "\n".join(output)
        try:
            await asyncio.sleep(2)
            await m.reply_text(f"<blockquote>{text}</blockquote>\n<blockquote><b>{anu}</b></blockquote>\n<b><blockquote>@SyntaxUpdate</blockquote></b>", quote=False)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await asyncio.sleep(2)
            await m.reply_text(f"<blockquote>{text}</blockquote>\n<blockquote><b>{anu}</b></blockquote>\n<b><blockquote>@SyntaxUpdate</blockquote></b>", quote=False)
    try:
        tagallgcid.remove(message.chat.id)
    except Exception:
        pass


@USU.UBOT("batal")
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
    admin = await list_admins(message)
    if message.from_user.id not in admin:
        return
    if message.chat.id in tagallgcid:
        return
    tagallgcid.append(message.chat.id)
    text = message.text.split(None, 1)[1] if len(message.text.split()) != 1 else (message.reply_to_message.text if message.reply_to_message else "")
    m = message.reply_to_message if message.reply_to_message else message
    users = [
        f"• <a href=tg://user?id={member.user.id}>{member.user.first_name} {member.user.last_name or ' '}</a>"
        async for member in message.chat.get_members()
        if not (member.user.is_bot or member.user.is_deleted)
    ]
    shuffle(users)
    for output in [users[i : i + 5] for i in range(0, len(users), 5)]:
        if message.chat.id not in tagallgcid:
            break
        anu = "\n".join(output)
        try:
            await asyncio.sleep(2)
            await m.reply_text(f"<blockquote>{text}</blockquote>\n<blockquote><b>{anu}</b></blockquote>\n<b><blockquote>@SyntaxUpdate</blockquote></b>", quote=False)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await asyncio.sleep(2)
            await m.reply_text(f"<blockquote>{text}</blockquote>\n<blockquote><b>{anu}</b></blockquote>\n<b><blockquote>@SyntaxUpdate</blockquote></b>", quote=False)
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
