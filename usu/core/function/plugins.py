import importlib 
from platform import python_version
from pyrogram import filters
import pytgcalls
import pyrogram
import asyncio
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from usu import bot
from usu.core.helpers import USU
from usu.modules import loadModule
from usu.core.database import *
from usu.config import OWNER_ID
from usu.core.helpers.help_usu import *



async def loadPlugins():
    modules = loadModule()  # Assuming loadModule() is defined elsewhere
    await asyncio.sleep(2)
    print(f"------------------------------")
    print(f"Client - Checking module...")
    await asyncio.sleep(2)
    print(f"------------------------------")
    await asyncio.sleep(2)
    print(f"Client - Module detected!")
    for mod in modules:
        try:
            imported_module = importlib.import_module(f"usu.modules.{mod}")
            utama = getattr(imported_module, "__UTAMA__", None)
            button_labels = getattr(imported_module, "__BUTTON__", None)
            text = getattr(imported_module, "__TEXT__", None)
            hasil = getattr(imported_module, "__HASIL__", None)

            if utama and button_labels and text and hasil:
                if utama not in tombol_utama:
                    tombol_utama[utama] = {"text": utama, "callback_data": f"usu {utama}", "__TEXT__": text, "HASIL": hasil}
                if utama not in tombol_anak:
                    tombol_anak[utama] = []

                buttons = []
                for label, hasil_labels in zip(button_labels, hasil):
                    callback_data = f"tousu {utama.lower()}_{label.replace(' ', '_').lower()}"
                    buttons.append({"text": label, "teks": hasil_labels, "callback_data": callback_data})

                tombol_anak[utama].extend(buttons)
        except Exception as e:
            print(f"Client - Error loading module {mod}: {e}")

    jumlah_button_usu = sum(len(buttons) for buttons in tombol_anak.values())
    print(f"------------------------------")
    await asyncio.sleep(2)
    print(f"Client - Successfully loaded {jumlah_button_usu} modules!")
    print(f"Client - Successfully started {len(ubot._ubot)} client!")
    await asyncio.sleep(2)
    print(f"------------------------------")
    for anjay in DEVS:
        try:
            await bot.send_message(
                anjay,
                f"""<b><i>Userbot Active!</i></b>

<i><b>Module:</b> {jumlah_button_usu}</i>
<i><b>Client:</b> {len(ubot._ubot)}</i>
<i><b>Pyrogram:</b> {pyrogram.__version__}</i>
<i><b>Pytgcalls:</b> {pytgcalls.__version__}</i>""")
        except Exception as e:
            return print(f"Silahkan /start @{bot.me.username} terlebih dahulu di semua akun DEVS!")