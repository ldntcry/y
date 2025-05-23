import asyncio
from random import randint

from pytgcalls.types import *
from pytgcalls.exceptions import *
from youtubesearchpython import VideosSearch

from pyrogram import *
from pyrogram.types import *
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.raw.types import InputPeerChannel, InputPeerChat
from pyrogram.errors import FloodWait, MessageNotModified

from usu import *


@USU.CALLBACK("^music")
async def _(c, cq):
    button = BTN.TAMBAH()
    pesan = f"""<i><b>Halo,
Saya adalah menu [Music]({PHOTO})

Command Devs:</b>
/activevc - melihat semua chat yang sedang memainkan music
/setname - mengganti nama assistant music
/setbio - mengganti bio assistant music

<b>Command Admins:</b>
/play or /vplay - memutar music
/end - hentikan music
/skip - memutar antrian music
/resume - melanjutkan music
/pause - jeda music
/playlist - lihat daftar antrian music</i>"""
    return await cq.edit_message_text(pesan, reply_markup=InlineKeyboardMarkup(button))


playlist = {}
paused = {}
waw = 0


@ubot.usu_stream()
async def leave_and_play_next(client, update):
    chat_id = update.chat_id

    if client.me.id in playlist and chat_id in playlist[client.me.id] and len(playlist[client.me.id][chat_id]) > 1:
        try:
            lagu_berikutnya = playlist[client.me.id][chat_id][1]['lagu']
            await client.play(chat_id, MediaStream(lagu_berikutnya))
            if playlist[client.me.id][chat_id]:
                playlist[client.me.id][chat_id].pop(0)
        except Exception as e:
            print(e)
    if client.me.id in playlist and chat_id in playlist[client.me.id] and len(playlist[client.me.id][chat_id]) == 1:
        try:
            await client.leave_call(chat_id)
            del playlist[client.me.id][chat_id]
        except NoActiveGroupCall:
            pass


@bot.usu_stream()
async def leave_and_play_next(client, update):
    chat_id = update.chat_id
    if chat_id in playlist and len(playlist[chat_id]) > 1:
        try:
            lagu_berikutnya = playlist[chat_id][1]['lagu']
            await client.play(chat_id, MediaStream(lagu_berikutnya))
            if playlist[chat_id]:
                playlist[chat_id].pop(0)
        except Exception as e:
            print(e)
    elif chat_id in playlist and len(playlist[chat_id]) == 1:
        try:
            await client.leave_call(chat_id)
            del playlist[chat_id]
        except NoActiveGroupCall:
            pass


async def gabung(usu, message):
    if FSUB:
        buttons = []
        anu = []
        for channel in FSUB:
            try:
                await usu.get_chat_member(channel, message.from_user.id)
            except UserNotParticipant:
                link = await usu.export_chat_invite_link(channel)
                anu.append(InlineKeyboardButton(f"{channel}", url=link))
                if len(anu) == 2:
                    buttons.append(anu)
                    anu = []
        if anu:
            buttons.append(anu)
        if buttons:
            kontol = InlineKeyboardMarkup(buttons)
            await message.reply_text(f"<b><i>Halo {message.from_user.mention},\nSilahkan bergabung terlebih dahulu ke Support chat!</i></b>", reply_markup=kontol)
            return False
        return True


@USU.UBOT("playlist")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    anu = await message.reply(f"<i><b>{prs}Processing...</b></i>")

    if message.chat.id not in playlist[client.me.id]:
        await anu.edit(f"<i><b>{ggl}Playlist kosong!</b></i>")
    else:
        text = f"<i><b>{broad}Sedang diputar:</b>\n{playlist[client.me.id][message.chat.id][0]['judul']}\n\n"
        if len(playlist[client.me.id][message.chat.id]) > 1:
            text += f"<b>{ptr}Daftar antrian:</b>\n"
            for i, lagu in enumerate(playlist[client.me.id][message.chat.id][1:], start=1):
                text += f"{i}.{lagu['judul']}\n\n"
        text += "</i>"
        await anu.edit(text)


@USU.UBOT("play")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    if message.reply_to_message:
        media = message.reply_to_message.audio if message.reply_to_message.audio else message.reply_to_message.voice if message.reply_to_message.voice else message.reply_to_message.video
        teks = message.reply_to_message.text
        if teks:
            query = teks
            infomsg = await message.reply(f"<i><b>{prs}Processing...</b></i>")
            try:
                search_result = VideosSearch(query, limit=1).result()["result"][0]
                link = f"https://youtu.be/{search_result['id']}"
            except Exception:
                return await infomsg.edit(f"<i><b>{ggl}Pencarian music gagal!</b></i>")

            try:
                file_name, title, url, duration, views, channel, thumb, data_ytp = await YoutubeDownload(link, as_video=False)
            except Exception:
                return await infomsg.edit(f"<i><b>{ggl}Gagal memutar music!</b></i>")
            nama = "Audio"
        elif media:
            infomsg = await message.reply(f"<i><b>{prs}Downloading {'Audio' if message.reply_to_message.audio else 'Voice' if message.reply_to_message.voice else 'Video'}...</b></i>")
            async def progress(current, total):
                percent = round((current / total) * 100)
                global waw
                if percent != waw:
                    waw = percent
                    try:
                        await infomsg.edit(f"<i><b>{prs}Downloading {'Audio' if message.reply_to_message.audio else 'Voice' if message.reply_to_message.voice else 'Video'} {percent}%...</b></i>")
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                        try:
                            await infomsg.edit(f"<i><b>{prs}Downloading {'Audio' if message.reply_to_message.audio else 'Voice' if message.reply_to_message.voice else 'Video'} {percent}%...</b></i>")
                        except Exception as e:
                            await infomsg.edit(e)
                    except Exception as e:
                        await infomsg.edit(e)
            file_name = await client.download_media(media, progress=progress)
            nama = "Audio" if message.reply_to_message.audio else "Voice" if message.reply_to_message.voice else "Video"
            title = "None"
            duration = media.duration or 0
            channel = "Local Audio" if message.reply_to_message.audio else "Local Voice" if message.reply_to_message.voice else "Local Video"
            views = "N/A"
            thumb = None
    else:
        if len(message.command) < 2:
            return await message.reply(f"<i><b>{ggl}Mohon berikan judul yang kamu inginkan!!</b></i>")

        query = message.text.split(None, 1)[1]
        if query.startswith(("https", "t.me")):
            if "t.me/c/" in query:
                msg_id = int(query.split("/")[-1])
                chat = int("-100" + str(query.split("/")[-2]))
                pv = await client.get_messages(chat, int(msg_id))
                if pv.video:
                    infomsg = await message.reply(f"<i><b>{prs}Downloading Video...</b></i>")
                    async def progress(current, total):
                        percent = round((current / total) * 100)
                        global waw
                        if percent != waw:
                            waw = percent
                            try:
                                await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                            except FloodWait as e:
                                await asyncio.sleep(e.value)
                                try:
                                    await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                                except Exception as e:
                                    await infomsg.edit(e)
                            except Exception as e:
                                await infomsg.edit(e)
                    file_name = await client.download_media(pv.video, progress=progress)
                    nama = "Video"
                    title = "None"
                    duration = pv.video.duration or 0
                    channel = "Local Video"
                    views = "N/A"
                    thumb = None
            else:
                chat = str(query.split("/")[-2])
                msg_id = str(query.split("/")[-1])
                pv = await client.get_messages(chat, int(msg_id))
                if pv.video:
                    infomsg = await message.reply(f"<i><b>{prs}Downloading Video...</b></i>")
                    async def progress(current, total):
                        percent = round((current / total) * 100)
                        global waw
                        if percent != waw:
                            waw = percent
                            try:
                                await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                            except FloodWait as e:
                                await asyncio.sleep(e.value)
                                try:
                                    await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                                except Exception as e:
                                    await infomsg.edit(e)
                            except Exception as e:
                                await infomsg.edit(e)
                    file_name = await client.download_media(pv.video, progress=progress)
                    nama = "Video"
                    title = "None"
                    duration = pv.video.duration or 0
                    channel = "Local Video"
                    views = "N/A"
                    thumb = None
        else:
            infomsg = await message.reply(f"<i><b>{prs}Processing...</b></i>")
            try:
                search_result = VideosSearch(query, limit=1).result()["result"][0]
                link = f"https://youtu.be/{search_result['id']}"
            except Exception:
                return await infomsg.edit(f"<i><b>{ggl}Pencarian music gagal!</b></i>")

            try:
                file_name, title, url, duration, views, channel, thumb, data_ytp = await YoutubeDownload(link, as_video=False)
            except Exception:
                return await infomsg.edit(f"<i><b>{ggl}Gagal memutar music!</b></i>")
            nama = "Audio"

    chat_id = message.chat.id
    a_calls = await client.call_py.calls
    if_chat = a_calls.get(chat_id)
    hasil = f"""<b>Title:</b> {title}
<b>Duration:</b> {timedelta(seconds=duration)}
<b>Views:</b> {views}
<b>Channel:</b> {channel}"""
    if client.me.id not in playlist:
        playlist[client.me.id] = {}
    if message.chat.id not in playlist[client.me.id]:
        playlist[client.me.id][message.chat.id] = []
    playlist[client.me.id][message.chat.id].append({"judul": hasil, "lagu": file_name})
    if if_chat:
        await infomsg.delete()
        return await message.reply(f"""<i><b>{sks}Ditambahkan ke antrian!</b>

{hasil}</i>
""")
    try:
        await client.call_py.play(chat_id, MediaStream(
            file_name,
            audio_parameters=AudioQuality.STUDIO,
            video_parameters=VideoQuality.FHD_1080p
        ))
        await infomsg.delete()
        await message.reply(f"""<i><b>{sks}Memutar {nama}!</b>

{hasil}</i>
""")
    except NoActiveGroupCall:
        await infomsg.edit(f"<i><b>{ggl}Voice chat tidak aktif, mohon aktifkan voice chat!</b></i>")
    except Exception:
        await infomsg.edit(f"<i><b>{ggl}Gagal memutar music!</b></i>")
    finally:
        if os.path.exists(file_name):
            os.remove(file_name)
        if thumb and os.path.exists(thumb):
            os.remove(thumb)


@USU.UBOT("vplay")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    if message.reply_to_message:
        media = message.reply_to_message.video
        teks = message.reply_to_message.text
        if teks:
            query = teks
            infomsg = await message.reply(f"<i><b>{prs}Processing...</b></i>")
            try:
                search_result = VideosSearch(query, limit=1).result()["result"][0]
                link = f"https://youtu.be/{search_result['id']}"
            except Exception:
                return await infomsg.edit(f"<i><b>{ggl}Pencarian video gagal!</b></i>")

            try:
                file_name, title, url, duration, views, channel, thumb, data_ytp = await YoutubeDownload(link, as_video=True)
            except Exception:
                return await infomsg.edit(f"<i><b>{ggl}Gagal memutar video!</b></i>")
        elif media:
            infomsg = await message.reply(f"<i><b>{prs}Downloading Video...</b></i>")
            async def progress(current, total):
                percent = round((current / total) * 100)
                global waw
                if percent != waw:
                    waw = percent
                    try:
                        await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                        try:
                            await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                        except Exception as e:
                            await infomsg.edit(e)
                    except Exception as e:
                        await infomsg.edit(e)
            file_name = await client.download_media(media, progress=progress)
            title = "None"
            duration = media.duration or 0
            channel = "Local Video" if message.reply_to_message.video else "Local Video"
            views = "N/A"
            thumb = None
    else:
        if len(message.command) < 2:
            return await message.reply(f"<i><b>{ggl}Mohon berikan judul yang kamu inginkan!!</b></i>")

        query = message.text.split(None, 1)[1]
        if query.startswith(("https", "t.me")):
            if "t.me/c/" in query:
                msg_id = int(query.split("/")[-1])
                chat = int("-100" + str(query.split("/")[-2]))
                pv = await client.get_messages(chat, int(msg_id))
                if pv.video:
                    infomsg = await message.reply(f"<i><b>{prs}Downloading Video...</b></i>")
                    async def progress(current, total):
                        percent = round((current / total) * 100)
                        global waw
                        if percent != waw:
                            waw = percent
                            try:
                                await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                            except FloodWait as e:
                                await asyncio.sleep(e.value)
                                try:
                                    await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                                except Exception as e:
                                    await infomsg.edit(e)
                            except Exception as e:
                                await infomsg.edit(e)
                    file_name = await client.download_media(pv.video, progress=progress)
                    title = "None"
                    duration = pv.video.duration or 0
                    channel = "Local Video"
                    views = "N/A"
                    thumb = None
            else:
                chat = str(query.split("/")[-2])
                msg_id = str(query.split("/")[-1])
                pv = await client.get_messages(chat, int(msg_id))
                if pv.video:
                    infomsg = await message.reply(f"<i><b>{prs}Downloading Video...</b></i>")
                    async def progress(current, total):
                        percent = round((current / total) * 100)
                        global waw
                        if percent != waw:
                            waw = percent
                            try:
                                await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                            except FloodWait as e:
                                await asyncio.sleep(e.value)
                                try:
                                    await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                                except Exception as e:
                                    await infomsg.edit(e)
                            except Exception as e:
                                await infomsg.edit(e)
                    file_name = await client.download_media(pv.video, progress=progress)
                    title = "None"
                    duration = pv.video.duration or 0
                    channel = "Local Video"
                    views = "N/A"
                    thumb = None
        else:
            infomsg = await message.reply(f"<i><b>{prs}Processing...</b></i>")
            try:
                search_result = VideosSearch(query, limit=1).result()["result"][0]
                link = f"https://youtu.be/{search_result['id']}"
            except Exception:
                return await infomsg.edit(f"<i><b>{ggl}Pencarian video gagal!</b></i>")

            try:
                file_name, title, url, duration, views, channel, thumb, data_ytp = await YoutubeDownload(link, as_video=True)
            except Exception:
                return await infomsg.edit(f"<i><b>{ggl}Gagal memutar video!</b></i>")

    chat_id = message.chat.id
    a_calls = await client.call_py.calls
    if_chat = a_calls.get(chat_id)
    hasil = f"""<b>Title:</b> {title}
<b>Duration:</b> {timedelta(seconds=duration)}
<b>Views:</b> {views}
<b>Channel:</b> {channel}"""
    if client.me.id not in playlist:
        playlist[client.me.id] = {}
    if message.chat.id not in playlist[client.me.id]:
        playlist[client.me.id][message.chat.id] = []
    playlist[client.me.id][message.chat.id].append({"judul": hasil, "lagu": file_name})
    if if_chat:
        await infomsg.delete()
        return await message.reply(f"""<i><b>{sks}Ditambahkan ke antrian!</b>

{hasil}</i>
""")

    try:
        await client.call_py.play(chat_id, MediaStream(file_name, audio_parameters=AudioQuality.STUDIO, video_parameters=VideoQuality.FHD_1080p))
        await infomsg.delete()
        await message.reply(f"""<i><b>{sks}Memutar Video!</b>

{hasil}</i>
""")
    except NoActiveGroupCall:
        await infomsg.edit(f"<i><b>{ggl}Voice chat tidak aktif, mohon aktifkan voice chat!</b></i>")
    except Exception:
        await infomsg.edit(f"<i><b>{ggl}Gagal memutar video!</b></i>")
    finally:
        if os.path.exists(file_name):
            os.remove(file_name)
        if thumb and os.path.exists(thumb):
            os.remove(thumb)


@USU.UBOT("end")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    chat_id = message.chat.id
    a_calls = await client.call_py.calls
    if_chat = a_calls.get(chat_id)
    if client.me.id in paused and chat_id in paused[client.me.id]:
        del paused[client.me.id][chat_id]
    if not if_chat:
        return await message.reply(f"<i><b>{ggl}Tidak ada streaming yang aktif!</b></i>")
    if client.me.id in playlist and chat_id in playlist[client.me.id]:
        del playlist[client.me.id][chat_id]
    try:
        await client.call_py.leave_call(chat_id)
        return await message.reply(f"<i><b>{sks}Streaming end!</b></i>")      
    except Exception as e:
        return await message.reply(f"<b>{ggl}Error:</b> {e}")



@USU.UBOT("pause")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    anu = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    chat_id = message.chat.id
    a_calls = await client.call_py.calls
    if_chat = a_calls.get(chat_id)

    if not if_chat:
        return await anu.edit(f"<i><b>{ggl}Tidak ada streaming yang aktif!</b></i>")

    if client.me.id not in paused:
        paused[client.me.id] = {}

    if chat_id in paused[client.me.id]:
        return await anu.edit(f"<i><b>{ggl}Streaming sudah dalam keadaan pause!</b></i>")

    try:
        await client.call_py.pause_stream(chat_id)
        await anu.edit(f"<i><b>{sks}Streaming di-pause!</b></i>")
        paused[client.me.id][chat_id] = True
    except Exception as e:
        return await anu.edit(f"<b>{ggl}Error:</b> {e}")


@USU.UBOT("resume")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    anu = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    chat_id = message.chat.id
    a_calls = await client.call_py.calls
    if_chat = a_calls.get(chat_id)
    if not if_chat:
        return await anu.edit(f"<i><b>{ggl}Tidak ada streaming yang aktif!</b></i>")

    if client.me.id in paused and chat_id not in paused[client.me.id]:
        return await anu.edit(f"<i><b>{ggl}Streaming sedang tidak di-pause!</b></i>")
    try:
        await client.call_py.resume_stream(chat_id)
        await anu.edit(f"<i><b>{sks}Streaming di-resume!</b></i>")
        del paused[client.me.id][chat_id]
    except Exception as e:
        return await anu.edit(f"<b>{ggl}Error:</b> {e}")


@USU.UBOT("skip")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    anu = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    chat_id = message.chat.id
    a_calls = await client.call_py.calls
    if_chat = a_calls.get(chat_id)
    if client.me.id in paused and chat_id in paused[client.me.id]:
        del paused[client.me.id][chat_id]
    if client.me.id in playlist and chat_id in playlist[client.me.id] and len(playlist[client.me.id][chat_id]) > 1:
        if if_chat:
            try:
                await client.call_py.play(chat_id, MediaStream(playlist[client.me.id][chat_id][1]['lagu']))
            except Exception as e:
                return await anu.edit(f"<b>{ggl}Error:</b> {e}")
        else:
            return await anu.edit(f"<i><b>{ggl}Tidak ada streaming yang aktif!</b></i>")
    else:
        return await anu.edit(f"<i><b>{ggl}Tidak ada antrian streaming!</b></i>")
    await anu.delete()
    await message.reply(f"""<i><b>{sks}Memutar antrian!</b>

{playlist[client.me.id][message.chat.id][1]['judul']}</i>""")
    return playlist[client.me.id][message.chat.id].pop(0)

#===================


@USU.BOT("playlist")
@USU.GC
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    anu = await message.reply(f"<i><b>{prs}Processing...</b></i>")

    if message.chat.id not in playlist:
        await anu.edit(f"<i><b>{ggl}Playlist kosong!</b></i>")
    else:
        text = f"<i><b>{broad}Sedang diputar:</b>\n{playlist[message.chat.id][0]['judul']}\n\n"
        if len(playlist[message.chat.id]) > 1:
            text += f"<b>{ptr}Daftar antrian:</b>\n"
            for i, lagu in enumerate(playlist[message.chat.id][1:], start=1):
                text += f"{i}.{lagu['judul']}\n\n"
        text += "</i>"
        await anu.edit(text)
    await message.delete()

@USU.BOT("play")
@USU.GC
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    susers = await get_list_from_vars(bot.me.id, "SAVED_USERS")
    if not await gabung(client, message):
        return
    if message.chat.id not in susers:
        if message.chat.type != ChatType.CHANNEL:
           await add_to_vars(bot.me.id, "SAVED_USERS", message.chat.id)
    if message.reply_to_message:
        media = message.reply_to_message.audio if message.reply_to_message.audio else message.reply_to_message.voice if message.reply_to_message.voice else message.reply_to_message.video
        teks = message.reply_to_message.text
        if teks:
            query = teks
            infomsg = await message.reply(f"<i><b>{prs}Processing...</b></i>")
            try:
                search_result = VideosSearch(query, limit=1).result()["result"][0]
                link = f"https://youtu.be/{search_result['id']}"
            except Exception:
                return await infomsg.edit(f"<i><b>{ggl}Pencarian music gagal!</b></i>")

            try:
                file_name, title, url, duration, views, channel, thumb, data_ytp = await YoutubeDownload(link, as_video=False)
            except Exception:
                return await infomsg.edit(f"<i><b>{ggl}Gagal memutar music!</b></i>")
            nama = "Audio"
        elif media:
            infomsg = await message.reply(f"<i><b>{prs}Downloading {'Audio' if message.reply_to_message.audio else 'Voice' if message.reply_to_message.voice else 'Video'}...</b></i>")
            async def progress(current, total):
                percent = round((current / total) * 100)
                global waw
                if percent != waw:
                    waw = percent
                    try:
                        await infomsg.edit(f"<i><b>{prs}Downloading {'Audio' if message.reply_to_message.audio else 'Voice' if message.reply_to_message.voice else 'Video'} {percent}%...</b></i>")
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                        try:
                            await infomsg.edit(f"<i><b>{prs}Downloading {'Audio' if message.reply_to_message.audio else 'Voice' if message.reply_to_message.voice else 'Video'} {percent}%...</b></i>")
                        except Exception as e:
                            await infomsg.edit(e)
                    except Exception as e:
                        await infomsg.edit(e)
            file_name = await client.download_media(media, progress=progress)
            nama = "Audio" if message.reply_to_message.audio else "Voice" if message.reply_to_message.voice else "Video"
            title = "None"
            duration = media.duration or 0
            channel = "Local Audio" if message.reply_to_message.audio else "Local Voice" if message.reply_to_message.voice else "Local Video"
            views = "N/A"
            thumb = None
    else:
        if len(message.command) < 2:
            return await message.reply(f"<i><b>{ggl}Mohon berikan judul yang kamu inginkan!!</b></i>")
        await message.delete()

        query = message.text.split(None, 1)[1]
        if query.startswith(("https", "t.me")):
            if "t.me/c/" in query:
                msg_id = int(query.split("/")[-1])
                chat = int("-100" + str(query.split("/")[-2]))
                pv = await client.get_messages(chat, int(msg_id))
                if pv.video:
                    infomsg = await message.reply(f"<i><b>{prs}Downloading Video...</b></i>")
                    async def progress(current, total):
                        percent = round((current / total) * 100)
                        global waw
                        if percent != waw:
                            waw = percent
                            try:
                                await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                            except FloodWait as e:
                                await asyncio.sleep(e.value)
                                try:
                                    await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                                except Exception as e:
                                    await infomsg.edit(e)
                            except Exception as e:
                                await infomsg.edit(e)
                    file_name = await client.download_media(pv.video, progress=progress)
                    nama = "Video"
                    title = "None"
                    duration = pv.video.duration or 0
                    channel = "Local Video"
                    views = "N/A"
                    thumb = None
            else:
                chat = str(query.split("/")[-2])
                msg_id = str(query.split("/")[-1])
                pv = await client.get_messages(chat, int(msg_id))
                if pv.video:
                    infomsg = await message.reply(f"<i><b>{prs}Downloading Video...</b></i>")
                    async def progress(current, total):
                        percent = round((current / total) * 100)
                        global waw
                        if percent != waw:
                            waw = percent
                            try:
                                await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                            except FloodWait as e:
                                await asyncio.sleep(e.value)
                                try:
                                    await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                                except Exception as e:
                                    await infomsg.edit(e)
                            except Exception as e:
                                await infomsg.edit(e)
                    file_name = await client.download_media(pv.video, progress=progress)
                    nama = "Video"
                    title = "None"
                    duration = pv.video.duration or 0
                    channel = "Local Video"
                    views = "N/A"
                    thumb = None
        else:
            infomsg = await message.reply(f"<i><b>{prs}Processing...</b></i>")
            try:
                search_result = VideosSearch(query, limit=1).result()["result"][0]
                link = f"https://youtu.be/{search_result['id']}"
            except Exception:
                return await infomsg.edit(f"<i><b>{ggl}Pencarian music gagal!</b></i>")

            try:
                file_name, title, url, duration, views, channel, thumb, data_ytp = await YoutubeDownload(link, as_video=False)
            except Exception:
                return await infomsg.edit(f"<i><b>{ggl}Gagal memutar music!</b></i>")
            nama = "Audio"

    chat_id = message.chat.id
    a_calls = await client.assistant.calls
    if_chat = a_calls.get(chat_id)
    hasil = f"""<b>Title:</b> {title}
<b>Duration:</b> {timedelta(seconds=duration)}
<b>Views:</b> {views}
<b>Channel:</b> {channel}"""
    try:
        await client.get_chat_member(message.chat.id, bot.usu.me.id)
    except Exception as e:
        try:
            chat = await client.get_chat(message.chat.id)
            if chat.invite_link:
                await client.usu.join_chat(chat.invite_link)
            else:
                export_link = await client.export_chat_invite_link(message.chat.id)
                await bot.usu.join_chat(export_link)
        except InviteRequestSent:
            try:
                await client.approve_chat_join_request(message.chat.id, bot.usu.me.id)
            except Exception as e:
                return print(e)
        except Exception as e:
            return print(e)
    if chat_id not in playlist:
        playlist[message.chat.id] = []
    playlist[message.chat.id].append({"judul": hasil, "lagu": file_name})
    if if_chat:
        await infomsg.delete()
        return await message.reply(f"""<i><b>{sks}Ditambahkan ke antrian!</b>

{hasil}</i>
""")

    try:
        await client.assistant.play(chat_id, MediaStream(
            file_name, audio_parameters=AudioQuality.STUDIO, video_parameters=VideoQuality.FHD_1080p
        ))
        await infomsg.delete()
        await message.reply(f"""<i><b>{sks}Memutar {nama}!</b>

{hasil}</i>
""")
    except NoActiveGroupCall:
        await infomsg.edit(f"<i><b>{ggl}Voice chat tidak aktif, mohon aktifkan voice chat!</b></i>")
    except Exception:
        await infomsg.edit(f"<i><b>{ggl}Gagal memutar music!</b></i>")
    finally:
        if os.path.exists(file_name):
            os.remove(file_name)
        if thumb and os.path.exists(thumb):
            os.remove(thumb)



@USU.BOT("vplay")
@USU.GC
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    susers = await get_list_from_vars(bot.me.id, "SAVED_USERS")
    if not await gabung(client, message):
        return
    if message.chat.id not in susers:
        if message.chat.type != ChatType.CHANNEL:
           await add_to_vars(bot.me.id, "SAVED_USERS", message.chat.id)
    if message.reply_to_message:
        media = message.reply_to_message.video
        teks = message.reply_to_message.text
        if teks:
            query = teks
            infomsg = await message.reply(f"<i><b>{prs}Processing...</b></i>")
            try:
                search_result = VideosSearch(query, limit=1).result()["result"][0]
                link = f"https://youtu.be/{search_result['id']}"
            except Exception:
                return await infomsg.edit(f"<i><b>{ggl}Pencarian video gagal!</b></i>")

            try:
                file_name, title, url, duration, views, channel, thumb, data_ytp = await YoutubeDownload(link, as_video=True)
            except Exception:
                return await infomsg.edit(f"<i><b>{ggl}Gagal memutar video!</b></i>")
        if media:
            infomsg = await message.reply(f"<i><b>{prs}Downloading Video...</b></i>")
            async def progress(current, total):
                percent = round((current / total) * 100)
                global waw
                if percent != waw:
                    waw = percent
                    try:
                        await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                        try:
                            await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                        except Exception as e:
                            await infomsg.edit(e)
                    except Exception as e:
                        await infomsg.edit(e)
            file_name = await client.download_media(media, progress=progress)
            title = "None"
            duration = media.duration or 0
            channel = "Local Video" if message.reply_to_message.video else "Local Video"
            views = "N/A"
            thumb = None
    else:
        if len(message.command) < 2:
            return await message.reply(f"<i><b>{ggl}Mohon berikan judul yang kamu inginkan!!</b></i>")
        await message.delete()

        query = message.text.split(None, 1)[1]
        if query.startswith(("https", "t.me")):
            if "t.me/c/" in query:
                msg_id = int(query.split("/")[-1])
                chat = int("-100" + str(query.split("/")[-2]))
                pv = await client.get_messages(chat, int(msg_id))
                if pv.video:
                    infomsg = await message.reply(f"<i><b>{prs}Downloading Video...</b></i>")
                    async def progress(current, total):
                        percent = round((current / total) * 100)
                        global waw
                        if percent != waw:
                            waw = percent
                            try:
                                await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                            except FloodWait as e:
                                await asyncio.sleep(e.value)
                                try:
                                    await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                                except Exception as e:
                                    await infomsg.edit(e)
                            except Exception as e:
                                await infomsg.edit(e)
                    file_name = await client.download_media(pv.video, progress=progress)
                    title = "None"
                    duration = pv.video.duration or 0
                    channel = "Local Video"
                    views = "N/A"
                    thumb = None
            else:
                chat = str(query.split("/")[-2])
                msg_id = str(query.split("/")[-1])
                pv = await client.get_messages(chat, int(msg_id))
                if pv.video:
                    infomsg = await message.reply(f"<i><b>{prs}Downloading Video...</b></i>")
                    async def progress(current, total):
                        percent = round((current / total) * 100)
                        global waw
                        if percent != waw:
                            waw = percent
                            try:
                                await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                            except FloodWait as e:
                                await asyncio.sleep(e.value)
                                try:
                                    await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                                except Exception as e:
                                    await infomsg.edit(e)
                            except Exception as e:
                                await infomsg.edit(e)
                    file_name = await client.download_media(pv.video, progress=progress)
                    title = "None"
                    duration = pv.video.duration or 0
                    channel = "Local Video"
                    views = "N/A"
                    thumb = None
        else:
            infomsg = await message.reply(f"<i><b>{prs}Processing...</b></i>")
            try:
                search_result = VideosSearch(query, limit=1).result()["result"][0]
                link = f"https://youtu.be/{search_result['id']}"
            except Exception:
                return await infomsg.edit(f"<i><b>{ggl}Pencarian video gagal!</b></i>")

            try:
                file_name, title, url, duration, views, channel, thumb, data_ytp = await YoutubeDownload(link, as_video=True)
            except Exception:
                return await infomsg.edit(f"<i><b>{ggl}Gagal memutar video!</b></i>")

    chat_id = message.chat.id
    a_calls = await client.assistant.calls
    if_chat = a_calls.get(chat_id)
    hasil = f"""<b>Title:</b> {title}
<b>Duration:</b> {timedelta(seconds=duration)}
<b>Views:</b> {views}
<b>Channel:</b> {channel}"""
    try:
        await client.get_chat_member(message.chat.id, bot.usu.me.id)
    except Exception as e:
        try:
            chat = await client.get_chat(message.chat.id)
            if chat.invite_link:
                await client.usu.join_chat(chat.invite_link)
            else:
                export_link = await client.export_chat_invite_link(message.chat.id)
                await bot.usu.join_chat(export_link)
        except InviteRequestSent:
            try:
                await client.approve_chat_join_request(message.chat.id, bot.usu.me.id)
            except Exception as e:
                return print(e)
        except Exception as e:
            return print(e)
    if chat_id not in playlist:
        playlist[message.chat.id] = []
    playlist[message.chat.id].append({"judul": hasil, "lagu": file_name})
    if if_chat:
        await infomsg.delete()
        return await message.reply(f"""<i><b>{sks}Ditambahkan ke antrian!</b>

{hasil}</i>
""")

    try:
        await client.assistant.play(chat_id, MediaStream(file_name, audio_parameters=AudioQuality.STUDIO, video_parameters=VideoQuality.FHD_1080p))
        await infomsg.delete()
        await message.reply(f"""<i><b>{sks}Memutar Video!</b>

{hasil}</i>
""")
    except NoActiveGroupCall:
        await infomsg.edit(f"<i><b>{ggl}Voice chat tidak aktif, mohon aktifkan voice chat!</b></i>")
    except Exception:
        await infomsg.edit(f"<i><b>{ggl}Gagal memutar video!</b></i>")
    finally:
        if os.path.exists(file_name):
            os.remove(file_name)
        if thumb and os.path.exists(thumb):
            os.remove(thumb)


@USU.BOT("end")
@USU.GC
@USU.ADMIN
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    chat_id = message.chat.id
    a_calls = await client.assistant.calls
    if_chat = a_calls.get(chat_id)
    if chat_id in paused:
        del paused[chat_id]
    if not if_chat:
        return await message.reply(f"<i><b>{ggl}Tidak ada streaming yang aktif!</b></i>")
    if chat_id in playlist:
        del playlist[message.chat.id]
    await message.delete()
    try:
        await client.assistant.leave_call(chat_id)
        return await message.reply(f"<i><b>{sks}Streaming end!</b></i>")      
    except Exception as e:
        return await message.reply(f"<b>{ggl}Error:</b> {e}")


@USU.BOT("pause")
@USU.GC
@USU.ADMIN
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    anu = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    chat_id = message.chat.id
    a_calls = await client.assistant.calls
    if_chat = a_calls.get(chat_id)

    if not if_chat:
        return await anu.edit(f"<i><b>{ggl}Tidak ada streaming yang aktif!</b></i>")

    if chat_id in paused:
        return await anu.edit(f"<i><b>{ggl}Streaming sudah dalam keadaan pause!</b></i>")
    await message.delete()
    try:
        await client.assistant.pause_stream(chat_id)
        await anu.edit(f"<i><b>{sks}Streaming di-pause!</b></i>")
        paused[chat_id] = True
    except Exception as e:
        return await anu.edit(f"<b>{ggl}Error:</b> {e}")


@USU.BOT("resume")
@USU.GC
@USU.ADMIN
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    anu = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    chat_id = message.chat.id
    a_calls = await client.assistant.calls
    if_chat = a_calls.get(chat_id)

    if not if_chat:
        return await anu.edit(f"<i><b>{ggl}Tidak ada streaming yang aktif!</b></i>")

    if chat_id not in paused:
        return await anu.edit(f"<i><b>{ggl}Streaming sedang tidak di-pause!</b></i>")
    await message.delete()
    try:
        await client.assistant.resume_stream(chat_id)
        await anu.edit(f"<i><b>{sks}Streaming di-resume!</b></i>")
        del paused[chat_id]
    except Exception as e:
        return await anu.edit(f"<b>{ggl}Error:</b> {e}")


@USU.BOT("skip")
@USU.GC
@USU.ADMIN
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    anu = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    chat_id = message.chat.id
    a_calls = await client.assistant.calls
    if_chat = a_calls.get(chat_id)
    if chat_id in paused:
        del paused[chat_id]
    if chat_id in playlist and len(playlist[chat_id]) > 1:
        if if_chat:
            try:
                await client.assistant.play(chat_id, MediaStream(playlist[chat_id][1]['lagu']))
            except Exception as e:
                return await anu.edit(f"<b>{ggl}Error:</b> {e}")
        else:
            return await anu.edit(f"<i><b>{ggl}Tidak ada streaming yang aktif!</b></i>")
    else:
        return await anu.edit(f"<i><b>{ggl}Tidak ada antrian streaming!</b></i>")
    await message.delete()
    await anu.delete()
    await message.reply(f"""<i><b>{sks}Memutar antrian!</b>

{playlist[message.chat.id][1]['judul']}</i>""")
    return playlist[message.chat.id].pop(0)