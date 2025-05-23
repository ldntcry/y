from usu import *
from usu import config
import random
import requests
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters
from pyrogram.types import Message
from MukeshAPI import api
from pyrogram import filters



"""
x = None


@USU.UBOT("gemini")
async def gemini_handler(client, message):
    global x
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prss = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    prs = await message.reply(f"<i><b>{prss}Proccesing...</b></i>")
    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    if message.reply_to_message and message.reply_to_message.text:
        user_input = message.reply_to_message.text
    else:
        if len(message.command) > 1:
            user_input = " ".join(message.command[1:])
        else:
            await prs.edit(f"<i><b>{ggl}{message.text} berikan sesuatu</b></i>")
            return

    try:
        response = api.chatgpt(user_input)
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)
        if response is not None and "results" in response:
            x = response["results"]
        await prs.delete()
        await message.reply(f"<i><b>{x}\n\n{sks}Dijawab Oleh: {bot.me.mention}</b></i>")
    except requests.exceptions.RequestException as e:
        pass

genai.configure(api_key=GEMINI_API)


async def start_gemini(text):
    try:
        name = "gemini-1.5-flash"
        con = {
            "temperature": 0.6,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
        set = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_ONLY_HIGH",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_ONLY_HIGH",
            },
        ]
        gemini = genai.GenerativeModel(
            model_name=name,
            generation_config=con,
            safety_settings=set,
        )
        respon = gemini.generate_content(text)
        if respon:
            return f"{respon.text}"
    except Exception as e:
        return f"Error generating text: {str(e)}"


@USU.UBOT("ask|ai")
async def ask_handler(client, message):
    global x
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prss = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    prs = await message.reply(f"<i><b>{prss}Proccesing...</b></i>")
    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    if message.reply_to_message and message.reply_to_message.text:
        user_input = message.reply_to_message.text
    else:
        if len(message.command) > 1:
            user_input = " ".join(message.command[1:])
        else:
            await prs.edit(f"<i><b>{ggl}{message.text} berikan sesuatu</b></i>")
            return

    try:
        response = api.gemini(user_input)
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)
        if response is not None and "results" in response:
            x = response["results"]
        await prs.delete()
        await message.reply(f"<i><b>{x}\n\n{sks}Dijawab Oleh: {bot.me.mention}</b></i>")
    except requests.exceptions.RequestException as e:
        pass"""

@USU.UBOT("ask|ai|gemini")
async def ask_handler(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prss = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    prs = await message.reply(f"<i><b>{prss}Proccesing...</b></i>")
    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    if message.reply_to_message and message.reply_to_message.text:
        user_input = message.reply_to_message.text
    else:
        if len(message.command) > 1:
            user_input = " ".join(message.command[1:])
        else:
            await prs.edit(f"<i><b>{ggl}{message.text} berikan sesuatu</b></i>")
            return

    try:
        anu = "https://api.botcahx.eu.org/api/search/openai-chat"
        key = {
            "apikey": "CrFNb9Qa",
            "text": user_input
        }

        res = requests.get(anu, key)

        await client.send_chat_action(message.chat.id, ChatAction.TYPING)
        if res is not None:
            x = res.json()["message"]
        await prs.delete()
        await message.reply(f"<b>{x}\n\n{sks}Dijawab Oleh: {bot.me.mention}</b>")
    except requests.exceptions.RequestException as e:
        pass


