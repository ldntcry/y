from usu import *
import subprocess
import importlib
import sys
import os

repo_dir = os.path.dirname(os.path.abspath(__file__))

@USU.BOT("update")
@USU.DEVS
async def update_code(client, message):
    try:
        subprocess.run(['git', 'pull'])
        for module in list(sys.modules.values()):
            try:
                module_file = getattr(module, '__file__', None)
                if module_file and module_file.startswith(repo_dir):
                    importlib.reload(module)
            except Exception as e:
                print(f"Error reload module {module}: {e}")
        await message.reply(f"<b><i>Kode berhasil diupdate</i></b>")
    except Exception as e:
        await message.reply(f"Error: {e}")