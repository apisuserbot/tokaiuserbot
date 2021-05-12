# frm Ultroid
# port by Koala @manusiarakitann
# @LordUserbot_Group
# Alvin Ganteng

from userbot.events import register
from userbot import CMD_HELP, bot
# Alvin Ganteng


@register(outgoing=True, pattern="^.gcast (.*)")
async def gcast(event):
    xx = event.pattern_match.group(1)
    if not xx:
        return await event.edit("`Beri aku Pesan!!!`")
    tt = event.text
    msg = tt[6:]
    kk = await event.edit("`Gcast sedang dalam proses...`")
    er = 0
    done = 0
    async for x in bot.iter_dialogs():
        if x.is_group:
            chat = x.id
            try:
                done += 1
                await bot.send_message(chat, msg)
            except BaseException:
                er += 1
    await kk.edit(f"**Gcast berhasil diluncurkan ke** `350` **grup, Gagal mengirim pesan ke** `{er}` **grup**")

# Alvin Ganteng
CMD_HELP.update(
    {
        "gcast": "`.gcast <pesan>`\
    \nPenjelasan: Global Broadcast mengirim pesan ke Seluruh Grup yang Bos Masuki."
    })
