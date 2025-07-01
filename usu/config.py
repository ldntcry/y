import os
import sys


MAX_BOT = int(os.getenv("MAX_BOT", "9999"))

API_ID = int(os.getenv("API_ID", "28767825"))

API_HASH = os.getenv("API_HASH", "92e40bda3ca8b6bc77fe9aabdcda6eda")

BOT_TOKEN = os.getenv("BOT_TOKEN", "7113180777:AAHBM6T7ZGx1vlYE-91EAFQzL1Hoj-13TBw")

DEVS = list(map(int, os.getenv("DEVS", "7694024335 6935749105 1992950127 931708433").split()))
OWNER_ID = int(os.getenv("OWNER_ID", "6935749105"))

AUTO_JOIN = os.getenv("AUTO_JOIN", "LmodeStore ellubotsupport").split()

AUTO_REACTION = os.getenv("AUTO_REACTION", "LmodeStore")

USERNAME = os.getenv("USERNAME", "Gitu_aj")

FSUB = os.getenv("FSUB", "LmodeStore ellubotsupport").split()

LOGS_CHAT = int(os.getenv("LOGS_CHAT", "-1002658213833"))

BLACKLIST_CHAT = list(map(int, os.getenv("BLACKLIST_CHAT", "-1002579277466 -1002501848632 -1002167927362").split()))

IMGBB_API_KEY = os.getenv("IMGBB_API_KEY", "1b54fa62c533c2eeca60e50dadce6c0b")

PHOTO = os.getenv("PHOTO", "https://files.catbox.moe/4sgj3s.jpg")

QRIS = os.getenv("QRIS", "https://files.catbox.moe/vm3z27.jpg")

RMBG_API = os.getenv("RMBG_API", "HgrmjXeGacBNXHnUGuw4msC1")

GEMINI_API = os.getenv("GEMINI_API", "AIzaSyAkHiriJ43kxfb4mIfxocF60mnN9wnIGZo")

DATABASE = os.getenv("DATABASE", "ell")

STRING = os.getenv("STRING", None) #String assistant anda
