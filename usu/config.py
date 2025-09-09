import os
import sys

DEVICE_NAME = os.getenv("DEVICE_NAME", "ell ubot") #Nama device bebas di ubah sesuka hati

DEVICE_VERSION = os.getenv("DEVICE_VERSION", "1.1.2") #Versi bebas di ubah sesuka hati

HARGA_USERBOT = int(os.getenv("HARGA_USERBOT", "25")) #Harga bebas di ubah sesuka hati

MAX_BOT = int(os.getenv("MAX_BOT", "999"))

API_ID = int(os.getenv("API_ID", "21871018"))

API_HASH = os.getenv("API_HASH","d65d6dd5b129805544498b265c92f3c4")

BOT_TOKEN = os.getenv("BOT_TOKEN", "7884852533:AAGQqIWqKRPpk1ksyDmugwkWCh-no3RHy3s")

DEVS = list(map(int, os.getenv("DEVS", "931708433 5492088564").split()))
OWNER_ID = int(os.getenv("OWNER_ID", "1404077683"))

AUTO_JOIN = os.getenv("AUTO_JOIN", "LmodeStore ellubotsupport").split()

AUTO_REACTION = os.getenv("AUTO_REACTION", "LmodeStore")

USERNAME = os.getenv("USERNAME", "bigastaa")

FSUB = os.getenv("FSUB", "LmodeStore ellubotsupport").split()

LOGS_CHAT = int(os.getenv("LOGS_CHAT", "-1002167927362"))

BLACKLIST_CHAT = list(map(int, os.getenv("BLACKLIST_CHAT", "-1002579277466 -1002501848632 -1002167927362").split()))

IMGBB_API_KEY = os.getenv("IMGBB_API_KEY", "1b54fa62c533c2eeca60e50dadce6c0b")

PHOTO = os.getenv("PHOTO", "https://files.catbox.moe/4sgj3s.jpg")

QRIS = os.getenv("QRIS", "https://files.catbox.moe/vm3z27.jpg")

RMBG_API = os.getenv("RMBG_API", "HgrmjXeGacBNXHnUGuw4msC1")

GEMINI_API = os.getenv("GEMINI_API", "AIzaSyAkHiriJ43kxfb4mIfxocF60mnN9wnIGZo")

DATABASE = os.getenv("DATABASE", "ell")

STRING = os.getenv("STRING", "NONE") #String assistant anda
