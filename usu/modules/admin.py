import asyncio

from pyrogram import *
from pyrogram.enums import *
from pyrogram.errors import *
from pyrogram.types import *
from pyrogram.errors.exceptions.bad_request_400 import (
    ChatAdminRequired,
    ChatNotModified,
)

from usu import *
 


MUTES = """
Command for <b>Mutes</b>

<b>Mutes</b>
 <i>bisukan anggota group</i>
    <code>{0}mute</code>
 <i>melepas pembisuan anggota group</i>
    <code>{0}unmute</code>"""

BANS = """
Command for <b>Bans</b>

<b>Bans</b>
 <i>memblokir anggota group</i>
    <code>{0}ban</code>
 <i>membuka blokir anggota group</i>
    <code>{0}unban</code>"""

ZOMBIES = """
Command for <b>Zombies</b>

<b>Zombies</b>
 <i>mengeluarkan akun terhapus</i>
    <code>{0}zombies</code>"""

KICKS = """
Command for <b>Kicks</b>

<b>Kicks</b>
 <i>mendang anggota group</i>
    <code>{0}kick</code>"""

PINS = """
Command for <b>Pins</b>

<b>Pins</b>
 <i>sematkan pesan</i>
    <code>{0}pin</code>
 <i>lepas sematan pesan</i>
    <code>{0}unpin</code>"""

PROMOTE = """
Command for <b>Promote</b>
 
<b>Promote</b>
 <i>adminkan anggota group</i>
    <code>{0}admin or {0}fulladmin</code>
 <i>turunkan admin anggota group</i>
    <code>{0}unadmin</code>"""

ANTIUSER = """
Command for <b>Anti-User</b>

<b>Blacklist user</b>
 <i>mengaktifkan/nonaktifkan antiuser</i>
    <code>{0}antiuser [on/off]</code>
 <i>tambahkan pengguna dalam blacklist</i>
    <code>{0}dor</code>
 <i>hapus pengguna dalam blacklist</i>
    <code>{0}undor</code>
 <i>melihat daftar blacklist</i>
    <code>{0}listdor</code>

<b>Notes:</b>
<i>pengguna yang di tambahkan tidak bisa 
mengirim pesan digroup yang anda admin</i>"""

ANTIGCAST = """
Command for <b>Antigcast</b>

<b>Antigcast</b>
 <i>mengaktifkan/nonaktifkan antigcast</i>
    <code>{0}ankes [on/off]</code>
 <i>tambahkan pengguna whitelist dalam antigcast</i>
    <code>{0}addwl [user_id/reply]</code>
 <i>hapus pengguna whitelist dalam antigcast</i>
    <code>{0}delwl [user_id/reply]</code>
 <i>tambahkan kata-kata dalam antigcast</i>
    <code>{0}addword [text/reply]</code>
 <i>hapus kata-kata dalam antigcast</i>
    <code>{0}delword [text/reply]</code>
 <i>melihat daftar kata-kata antigcast</i>
    <code>{0}listword</code>

<b>Catatan:</b>
<i>jika antigcast on maka sistem otomatis detect pesan yang bukan tulisan tangan, maka otomatis pesan dihapus!

kata-kata yang di tambahkan tidak bisa 
mengirim pesan digroup yang anda admin</i>"""

DEL = """
Command for <b>Del</b>

<b>Delete</b>
 <i>menghapus pesan yang di reply</i>
    <code>{0}del</code> [reply text]"""


__UTAMA__ = "Admins"

__TEXT__ = f"Menu Bantuan {__UTAMA__}!"

__BUTTON__ = "Mutes", "Kicks", "Bans", "Pins", "Promote", "Antiuser", "Antigcast", "Del", "Zombies"
__HASIL__ = MUTES, KICKS, BANS, PINS, PROMOTE, ANTIUSER, ANTIGCAST, DEL, ZOMBIES

data = {
    "msg": "can_send_messages",
    "stickers": "can_send_other_messages",
    "gifs": "can_send_other_messages",
    "media": "can_send_media_messages",
    "games": "can_send_other_messages",
    "inline": "can_send_other_messages",
    "url": "can_add_web_page_previews",
    "polls": "can_send_polls",
    "info": "can_change_info",
    "invite": "can_invite_users",
    "pin": "can_pin_messages",
}


async def current_chat_permissions(client, chat_id):
    perms = []
    perm = (await client.get_chat(chat_id)).permissions
    if perm.can_send_messages:
        perms.append("can_send_messages")
    if perm.can_send_media_messages:
        perms.append("can_send_media_messages")
    if perm.can_send_other_messages:
        perms.append("can_send_other_messages")
    if perm.can_add_web_page_previews:
        perms.append("can_add_web_page_previews")
    if perm.can_send_polls:
        perms.append("can_send_polls")
    if perm.can_change_info:
        perms.append("can_change_info")
    if perm.can_invite_users:
        perms.append("can_invite_users")
    if perm.can_pin_messages:
        perms.append("can_pin_messages")
    return perms


async def tg_lock(
    client,
    message,
    parameter,
    permissions: list,
    perm: str,
    lock: bool,
):
    if lock:
        if perm not in permissions:
            return await message.reply(f"<b><i>{parameter} Sudah terkunci</i></b>")
        permissions.remove(perm)
    else:
        if perm in permissions:
            return await message.reply(f"<b><i>{parameter} Sudah terbuka</i></b>")
        permissions.append(perm)
    permissions = {perm: True for perm in set(permissions)}
    try:
        await client.set_chat_permissions(
            message.chat.id, ChatPermissions(**permissions)
        )
    except ChatNotModified:
        return await message.reply(
            f"<code>{message.text.split()[0]}</code> <b><i>[type]</i></b>"
        )
    except ChatAdminRequired:
        return await message.reply(f"<b><i>Tidak mempunyai izin!</i></b>")
    await message.reply(
        (
            f"<b><i>Terkunci untuk non-admin!\nType: <code>{parameter}</code>\nGroup: {message.chat.title}</i></b>"
            if lock
            else f"<b><i>Terbuka untuk non-admin!\nType: <code>{parameter}</code>\nGroup: {message.chat.title}</i></b>"
        )
    )


@USU.UBOT("lock|unlock")
@USU.GROUP
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    if len(message.command) != 2:
        return await message.reply(f"{ggl}<code>{message.text.split()[0]}</code> <b>[type]</b>")
    chat_id = message.chat.id
    parameter = message.text.strip().split(None, 1)[1].lower()
    state = message.command[0].lower()
    if parameter not in data and parameter != "all":
        return await message.reply(incorrect_parameters)
    permissions = await current_chat_permissions(client, chat_id)
    if parameter in data:
        await tg_lock(
            client,
            message,
            parameter,
            permissions,
            data[parameter],
            bool(state == "lock"),
        )
    elif parameter == "all" and state == "lock":
        try:
            await client.set_chat_permissions(chat_id, ChatPermissions())
            await message.reply(
                f"<b><i>{sks}Terkunci untuk non-admin!</i></b>"
            )
        except ChatAdminRequired:
            return await message.reply(f"<b><i>{ggl}Not access!</i></b>")
        except ChatNotModified:
            return await message.reply(
                f"<b><i>{sks}Terkunci untuk non-admin!</i></b>"
            )
    elif parameter == "all" and state == "unlock":
        try:
            await client.set_chat_permissions(
                chat_id,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True,
                    can_send_polls=True,
                    can_change_info=False,
                    can_invite_users=True,
                    can_pin_messages=False,
                ),
            )
        except ChatAdminRequired:
            return await message.reply(f"<b><i>{ggl}Not access!</b>")
        await message.reply(
            f"<b><i>{sks}Terkunci untuk nonadmin!</i></b>"
        )


@USU.UBOT("locks")
@USU.GROUP
async def _(client, message):
    permissions = await current_chat_permissions(client, message.chat.id)
    if not permissions:
        return await message.reply(f"<b><i>Terkunci untuk semua</i></b>")

    perms = "-> __**" + "\n-> __**".join(permissions) + "**__"
    await message.reply(f"<b><i>{perms}</i></b>")
    

@USU.UBOT("pin|unpin")
@USU.GROUP
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    if not message.reply_to_message:
        return await message.edit(f"<b><i>{ggl}Reply text!</i></b>")
    r = message.reply_to_message
    await message.edit(f"<b><i>{prs}Processing...</i></b>")
    if message.command[0][0] == "u":
        await r.unpin()
        return await message.edit(
            f"<b><i>{sks}Unpinned!</i></b>",
            disable_web_page_preview=True,
        )
    try:
        await r.pin(disable_notification=True)
        await message.edit(
            f"<b><i>{sks}Pinned!</i></b>",
            disable_web_page_preview=True,
        )
    except ChatAdminRequired:
        await message.edit(f"<b><i>{ggl}Not access!</i></b>")
        await message.delete()


@USU.UBOT("admin|fulladmin")
@USU.GROUP
async def _(client: Client, message: Message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    biji = await eor(message, f"<b><i>{prs}Processing...</i></b>")
    replied = message.reply_to_message
    usu = message.command
    try:
        if replied:
            user_id = replied.from_user.id
            title = " ".join(usu[1:])
        elif len(usu) > 1 and usu[1].isdigit():
            user_id = int(usu[1])
            title = " ".join(usu[2:])
        elif len(usu) > 1:
            if usu[1].isdigit():
                user_id = int(usu[1])
                title = " ".join(usu[2:])
            else:
                try:
                    user_id = (await client.resolve_peer(usu[1])).user_id
                    title = " ".join(usu[2:])
                except Exception as error:
                    return await biji.edit(error)
        else:
            return await biji.edit(f"<i><b>{ggl}reply/user_id - title</b></i>")
        
        if message.command[0] == "admin":
            privileges = ChatPrivileges(
                can_manage_chat=True,
                can_delete_messages=True,
                can_manage_video_chats=True,
                can_restrict_members=True,
                can_change_info=False,
                can_invite_users=True,
                can_pin_messages=True,
                can_promote_members=False,
            )
        elif message.command[0] == "fulladmin":
            privileges = ChatPrivileges(
                can_manage_chat=True,
                can_delete_messages=True,
                can_manage_video_chats=True,
                can_restrict_members=True,
                can_change_info=True,
                can_invite_users=True,
                can_pin_messages=True,
                can_promote_members=True,
            )
        
        await message.chat.promote_member(user_id, privileges=privileges)
        await client.set_administrator_title(message.chat.id, user_id, title)
        await biji.edit(f"<b><i>{sks}Berhasil memberikan hak admin!</i></b>")
    
    except ChatAdminRequired:
        await biji.edit(f"<b><i>{ggl}Not access!</i></b>")


@USU.UBOT("unadmin")
@USU.GROUP
async def _(client: Client, message: Message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    user_id = await extract_user(message)
    sempak = await eor(message, f"<b><i>{prs}Processing...</i></b>")
    if not user_id:
        return await sempak.edit(f"<b><i>{ggl}Pengguna tidak ditemukan!</i></b>")
    if user_id == client.me.id:
        return await sempak.edit(f"<b><i>{ggl}Reply pengguna lain!</i></b>")
    await message.chat.promote_member(
        user_id,
        privileges=ChatPrivileges(
            can_manage_chat=False,
            can_delete_messages=False,
            can_manage_video_chats=False,
            can_restrict_members=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_promote_members=False,
        ),
    )
    await asyncio.sleep(1)
    umention = (await client.get_users(user_id)).mention
    await sempak.edit(f"<b><i>{sks}Lepas hak admin!</i></b>")


@USU.UBOT("kick|ban|mute|unmute|unban")
@USU.GROUP
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    if message.command[0] == "kick":
        user_id, reason = await extract_user_and_reason(message)
        if not user_id:
            return await message.reply_text(f"<b><i>{ggl}Pengguna tidak ditemukan!</i></b>")
        if user_id in DEVS:
            return await message.reply_text(f"<b><i>{ggl}Dia pemilik bot!</i></b>")
        if user_id in (await list_admins(message)):
            return await message.reply_text(
                f"<b><i>{ggl}Dia adalah admin group ini!</i></b>"
            )
        try:
            mention = (await client.get_users(user_id)).mention
        except Exception as error:
            await message.reply(error)
        msg_kick = f"""<b><i>{sks}Success kick pengguna!</i></b>"""
        try:
            await message.chat.ban_member(user_id)
            await message.reply(msg_kick)
            await asyncio.sleep(1)
            await message.chat.unban_member(user_id)
        except Exception as error:
            await message.reply(error)
    elif message.command[0] == "ban":
        user_id, reason = await extract_user_and_reason(message)
        if not user_id:
            return await message.reply_text(f"<b><i>{ggl}Pengguna tidak ditemukan!</i></b>")
        if user_id in DEVS:
            return await message.reply_text(f"<b><i>{ggl}Dia pemilik bot!</i></b>")
        if user_id in (await list_admins(message)):
            return await message.reply_text(
                f"<b><i>{ggl}Dia adalah admin group ini!</i></b>"
            )
        try:
            mention = (await client.get_users(user_id)).mention
        except Exception as error:
            await message.reply(error)
        msg_ban = f"""<b><i>{sks}Success ban pengguna!</i></b>"""
        try:
            await message.chat.ban_member(user_id)
            await message.reply(msg_ban)
        except Exception as error:
            await message.reply(error)
    elif message.command[0] == "mute":
        user_id, reason = await extract_user_and_reason(message)
        if not user_id:
            return await message.reply_text(f"<b><i>{ggl}Pengguna tidak ditemukan!</i></b>")
        if user_id in DEVS:
            return await message.reply_text(f"<b><i>{ggl}Dia pemilik bot!</i></b>")
        if user_id in (await list_admins(message)):
            return await message.reply_text(
                f"<b><i>{ggl}Dia adalah admin group ini!</i></b>"
            )
        try:
            mention = (await client.get_users(user_id)).mention
        except Exception as error:
            await message.reply(error)
        msg_mute = f"""<b><i>{sks}Success mute pengguna!</i></b>"""
        try:
            await message.chat.restrict_member(user_id, ChatPermissions())
            await message.reply(msg_mute)
        except Exception as error:
            await message.reply(error)
    elif message.command[0] == "unmute":
        user_id = await extract_user(message)
        if not user_id:
            return await message.reply_text(f"<b><i>{ggl}Pengguna tidak ditemukan!</i></b>")
        try:
            mention = (await client.get_users(user_id)).mention
        except Exception as error:
            await message.reply(error)
        try:
            await message.chat.unban_member(user_id)
            await message.reply(f"<b><i>{sks}Success unmute pengguna!</i></b>")
        except Exception as error:
            await message.reply(error)
    elif message.command[0] == "unban":
        user_id = await extract_user(message)
        if not user_id:
            return await message.reply_text(f"<b><i>{ggl}Pengguna tidak ditemukan!</i></b>")
        try:
            mention = (await client.get_users(user_id)).mention
        except Exception as error:
            await message.reply(error)
        try:
            await message.chat.unban_member(user_id)
            await message.reply(f"<b><i>{sks}Success unban pengguna!</i></b>")
        except Exception as error:
            await message.reply(error)


@USU.UBOT("zombies")
@USU.GROUP
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    chat_id = message.chat.id
    deleted_users = []
    banned_users = 0
    Tm = await message.reply(f"<b><i>{prs}Processing...</i></b>")
    async for i in client.get_chat_members(chat_id):
        if i.user.is_deleted and i.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
            deleted_users.append(i.user.id)
    if len(deleted_users) > 0:
        for deleted_user in deleted_users:
            try:
                banned_users += 1
                await message.chat.ban_member(deleted_user)
            except Exception:
                pass
        await Tm.edit(f"<b><i>{sks}Success kick {banned_users} accounts deleted!</i></b>")
    else:
        await Tm.edit(f"<b><i>{ggl}No accounts deleted!</i></b>")


