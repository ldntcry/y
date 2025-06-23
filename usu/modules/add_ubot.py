import asyncio
import importlib
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from pytz import timezone

from pyrogram.enums import SentCodeType
from pyrogram.errors import *
from pyrogram.types import *
from pyrogram.raw import functions
from pyrogram import Client


from usu import *

langganan = {}

@USU.BOT("start")
@USU.PRIVATE
@USU.START
async def _(client, message):
    user_id = message.from_user.id
    save = await db.get_list_from_vars(client.me.id, "SAVED_USERS")
    buttons = BTN.PILIHAN()
    msg = await MSG.PILIHAN()
    teks = message.text.split()[1:]
    if teks:
        if teks[0].startswith("REF"):
            user = int(teks[0].replace("REF", ""))
            sudah = await db.get_list_from_vars(user, "REF")
            if user != user_id:
                if user in save and user_id not in save and user_id not in sudah:

                    vars = await db.get_vars(user, "SALDO")
                    duit = vars if vars else 0
                    tambah = duit + 4000
                    await db.set_vars(user, "SALDO", tambah)
                    await db.add_to_vars(user, "REF", user_id)
                    await bot.send_message(user, f"<i><b>Anda berhasil mengundang 1 pengguna baru, saldo anda telah bertambah Rp 4.000</b></i>")
    return await message.reply(msg, reply_markup=InlineKeyboardMarkup(buttons))


@USU.CALLBACK("toko_adm")
async def _(client, callback_query):
    button = InlineKeyboardMarkup([])
    sel = []
    teks = f"<i><b>Daftar seller resmi [Userbot]({PHOTO}) ada di bawah ini,\nSelain seller di bawah ini sudah di pastikan bukan dari kami!\nCatatan:</b> berhati - hati lah dalam jual/beli sesuatu di online</i>"
    seles_users = await db.get_list_from_vars(client.me.id, "SELER_USERS")
    button.inline_keyboard.append([InlineKeyboardButton(f"Owners", url=f"https://t.me/{USERNAME}")])
    if seles_users:
        for id in seles_users:
            if id in DEVS:
                continue
            try:
                user = await client.get_users(id)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                user = await client.get_users(id)
            except Exception as e:
                continue
            first = user.first_name
            last = user.last_name
            user_id = user.id
            sel.append(InlineKeyboardButton(f"{first} {last or ''}", url=f"tg://openmessage?user_id={user_id}"))
            if len(sel) == 2:
                button.inline_keyboard.append(sel)
                sel = []
    if sel:
        button.inline_keyboard.append(sel)
    button.inline_keyboard.append([InlineKeyboardButton(f"🔙 Kembali", callback_data=f"awal")])
    return await callback_query.edit_message_text(teks, reply_markup=button)

@USU.CALLBACK("^reset")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id not in ubot._ubot:
        return await callback_query.answer(f"Anda bukan pengguna userbot ini!", show_alert=True)

    default_prefix = "."

    ubot.set_prefix(user_id, default_prefix)
    await db.set_pref(user_id, default_prefix)
    await callback_query.answer(
        f"Prefix anda berhasil di reset!",
        show_alert=True
    )

@USU.CALLBACK("^awal")
async def _(c, cq):
    return await cq.edit_message_text(await MSG.START(), reply_markup=InlineKeyboardMarkup(BTN.START()))


@USU.CALLBACK("^pilihan")
async def _(c, cq):
    return await cq.edit_message_text(await MSG.PILIHAN(), reply_markup=InlineKeyboardMarkup(BTN.PILIHAN()))


@USU.CALLBACK("^complain")
async def _(c, cq):
    button = BTN.SUPPORT()
    pesan = f"<b><i>Jika ada bug/kerusakan pada [Bot]({PHOTO}) kami, silahkan lapor ke group/channel di bawah ini</i></b>"
    return await cq.edit_message_text(pesan, reply_markup=InlineKeyboardMarkup(button))


@USU.CALLBACK("^status")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    expired = await db.get_expired_date(user_id)
    if user_id in ubot._ubot:
        if expired is None:
            return await callback_query.answer("Tidak ada tanggal kadaluarsa!", show_alert=True)
        jkt = pytz.timezone("Asia/Jakarta")
        now_utc = datetime.now(jkt) 
        sisa = (expired - now_utc).days
        return await callback_query.answer(
            f"""Expired {sisa} Days! """,
            show_alert=True
        )
    else:
        return await callback_query.answer(
            f"""Silahkan install userbot terlebih dahulu!""",
            show_alert=True
        )


@USU.CALLBACK("kirii_")
async def prev_bulan(client, callback_query):
    user_id = callback_query.from_user.id
    vars = await db.get_vars(user_id, "SALDO")
    saldo = vars if vars else 0
    teks = f"{int(saldo):,}".replace(",", ".")
    try:
        bulan_saat_ini = int(callback_query.data.split("_")[1])
        if bulan_saat_ini > 1:
            langganan[user_id] = bulan_saat_ini - 1
            jumlah_bulan = langganan[user_id]
            total_harga = jumlah_bulan * HARGA_USERBOT
            return await callback_query.edit_message_text(
                f"""<i><b>Saldo [Userbot]({PHOTO}) anda saat ini:</b>\nRp {teks}\n\n<b>Memilih:</b> {langganan[user_id]} Bulan - Rp {HARGA_USERBOT}.000</i>""", reply_markup=InlineKeyboardMarkup(BTN.KONFIR(jumlah_bulan)))
        else:
            await callback_query.answer("Ini adalah bulan pertama.", show_alert=True)
    except Exception as e:
        return print(e)


@USU.CALLBACK("kanann_")
async def next_bulan(client, callback_query):
    user_id = callback_query.from_user.id
    vars = await db.get_vars(user_id, "SALDO")
    saldo = vars if vars else 0
    teks = f"{int(saldo):,}".replace(",", ".")
    try:
        bulan_saat_ini = int(callback_query.data.split("_")[1])
        langganan[user_id] = bulan_saat_ini + 1
        jumlah_bulan = langganan[user_id]
        total_harga = jumlah_bulan * HARGA_USERBOT
        return await callback_query.edit_message_text(
            f"""<i><b>Saldo [Userbot]({PHOTO}) anda saat ini:</b>\nRp {teks}\n\n<b>Memilih:</b> {langganan[user_id]} Bulan - Rp {HARGA_USERBOT}.000</i>""", reply_markup=InlineKeyboardMarkup(BTN.KONFIR(jumlah_bulan)))
    except Exception as e:
        return print(e)

@USU.CALLBACK("setuju")
async def setuju(c, cq):
    user_id = cq.from_user.id
    vars = await db.get_vars(user_id, "SALDO")
    saldo = vars if vars else 0
    jumlah_bulan = langganan[user_id]
    total_harga = jumlah_bulan * HARGA_USERBOT * 1000
    if saldo < total_harga:
        return await cq.answer(f"Saldo anda tidak mencukupi!", True)       
    if user_id in await db.get_list_from_vars(c.me.id, "AKSES") or user_id in ubot._ubot:
        return await cq.answer(f"Mohon maaf anda sudah memiliki Userbot!", True)
    else:
        now = datetime.now(pytz.timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=int(jumlah_bulan))
        await db.set_expired_date(user_id, expired)
        await db.add_to_vars(c.me.id, "AKSES", user_id)
        duit = int(saldo) - int(total_harga)
        await db.set_vars(user_id, "SALDO", duit)
        await cq.answer(f"Anda berhasil membeli userbot, silahkan install userbot anda!", True)
        del langganan[user_id]
        return await cq.edit_message_text(await MSG.START(), reply_markup=InlineKeyboardMarkup(BTN.START()))



@USU.CALLBACK("hajar")
async def hajar(c, cq):
    user_id = cq.from_user.id
    vars = await db.get_vars(user_id, "SALDO")
    saldo = vars if vars else 0
    teks = f"{int(saldo):,}".replace(",", ".")
    langganan[user_id] = 1
    return await cq.edit_message_text(
        f"""<i><b>Saldo [Userbot]({PHOTO}) anda saat ini:</b>\nRp {teks}\n\n<b>Memilih:</b> {langganan[user_id]} Bulan - Rp {HARGA_USERBOT}.000</i>""", reply_markup=InlineKeyboardMarkup(BTN.KONFIR(langganan[user_id])))


@USU.CALLBACK("metode_beli")
async def metode_beli(c, cq):
    return await cq.edit_message_text(
        f"""<b><i>Beli/Berlangganan [Userbot]({PHOTO}) bisa lewat tombol di bawah ini!</i></b>""", reply_markup=InlineKeyboardMarkup(BTN.BELI()))


salah = 0 #by usu

@USU.CALLBACK("^buat")
async def _(client, callback_query):
    global salah
    user_id = callback_query.from_user.id
    if user_id in ubot._ubot:
        return await callback_query.answer(f"""Anda telah membuat/memiliki userbot!""", show_alert=True)
    elif len(ubot._ubot) + 1 > MAX_BOT:
        return await callback_query.answer(f"""Userbot mencapai maxsimal pengguna!""", show_alert=True)
    if user_id in await db.get_list_from_vars(client.me.id, "AKSES") or user_id in DEVS:
        try:
            buttons = ReplyKeyboardMarkup([
                [KeyboardButton("My Contact", request_contact=True)]], one_time_keyboard=True, resize_keyboard=True)
            while True:
                phone = await client.ask(
                    user_id,
                    f"<b><i>Silakan pencet tombol My Contact untuk memasukkan nomor akun Telegram Anda!</i></b>",
                    reply_markup=buttons,
                    timeout=300,
                )
                if phone.contact is not None:
                    salah = 0
                    usu_msg = await client.send_message(user_id, f"<b><i>Processing...</i></b>", reply_markup=ReplyKeyboardRemove())
                    await usu_msg.delete()
                    break
                else:
                    salah += 1
                    if salah >= 3:
                        return await client.send_message(
                            user_id,
                            f"<b><i>Anda terlalu sering mencoba, silahkan ulangi dari awal!</i></b>",
                            reply_markup=ReplyKeyboardRemove()
                        )
        except asyncio.TimeoutError:
            return await client.send_message(user_id, f"<b><i>Automatic cancellation!\n Use /start to restart</i></b>", reply_markup=ReplyKeyboardRemove())
        phone_number = phone.contact.phone_number
        new_client = Ubot(
            name=str(callback_query.id),
            api_id=API_ID,
            api_hash=API_HASH,
            in_memory=True,
        )
        get_otp = await client.send_message(user_id, f"<b><i>Sending OTP code...</i></b>", reply_markup=ReplyKeyboardRemove())
        await new_client.connect()
        try:
            code = await new_client.send_code(phone_number.strip())
        except ApiIdInvalid as AID:
            await get_otp.delete()
            return await client.send_message(user_id, AID, reply_markup=ReplyKeyboardRemove())
        except PhoneNumberInvalid as PNI:
            await get_otp.delete()
            return await client.send_message(user_id, PNI, reply_markup=ReplyKeyboardRemove())
        except PhoneNumberFlood as PNF:
            await get_otp.delete()
            return await client.send_message(user_id, PNF, reply_markup=ReplyKeyboardRemove())
        except PhoneNumberBanned as PNB:
            await get_otp.delete()
            return await client.send_message(user_id, PNB, reply_markup=ReplyKeyboardRemove())
        except PhoneNumberUnoccupied as PNU:
            await get_otp.delete()
            return await client.send_message(user_id, PNU, reply_markup=ReplyKeyboardRemove())
        except Exception as error:
            await get_otp.delete()
            return await client.send_message(user_id, f"<b>ERROR:</b> {error}", reply_markup=ReplyKeyboardRemove())
        try:
            sent_code = {
                SentCodeType.APP: "<a href=tg://openmessage?user_id=777000>Akun Telegram</a> resmi",
                SentCodeType.SMS: "Sms Anda",
                SentCodeType.CALL: "Panggilan Telpon",
                SentCodeType.FLASH_CALL: "Panggilan Kilat",
                SentCodeType.FRAGMENT_SMS: "Fragment Sms",
                SentCodeType.EMAIL_CODE: "Email Anda",
            }
            await get_otp.delete()
            while True:
                otp = await client.ask(
                    user_id,
                    f"<i><b>Silakan periksa kode OTP dari {sent_code[code.type]}, kirim kode otp anda menggunakan spasi!\nContoh:</b> 4 7 2 3 5</i>",
                    timeout=300,
                )
                if len(otp.text.split()) == 5:
                    salah = 0
                    break
                else:
                    salah += 1
                    if salah >= 3:
                        return await client.send_message(
                            user_id,
                            f"<b><i>Anda terlalu sering mencoba, silahkan ulangi dari awal!</i></b>", reply_markup=ReplyKeyboardRemove()
                        )
        except asyncio.TimeoutError:
            return await client.send_message(user_id, f"<b><i>Automatic cancellation!\n Use /start to restart</i></b>", reply_markup=ReplyKeyboardRemove())
        try:
            await new_client.sign_in(
                phone_number.strip(),
                code.phone_code_hash,
                phone_code=otp.text,
            )
        except PhoneCodeInvalid as PCI:
            return await client.send_message(user_id, PCI)
        except PhoneCodeExpired as PCE:
            return await bot.send_message(user_id, PCE)
        except BadRequest as error:
            return await client.send_message(user_id, f"<b>ERROR:</b> {error}", reply_markup=ReplyKeyboardRemove())
        except SessionPasswordNeeded:
            try:
                while True:
                    two_step_code = await client.ask(
                        user_id,
                        f"<b><i>Akun Anda telah mengaktifkan verifikasi dua langkah. Harap kirimkan kata sandinya.</i></b>",
                        timeout=300,
                    )
                    try:
                        await new_client.check_password(two_step_code.text)
                        await db.set_two_factor(user_id, two_step_code.text)
                        salah = 0
                        break
                    except Exception as error:
                        salah += 1
                        if salah >= 3:
                            return await client.send_message(
                                user_id,
                                f"<b><i>Anda terlalu sering mencoba, silahkan ulangi dari awal!</i></b>",
                            )
            except asyncio.TimeoutError:
                return await client.send_message(user_id, f"<b><i>Automatic cancellation!\n Use /start to restart</i></b>", reply_markup=ReplyKeyboardRemove())
        session_string = await new_client.export_session_string()
        await new_client.disconnect()
        new_client.storage.session_string = session_string
        new_client.in_memory = False
        bot_msg = await client.send_message(
            user_id,
            f"<b><i>Processing...</i></b>",
            disable_web_page_preview=True,
         )
        await new_client.start()
        if not user_id == new_client.me.id:
            del ubot._ubot[new_client.me.id]
            await db.rem_two_factor(new_client.me.id)
            return await bot_msg.edit(
            f"<b><i>Please use your Telegram account number!\n And not a telegram number from someone else's account</i></b>"
            )
        await db.add_ubot(
            user_id=int(new_client.me.id),
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=session_string,
        )
        await db.remove_from_vars(client.me.id, "AKSES", user_id)
        await db.set_vars(user_id, "switch", True)
        for mod in loadModule():
            importlib.reload(importlib.import_module(f"usu.modules.{mod}"))
        SH = await ubot.get_prefix(new_client.me.id)
        await asyncio.sleep(5)
        await bot_msg.delete()
        text_done = f"""<i><b>Information!</b>
 <b>Status :</b> Active!
 <b>Name :</b> <a href=tg://user?id={new_client.me.id}>{new_client.me.first_name} {new_client.me.last_name or ''}</a>
 <b>ID :</b> <code>{new_client.me.id}</code>
 <b>Prefix :</b> {' '.join(SH)}</i>
            """
        await client.send_message(user_id, text_done, reply_markup=ReplyKeyboardRemove())
        await asyncio.sleep(5)
        await client.send_message(user_id, f"<b><i>Information!\nJika ada sesi perangkat login botnya, harap di konfirmasi</i></b>", reply_markup=ReplyKeyboardRemove())
        user_link = f"{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}"
        gbt = [
            [
                InlineKeyboardButton(
                            user_link,
                            url=f"tg://openmessage?user_id={callback_query.from_user.id}"
                ),
            ],
        ]
        await client.send_message(LOGS_CHAT, f"<i><b>Information Active!\nName: {callback_query.from_user.mention}\nID: {callback_query.from_user.id}</b></i>", reply_markup=InlineKeyboardMarkup(gbt))
        await bash("rm -rf *session*")
        await install_my_peer(new_client)
        for auto in AUTO_JOIN:
            try:
                await new_client.join_chat(auto)
            except UserAlreadyParticipant:
                pass
    else:
        return await callback_query.answer(
            f"""Anda belum ada akses membuat userbot!""",
            show_alert=True
        )



@USU.BOT("restart")
async def _(client, message):
    buttons = [
            [InlineKeyboardButton("Restart", callback_data=f"ress_ubot")],
        ]
    await message.reply_photo(
            caption=f"""<b>Anda akan memulai ulang?!
Jika ya, tekan tombol di bawah ini</b>""",
            photo=PHOTO,
            reply_markup=InlineKeyboardMarkup(buttons),
        )


@USU.CALLBACK("ress_ubot")
async def _(client, callback_query):
    if callback_query.from_user.id not in ubot._ubot:
        return await callback_query.answer(
            f"Tombol ini bukan untukmu!",
            True,
        )
    for X in ubot._ubot.values():
        if callback_query.from_user.id == X.me.id:
            for _ubot_ in await db.get_userbots():
                if X.me.id == int(_ubot_["name"]):
                    try:
                        del ubot._ubot[X.me.id]
                        UB = Ubot(**_ubot_)
                        await UB.start()
                        for mod in loadModule():
                            importlib.reload(
                                importlib.import_module(f"usu.modules.{mod}")
                            )
                        return await callback_query.edit_message_text(
                            f"<i><b>Restart berhasil dilakukan!\n\nName:</b> {UB.me.mention} {UB.me.last_name or ''} <b>|</b> {UB.me.id}</i>"
                        )
                    except Exception as error:
                        return await callback_query.edit_message_text(f"<b>{error}</b>")



@USU.CALLBACK("^(get_otp|ub_deak|deak_akun_konfirm|get_phone|get_faktor)")
async def _(client, callback_query):
    query = callback_query.data.split()
    user_id = callback_query.from_user.id
    if user_id not in DEVS:
        return await callback_query.answer(
            f"Tombol ini bukan untuk anda! {callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}",
            True,
        )
    try:
        X = ubot._ubot[tuple(ubot._ubot.keys())[int(query[1])]]
    except IndexError:
        return await callback_query.answer("Invalid query", True)

    if query[0] == "get_otp":
        history = X.get_chat_history(chat_id=777000, limit=1)
        try:
            async for msg in history:
                kode_baru = msg.text
                if kode_baru:
                    await callback_query.edit_message_text(
                        kode_baru,
                        reply_markup=InlineKeyboardMarkup(
                            BTN.UBOT(X.me.id, int(query[1]))
                        ),
                    )
                else:
                    await callback_query.answer("Tidak ada kode terbaru!", True)
        except Exception as error:
            return await callback_query.answer(error, True)

    elif query[0] == "get_phone":
        try:
            return await callback_query.edit_message_text(
                f"<b><i>Phone Number: <code>{X.me.phone_number}</code></i></b>",
                reply_markup=InlineKeyboardMarkup(
                    BTN.UBOT(X.me.id, int(query[1]))
                ),
            )
        except Exception as error:
            return await callback_query.answer(error, True)

    elif query[0] == "get_faktor":
        code = await db.get_two_factor(X.me.id)
        if code == None:
            return await callback_query.answer(
                "No two-factor authentication!", True
            )
        else:
            return await callback_query.edit_message_text(
                f"<b><i>two-factor authentication: <code>{code}</code></i></b>",
                reply_markup=InlineKeyboardMarkup(
                    BTN.UBOT(X.me.id, int(query[1]))
                ),
            )

    elif query[0] == "ub_deak":
        return await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(BTN.DEAK(X.me.id, int(query[1])))
        )

    elif query[0] == "deak_akun_konfirm":
        del ubot._ubot[X.me.id]
        await X.invoke(functions.account.DeleteAccount(reason="madarchod hu me"))
        return await callback_query.answer(f"Account successfully deleted from telegram!", True)




@USU.CALLBACK("cek_masa_aktif")
async def _(client, callback_query):
    user_id = int(callback_query.data.split()[1])
    expired = await db.get_expired_date(user_id)
    try:
        if expired is None:
            return await callback_query.answer("Tidak ada tanggal kadaluarsa!", True)

        now_utc = datetime.now(pytz.utc) 

        remainder = (expired - now_utc).days

        if remainder < 0:
            return await callback_query.answer("Sudah kadaluarsa!", True)

        return await callback_query.answer(f"Sisa waktu: {remainder} hari!", True)

    except Exception as e:
        return await callback_query.answer(f"Terjadi kesalahan: {e}", True)




@USU.CALLBACK("^(del_ubot|konfir_del_ubot)")
async def _(client, callback_query):
    query = callback_query.data.split()
    user_id = callback_query.from_user.id
    if user_id not in DEVS:
        return await callback_query.answer(
            f"Tombol ini bukan untuk anda! {callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}",
            True,
        )
    try:
        X = ubot._ubot[tuple(ubot._ubot.keys())[int(query[1])]]
    except Exception:
        return await callback_query.answer("Invalid query", True)

    if query[0] == "del_ubot":
        if int(query[1]) < len(ubot._ubot):
            return await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(BTN.DEL(X.me.id, int(query[1])))
            )
    elif query[0] == "konfir_del_ubot":
        await X.unblock_user(bot.me.username)
        await db.remove_ubot(X.me.id)
        await db.rem_expired_date(X.me.id)
        del ubot._ubot[X.me.id]
        await X.log_out()
        await callback_query.answer(
                    f"Successfully deleted from database!", True
                )
        await callback_query.edit_message_text(
            await MSG.UBOT(0),
            reply_markup=InlineKeyboardMarkup(
                BTN.UBOT(ubot._ubot[tuple(ubot._ubot.keys())[0]].me.id, 0)
            ),
        )
        await bot.send_message(
            X.me.id,
            MSG.EXP_MSG_UBOT(X),
        )


@USU.CALLBACK("^(p_ub|n_ub)")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id not in DEVS:
        return await callback_query.answer(
            f"Tombol ini bukan untuk anda! {callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}",
            True,
        )
    query = callback_query.data.split()
    count = int(query[1])
    if query[0] == "n_ub":
        if count == len(ubot._ubot) - 1:
            count = 0
        else:
            count += 1
    elif query[0] == "p_ub":
        if count == 0:
            count = len(ubot._ubot) - 1
        else:
            count -= 1
    await callback_query.edit_message_text(
        await MSG.UBOT(count),
        reply_markup=InlineKeyboardMarkup(
            BTN.UBOT(ubot._ubot[tuple(ubot._ubot.keys())[count]].me.id, count)
        ),
    )