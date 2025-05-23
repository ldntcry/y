import asyncio

from pyrogram import Client as c

API_ID = input("\nMasukan API_ID:\n > ")
API_HASH = input("\nMasukan API_HASH:\n > ")


print("\n\n Masukan nomor telegram anda\n\n")

i = c("string", in_memory=True, api_id=API_ID, api_hash=API_HASH)


async def main():
    await i.start()
    ss = await i.export_session_string()
    xx = f"String anda!!\n\n`{ss}`"
    try:
        await i.send_message("me", xx)
    except BaseException:
        pass
    print("\nJangan pernah membagikan string ini ke siapapun\n")
    print(f"\n{ss}\n")
    print("\n Terima kasih\n")


asyncio.run(main())
