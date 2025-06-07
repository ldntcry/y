import asyncio

from pyrogram.enums import ChatType

from usu import *
from usu.core.database.local import db



chat_type = {
    "global": [ChatType.GROUP, ChatType.SUPERGROUP, ChatType.CHANNEL],
    "group": [ChatType.GROUP, ChatType.SUPERGROUP],
    "channel": [ChatType.CHANNEL],
    "users": [ChatType.PRIVATE],
    "all": [ChatType.GROUP, ChatType.SUPERGROUP, ChatType.PRIVATE, ChatType.CHANNEL],
}



async def get_private_and_group_chats(client):
    user = []
    group = []
    gb = []
    channel = []
    all = []
    database = await db.get_list_from_vars(client.me.id, "bcdb") or []

    async for dialog in client.get_dialogs(limit=None):
        try:
            if dialog.chat.type in chat_type.get("users"):
                user.append(dialog.chat.id)
            elif dialog.chat.type in chat_type.get("group"):
                group.append(dialog.chat.id)
            elif dialog.chat.type in chat_type.get("channel"):
                channel.append(dialog.chat.id)
            elif dialog.chat.type in chat_type.get("global"):
                gb.append(dialog.chat.id)
            elif dialog.chat.type in chat_type.get("all"):
                all.append(dialog.chat.id)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            if dialog.chat.type in chat_type.get("users"):
                user.append(dialog.chat.id)
            elif dialog.chat.type in chat_type.get("group"):
                group.append(dialog.chat.id)
            elif dialog.chat.type in chat_type.get("channel"):
                channel.append(dialog.chat.id)
            elif dialog.chat.type in chat_type.get("global"):
                gb.append(dialog.chat.id)
            elif dialog.chat.type in chat_type.get("all"):
                all.append(dialog.chat.id)
        except Exception as e:
            print(f"[INFO]: {e}")

    return user, group, gb, channel, all, database


async def install_my_peer(client):
    user, group, gb, channel, all, database = await get_private_and_group_chats(client)
    client_id = client.me.id
    client.peer[client_id] = {"user": user, "group": group, "global": gb, "channel": channel, "all": all, "db": database}


async def installPeer():
    task = []
    for client in ubot._ubot.values():
        task.append(install_my_peer(client))
    await asyncio.gather(*task)



