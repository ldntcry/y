import asyncio
import base64
import asyncio
import math
import string
import os
import shlex
import textwrap

from io import BytesIO
from time import time
from base64 import urlsafe_b64decode
from struct import unpack
from attrify import Attrify as Atr

from gc import get_objects
from pyrogram import enums
from PIL import Image, ImageDraw, ImageFont
from pymediainfo import MediaInfo
from pyrogram.enums import ChatType
from pyrogram.errors import *
from usu.core.database.local import *
from pyrogram import Client



def unpackInlineMessage(inline_message_id: str):
    dc_id, message_id, chat_id, query_id = unpack(
        "<iiiq",
        urlsafe_b64decode(
            inline_message_id + "=" * (len(inline_message_id) % 4),
        ),
    )
    temp = {
        "dc_id": dc_id,
        "message_id": message_id,
        "chat_id": int(str(chat_id).replace("-1", "-1001")),
        "query_id": query_id,
        "inline_message_id": inline_message_id,
    }
    return Atr(temp)

async def extract_id(message, text):
    def is_int(text):
        try:
            return int(text)
        except ValueError:
            return None

    if is_int(text) is not None:
        return is_int(text)

    text = text.strip() if text else ''
    chat_id = is_int(text)
    if chat_id:
        return chat_id

    entities = message.entities
    app = message._client

    if entities:
        entity = entities[1 if message.text.startswith("/") else 0]
        if entity.type == enums.MessageEntityType.MENTION:
            user = await app.get_chat(text)
            if user:
                return user.id
        elif entity.type == enums.MessageEntityType.TEXT_MENTION:
            return entity.user.id

    if text.startswith('@') or text.startswith('https://'):
        try:
            chat = await app.get_chat(text)
            return chat.id
        except Exception:
            pass

    return None


async def extract_userid(message, text):
    def is_int(text):
        try:
            int(text)
        except ValueError:
            return False
        return True

    text = text.strip()

    if is_int(text):
        return int(text)

    entities = message.entities
    app = message._client
    
    if entities is not None and len(entities) > 0:
        entity = entities[1 if message.text.startswith("/") else 0]
        if entity.type == enums.MessageEntityType.MENTION:
            try:
                user = await app.get_users(text)
                if user is not None:
                    return user.id
            except Exception as e:
                print(e)
        elif entity.type == enums.MessageEntityType.TEXT_MENTION:
            return entity.user.id

    return None


async def extract_user_and_reason(message, sender_chat=False):
    args = message.text.strip().split()
    text = message.text
    user = None
    reason = None

    if message.reply_to_message:
        reply = message.reply_to_message
        if not reply.from_user and (reply.sender_chat and reply.sender_chat != message.chat.id and sender_chat):
            id_ = reply.sender_chat.id
        elif reply.from_user:
            id_ = reply.from_user.id
        else:
            return None, None

        reason = ' '.join(args[1:]) if len(args) > 1 else None
        return id_, reason

    if len(args) >= 2:
        user = ' '.join(args[1:])
        return await extract_userid(message, user), None

    return user, reason


async def extract_user(message):
    return (await extract_user_and_reason(message))[0]


admins_in_chat = {}


async def list_admins(message):
    global admins_in_chat
    if message.chat.id in admins_in_chat:
        interval = time() - admins_in_chat[message.chat.id]["last_updated_at"]
        if interval < 3600:
            return admins_in_chat[message.chat.id]["data"]

    admins_in_chat[message.chat.id] = {
        "last_updated_at": time(),
        "data": [
            member.user.id
            async for member in message._client.get_chat_members(
                message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS
            )
        ],
    }
    return admins_in_chat[message.chat.id]["data"]




def get_text(message):
    if message.reply_to_message:
        if len(message.command) < 2:
            text = message.reply_to_message.text or message.reply_to_message.caption
        else:
            text = (
                (message.reply_to_message.text or message.reply_to_message.caption)
                + "\n\n"
                + message.text.split(None, 1)[1]
            )
    else:
        if len(message.command) < 2:
            text = ""
        else:
            text = message.text.split(None, 1)[1]
    return text


def get_message(message):
    if message.reply_to_message:
        return message.reply_to_message  # Mengembalikan *seluruh* objek pesan reply
    elif len(message.command) > 1:  # Jika ada teks setelah perintah
        return message.text.split(None, 1)[1]  # Mengembalikan teks setelah perintah
    else:
        return None  # Tidak ada pesan yang valid


async def encode(string):
    string_bytes = string.encode("ascii")
    base64_bytes = base64.urlsafe_b64encode(string_bytes)
    return (base64_bytes.decode("ascii")).strip("=")


async def decode(base64_string):
    base64_string = base64_string.strip("=")
    base64_bytes = (base64_string + "=" * (-len(base64_string) % 4)).encode("ascii")
    string_bytes = base64.urlsafe_b64decode(base64_bytes)
    return string_bytes.decode("ascii")


async def get_data_id(client, query):
    anu = await db.get_list_from_vars(client.me.id, "bcdb")
    chat_types = {
        "all": [ChatType.GROUP, ChatType.SUPERGROUP, ChatType.PRIVATE, ChatType.CHANNEL],
        "global": [ChatType.GROUP, ChatType.SUPERGROUP, ChatType.CHANNEL],
        "group": [ChatType.GROUP, ChatType.SUPERGROUP],
        "channel": [ChatType.CHANNEL],
        "users": [ChatType.PRIVATE],
    }
    usu = []
    async for dialog in client.get_dialogs():
        try:
            if dialog.chat.type in chat_types.get(query, []):
                usu.append(dialog.chat.id)
        except ChannelPrivate as e:
            pass
        except FloodWait as e:
            await asyncio.sleep(e.value)
            if dialog.chat.type in chat_types.get(query, []):
                usu.append(dialog.chat.id)
        except Exception as e:
            pass

    hasil = usu if query != "db" else anu
    return hasil


def extract_type_and_msg(message):
    args = message.text.split(None, 2)
    if len(args) < 2:
        return None, None
    
    type = args[1]
    msg = message.reply_to_message if message.reply_to_message else args[2] if len(args) > 2 else None
    return type, msg


def extract_type_and_text(message):
    args = message.text.split(None, 2)
    if len(args) < 2:
        return None, None

    type = args[1]
    msg = (
        message.reply_to_message.text
        if message.reply_to_message
        else args[2]
        if len(args) > 2
        else None
    )
    return type, msg


class Media_Info:
    def data(media):
        found = False
        media_info = MediaInfo.parse(media)
        for track in media_info.tracks:
            if track.track_type == "Video":
                found = True
                type_ = track.track_type
                format_ = track.format
                duration_1 = track.duration
                other_duration_ = track.other_duration
                duration_2 = (
                    f"{other_duration_[0]} - ({other_duration_[3]})"
                    if other_duration_
                    else None
                )
                pixel_ratio_ = [track.width, track.height]
                aspect_ratio_1 = track.display_aspect_ratio
                other_aspect_ratio_ = track.other_display_aspect_ratio
                aspect_ratio_2 = other_aspect_ratio_[0] if other_aspect_ratio_ else None
                fps_ = track.frame_rate
                fc_ = track.frame_count
                media_size_1 = track.stream_size
                other_media_size_ = track.other_stream_size
                media_size_2 = (
                    [
                        other_media_size_[1],
                        other_media_size_[2],
                        other_media_size_[3],
                        other_media_size_[4],
                    ]
                    if other_media_size_
                    else None
                )

        dict_ = (
            {
                "media_type": type_,
                "format": format_,
                "duration_in_ms": duration_1,
                "duration": duration_2,
                "pixel_sizes": pixel_ratio_,
                "aspect_ratio_in_fraction": aspect_ratio_1,
                "aspect_ratio": aspect_ratio_2,
                "frame_rate": fps_,
                "frame_count": fc_,
                "file_size_in_bytes": media_size_1,
                "file_size": media_size_2,
            }
            if found
            else None
        )
        return dict_


def get_arg(message):
    if message.reply_to_message and len(message.command) < 2:
        msg = message.reply_to_message.text or message.reply_to_message.caption
        if not msg:
            return ""
        msg = msg.encode().decode("UTF-8")
        if len(msg) > 1:
            msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
        return msg
    elif len(message.command) > 1:
        return " ".join(message.command[1:])
    else:
        return ""



async def resize_media(media, video, fast_forward):
    if video:
        info_ = Media_Info.data(media)
        width = info_["pixel_sizes"][0]
        height = info_["pixel_sizes"][1]
        sec = info_["duration_in_ms"]
        s = round(float(sec)) / 1000

        if height == width:
            height, width = 512, 512
        elif height > width:
            height, width = 512, -1
        elif width > height:
            height, width = -1, 512

        resized_video = f"{media}.webm"
        if fast_forward:
            if s > 3:
                fract_ = 3 / s
                ff_f = round(fract_, 2)
                set_pts_ = ff_f - 0.01 if ff_f > fract_ else ff_f
                cmd_f = f"-filter:v 'setpts={set_pts_}*PTS',scale={width}:{height}"
            else:
                cmd_f = f"-filter:v scale={width}:{height}"
        else:
            cmd_f = f"-filter:v scale={width}:{height}"
        fps_ = float(info_["frame_rate"])
        fps_cmd = "-r 30 " if fps_ > 30 else ""
        cmd = f"ffmpeg -i {media} {cmd_f} -ss 00:00:00 -to 00:00:03 -an -c:v libvpx-vp9 {fps_cmd}-fs 256K {resized_video}"
        _, error, __, ___ = await run_cmd(cmd)
        os.remove(media)
        return resized_video

    image = Image.open(media)
    maxsize = 512
    scale = maxsize / max(image.width, image.height)
    new_size = (int(image.width * scale), int(image.height * scale))

    image = image.resize(new_size, Image.LANCZOS)
    resized_photo = "sticker.png"
    image.save(resized_photo)
    os.remove(media)
    return resized_photo


async def add_text_img(image_path, text):
    font_size = 12
    stroke_width = 1

    if ";" in text:
        upper_text, lower_text = text.split(";")
    else:
        upper_text = text
        lower_text = ""

    img = Image.open(image_path).convert("RGBA")
    img_info = img.info
    image_width, image_height = img.size
    font = ImageFont.truetype(
        font="storage/default.ttf",
        size=int(image_height * font_size) // 100,
    )
    draw = ImageDraw.Draw(img)

    char_width, char_height = font.getsize("A")
    chars_per_line = image_width // char_width
    top_lines = textwrap.wrap(upper_text, width=chars_per_line)
    bottom_lines = textwrap.wrap(lower_text, width=chars_per_line)

    if top_lines:
        y = 10
        for line in top_lines:
            line_width, line_height = font.getsize(line)
            x = (image_width - line_width) / 2
            draw.text(
                (x, y),
                line,
                fill="white",
                font=font,
                stroke_width=stroke_width,
                stroke_fill="black",
            )
            y += line_height

    if bottom_lines:
        y = image_height - char_height * len(bottom_lines) - 15
        for line in bottom_lines:
            line_width, line_height = font.getsize(line)
            x = (image_width - line_width) / 2
            draw.text(
                (x, y),
                line,
                fill="white",
                font=font,
                stroke_width=stroke_width,
                stroke_fill="black",
            )
            y += line_height

    final_image = os.path.join("memify.webp")
    img.save(final_image, **img_info)
    return final_image


async def aexec(code, user, message):
    exec(
        "async def __aexec(user, message): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](user, message)


async def bash(cmd):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    err = stderr.decode().strip()
    out = stdout.decode().strip()
    return out, err


async def run_cmd(cmd):
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )


async def edit_or_reply(message, text):
    msg = (
        message.reply_text
        if bool(message.from_user and message.from_user.is_self or message.outgoing)
        else (message.reply_to_message or message).reply_text
    )
    return await msg(text)


eor = edit_or_reply



def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


async def dl_pic(client, download):
    path = await client.download_media(download)
    with open(path, "rb") as f:
        content = f.read()
    os.remove(path)
    get_photo = BytesIO(content)
    return get_photo


def humanbytes(size):
    if not size:
        return ""
    power = 2**10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "ᴋʙ", 2: "ᴍʙ", 3: "ɢʙ", 4: "ᴛʙ"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return f"{str(round(size, 2))} {dict_power_n[raised_to_pow]}"


def time_formatter(milliseconds):
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        (f"{str(days)} ʜᴀʀɪ, " if days else "")
        + (f"{str(hours)} ᴊᴀᴍ, " if hours else "")
        + (f"{str(minutes)} ᴍᴇɴɪᴛ, " if minutes else "")
        + (f"{str(seconds)} ᴅᴇᴛɪᴋ, " if seconds else "")
        + (f"{str(milliseconds)} ᴍɪᴋʀᴏᴅᴇᴛɪᴋ, " if milliseconds else "")
    )
    return tmp[:-2]


async def progress(current, total, message, start, type_of_ps, file_name=None):
    now = time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        if elapsed_time == 0:
            return
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "💢 ᴘᴇʀsᴇɴᴛᴀsᴇ: {0}{1} {2}%\n".format(
            "".join("°" for _ in range(math.floor(percentage / 10))),
            "".join("-" for _ in range(10 - math.floor(percentage / 10))),
            round(percentage, 2),
        )
        tmp = "📂 ғɪʟᴇ_sɪᴢᴇ: {0} - {1}\n{3}\n⏳ ᴇsᴛɪᴍᴀsɪ: {2}\n".format(
            humanbytes(current),
            humanbytes(total),
            time_formatter(estimated_total_time),
            progress_str,
        )
        if file_name:
            try:
                await message.edit(
                    f"""
<b>📥 {type_of_ps}</b>

<b>🆔 ғɪʟᴇ_ɪᴅ:</b> <code>{file_name}</code>
<b>{tmp}</b>
"""
                )
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except MessageNotModified:
                pass
        else:
            try:
                await message.edit(f"{type_of_ps}\n{tmp}")
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except MessageNotModified:
                pass


