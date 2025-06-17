import os
import sys

DEVICE_NAME = os.getenv("DEVICE_NAME", "AIO-Device") #Nama device bebas di ubah sesuka hati

DEVICE_VERSION = os.getenv("DEVICE_VERSION", "1.1.2") #Versi bebas di ubah sesuka hati

HARGA_USERBOT = int(os.getenv("HARGA_USERBOT", "25")) #Harga bebas di ubah sesuka hati

MAX_BOT = int(os.getenv("MAX_BOT", "500")) #Maksimal pengguna userbot anda

API_ID = int(os.getenv("API_ID", "28041411")) #Api ID bisa ke web my.telegram.org

API_HASH = os.getenv("API_HASH", "c4c9395a19f3dd1f6a3a11f2e98251e8") #Api Hash bisa ke web my.telegram.org

BOT_TOKEN = os.getenv("BOT_TOKEN", "7600377233:AAHvwCN_7YYKr0XRjsy2CYtAZ3_lg9kPza4") #Token bot

DEVS = list(map(int, os.getenv("DEVS", "6904554940 7604277685 1992950127 931708433").split())) #ID akun ini full control bot

OWNER_ID = int(os.getenv("OWNER_ID", "1992950127")) #ID akun anda

AUTO_JOIN = os.getenv("AUTO_JOIN", "TCNSupportBot TeleSupport_Id AIOProjectTeams AIOProjectStore").split() #Auto join semua client ke chat ini

AUTO_REACTION = os.getenv("AUTO_REACTION", "LmodeStore") #Auto reaction postingan channel anda

USERNAME = os.getenv("USERNAME", "Khoccak") #Username akun anda

CHANNEL = os.getenv("CHANNEL", "LmodeStore") #Support channel

GROUP = os.getenv("GROUP", "ellubotsupport") #Support group

FSUB = os.getenv("FSUB", "LmodeStore MahaEsaInHere").split() #Wajib adminkan bot di semua chat fsub ini

LOGS_CHAT = int(os.getenv("LOGS_CHAT", "-1002167927362")) #Wajib adminkan bot di logs chat ini

BLACKLIST_CHAT = list(map(int, os.getenv("BLACKLIST_CHAT", "-1002579277466 -1002501848632 -1002167927362").split())) #Ini agar gcast yang make bot anda ga masuk ke chat tersebut

IMGBB_API_KEY = os.getenv("IMGBB_API_KEY", "1b54fa62c533c2eeca60e50dadce6c0b")

PHOTO = os.getenv("PHOTO", "https://files.catbox.moe/4sgj3s.jpg") #Photo bot anda

QRIS = os.getenv("QRIS", "https://files.catbox.moe/vm3z27.jpg") #foto qris anda

RMBG_API = os.getenv("RMBG_API", "HgrmjXeGacBNXHnUGuw4msC1")

GEMINI_API = os.getenv("GEMINI_API", "AIzaSyAkHiriJ43kxfb4mIfxocF60mnN9wnIGZo")

DATABASE = os.getenv("DATABASE", "ell") #Nama database

STRING = os.getenv("STRING", "BQGQTkQAxLQql8m3YqUD1FZv0rt-v3WjR3m93cTjEdgJFz_1R-jVY3Jba4hv1GnGa4H_-wo0SFbjZ8iZMgOVt4Y64W1JeBME2QlcDPbHoJ0P74osHz_lIdyDftD3xDE5M1hIKUQ0r1UWvVU3GVMffnKJRhrtk9Th7EGPz6zGfOgCWd8TF6Z1l9pjV_rvQGWwuJ9zZxWlBmM7mpBb5oY1Zoi68PIBupo8zLHDcA1LzZvftwkzkMVWIkrAcX6Uigc2M2wd6j1rShIVahAq5nmlb26pVdVXrvL_Ac0XjPdofPTL0aJdDLHlkU-tqxzQZtwN6xBEnnFbqDZzMSMN7QnxADkGHcYcFgAAAAA3iL4RAA") #String assistant anda


