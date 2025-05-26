from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ChatType

from usu import *
from usu.config import OWNER_ID, DEVS
import time
from usu.core.helpers.tools import list_admins


async def if_sudo(_, client, message):
    sudo_users = await get_list_from_vars(client.me.id, "SUDO_USERS")
    is_user = message.from_user if message.from_user else message.sender_chat
    saya = message.from_user and (message.from_user.is_self or message.outgoing or message.from_user.id == client.me.id)
    return bool(is_user.id in sudo_users or saya)

async def if_filter_gc(_, client, message):
    on_off = await get_vars(client.me.id, "FILTERS_GC_ON_OFF")
    return bool(on_off)

async def if_filter_gc_bot(_, client, message):
    on_off = await get_vars(message.chat.id, "FILTERS_GC_ON_OFF")
    return bool(on_off)

async def if_filter_pv(_, client, message):
    on_off = await get_vars(client.me.id, "FILTERS_PV_ON_OFF")
    return bool(on_off)

async def dor(_, client, message):
    on_off = await get_vars(client.me.id, "ON_OFF_DOR")
    return bool(on_off)

async def antiscam(_, client, message):
    on_off = await get_vars(client.me.id, "ON_OFF_ANTI_SCAM")
    return bool(on_off)

async def protect(_, client, message):
    on_off = await get_vars(client.me.id, "ON_OFF_WORD")
    return bool(on_off)

async def protect_bot(_, client, message):
    on_off = await get_vars(message.chat.id, "ON_OFF_WORD")
    return bool(on_off)

async def update_cmd(user_id, command, field, increment=False):
    top = await get_vars(user_id, command, field)
    new_value = int(top) + 1 if top and increment else 1
    await set_vars(user_id, command, new_value, field)
    return new_value

class USU:
    @staticmethod
    def ADMIN(func):
        async def function(client, message):
            admin = await list_admins(message)
            user = message.from_user
            if user.id not in admin and user.id not in DEVS:                   
                return
            return await func(client, message)

        return function

    @staticmethod
    def DEVS(func):
        async def function(client, message):
            user = message.from_user
            if user.id not in DEVS:
                return await message.reply(f"<b><i>fitur ini untuk owner bot!</i></b>")
            return await func(client, message)

        return function

    @staticmethod
    def SELLER(func):
        async def function(client, message):
            user = message.from_user
            seller_id = await get_list_from_vars(bot.me.id, "SELER_USERS")
            if user.id not in seller_id and user.id not in DEVS:
                return await message.reply(f"<b><i>Untuk menggunakan fitur ini ada harus menjadi seller bot terlebih dahulu!</b></i>")
            return await func(client, message)

        return function
    
    @staticmethod
    def NO_CMD_UBOT(result, asu):
        query_mapping = {
            "AFK": {
                "query": (
                    (filters.mentioned | filters.private)
                    & ~filters.bot
                    & ~filters.me
                    & filters.incoming
                ),
                "group": 1,
            },
            "PMPERMIT": {
                "query": (
                    filters.private
                    & filters.incoming
                    & ~filters.me
                    & ~filters.bot
                    & ~filters.via_bot
                    & ~filters.service
                ),
                "group": 2,
            },
            "LOGS_GROUP": {
                "query": (
                    filters.group
                    & filters.incoming
                    & filters.mentioned
                    & ~filters.bot
                ),
                "group": 3,
            },
            "LOGS_PRIVATE": {
                "query": (
                    filters.private
                    & filters.incoming
                    & ~filters.me
                    & ~filters.bot
                    & ~filters.service
                ),
                "group": 4,
            },
            "PROTECT": {
                "query": (
                    filters.group
                    & ~filters.me
                    & ~filters.bot & filters.create(protect)
                ),
                "group": 5,
            },
            "ANTI_USERS": {
                "query": (
                    (filters.text | filters.group)
                    & ~filters.private
                    & ~filters.me
                    & ~filters.bot
                    & ~filters.audio
                    & ~filters.document
                    & ~filters.photo
                    & ~filters.sticker
                    & ~filters.video
                    & ~filters.poll
                    & ~filters.pinned_message
                    & ~filters.media & filters.create(dor)
                ),
                "group": 6,
            },
            "FILTERS_GC": {
                "query": (
                    filters.create(if_filter_gc)
                    & ~filters.private                 
                    & ~filters.bot
                    & ~filters.me
                    & ~filters.via_bot
                    & ~filters.forwarded
                ),
                "group": 7,
            },
            "FILTERS_GC_BOT": {
                "query": (
                    filters.create(if_filter_gc_bot)
                    & ~filters.private                 
                    & ~filters.bot
                    & ~filters.me
                    & ~filters.via_bot
                    & ~filters.forwarded
                ),
                "group": 8,
            },
            "PROTECT_BOT": {
                "query": (
                    filters.group
                    & ~filters.me
                    & ~filters.bot & filters.create(protect_bot)
                ),
                "group": 9,
            },
            "FILTERS_PV": {
                "query": (
                    filters.create(if_filter_pv)
                    & ~filters.group
                    & ~filters.me
                    & ~filters.bot
                    & ~filters.via_bot
                    & ~filters.forwarded
                ),
                "group": 10,
            },
            "ANTI_SCAM": {
                "query": (
                    filters.text
                    & ~filters.me
                    & ~filters.bot
                    & ~filters.audio
                    & ~filters.document
                    & ~filters.photo
                    & ~filters.sticker
                    & ~filters.video
                    & ~filters.poll
                    & ~filters.pinned_message
                    & ~filters.media & filters.create(antiscam)
                ),
                "group": 11,
            },
            "REPLY": {
                "query": ((filters.group & filters.mentioned) | filters.private) ,
                "group": 12,
            },
        }
        result_query = query_mapping.get(result)

        def decorator(func):
            if result_query:
                async def wrapped_func(client, message):
                    await func(client, message)

                asu.on_message(result_query["query"], group=int(result_query["group"]))(wrapped_func)
                return wrapped_func
            else:
                return func

        return decorator
        
    @staticmethod
    def BOT(command, filter=False):
        def wrapper(func):
            message_filters = (
                filters.command(command) & filter
                if filter
                else filters.command(command)
            )

            @bot.on_message(message_filters)
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def REGEX(command, filter=False):
        def wrapper(func):
            message_filters = (
                filters.regex(command) & filter
                if filter
                else filters.regex(command)
            )

            @bot.on_message(message_filters)
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper
        
    @staticmethod
    def UBOT(command, filter=None):
        if filter is None:
            filter = filters.create(if_sudo)

        def decorator(func):
            @ubot.on_message(ubot.cmd_prefix(command) & filter)
            async def wrapped_func(client, message):
                cmd = message.command[0].lower()
                await update_cmd(bot.me.id, cmd, "TOP", increment=True)
                return await func(client, message)

            return wrapped_func

        return decorator

    @staticmethod
    def INLINE(command):
        def wrapper(func):
            @bot.on_inline_query(filters.regex(command))
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def CALLBACK(command):
        def wrapper(func):
            @bot.on_callback_query(filters.regex(command))
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def PRIVATE(func):
        async def function(client, message):
            if not message.chat.type == ChatType.PRIVATE:
                return await message.reply(f"<b><i>Silahkan gunakan fitur ini di private chat!</b></i>") 
            return await func(client, message)

        return function

    @staticmethod
    def GROUP(func):
        async def function(client, message):
            if message.chat.type not in (ChatType.GROUP, ChatType.SUPERGROUP):
                return await message.reply(f"<b><i>Silahkan gunakan fitur ini di group chat!</i></b>") 
            return await func(client, message)

        return function

    @staticmethod
    def GC(func):
        async def function(client, message):
            if message.chat.type not in (ChatType.GROUP, ChatType.SUPERGROUP, ChatType.CHANNEL):
                return await message.reply(f"<b><i>Silahkan gunakan fitur ini di group/channel chat!</i></b>") 
            return await func(client, message)

        return function
        
    @staticmethod
    def START(func):
        async def function(client, message):
            seved_users = await get_list_from_vars(bot.me.id, "SAVED_USERS")
            user_id = message.from_user.id
            if user_id != OWNER_ID and user_id not in DEVS:
                if user_id not in seved_users:
                    await add_to_vars(bot.me.id, "SAVED_USERS", user_id)
                user_link = f"{message.from_user.first_name} {message.from_user.last_name or ''}"
                formatted_text = f"<b><i>{message.text}\n\nName: {message.from_user.mention}\nID: {user_id}</i></b>"
                buttons = [
                    [
                        InlineKeyboardButton(
                            user_link,
                            url=f"tg://openmessage?user_id={message.from_user.id}",
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "Kirim Pesan",
                            callback_data=f"jawab_pesan {message.from_user.id}",
                        ),
                    ]
                ]
                for anu in DEVS:
                    await bot.send_message(
                        anu,
                        formatted_text,
                        reply_markup=InlineKeyboardMarkup(buttons),
                    )
            return await func(client, message)

        return function