import os
import platform
import subprocess
import sys
import traceback
from datetime import datetime
from io import BytesIO, StringIO
from meval import meval
import asyncio

import inspect
import io
import pyrogram
import re
import uuid

from html import escape
from meval import meval
from pyrogram import filters
from typing import Any, Optional, Tuple, Union, List

import psutil
import socket


from usu import *
from usu.__main__ import stopped
from usu.config import OWNER_ID
from usu.core.database.local import db

def format_exception(exp: BaseException,
                     tb: Optional[List[traceback.FrameSummary]] = None) -> str:
    """Formats an exception traceback as a string, similar to the Python interpreter."""

    if tb is None:
        tb = traceback.extract_tb(exp.__traceback__)

    # Replace absolute paths with relative paths
    cwd = os.getcwd()
    for frame in tb:
        if cwd in frame.filename:
            frame.filename = os.path.relpath(frame.filename)

    stack = "".join(traceback.format_list(tb))
    msg = str(exp)
    if msg:
        msg = ": " + msg

    return f"Traceback (most recent call last):\n{stack}{type(exp).__name__}{msg}"

def format_duration_us(t_us: Union[int, float]) -> str:
    """Formats the given microsecond duration as a string."""

    t_us = int(t_us)

    t_ms = t_us / 1000
    t_s = t_ms / 1000
    t_m = t_s / 60
    t_h = t_m / 60
    t_d = t_h / 24

    if t_d >= 1:
        rem_h = t_h % 24
        return "%dd %dh" % (t_d, rem_h)

    if t_h >= 1:
        rem_m = t_m % 60
        return "%dh %dm" % (t_h, rem_m)

    if t_m >= 1:
        rem_s = t_s % 60
        return "%dm %ds" % (t_m, rem_s)

    if t_s >= 1:
        return "%d sec" % t_s

    if t_ms >= 1:
        return "%d ms" % t_ms

    return "%d μs" % t_us

def usec() -> int:
    """Returns the current time in microseconds since the Unix epoch."""

    return int(time() * 1000000)




@USU.UBOT("eval")
@USU.DEVS
async def exec_eval(c, m):
    sks = await EMO.SUKSES(c)
    ggl = await EMO.GAGAL(c)
    prs = await EMO.PROSES(c)
    broad = await EMO.BROADCAST(c)
    ptr = await EMO.PUTARAN(c)
    if m.reply_to_message and len(m.text.split()) > 1:
        code = m.text.split(" ", maxsplit=1)[1]
    elif m.reply_to_message and len(m.text.split()) == 1:
        code = m.reply_to_message.text
    elif len(m.text.split()) > 1:
        code = m.text.split(" ", maxsplit=1)[1]
    else:
        return await m.reply_text(f"<i><b>{ggl}{m.text} [reply/teks]</b></i>")
    usu = await m.reply_text(f"<i><b>{prs}Processing...</b></i>")
    out_buf = io.StringIO()
    async def _eval() -> Tuple[str, Optional[str]]:
            async def send(*args: Any, **kwargs: Any) -> pyrogram.types.Message:
                    return await m.reply(*args, **kwargs)

            def _print(*args: Any, **kwargs: Any) -> None:
                    if "file" not in kwargs:
                            kwargs["file"] = out_buf
                            return print(*args, **kwargs)

            eval_vars = {
    "MSG": MSG,
    "db": db,
    "BTN": BTN,
    "ubot": ubot,
    "bot": bot,
    "USU": USU,
    # Informasi Konteks
    "loop": c.loop,
    "client": c,
    "stdout": out_buf,
    # Alias Kenyamanan
    "c": c,
    "m": m,
    "msg": m,
    "message": m,
    "raw": pyrogram.raw,
    # Fungsi Pembantu
    "send": send,
    "print": _print,
    # Modul Bawaan
    "inspect": inspect,
    "os": os,
    "re": re,
    "sys": sys,
    "traceback": traceback,
    "pyrogram": pyrogram,
    # Tipe Pyrogram
    "Client": pyrogram.Client,
    "Message": pyrogram.types.Message,
    "User": pyrogram.types.User,
    "Chat": pyrogram.types.Chat,
    "CallbackQuery": pyrogram.types.CallbackQuery,
    "InlineQuery": pyrogram.types.InlineQuery,
    "InlineKeyboardButton": pyrogram.types.InlineKeyboardButton,
    "InlineKeyboardMarkup": pyrogram.types.InlineKeyboardMarkup,
    "ReplyKeyboardMarkup": pyrogram.types.ReplyKeyboardMarkup,
    "ReplyKeyboardRemove": pyrogram.types.ReplyKeyboardRemove,
    "ForceReply": pyrogram.types.ForceReply,
    "InlineQueryResultArticle": pyrogram.types.InlineQueryResultArticle,
    "InputTextMessageContent": pyrogram.types.InputTextMessageContent,
    "InlineQueryResultCachedPhoto": pyrogram.types.InlineQueryResultCachedPhoto,
    "InlineQueryResultPhoto": pyrogram.types.InlineQueryResultPhoto,
            }

            try:
                    return "", await meval(code, globals(), **eval_vars)
            except Exception as e:  # skipcq: PYL-W0703
                    # Find first traceback frame involving the snippet
                    first_snip_idx = -1
                    tb = traceback.extract_tb(e.__traceback__)
                    for i, frame in enumerate(tb):
                            if frame.filename == "<string>" or frame.filename.endswith("ast.py"):
                                first_snip_idx = i
                                break


                    if first_snip_idx == -1:
                            raise e

                    stripped_tb = tb[first_snip_idx:]
                    formatted_tb = format_exception(e, tb=stripped_tb)
                    return "Error!\n\n", formatted_tb
    before = usec()
    prefix, result = await _eval()
    after = usec()

    if not out_buf.getvalue() or result is not None:
            print(result, file=out_buf)

    el_us = after - before
    el_str = format_duration_us(el_us)

    out = out_buf.getvalue()

    if out.endswith("\n"):
            out = out[:-1]

    result = f"""{prefix}<b>In:</b>
<pre language="python">{escape(code)}</pre>
<b>Out:</b>
<pre language="python">{escape(out)}</pre>
Time: {el_str}"""

    if len(result) > 4096:
            with io.BytesIO(str.encode(out)) as out_file:
                    out_file.name = str(uuid.uuid4()).split("-")[0].upper() + ".txt"
                    caption = f"""{prefix}<b>In:</b>
<pre language="python">{escape(code)}</pre>

Time: {el_str}"""
                    await m.reply_document(
                                document=out_file, caption=caption, disable_notification=True,parse_mode=pyrogram.enums.parse_mode.ParseMode.HTML
                        )
            None
    else:
        await m.reply_text(
            result,
            parse_mode=pyrogram.enums.parse_mode.ParseMode.HTML,
    )
    await usu.delete()



@USU.BOT("eval")
@USU.DEVS
async def exec_eval(c: Client, m: Message):
    if m.reply_to_message and len(m.text.split()) > 1:
        code = m.text.split(" ", maxsplit=1)[1]
    elif m.reply_to_message and len(m.text.split()) == 1:
        code = m.reply_to_message.text
    elif len(m.text.split()) > 1:
        code = m.text.split(" ", maxsplit=1)[1]
    else:
        return await m.reply_text(f"<i><b>{m.text} [reply/teks]</b></i>")
    usu = await m.reply_text(f"<i><b>Processing...</b></i>")
    code = m.text.split(" ", maxsplit=1)[1]
    out_buf = io.StringIO()
    async def _eval() -> Tuple[str, Optional[str]]:
            async def send(*args: Any, **kwargs: Any) -> pyrogram.types.Message:
                    return await m.reply(*args, **kwargs)

            def _print(*args: Any, **kwargs: Any) -> None:
                    if "file" not in kwargs:
                            kwargs["file"] = out_buf
                            return print(*args, **kwargs)

            eval_vars = {
    "MSG": MSG,
    "db": db,
    "BTN": BTN,
    "ubot": ubot,
    "bot": bot,
    "USU": USU,
    # Informasi Konteks
    "loop": c.loop,
    "client": c,
    "stdout": out_buf,
    # Alias Kenyamanan
    "c": c,
    "m": m,
    "msg": m,
    "message": m,
    "raw": pyrogram.raw,
    # Fungsi Pembantu
    "send": send,
    "print": _print,
    # Modul Bawaan
    "inspect": inspect,
    "os": os,
    "re": re,
    "sys": sys,
    "traceback": traceback,
    "pyrogram": pyrogram,
    # Tipe Pyrogram
    "Client": pyrogram.Client,
    "Message": pyrogram.types.Message,
    "User": pyrogram.types.User,
    "Chat": pyrogram.types.Chat,
    "CallbackQuery": pyrogram.types.CallbackQuery,
    "InlineQuery": pyrogram.types.InlineQuery,
    "InlineKeyboardButton": pyrogram.types.InlineKeyboardButton,
    "InlineKeyboardMarkup": pyrogram.types.InlineKeyboardMarkup,
    "ReplyKeyboardMarkup": pyrogram.types.ReplyKeyboardMarkup,
    "ReplyKeyboardRemove": pyrogram.types.ReplyKeyboardRemove,
    "ForceReply": pyrogram.types.ForceReply,
    "InlineQueryResultArticle": pyrogram.types.InlineQueryResultArticle,
    "InputTextMessageContent": pyrogram.types.InputTextMessageContent,
    "InlineQueryResultCachedPhoto": pyrogram.types.InlineQueryResultCachedPhoto,
    "InlineQueryResultPhoto": pyrogram.types.InlineQueryResultPhoto,
            }

            try:
                    return "", await meval(code, globals(), **eval_vars)
            except Exception as e:  # skipcq: PYL-W0703
                    # Find first traceback frame involving the snippet
                    first_snip_idx = -1
                    tb = traceback.extract_tb(e.__traceback__)
                    for i, frame in enumerate(tb):
                            if frame.filename == "<string>" or frame.filename.endswith("ast.py"):
                                first_snip_idx = i
                                break


                    if first_snip_idx == -1:
                            raise e

                    stripped_tb = tb[first_snip_idx:]
                    formatted_tb = format_exception(e, tb=stripped_tb)
                    return "Error!\n\n", formatted_tb
    before = usec()
    prefix, result = await _eval()
    after = usec()

    if not out_buf.getvalue() or result is not None:
            print(result, file=out_buf)

    el_us = after - before
    el_str = format_duration_us(el_us)

    out = out_buf.getvalue()

    if out.endswith("\n"):
            out = out[:-1]

    result = f"""{prefix}<b>In:</b>
<pre language="python">{escape(code)}</pre>
<b>Out:</b>
<pre language="python">{escape(out)}</pre>
Time: {el_str}"""

    if len(result) > 4096:
            with io.BytesIO(str.encode(out)) as out_file:
                    out_file.name = str(uuid.uuid4()).split("-")[0].upper() + ".txt"
                    caption = f"""{prefix}<b>In:</b>
<pre language="python">{escape(code)}</pre>

Time: {el_str}"""
                    await m.reply_document(
                                document=out_file, caption=caption, disable_notification=True,parse_mode=pyrogram.enums.parse_mode.ParseMode.HTML
                        )
            None
    else:
        await m.reply_text(
            result,
            parse_mode=pyrogram.enums.parse_mode.ParseMode.HTML,
    )
    await usu.delete()





@USU.UBOT("sh")
@USU.DEVS
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    command = get_arg(message)
    msg = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    if not command:
        return await msg.edit(f"<i><b>{ggl}Invalid!</b></i>")
    try:
        if command == "shutdown":
            await msg.delete()
            await handle_shutdown(message)
        elif command == "restart":
            await msg.delete()
            await handle_restart(message)
        elif command == "update":
            await msg.delete()
            await handle_update(message)
        elif command == "clean":
            await msg.delete()
            await handle_clean(message)
        else:
            await process_command(message, command)
            await msg.delete()
    except Exception as error:
        await message.reply(error)

@USU.BOT("sh")
@USU.DEVS
async def _(client, message):
    command = get_arg(message)
    msg = await message.reply(f"<i><b>Processing...</b></i>")
    if not command:
        return await msg.edit(f"<i><b>Invalid!</b></i>")
    try:
        if command == "shutdown":
            await msg.delete()
            await handle_shutdown(message)
        elif command == "restart":
            await msg.delete()
            await handle_restart(message)
        elif command == "update":
            await msg.delete()
            await handle_update(message)
        elif command == "clean":
            await msg.delete()
            await handle_clean(message)
        else:
            await process_command(message, command)
            await msg.delete()
    except Exception as error:
        await message.reply(error)

async def handle_clean(message):
    # Define paths to clean
    temp_dirs = ['/tmp', '/var/tmp', 'path_to_cache_directory']

    deleted_files = 0
    deleted_dirs = 0

    for temp_dir in temp_dirs:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                try:
                    os.remove(os.path.join(root, file))
                    deleted_files += 1
                except Exception as e:
                    pass
            for dir in dirs:
                try:
                    os.rmdir(os.path.join(root, dir))
                    deleted_dirs += 1
                except Exception as e:
                    pass

    await message.reply(f"<i><b>System cleaned!</b></i>", quote=True)


async def handle_shutdown(message):
    await message.reply(f"<i><b>System turned off!</b></i>", quote=True)
    await stopped()
    os.system(f"kill -9 {os.getpid()}")


async def handle_restart(message):
    await message.reply(f"<i><b>System restarted!</b></i>", quote=True)
    await stopped()
    os.system(f"kill -9 {os.getpid()} && bash start.sh")


async def handle_update(message):
    out = subprocess.check_output(["git", "pull"]).decode("UTF-8")
    if "Already up to date." in str(out):
        return await message.reply(f"<pre>{out}</pre>", quote=True)
    elif int(len(str(out))) > 4096:
        await send_large_output(message, out)
    else:
        await message.reply(f"<pre>{out}</pre>", quote=True)
    await stopped()
    os.system(f"kill -9 {os.getpid()} && bash start.sh")

async def process_command(message, command):
    result = (await bash(command))[0]
    if int(len(str(result))) > 4096:
        await send_large_output(message, result)
    else:
        await message.reply(f"<pre>{result}</pre>")


async def send_large_output(message, output):
    with BytesIO(str.encode(str(output))) as out_file:
        out_file.name = "result.txt"
        await message.reply_document(document=out_file)


@USU.UBOT("trash")
@USU.DEVS
async def _(client, message):
    if message.reply_to_message:
        try:
            if len(message.command) < 2:
                if len(str(message.reply_to_message)) > 4096:
                    with BytesIO(str.encode(str(message.reply_to_message))) as out_file:
                        out_file.name = "trash.txt"
                        return await message.reply_document(document=out_file)
                else:
                    return await message.reply(message.reply_to_message)
            else:
                value = eval(f"message.reply_to_message.{message.command[1]}")
                return await message.reply(value)
        except Exception as error:
            return await message.reply(str(error))
    else:
        return await message.reply(f"<b><i>Invalid!</i></b>")


@USU.UBOT("sys")
@USU.DEVS
async def _(client, message):
    usu = ["<b>Processing...</b>", "<b>Checking Your System...</b>", "<b>Collect Your System...</b>"]
    usu_msg = await message.reply(f"<i>{usu[0]}</i>")
    for usu_text in usu[1:]:
        await asyncio.sleep(1)
        await usu_msg.edit_text(f"<i>{usu_text}</i>")
    await asyncio.sleep(1)

    uname = platform.uname()
    nama_host = socket.gethostname()
    cpufreq = psutil.cpu_freq()
    svmem = psutil.virtual_memory()
    penggunaan_disk = psutil.disk_usage("/")

    softw = f"<i><b>Information!</b></i>\n\n"
    softw += f"<b>System :</b> <code>{uname.system}</code>\n"
    softw += f"<b>Release :</b> <code>{uname.release}</code>\n"
    softw += f"<b>Version :</b> <code>{uname.version}</code>\n"
    softw += f"<b>Machine :</b> <code>{uname.machine}</code>\n"
    softw += f"<b>Host :</b> <code>{nama_host}</code>\n\n"

    softw += f"<b>CPU :</b>\n"
    softw += f"<b>Physical Core :</b> <code>{psutil.cpu_count(logical=False)}</code>\n"
    softw += f"<b>Total Core :</b> <code>{psutil.cpu_count(logical=True)}</code>\n"
    softw += f"<b>Max Frequency :</b> <code>{cpufreq.max:.2f}Mhz</code>\n"
    softw += f"<b>Min Frequency :</b> <code>{cpufreq.min:.2f}Mhz</code>\n"
    softw += f"<b>Current Frequency :</b> <code>{cpufreq.current:.2f}Mhz</code>\n\n"

    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        softw += f"<b>Core {i} :</b> <code>{percentage}%</code>\n"
    softw += f"<b>All Core :</b> <code>{psutil.cpu_percent()}%</code>\n\n"

    softw += f"<b>Network :</b>\n"
    softw += f"<b>Upload :</b> <code>{get_size(psutil.net_io_counters().bytes_sent)}</code>\n"
    softw += f"<b>Download :</b> <code>{get_size(psutil.net_io_counters().bytes_recv)}</code>\n\n"

    softw += f"<b>Memory :</b>\n"
    softw += f"<b>Total :</b> <code>{get_size(svmem.total)}</code>\n"
    softw += f"<b>Available :</b> <code>{get_size(svmem.available)}</code>\n"
    softw += f"<b>Used :</b> <code>{get_size(svmem.used)}</code>\n"
    softw += f"<b>Percentage :</b> <code>{svmem.percent}%</code>\n\n"

    softw += f"<b>Disk :</b> <code>{humanbytes(penggunaan_disk.used)} / {humanbytes(penggunaan_disk.total)} ({penggunaan_disk.percent}%)</code>\n"

    await usu_msg.edit(f"<i><b>{softw}</b></i>")


@USU.BOT("sys")
@USU.DEVS
async def _(client, message):
    usu = ["<b>Processing...</b>", "<b>Checking Your System...</b>", "<b>Collect Your System...</b>"]
    usu_msg = await message.reply(f"<i>{usu[0]}</i>")
    for usu_text in usu[1:]:
        await asyncio.sleep(1)
        await usu_msg.edit_text(f"<i>{usu_text}</i>")
    await asyncio.sleep(1)

    uname = platform.uname()
    nama_host = socket.gethostname()
    cpufreq = psutil.cpu_freq()
    svmem = psutil.virtual_memory()
    penggunaan_disk = psutil.disk_usage("/")

    softw = f"<i><b>Information!</b></i>\n\n"
    softw += f"<b>System :</b> <code>{uname.system}</code>\n"
    softw += f"<b>Release :</b> <code>{uname.release}</code>\n"
    softw += f"<b>Version :</b> <code>{uname.version}</code>\n"
    softw += f"<b>Machine :</b> <code>{uname.machine}</code>\n"
    softw += f"<b>Host :</b> <code>{nama_host}</code>\n\n"

    softw += f"<b>CPU :</b>\n"
    softw += f"<b>Physical Core :</b> <code>{psutil.cpu_count(logical=False)}</code>\n"
    softw += f"<b>Total Core :</b> <code>{psutil.cpu_count(logical=True)}</code>\n"
    softw += f"<b>Max Frequency :</b> <code>{cpufreq.max:.2f}Mhz</code>\n"
    softw += f"<b>Min Frequency :</b> <code>{cpufreq.min:.2f}Mhz</code>\n"
    softw += f"<b>Current Frequency :</b> <code>{cpufreq.current:.2f}Mhz</code>\n\n"

    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        softw += f"<b>Core {i} :</b> <code>{percentage}%</code>\n"
    softw += f"<b>All Core :</b> <code>{psutil.cpu_percent()}%</code>\n\n"

    softw += f"<b>Network :</b>\n"
    softw += f"<b>Upload :</b> <code>{get_size(psutil.net_io_counters().bytes_sent)}</code>\n"
    softw += f"<b>Download :</b> <code>{get_size(psutil.net_io_counters().bytes_recv)}</code>\n\n"

    softw += f"<b>Memory :</b>\n"
    softw += f"<b>Total :</b> <code>{get_size(svmem.total)}</code>\n"
    softw += f"<b>Available :</b> <code>{get_size(svmem.available)}</code>\n"
    softw += f"<b>Used :</b> <code>{get_size(svmem.used)}</code>\n"
    softw += f"<b>Percentage :</b> <code>{svmem.percent}%</code>\n\n"

    softw += f"<b>Disk :</b> <code>{humanbytes(penggunaan_disk.used)} / {humanbytes(penggunaan_disk.total)} ({penggunaan_disk.percent}%)</code>\n"

    await usu_msg.edit(f"<i><b>{softw}</b></i>")



@USU.UBOT("run")
@USU.DEVS
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)

    code: Optional[str] = None
    if message.reply_to_message:
        if len(message.text.split()) > 1:
            code = message.text.split(" ", maxsplit=1)[1]
        else:
            code = message.reply_to_message.text
    elif len(message.text.split()) > 1:
        code = message.text.split(" ", maxsplit=1)[1]

    if not code:
        return await message.reply_text(
            f"<i><b>{ggl} Penggunaan: {message.text.split()[0]} [kode] atau balas pesan dengan {message.text.split()[0]}</b></i>",
            parse_mode=ParseMode.HTML
        )

    usu_msg = await message.reply_text(f"<i><b>{prs}Processing...</b></i>", parse_mode=ParseMode.HTML)

    out_buf = io.StringIO()

    async def _eval_executor() -> Tuple[str, Optional[str]]:
        async def send(*args: Any, **kwargs: Any) -> Message:
            return await message.reply(*args, **kwargs)

        def _print(*args: Any, **kwargs: Any) -> None:
            if "file" not in kwargs:
                kwargs["file"] = out_buf
            return print(*args, **kwargs)

        eval_vars = {
            "MSG": MSG,
            "db": db,
            "BTN": BTN,
            "ubot": ubot,
            "bot": bot,
            "USU": USU,
            "loop": client.loop,
            "client": client,
            "stdout": out_buf,
            "c": client,
            "m": message,
            "msg": message,
            "message": message,
            "raw": pyrogram.raw,
            "send": send,
            "print": _print,
            "inspect": inspect,
            "os": os,
            "re": re,
            "sys": sys,
            "traceback": traceback,
            "pyrogram": pyrogram,
            "asyncio": asyncio,
            "Client": pyrogram.Client,
            "Message": Message,
            "User": pyrogram.types.User,
            "Chat": pyrogram.types.Chat,
            "CallbackQuery": CallbackQuery,
            "InlineQuery": InlineQuery,
            "InlineKeyboardButton": pyrogram.types.InlineKeyboardButton,
            "InlineKeyboardMarkup": pyrogram.types.InlineKeyboardMarkup,
            "ReplyKeyboardMarkup": pyrogram.types.ReplyKeyboardMarkup,
            "ReplyKeyboardRemove": pyrogram.types.ReplyKeyboardRemove,
            "ForceReply": pyrogram.types.ForceReply,
            "InlineQueryResultArticle": pyrogram.types.InlineQueryResultArticle,
            "InputTextMessageContent": pyrogram.types.InputTextMessageContent,
            "InlineQueryResultCachedPhoto": pyrogram.types.InlineQueryResultCachedPhoto,
            "InlineQueryResultPhoto": pyrogram.types.InlineQueryResultPhoto,
        }

        try:
            # Panggil fungsi meval (yang diimpor dari library)
            return "", await meval(code, globals(), **eval_vars)
        except Exception as e:
            first_snip_idx = -1
            tb = traceback.extract_tb(e.__traceback__)
            for i, frame in enumerate(tb):
                if frame.filename == "<string>" or (frame.filename and frame.filename.endswith("ast.py")):
                    first_snip_idx = i
                    break

            if first_snip_idx == -1:
                raise e

            stripped_tb = tb[first_snip_idx:]
            formatted_tb = "".join(traceback.format_list(stripped_tb)) + f"\n{type(e).__name__}: {e}"
            return "Error!\n\n", formatted_tb

    before = usec()
    prefix, result_from_eval = await _eval_executor()
    after = usec()

    if not out_buf.getvalue() and result_from_eval is not None:
        _print(result_from_eval)

    out = out_buf.getvalue()

    if out.endswith("\n"):
        out = out[:-1]

    el_str = format_duration_us(after - before)

    final_output_message = f"""{prefix}<b>In:</b>
<pre language="python">{escape(code)}</pre>
<b>Out:</b>
<pre language="python">{escape(out)}</pre>
Time: {el_str}"""

    if len(final_output_message) > 4096:
        with io.BytesIO(str.encode(out)) as out_file:
            out_file.name = str(uuid.uuid4()).split("-")[0].upper() + ".txt"
            caption = f"""{prefix}<b>In:</b>
<pre language="python">{escape(code)}</pre>
Time: {el_str}"""
            await message.reply_document(
                document=out_file,
                caption=caption,
                disable_notification=True,
                parse_mode=ParseMode.HTML
            )
    else:
        await message.reply_text(
            final_output_message,
            parse_mode=ParseMode.HTML,
        )

    await usu_msg.delete()


