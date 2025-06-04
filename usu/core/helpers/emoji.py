from usu import *



class EMO:
    async def PING(client):
        varss = await get_vars(client.me.id, "switch")
        emot_1 = await get_vars(client.me.id, "EMOJI_PING")
        emot_ping = emot_1 if emot_1 else "5202089931085718160"
        if varss:
            _pong = f"<emoji id={emot_ping}>🏓</emoji>"
        else:
            _pong = ""
        return _pong


    async def MENTION(client):
        varss = await get_vars(client.me.id, "switch")
        emot_2 = await get_vars(client.me.id, "EMOJI_MENTION")
        emot_tion = emot_2 if emot_2 else "5424605254614262924"
        if varss:
            _men = f"<emoji id={emot_tion}>⭐️</emoji>"
        else:
            _men = ""
        return _men


    async def UPTIME(client):
        varss = await get_vars(client.me.id, "switch")
        emot_12 = await get_vars(client.me.id, "EMOJI_UPTIME")
        emot_up = emot_12 if emot_12 else "5224533828151812094"
        if varss:
            _up = f"<emoji id={emot_up}>⏰</emoji>"
        else:
            _up = ""
        return _up


    async def PROSES(client):
        varss = await get_vars(client.me.id, "switch")
        emot_4 = await get_vars(client.me.id, "EMOJI_PROSES")
        emot_prs = emot_4 if emot_4 else "5201877502003258204"
        if varss:
            _prses = f"<emoji id={emot_prs}>⏳</emoji>"
        else:
            _prses = ""
        return _prses


    async def SUKSES(client):
        varss = await get_vars(client.me.id, "switch")
        emot_5 = await get_vars(client.me.id, "EMOJI_SUKSES")
        emot_brhsl = emot_5 if emot_5 else "5427295974315793487"
        if varss:
            _berhasil = f"<emoji id={emot_brhsl}>✅</emoji>"
        else:
            _berhasil = ""
        return _berhasil


    async def GAGAL(client):
        varss = await get_vars(client.me.id, "switch")
        emot_6 = await get_vars(client.me.id, "EMOJI_GAGAL")
        emot_ggl = emot_6 if emot_6 else "5292222401067626057"
        if varss:
            _gagal = f"<emoji id={emot_ggl}>❌</emoji>"
        else:
            _gagal = ""
        return _gagal


    async def BROADCAST(client):
        varss = await get_vars(client.me.id, "switch")
        emot_7 = await get_vars(client.me.id, "EMOJI_BROADCAST")
        emot_gcs = emot_7 if emot_7 else "5451694459458690201"
        if varss:
            _bc = f"<emoji id={emot_gcs}>📣</emoji>"
        else:
            _bc = ""
        return _bc


    async def MENUNGGU(client):
        varss = await get_vars(client.me.id, "switch")
        emot_10 = await get_vars(client.me.id, "EMOJI_MENUNGGU")
        emot_mng = emot_10 if emot_10 else "5285409457654737374"
        if varss:
            _ktr = f"<emoji id={emot_mng}>⏰</emoji>"
        else:
            _ktr = ""
        return _ktr


    async def PUTARAN(client):
        varss = await get_vars(client.me.id, "switch")
        emot_11 = await get_vars(client.me.id, "EMOJI_PUTARAN")
        emot_ptr = emot_11 if emot_11 else "5258513401784573443"
        if varss:
            mmk = f"<emoji id={emot_ptr}>🌀</emoji>"
        else:
            mmk = ""
        return mmk

