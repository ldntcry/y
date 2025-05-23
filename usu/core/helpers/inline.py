from pykeyboard import InlineKeyboard
from pyrogram.errors import MessageNotModified
from pyrogram.types import *

from usu import *


def detect_url_links(text):
    link_pattern = (
        r"(?:https?://)?(?:www\.)?[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})+(?:[/?]\S+)?"
    )
    link_found = re.findall(link_pattern, text)
    return link_found


def detect_button_and_text(text):
    button_matches = re.findall(r"\| ([^|]+) - ([^|]+) \|", text)
    text_matches = (
        re.search(r"(.*?) \|", text, re.DOTALL).group(1) if "|" in text else text
    )
    return button_matches, text_matches


def create_inline_keyboard(text, user_id=False, is_back=False):
    keyboard = []
    button_matches, text_matches = detect_button_and_text(text)

    prev_button_data = None
    for button_text, button_data in button_matches:
        data = (
            button_data.split(";same")[0]
            if detect_url_links(button_data.split(";same")[0])
            else f"_gtnote {int(user_id.split('_')[0])}_{user_id.split('_')[1]} {button_data.split(';same')[0]}"
        )
        cb_data = data if user_id else button_data.split(";same")[0]
        if ";same" in button_data:
            if prev_button_data:
                if detect_url_links(cb_data):
                    keyboard[-1].append(InlineKeyboardButton(button_text, url=cb_data))
                else:
                    keyboard[-1].append(
                        InlineKeyboardButton(button_text, callback_data=cb_data)
                    )
            else:
                if detect_url_links(cb_data):
                    button_row = [InlineKeyboardButton(button_text, url=cb_data)]
                else:
                    button_row = [
                        InlineKeyboardButton(button_text, callback_data=cb_data)
                    ]
                keyboard.append(button_row)
        else:
            if button_data.startswith("http"):
                button_row = [InlineKeyboardButton(button_text, url=cb_data)]
            else:
                button_row = [InlineKeyboardButton(button_text, callback_data=cb_data)]
            keyboard.append(button_row)

        prev_button_data = button_data

    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    if user_id and is_back:
        markup.inline_keyboard.append(
            [
                InlineKeyboardButton(
                    "Back",
                    f"_gtnote {int(user_id.split('_')[0])}_{user_id.split('_')[1]}",
                )
            ]
        )

    return markup, text_matches


class BTN:
    def PILIHAN():
        button = [
            [
                InlineKeyboardButton(
                    text="Menu Userbot",
                    callback_data=f"awal",
                ),
                InlineKeyboardButton(
                    text="Menu Manage",
                    callback_data=f"manage",
                )
            ],
            [
                InlineKeyboardButton(
                    text="Menu Music",
                    callback_data=f"music",
                ),
                InlineKeyboardButton(
                    text="Menu AntiGcast",
                    callback_data=f"ankes",
                )
            ],
            [
                InlineKeyboardButton("Report Bug", callback_data=f"complain"
                ),
            ],
        ]
        return button

    def TAMBAH():
        button = [
            [
                InlineKeyboardButton(
                    text="Tambahkan Saya Ke Group",
                    url=f"https://t.me/{bot.me.username}?startgroup=true"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Kembali",
                    callback_data=f"pilihan",
                )
            ],
        ]
        return button

    def UTAMA():
        button = [
            [
                InlineKeyboardButton(
                    text="Saldo Userbot",
                    callback_data=f"saldo_userbot",
                ),
                InlineKeyboardButton(
                    text="Status",
                    callback_data=f"alive",
                )
            ],
            [
                InlineKeyboardButton(
                    text="Fitur",
                    callback_data=f"kembali",
                )
            ]
        ]
        return button

    def BACK_SALDO():
        button = [
            [
                InlineKeyboardButton(
                    text="Kembali",
                    callback_data=f"menu_utama",
                )
            ]
        ]
        return button

    def ALIVE():
        button = [
            [
                InlineKeyboardButton(
                    text="Ping!",
                    callback_data=f"alv_cls",
                )
            ],
            [
                InlineKeyboardButton(
                    text="Kembali",
                    callback_data=f"menu_utama",
                )
            ]
        ]
        return button

    def BOT_HELP(message):
        button = [
            [InlineKeyboardButton("System", callback_data="system")],
            [InlineKeyboardButton("Ubot", callback_data="statss")],
            [InlineKeyboardButton("Restart", callback_data="reboot")],
            [InlineKeyboardButton("Update", callback_data="update")],
            [InlineKeyboardButton("Shutdown", callback_data="shutdown")],
        ]
        return button

    def REF(username, ref):
        button = [
            [
                InlineKeyboardButton("Undang", url=f"https://t.me/share/url?url=https://t.me/{username}?start={ref}"),
            ],
            [
                InlineKeyboardButton("Kembali", callback_data=f"saldo"
                )
            ]
        ]
        return button

    def KONFIR(bulan):
        button = [
            [
                InlineKeyboardButton("« Prev", callback_data=f"kirii_{bulan}"),
                InlineKeyboardButton("Next »", callback_data=f"kanann_{bulan}"),
            ],
            [
                InlineKeyboardButton("Setuju", callback_data="setuju"
                )
            ],
            [
                InlineKeyboardButton("Kembali", callback_data=f"metode_beli"
                )
            ]
        ]
        return button

    def BELI():
        button = [
            [
                InlineKeyboardButton("Beli Via Saldo", callback_data="hajar"
                ),
                InlineKeyboardButton("Beli Via Qris", callback_data="beli"
                ),
            ],
            [
                InlineKeyboardButton("Beli Via Owners", url=f"https://t.me/{USERNAME}"
                ),
            ],
            [
                InlineKeyboardButton("Kembali", callback_data=f"awal"
                ),
            ]
        ]
        return button

    def START():
        button = [
            [
                InlineKeyboardButton("Saldo Saya", callback_data="saldo"
                ),
            ],
            [
                InlineKeyboardButton("Beli/Berlangganan", callback_data="metode_beli"
                ),
                InlineKeyboardButton("Install Userbot", callback_data=f"buat"
                ),
            ],
            [
                InlineKeyboardButton("Ketentuan Userbot!", url=f"https://telegra.ph/Ketentuan-Userbot-04-11"
                ),
                InlineKeyboardButton(
                    "Masa Aktif", callback_data=f"status"
                ),
            ],
            [
                InlineKeyboardButton("Reset Prefix/Handler", callback_data=f"reset"
                ),
                InlineKeyboardButton("Fitur", callback_data=f"menu_utama"
                ),
            ],
            [
                InlineKeyboardButton("Admin Userbot", callback_data=f"seller"
                ),
            ],
            [
                InlineKeyboardButton("Kembali", callback_data=f"pilihan"
                ),
            ]
        ]
        return button

    def TOPUP():
        keyboard = [
            [
                InlineKeyboardButton("Isi Saldo", callback_data=f"isi"),
                InlineKeyboardButton("Kode Referral", callback_data=f"kode")
            ],
            [
                InlineKeyboardButton("Kembali", callback_data=f"awal"
                ),
            ]
        ]
        return keyboard

    def PAY(bulan):
        keyboard = [
            [
                InlineKeyboardButton("« Prev", callback_data=f"kiri_{bulan}"),
                InlineKeyboardButton("Next »", callback_data=f"kanan_{bulan}"),
            ],
            [
                InlineKeyboardButton("Konfirmasi & Bayar", callback_data=f"bayar_{bulan}"),
            ],
            [
                InlineKeyboardButton("Kembali", callback_data=f"metode_beli"
                ),
            ]
        ]
        return keyboard

    def SUPPORT():
        button = [
            [
                InlineKeyboardButton("Groups", url=f"https://t.me/ellubotsupport"
                ),
                InlineKeyboardButton(
                    "Channels", url=f"https://t.me/LModeStore"
                ),
            ],
            [
                InlineKeyboardButton("Kembali", callback_data=f"pilihan"
                ),
            ]
        ]
        return button

    def UBOT(user_id, count):
        button = [
            [
                InlineKeyboardButton(
                    "Remove Userbot",
                    callback_data=f"del_ubot {int(count)}",
                ),
            ],
            [
                InlineKeyboardButton(
                    "Delete Account",
                    callback_data=f"ub_deak {int(count)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "Check Expired",
                    callback_data=f"cek_masa_aktif {int(user_id)}",
                ),
            ],
            [
                InlineKeyboardButton(
                    "Check Otp",
                    callback_data=f"get_otp {int(count)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "Check Phone Number",
                    callback_data=f"get_phone {int(count)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "Check Two-Factor",
                    callback_data=f"get_faktor {int(count)}",
                )
            ],
            [
                InlineKeyboardButton("☚", callback_data=f"p_ub {int(count)}"),
                InlineKeyboardButton("☛", callback_data=f"n_ub {int(count)}"),
            ],  
        ]
        return button

    def DEAK(user_id, count):
        button = [
            [
                InlineKeyboardButton(
                    "Back",
                    callback_data=f"p_ub {int(count)}"
                ),
                InlineKeyboardButton(
                    "Approve", callback_data=f"deak_akun_konfirm {int(count)}",
                ),
            ],
        ]
        return button

    def DEL(user_id, count):
        button = [
            [
                InlineKeyboardButton(
                    "Back",
                    callback_data=f"p_ub {int(count)}"
                ),
                InlineKeyboardButton(
                    "Approve", callback_data=f"konfir_del_ubot {int(count)}",
                ),
            ],
        ]
        return button
