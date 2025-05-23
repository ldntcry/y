import asyncio
import random
from pyrogram import idle
from usu import *
import tornado.ioloop
import tornado.platform.asyncio
import os
import sys

async def auto_reaction_task(client, reactions):
    random_emoji = random.choice(reactions)
    reacted = set()
    try:
        peer = await client.get_chat(AUTO_REACTION)
        async for message in client.get_chat_history(peer.id, limit=1):
            if client.me.id in reacted:
                continue
            try:
                await message.react(random_emoji)
                reacted.add(client.me.id)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                try:
                    await message.react(random_emoji)
                    reacted.add(client.me.id)
                except Exception as e:
                    pass
            except Exception as e:
                pass
    except Exception as e:
        pass


async def auto_reaction():
    reactions = ["👍", "🤩", "🎉", "😍", "👏", "🔥", "🙈", "💯", "🌚", "😎", "🍓", "🏆", "❤️‍🔥", "⚡", "🙉", "🙊", "👻", "🌭"]
    while True:
        tasks = []
        for client in ubot._ubot.values():
            task = asyncio.create_task(auto_reaction_task(client, reactions))
            tasks.append(task)
        await asyncio.gather(*tasks)
        await asyncio.sleep(60)

async def main():
    print(f"Database load: {DATABASE}.db")
    print(f"------------------------------")
    await bot.start()
    for _ubot in await get_userbots():
        ubot_ = Ubot(**_ubot)
        try:
            await ubot_.start()
            for auto in AUTO_JOIN:
                await ubot_.join_chat(auto)
        except Exception:
            pass
    try:
        await bash("rm -rf *session*")
    except Exception:
        pass
    await asyncio.gather(loadPlugins(), installPeer(), expiredUserbots(), check_session(), auto_reaction())


if __name__ == "__main__":
    tornado.platform.asyncio.AsyncIOMainLoop().install()
    loop = tornado.ioloop.IOLoop.current().asyncio_loop
    loop.run_until_complete(main())
    idle()
