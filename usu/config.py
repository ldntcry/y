import os
import sys


MAX_BOT = int(os.getenv("MAX_BOT", "9999"))

API_ID = int(os.getenv("API_ID", "28041411"))

API_HASH = os.getenv("API_HASH", "c4c9395a19f3dd1f6a3a11f2e98251e8")

BOT_TOKEN = os.getenv("BOT_TOKEN", "isi")

DEVS = list(map(int, os.getenv("DEVS", "6904554940 5581521071 7604277685 1992950127 931708433").split()))
OWNER_ID = int(os.getenv("OWNER_ID", "1992950127"))

AUTO_JOIN = os.getenv("AUTO_JOIN", "LmodeStore ellubotsupport").split()

AUTO_REACTION = os.getenv("AUTO_REACTION", "LmodeStore")

USERNAME = os.getenv("USERNAME", "Khoccak")

FSUB = os.getenv("FSUB", "LmodeStore MahaEsaInHere").split()

LOGS_CHAT = int(os.getenv("LOGS_CHAT", "-1002547434184"))

BLACKLIST_CHAT = list(map(int, os.getenv("BLACKLIST_CHAT", "-1002579277466 -1002501848632").split()))

IMGBB_API_KEY = os.getenv("IMGBB_API_KEY", "1b54fa62c533c2eeca60e50dadce6c0b")

PHOTO = os.getenv("PHOTO", "https://files.catbox.moe/rh2l7c.jpg")

QRIS = os.getenv("QRIS", "https://files.catbox.moe/snv8qt.jpg")

RMBG_API = os.getenv("RMBG_API", "HgrmjXeGacBNXHnUGuw4msC1")

GEMINI_API = os.getenv("GEMINI_API", "AIzaSyAkHiriJ43kxfb4mIfxocF60mnN9wnIGZo")

DATABASE = os.getenv("DATABASE", "namadb")

STRING = os.getenv("STRING", "isi")
